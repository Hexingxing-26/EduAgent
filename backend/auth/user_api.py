from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from .jwt_util import create_access_token, verify_token
from .pwd_util import hash_password, verify_password

auth_router = APIRouter(prefix="/user", tags=["用户鉴权"])

# 登录入参模型
class LoginForm(BaseModel):
    username: str
    password: str

# 测试用户数据，后续对接数据库替换
fake_user_db = {
    "student1": {
        "username": "student1",
        "hashed_pwd": hash_password("123456"),
        "role": "student"
    }
}

@auth_router.post("/login")
def login(form: LoginForm):
    """用户登录接口，返回Token"""
    user = fake_user_db.get(form.username)
    if not user or not verify_password(form.password, user["hashed_pwd"]):
        raise HTTPException(status_code=401, detail="账号或密码错误")
    # 生成token，携带用户名、角色
    token = create_access_token({"username": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str):
    """全局鉴权依赖函数，所有需要登录的接口调用"""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="登录已失效，请重新登录")
    return payload

@auth_router.get("/info")
def get_user_info(user_info = Depends(get_current_user)):
    """获取当前登录用户信息，必须携带有效Token"""
    return user_info