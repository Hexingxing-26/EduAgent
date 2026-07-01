from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connect import get_db
from database.crud import (
    create_edu_resource,
    update_resource_progress,
    update_resource_content,
    get_user_resource_list,
    delete_resource
)
from api.user import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/resource", tags=["edu资源管理模块"])

# 请求体模型定义
class CreateResourceReq(BaseModel):
    portrait_id: int
    resource_type: str

class UpdateProgressReq(BaseModel):
    task_id: str
    progress: int

class UpdateContentReq(BaseModel):
    task_id: str
    doc_content: str
    mermaid_code: str
    question_json: str

# 1. 创建资源生成任务（初始化记录，进度0）
@router.post("/create")
def create_resource(
    req: CreateResourceReq,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    res = create_edu_resource(
        db=db,
        user_id=current_user.id,
        portrait_id=req.portrait_id,
        resource_type=req.resource_type
    )
    return {"code": 200, "msg": "创建生成任务成功", "data": res}

# 2. 更新AI生成进度（给D同学智能体回调使用）
@router.put("/update/progress")
def update_progress(
    req: UpdateProgressReq,
    db: Session = Depends(get_db)
):
    if not 0 <= req.progress <= 100:
        raise HTTPException(status_code=400, detail="进度必须在0~100之间")
    res = update_resource_progress(db=db, task_id=req.task_id, progress=req.progress)
    if not res:
        raise HTTPException(status_code=404, detail="不存在该task_id任务")
    return {"code": 200, "msg": "进度更新完成", "data": res}

# 3. AI全部生成完成后回填完整内容
@router.put("/update/content")
def fill_resource_content(
    req: UpdateContentReq,
    db: Session = Depends(get_db)
):
    res = update_resource_content(
        db=db,
        task_id=req.task_id,
        doc_content=req.doc_content,
        mermaid_code=req.mermaid_code,
        question_json=req.question_json
    )
    if not res:
        raise HTTPException(status_code=404, detail="不存在该task_id任务")
    return {"code": 200, "msg": "资源内容入库完成", "data": res}

# 4. 分页查询当前用户资源（给前端B页面展示）
@router.get("/list")
def get_user_resource(
    page: int = 1,
    page_size: int = 10,
    resource_type: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    data = get_user_resource_list(
        db=db,
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        res_type=resource_type
    )
    return {"code": 200, "msg": "查询成功", "data": data}

# 5. 逻辑删除资源
@router.delete("/delete/{resource_id}")
def remove_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    res = delete_resource(db=db, resource_id=resource_id)
    if not res:
        raise HTTPException(status_code=404, detail="目标资源不存在")
    return {"code": 200, "msg": "资源已删除"}