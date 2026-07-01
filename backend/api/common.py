from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, Header
import jwt
from sqlalchemy.orm import Session
from database.connect import get_db
from database.crud import get_user_by_id

SECRET_KEY = "secret123456"
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 120

# 生成Token函数保持不变
def create_token(user_id: int, role: Optional[str] = None):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    if role is not None:
        payload["role"] = role
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# 重写鉴权函数：从Header拿token，抛弃OAuth2PasswordBearer
def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    # 校验请求头是否携带Token
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未携带Token，请重新登录")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid = int(payload.get("sub"))
        user_role = payload.get("role", "student")

        if not uid:
            raise HTTPException(401, "Token无效")
        # 校验用户是否还存在于数据库
        db_user = get_user_by_id(db, uid)
        if not db_user:
            raise HTTPException(401, "用户已被注销")

    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token已过期")
    except Exception:
        raise HTTPException(401, "Token错误")

    return {"user_id": uid, "role": user_role}

# 封装好的角色权限依赖，后续业务接口直接用
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