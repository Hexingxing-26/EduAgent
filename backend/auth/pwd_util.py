from passlib.context import CryptContext

# 密码加密算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(raw_pwd: str) -> str:
    """明文密码加密"""
    return pwd_context.hash(raw_pwd)

def verify_password(raw_pwd: str, hashed_pwd: str) -> bool:
    """比对明文和加密密码是否一致"""
    return pwd_context.verify(raw_pwd, hashed_pwd)