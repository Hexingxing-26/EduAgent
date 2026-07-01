from sqlalchemy.orm import Session
from database.models import EduResource
from pydantic import BaseModel
import uuid

# 创建资源任务记录（初始化进度0）
def create_edu_resource(db: Session, user_id: int, portrait_id: int, resource_type: str):
    task_id = str(uuid.uuid4())
    db_record = EduResource(
        user_id=user_id,
        portrait_id=portrait_id,
        resource_type=resource_type,
        generate_progress=0,
        task_id=task_id
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

# 更新生成进度
def update_resource_progress(db: Session, task_id: str, progress: int):
    record = db.query(EduResource).filter(EduResource.task_id == task_id).first()
    if not record:
        return None
    record.generate_progress = progress
    db.commit()
    db.refresh(record)
    return record

# 回填完整生成内容（文档、思维导图、题库）
def update_resource_content(db: Session, task_id: str, doc_content: str, mermaid_code: str, question_json: str):
    record = db.query(EduResource).filter(EduResource.task_id == task_id).first()
    if not record:
        return None
    record.content = doc_content
    record.mermaid_code = mermaid_code
    record.question_json = question_json
    record.generate_progress = 100
    db.commit()
    db.refresh(record)
    return record

# 分页查询用户资源列表
def get_user_resource_list(db: Session, user_id: int, page: int = 1, page_size: int = 10, res_type: str = None):
    offset = (page - 1) * page_size
    query = db.query(EduResource).filter(EduResource.user_id == user_id, EduResource.is_delete == 0)
    if res_type:
        query = query.filter(EduResource.resource_type == res_type)
    total = query.count()
    data = query.offset(offset).limit(page_size).all()
    return {"total": total, "list": data, "page": page, "page_size": page_size}

# 逻辑删除资源
def delete_resource(db: Session, resource_id: int):
    record = db.query(EduResource).filter(EduResource.id == resource_id).first()
    if not record:
        return None
    record.is_delete = 1
    db.commit()
    return record