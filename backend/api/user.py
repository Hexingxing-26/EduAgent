from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connect import get_db
from database import crud
from schemas.base import UserCreate, UserOut
from api.common import create_token, get_current_user
from utils.response import success
from utils.exception import ApiException

router = APIRouter(prefix="/user", tags=["用户模块"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise ApiException(code=400, msg="用户名已存在")
    # 角色校验
    allowed_roles = {"student", "teacher", "admin"}
    role = getattr(user, "role", None)
    if role is None or role not in allowed_roles:
        raise ApiException(code=400, msg="角色不合法，可选值：student/teacher/admin")
    new_user = crud.create_user(db, user.dict())
    return success(data=UserOut.model_validate(new_user).model_dump())

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user or user.password != password:
        raise ApiException(400, "账号密码错误")
    # token 中携带真实 role
    token = create_token(user.id, role=getattr(user, "role", None))
    return success(data={"token": token})

@router.get("/info")
def user_info(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = current_user["user_id"]
    user = crud.get_user_by_id(db, uid)
    if not user:
        raise ApiException(404, "用户不存在")
    return success(data=UserOut.model_validate(user).model_dump())