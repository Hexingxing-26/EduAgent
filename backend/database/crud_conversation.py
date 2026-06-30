from sqlalchemy.orm import Session
from database.models import Conversation
from sqlalchemy import desc

# 1. 新增一条对话消息
def create_conversation(
    db: Session,
    user_id: int,
    session_id: str,
    role: str,
    content: str,
    portrait_json: dict = None
):
    db_conv = Conversation(
        user_id=user_id,
        session_id=session_id,
        role=role,
        content=content,
        portrait_json=portrait_json
    )
    db.add(db_conv)
    db.commit()
    db.refresh(db_conv)
    return db_conv

# 2. 根据会话ID，查询该会话下所有对话（按时间倒序，最新在前）
def get_session_conversations(db: Session, user_id: int, session_id: str):
    return db.query(Conversation)\
        .filter(Conversation.user_id == user_id, Conversation.session_id == session_id)\
        .order_by(desc(Conversation.create_time))\
        .all()

# 3. 查询用户全部会话（去重session_id）
def get_user_all_session_ids(db: Session, user_id: int):
    res = db.query(Conversation.session_id)\
        .filter(Conversation.user_id == user_id)\
        .distinct()\
        .all()
    return [row[0] for row in res]

# 4. 删除单个会话所有对话
def delete_session_conversation(db: Session, user_id: int, session_id: str):
    db.query(Conversation)\
        .filter(Conversation.user_id == user_id, Conversation.session_id == session_id)\
        .delete()
    db.commit()
    return True

# 5. 删除用户全部对话记录
def delete_user_all_conversation(db: Session, user_id: int):
    db.query(Conversation).filter(Conversation.user_id == user_id).delete()
    db.commit()
    return True