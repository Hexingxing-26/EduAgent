from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json
from datetime import datetime
from app.workflow import graph_app
from app.database import init_db, get_db, EduUser, EduProfile, EduChat, LearningRecord, EduResource
from app.prompt_manager import prompt_manager

app = FastAPI(title="AI智能学习助手", version="1.0.0")

init_db()


class ChatRequest(BaseModel):
    user_id: str
    message: str
    session_id: str = ""


class UserProfileRequest(BaseModel):
    user_id: str
    name: str = ""
    major: str = ""
    course: str = ""
    goal: str = ""
    knowledge_base: str = ""
    preference: str = ""
    weakness: str = ""
    time: str = ""


@app.on_event("startup")
def on_startup():
    print(">>> AI智能学习助手启动中...")
    print(">>> 数据库已初始化")


@app.get("/")
def root():
    return {"message": "AI智能学习助手已启动！", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    initial_state = {
        "user_id": request.user_id,
        "session_id": request.session_id,
        "messages": [{"role": "user", "content": request.message}],
        "profile": {}, "retrieved_docs": [], "generated_resource": {},
        "is_approved": False, "learning_path": [], "retry_count": 0
    }
    
    async def event_generator():
        async for event in graph_app.astream(initial_state):
            for node_name, node_output in event.items():
                if node_name == "profile":
                    yield f"data: {json.dumps({'type': '画像', 'content': node_output.get('profile', {})})}\n\n"
                elif node_name == "rag":
                    doc_count = len(node_output.get("retrieved_docs", []))
                    yield f"data: {json.dumps({'type': '检索', 'content': f'找到 {doc_count} 条相关知识'})}\n\n"
                elif node_name == "generator":
                    yield f"data: {json.dumps({'type': '学习资料', 'content': node_output.get('generated_resource', {})})}\n\n"
                elif node_name == "guardrail":
                    status = "审核通过" if node_output.get("is_approved") else "审核失败重试"
                    yield f"data: {json.dumps({'type': '状态', 'content': status})}\n\n"
                elif node_name == "planner":
                    yield f"data: {json.dumps({'type': '学习路线', 'content': node_output.get('learning_path', [])})}\n\n"
        yield f"data: {json.dumps({'type': '完成', 'content': '全部生成完毕'})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")


def clean_text(text):
    if not text:
        return text
    return text.encode('utf-8', 'replace').decode('utf-8')


@app.post("/chat")
async def chat(request: ChatRequest):
    initial_state = {
        "user_id": request.user_id,
        "session_id": request.session_id,
        "messages": [{"role": "user", "content": request.message}],
        "profile": {}, "retrieved_docs": [], "generated_resource": {},
        "is_approved": False, "learning_path": [], "retry_count": 0
    }
    
    import asyncio
    loop = asyncio.get_event_loop()
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        final_state = await loop.run_in_executor(executor, lambda: graph_app.invoke(initial_state))
    
    resource = final_state.get("generated_resource", {})
    if isinstance(resource, dict) and "content" in resource:
        resource["content"] = clean_text(resource["content"])
    
    return {
        "user_id": request.user_id,
        "profile": final_state.get("profile", {}),
        "retrieved_docs": final_state.get("retrieved_docs", []),
        "generated_resource": resource,
        "learning_path": final_state.get("learning_path", []),
        "is_approved": final_state.get("is_approved", False)
    }


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(EduUser).all()
    return [{"id": u.id, "username": u.username, "nickname": u.nickname, "major": u.major} for u in users]


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(EduUser).filter(EduUser.id == user_id).first()
    if not user:
        return {"error": "用户不存在"}
    return {"id": user.id, "username": user.username, "nickname": user.nickname, "major": user.major}


@app.get("/users/{user_id}/profile")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(EduProfile).filter(EduProfile.user_id == user_id).first()
    if not profile:
        return {"error": "用户画像不存在"}
    try:
        learning_data = json.loads(profile.learning_json)
        return {"user_id": profile.user_id, "weak_points": profile.weak_points, "learning_data": learning_data}
    except:
        return {"user_id": profile.user_id, "weak_points": profile.weak_points}


@app.post("/users/{user_id}/profile")
def update_user_profile(user_id: int, request: UserProfileRequest, db: Session = Depends(get_db)):
    profile = db.query(EduProfile).filter(EduProfile.user_id == user_id).first()
    
    learning_json = json.dumps({
        "姓名": request.name,
        "专业": request.major,
        "课程": request.course,
        "学习目标": request.goal,
        "知识基础": request.knowledge_base,
        "学习偏好": request.preference,
        "薄弱知识": request.weakness,
        "学习时间": request.time
    }, ensure_ascii=False)
    
    if profile:
        profile.weak_points = request.weakness
        profile.learning_json = learning_json
    else:
        profile = EduProfile(user_id=user_id, weak_points=request.weakness, learning_json=learning_json)
        db.add(profile)
    
    db.commit()
    return {"message": "用户画像更新成功"}


@app.get("/users/{user_id}/learning_records")
def get_learning_records(user_id: str, db: Session = Depends(get_db)):
    records = db.query(LearningRecord).filter(LearningRecord.user_id == user_id).all()
    return [
        {
            "id": r.id,
            "course": r.course,
            "chapter": r.chapter,
            "score": r.score,
            "correct_rate": r.correct_rate,
            "problems_done": r.problems_done,
            "duration_minutes": r.duration_minutes,
            "date": str(r.date),
            "time_slot": r.time_slot
        } for r in records
    ]


@app.get("/prompts")
def get_prompts():
    return prompt_manager.get_all_prompts()


@app.get("/prompts/{prompt_id}")
def get_prompt(prompt_id: str):
    prompt = prompt_manager.get_prompt(prompt_id)
    if not prompt:
        return {"error": "Prompt模板不存在"}
    return prompt


@app.get("/prompts/search/{keyword}")
def search_prompts(keyword: str):
    return prompt_manager.search_prompts(keyword)


@app.get("/resources")
def get_resources(db: Session = Depends(get_db)):
    resources = db.query(EduResource).all()
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "resource_type": r.resource_type,
            "progress": r.progress,
            "create_time": str(r.create_time)
        } for r in resources
    ]