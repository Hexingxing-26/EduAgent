import os
import json
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

# ----- 配置讯飞 API -----
APP_ID = os.getenv("SPARK_APP_ID")
API_KEY = os.getenv("SPARK_API_KEY")
API_SECRET = os.getenv("SPARK_API_SECRET")
MODEL = os.getenv("SPARK_MODEL", "spark-x2")
BASE_URL = os.getenv("SPARK_BASE_URL", "https://spark-api-open.xf-yun.com/x2/chat/completions")


def call_llm(messages, temperature=0.7, max_tokens=4096):
    """调用讯飞星火 API（HTTP方式，直接使用requests）"""
    # 认证：将 APIKey:APISecret 进行 Base64 编码
    auth_string = f"{API_KEY}:{API_SECRET}"
    encoded_auth = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {encoded_auth}"
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }
    try:
        response = requests.post(BASE_URL, json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f">>> API 错误 (HTTP {response.status_code}): {response.text}")
            return None
    except Exception as e:
        print(f">>> 请求异常: {e}")
        return None


# ----- 1. 画像机器人 -----
def profile_agent(state: dict):
    print(">>> 1. 画像机器人：正在分析你的学习特征...")
    last_msg = state["messages"][-1].content if state["messages"] else "无"
    
    prompt = f"""你是一个教育心理学专家。根据学生的发言："{last_msg}"。
输出一份严格的JSON格式学生画像（不要带任何其他废话，只输出JSON）。
维度包括：knowledge_base, cognitive_style, weak_points, interest, learning_pace, emotional_state。"""

    response = call_llm([{"role": "user", "content": prompt}])
    
    try:
        profile = json.loads(response)
    except:
        profile = {
            "knowledge_base": "初学者",
            "cognitive_style": "视觉型",
            "weak_points": "数学推导",
            "interest": "AI",
            "learning_pace": "中等",
            "emotional_state": "积极"
        }
    return {"profile": profile}


# ----- 2. RAG检索机器人 -----
def rag_agent(state: dict):
    print(">>> 2. RAG机器人：正在翻阅课本找知识点...")
    try:
        with open("data/demo.txt", "r", encoding="utf-8") as f:
            knowledge = f.read()
    except:
        knowledge = "决策树、SVM、CNN是常见机器学习算法。"
    return {"retrieved_docs": [knowledge]}


# ----- 3. 资源生成机器人 -----
def generator_agent(state: dict):
    print(">>> 3. 生成机器人：正在为你制作学习资料...")
    profile = state.get("profile", {})
    docs = state.get("retrieved_docs", ["通用AI知识"])[0]
    
    prompt = f"""你是一名资深教授。学生的画像特征是：{profile}。
请根据以下知识点"{docs}"，生成3种学习资源（用Markdown格式输出）：
1. **知识讲解文档**（通俗易懂）
2. **随堂测验（2道选择题）**（包含答案和解析）
3. **思维导图大纲**（用列表层级表示）"""

    content = call_llm([{"role": "user", "content": prompt}])
    
    # 如果调用失败，使用备用内容（防止无限循环）
    if content is None:
        content = """
1. **知识讲解文档**：决策树是一种常用的机器学习算法，通过树形结构进行决策，易于理解。
2. **随堂测验**：
   - 题目1：决策树中，ID3算法使用什么指标选择特征？ 答案：信息增益。
   - 题目2：CART算法使用什么指标？ 答案：基尼指数。
3. **思维导图大纲**：- 决策树 - 分类 - 回归 - 剪枝"""
    
    return {"generated_resource": {"type": "multi_resource", "content": content}}


# ----- 4. 审核机器人 -----
def guardrail_agent(state: dict):
    print(">>> 4. 审核机器人：正在检查有没有胡说八道...")
    content = state.get("generated_resource", {}).get("content", "")
    retry_count = state.get("retry_count", 0)
    
    keywords = ["决策树", "SVM", "CNN", "机器学习", "算法", "分类", "深度"]
    has_knowledge = any(k in content for k in keywords)
    
    if has_knowledge and len(content) > 50:
        return {"is_approved": True, "retry_count": retry_count}
    else:
        print(">>> 警告：内容疑似幻觉，已拦截！")
        return {"is_approved": False, "retry_count": retry_count + 1}


# ----- 5. 路径规划机器人 -----
def planner_agent(state: dict):
    print(">>> 5. 规划机器人：正在制定专属学习路线...")
    profile = state.get("profile", {})
    resource = state.get("generated_resource", {}).get("content", "")
    
    prompt = f"""你是学业规划师。学生画像：{profile}。
刚刚生成了学习资料：{resource[:200]}...
请规划3个连续的学习步骤（只输出JSON数组格式）：
[{{"step_name": "步骤名", "action": "具体行动", "time_minutes": 分钟数}}]"""

    response = call_llm([{"role": "user", "content": prompt}])
    
    try:
        path = json.loads(response)
    except:
        path = [
            {"step_name": "理论学习", "action": "阅读讲解文档", "time_minutes": 20},
            {"step_name": "巩固练习", "action": "完成随堂测验", "time_minutes": 15},
            {"step_name": "知识总结", "action": "绘制思维导图", "time_minutes": 10}
        ]
    return {"learning_path": path}