from sqlalchemy.orm import Session
from database.models import Students

# 根据用户ID查询专属画像
def get_user_profile(db: Session, user_id: int):
    # 仅查询当前用户的画像数据，实现数据隔离
    return db.query(Students).filter(Students.id == user_id).first()

# 更新用户画像，无记录则自动创建空记录再更新
def update_user_profile(db: Session, user_id: int, portrait_data: dict):
    # 先查询用户是否已有画像
    user_profile = get_user_profile(db, user_id)
    # 不存在则新建空画像记录
    if not user_profile:
        user_profile = Students(
            user_id=user_id,
            portrait_json=None
        )
        db.add(user_profile)
    # 覆盖更新画像JSON内容
    user_profile.portrait_json = portrait_data
    # 提交事务刷新数据
    db.commit()
    db.refresh(user_profile)
    return user_profile