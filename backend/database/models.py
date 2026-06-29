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