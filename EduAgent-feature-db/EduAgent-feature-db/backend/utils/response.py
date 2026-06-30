from pydantic import BaseModel

class ResModel(BaseModel):
    code: int
    msg: str
    data: dict | None = None

def success(data=None, msg="操作成功") -> ResModel:
    return ResModel(code=200, msg=msg, data=data)

def fail(msg="操作失败", code=400) -> ResModel:
    return ResModel(code=code, msg=msg)