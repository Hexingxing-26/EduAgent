from fastapi import APIRouter, Depends
from pydantic import BaseModel  # 新增：用来做登录JSON校验
from sqlalchemy.orm import Session
from database.connect import get_db
from database import crud
from schemas.base import UserCreate, UserOut
from api.common import create_token, get_current_user
from utils.response import success
from utils.exception import ApiException
from auth.pwd_util import hash_password, verify_password

# 新增：登录接口的JSON请求体模型
class LoginForm(BaseModel):
    username: str
    password: str
router = APIRouter(prefix="/user", tags=["用户模块"])

# 公开注册：仅注册学生，强制固定role
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise ApiException(code=400, msg="用户名已存在")

    user_data = user.dict()
    # 强制覆盖，拒绝前端传入的role
    user_data["role"] = "student"
    user_data["password"] = hash_password(user_data["password"])
    new_user = crud.create_user(db, user_data)
    return success(data=UserOut.model_validate(new_user).model_dump())

# 管理员创建教师账号
@router.post("/register/teacher")
def create_teacher_account(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise ApiException(code=403, msg="权限不足，仅管理员可创建教师账号")

    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise ApiException(code=400, msg="用户名已存在")

    user_data = user.dict()
    user_data["role"] = "teacher"
    user_data["password"] = hash_password(user_data["password"])
    new_user = crud.create_user(db, user_data)
    return success(data=UserOut.model_validate(new_user).model_dump())

# 登录接口
@router.post("/login")
def login(form: LoginForm, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form.username)
    if not user or not verify_password(form.password, user.password):
        raise ApiException(400, "账号密码错误")
    token = create_token(user.id, role=user.role)
    return success(data={"token": token})

# 获取用户信息
@router.get("/info")
def user_info(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = current_user["user_id"]
    user = crud.get_user_by_id(db, uid)
    if not user:
        raise ApiException(404, "用户不存在")
    return success(data=UserOut.model_validate(user).model_dump())