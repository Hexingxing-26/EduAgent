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

class UserOut(UserBase):
    id: int
    create_time: datetime
    class Config:
        orm_mode = True