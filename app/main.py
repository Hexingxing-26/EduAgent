from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
from app.workflow import graph_app
from app.models import AgentState

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    initial_state = {
        "user_id": request.user_id,
        "messages": [{"role": "user", "content": request.message}],
        "profile": {}, "retrieved_docs": [], "generated_resource": {},
        "is_approved": False, "learning_path": [], "retry_count": 0
    }
    async def event_generator():
        async for event in graph_app.astream(initial_state):
            for node_name, node_output in event.items():
                if node_name == "profile":
                    yield f"data: {json.dumps({'type': '画像', 'content': node_output.get('profile', {})})}\n\n"
                elif node_name == "generator":
                    yield f"data: {json.dumps({'type': '学习资料', 'content': node_output.get('generated_resource', {})})}\n\n"
                elif node_name == "planner":
                    yield f"data: {json.dumps({'type': '学习路线', 'content': node_output.get('learning_path', [])})}\n\n"
                elif node_name == "guardrail":
                    yield f"data: {json.dumps({'type': '状态', 'content': '审核通过' if node_output.get('is_approved') else '审核失败重试'})}\n\n"
        yield f"data: {json.dumps({'type': '完成', 'content': '全部生成完毕'})}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/")
def root():
    return {"message": "AI系统已启动！"}