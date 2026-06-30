from pydantic import BaseModel
from typing import Dict, Optional

# 更新画像接口的请求入参
class PortraitUpdate(BaseModel):
    # 存储多维度用户标签，例如学习基础、薄弱科目、学习习惯等
    portrait_json: Dict

# 查询画像接口的返回结构
class PortraitResp(BaseModel):
    user_id: int
    portrait_json: Optional[Dict]

    # Pydantic V2 标准写法，替代过时的 orm_mode = True
    class Config:
        from_attributes = True