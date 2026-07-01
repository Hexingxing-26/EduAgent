from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# 数据库会话依赖
from database.connect import get_db
# 用户鉴权依赖
from api.common import get_current_user
# CRUD操作
from database.crud_conversation import (
    create_conversation,
    get_session_conversations,
    get_user_all_session_ids,
    delete_session_conversation,
    delete_user_all_conversation
)
# 数据模型
from schemas.conversation_schema import ConversationCreate, ConversationItem,SessionListResp

router = APIRouter(prefix="/conversation", tags=["对话会话模块"])

# 1. 新增一条对话消息
@router.post("/add", response_model=ConversationItem)
def add_conversation(
    conv_data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return create_conversation(
        db=db,
        user_id=current_user["user_id"],
        session_id=conv_data.session_id,
        role=conv_data.role,
        content=conv_data.content,
        portrait_json=conv_data.portrait_json
    )

# 2. 查询单个会话全部对话记录
@router.get("/session/{session_id}", response_model=List[ConversationItem])
def get_one_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_session_conversations(db, current_user["user_id"], session_id)

# 3. 查询用户所有会话ID列表
@router.get("/session/list", response_model=SessionListResp)
def get_all_session(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    session_ids = get_user_all_session_ids(db, current_user["user_id"])
    return {"session_ids": session_ids}

# 4. 删除指定会话全部消息
@router.delete("/session/{session_id}")
def del_one_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    delete_session_conversation(db, current_user["user_id"], session_id)
    return {"msg": "当前会话对话已清空"}

# 5. 清空用户全部对话记录
@router.delete("/all")
def del_all_conversation(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    delete_user_all_conversation(db, current_user["user_id"])
    return {"msg": "您所有对话记录已清空"}