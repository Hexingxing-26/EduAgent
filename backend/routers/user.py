from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connect import get_db
from database import crud
from schemas.base import UserCreate, UserOut

router = APIRouter(prefix="/user", tags=["用户模块"])

# 注册接口
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return crud.create_user(db, user.dict())