import json
import asyncio
import logging
import aiohttp
import base64
from typing import AsyncGenerator
from fastapi.responses import EventSourceResponse
from sqlalchemy.orm import Session

# 项目内部依赖
from database.crud_conversation import create_conversation
from database.crud_profile import get_user_profile, update_user_profile, update_user_student
from services.llm_utils import LLMClient, extract_profile, get_default_profile

logger = logging.getLogger(__name__)

def format_sse(data: dict) -> str:
    """标准SSE返回格式"""
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

def check_profile_format(profile_dict: dict) -> dict:
    standard_keys = {
        "knowledge_base", "cognitive_style", "weak_points",
        "interest", "learning_pace", "emotional_state"
    }
    default = {
        "knowledge_base": "初学者",
        "cognitive_style": "视觉型",
        "weak_points": "数学推导,逻辑推理",
        "interest": "人工智能,编程",
        "learning_pace": "中等",
        "emotional_state": "积极"
    }
    # 补齐缺失字段
    for k in standard_keys:
        if k not in profile_dict or not isinstance(profile_dict[k], str):
            profile_dict[k] = default[k]
    return profile_dict

def trim_dialogue_text(text: str, max_length=1800) -> str:
    """截取最新一段对话，控制送入画像抽取文本长度"""
    if len(text) <= max_length:
        return text
    # 保留末尾内容
    return text[-max_length:]

# 自建异步流式大模型调用函数，全部写在此文件
async def chat_stream(messages, temperature=0.7, max_tokens=4096, provider="xunfei"):
    client = LLMClient(provider=provider)
    config = client._load_config()
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": config["model"],
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True
    }
    # 区分讯飞/DeepSeek鉴权
    if provider == "xunfei":
        auth_str = f"{config['api_key']}:{config['api_secret']}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()
        headers["Authorization"] = f"Bearer {encoded_auth}"
    else:
        headers["Authorization"] = f"Bearer {config['api_key']}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(config["base_url"], json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=120)) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    logger.error(f"流式请求失败 HTTP{resp.status}: {text}")
                    return
                async for line in resp.content.iter_any():
                    chunk = line.decode("utf-8").strip()
                    if not chunk or not chunk.startswith("data:"):
                        continue
                    data_str = chunk.replace("data:", "").strip()
                    if data_str == "[DONE]":
                        break
                    try:
                        data = json.loads(data_str)
                        delta = data["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield delta
                    except Exception:
                        continue
    except Exception as e:
        logger.error(f"流式请求异常: {str(e)}")
        return

# 包装D的同步画像抽取函数，转为异步（不改动源文件）
async def extract_portrait_prompt(dialogue_text: str):
    profile_dict = await asyncio.to_thread(extract_profile, dialogue_text)
    if not profile_dict:
        return get_default_profile()
    # 新增标准化校验
    fixed_profile = check_profile_format(profile_dict)
    return fixed_profile

# 流式对话主生成器，接口调用入口
async def stream_chat_response(
    session_id: str,
    user_msg: str,
    user_id: str,
    db: Session
) -> AsyncGenerator[str, None]:
    full_ai_reply = ""
    try:
        # 获取当前用户已有画像
        student_info = get_user_profile(db=db, user_id=user_id)
        portrait_context = student_info.model_dump_json() if student_info else "暂无学生学习画像"
        # 组装大模型上下文
        messages = [
            {"role": "system", "content": f"根据以下学生画像进行个性化答疑：{portrait_context}"},
            {"role": "user", "content": user_msg}
        ]
        # 逐token流式推送
        async for token in chat_stream(messages):
            full_ai_reply += token
            yield format_sse({"type": "delta", "content": token})
            await asyncio.sleep(0.005)
        # 保存AI回复到对话表
        create_conversation(
            db=db,
            user_id=user_id,
            session_id=session_id,
            role="assistant",
            content=full_ai_reply
        )
        # 整合对话抽取画像
        all_dialog = f"用户提问：{user_msg}\nAI回答：{full_ai_reply}"
        # 超长文本截断
        trim_dialog = trim_dialogue_text(all_dialog)
        logger.info(f"画像抽取输入文本（截断后）：{trim_dialog[:600]}")
        portrait_result = await extract_portrait_prompt(trim_dialog)
        logger.info(f"标准化后的画像数据：{portrait_result}")
        # 更新学生画像表
        update_user_profile(db=db, user_id=user_id, portrait_data=portrait_result)
        update_user_student(db=db, user_id=user_id, portrait_data=portrait_result)
        logger.info(f"用户{user_id}画像更新成功，已写入students表")
        # 推送结束标识
        yield format_sse({"type": "done"})

    except aiohttp.ClientError as e:
        # 大模型流式网络/超时异常
        err_msg = f"大模型流式接口请求异常：{str(e)}"
        logger.error(err_msg)
        yield format_sse({"type": "error", "msg": err_msg})
    except json.JSONDecodeError as e:
        # AI返回画像JSON解析失败
        err_msg = "画像JSON解析失败，自动使用默认画像"
        logger.error(f"{err_msg} 错误详情：{str(e)}")
        # 解析失败兜底写入默认画像
        default_p = get_default_profile()
        update_user_student(db, user_id, default_p)
        yield format_sse({"type": "done"})
    except Exception as e:
        # 全局兜底未知异常
        err_msg = f"对话服务未知异常：{str(e)}"
        logger.error(err_msg, exc_info=True)
        yield format_sse({"type": "error", "msg": err_msg})
