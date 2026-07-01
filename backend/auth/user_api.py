from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .jwt_util import create_access_token, verify_token
from .pwd_util import verify_password
# 修正1：get_db从connect.py导入
from backend.database.connect import get_db
# 修正2：用户模型类名改为EduUser
from backend.database.models import EduUser

auth_router = APIRouter(prefix="/user", tags=["用户鉴权"])

# 登录入参模型
class LoginForm(BaseModel):
    username: str
    password: str

# 登录接口（适配队友的EduUser表）
@auth_router.post("/login")
def login(form: LoginForm, db: Session = Depends(get_db)):
    # 根据用户名查询EduUser表
    user = db.query(EduUser).filter(EduUser.username == form.username).first()
    # 修正3：密码字段由 hashed_pwd 改为 password
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="账号或密码错误")
    # 暂时先把role写为固定值，后续如果表内新增role字段再优化
    token_data = {"username": user.username, "role": user.role}
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}

# 全局鉴权依赖函数
def get_current_user(token: str, db: Session = Depends(get_db)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="登录已失效，请重新登录")
    username = payload.get("username")
    user = db.query(EduUser).filter(EduUser.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user

# 获取用户信息接口
@auth_router.get("/info")
def get_user_info(user = Depends(get_current_user)):
    return {
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "major": user.major,
        "role": user.role
    }