from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .connect import Base

# 用户表
class EduUser(Base):
    __tablename__ = "edu_user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    nickname = Column(String(50))
    major = Column(String(50))
    create_time = Column(DateTime, default=func.now())

# 对话记录表
class EduChat(Base):
    __tablename__ = "edu_chat"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer)
    session_id = Column(String(100))
    content = Column(Text)
    role = Column(String(20))
    create_time = Column(DateTime, default=func.now())

# 用户学习画像表
class EduProfile(Base):
    __tablename__ = "edu_profile"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    weak_points = Column(Text)
    learning_json = Column(Text)
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())

# 资源存储表
class EduResource(Base):
    __tablename__ = "edu_resource"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer)
    resource_type = Column(String(30))
    content = Column(Text)
    progress = Column(Integer, default=0)
    create_time = Column(DateTime, default=func.now())
from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
# Base 在 schemas 文件夹
from schemas.base import Base

class Conversation(Base):
    __tablename__ = "conversation"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="对话主键")
    # 临时注释外键
    # user_id = Column(Integer, ForeignKey("edu_user.id"), nullable=False, comment="关联用户")
    user_id = Column(Integer, nullable=False, comment="关联用户")
    session_id = Column(String(128), nullable=False, comment="会话唯一标识")
    role = Column(String(32), nullable=False, comment="user/assistant")
    content = Column(Text, nullable=False, comment="对话内容")
    portrait_json = Column(JSON, nullable=True, comment="画像快照")
    create_time = Column(DateTime, server_default=func.now())
    # 临时注释关联
    # user = relationship("User")