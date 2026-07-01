from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# 全局数据库会话依赖
from database.connect import get_db
# 登录鉴权依赖，校验当前登录用户
from api.common import get_current_user
# 画像数据库操作函数
from database.crud_profile import get_user_profile, update_user_profile
# 画像请求/返回模型
from schemas.portrait_schema import PortraitUpdate, PortraitResp

# 路由统一前缀、接口分组标签
router = APIRouter(prefix="/portrait", tags=["用户画像模块"])

# 接口1：获取当前登录用户的个人画像
@router.get("/me", response_model=PortraitResp)
def get_my_user_portrait(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # 传入当前登录用户ID，只查询本人画像
    return get_user_profile(db=db, user_id=current_user["user_id"]) 

# 接口2：更新当前登录用户的画像数据
@router.post("/update", response_model=PortraitResp)
def update_my_user_portrait(
    req_body: PortraitUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # 仅更新当前登录用户的画像，无法篡改其他用户数据
    return update_user_profile(
        db=db,
        user_id=current_user["user_id"],
        portrait_data=req_body.portrait_json
    )