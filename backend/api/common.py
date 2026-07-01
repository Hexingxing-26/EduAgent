from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from database.crud import get_user_by_id

SECRET_KEY = "secret123456"
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 120

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def create_token(user_id: int, role: Optional[str] = None):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    if role is not None:
        payload["role"] = role
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid = int(payload.get("sub"))
        user_role = payload.get("role", "student")  # 兜底默认 student
        if uid is None:
            raise HTTPException(status_code=401, detail="token无效")
    except Exception:
        raise HTTPException(status_code=401, detail="token过期或错误")
    # 返回包含用户ID和角色的字典
    return {"user_id": uid, "role": user_role}


# ---------- 角色权限依赖（可在路由中复用） ----------
def only_student(user_info = Depends(get_current_user)):
    if user_info["role"] != "student":
        raise HTTPException(status_code=403, detail="仅学生可访问")
    return user_info

def teacher_or_admin(user_info = Depends(get_current_user)):
    if user_info["role"] not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="仅教师、管理员可访问")
    return user_info

def only_admin(user_info = Depends(get_current_user)):
    if user_info["role"] != "admin":
        raise HTTPException(status_code=403, detail="仅超级管理员可访问")
    return user_info