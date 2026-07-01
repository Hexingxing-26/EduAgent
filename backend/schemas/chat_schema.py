from pydantic import BaseModel

class StreamChatRequest(BaseModel):
    """SSE流式对话接口入参"""
    session_id: str
    user_content: str