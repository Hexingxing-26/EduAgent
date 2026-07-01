from sqlalchemy.orm import Session
from .models import EduUser, EduChat, Students, EduResource, LearningRecords
from .crud_edu_resource import (
    create_edu_resource,
    update_resource_progress,
    update_resource_content,
    get_user_resource_list,
    delete_resource
)

# 根据用户名查询用户
def get_user_by_username(db: Session, username: str):
    return db.query(EduUser).filter(EduUser.username == username).first()

# 根据ID查询用户
def get_user_by_id(db: Session, user_id: int):
    return db.query(EduUser).filter(EduUser.id == user_id).first()

# 新增用户
def create_user(db: Session, user_data: dict):
    db_user = EduUser(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user