from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# 用户基础校验模型
class UserBase(BaseModel):
    username: str
    nickname: str | None = None
    major: str | None = None

class UserCreate(UserBase):
    password: str
    role: str | None = "student"

class UserOut(UserBase):
    id: int
    role: str | None = "student"
    create_time: datetime
    class Config:
        orm_mode = True