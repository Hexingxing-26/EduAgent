from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from utils.response import fail
from utils.logger import log

class ApiException(Exception):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

def register_exception(app: FastAPI):
    @app.exception_handler(ApiException)
    async def api_err_handler(request: Request, exc: ApiException):
        log.error(f"业务异常：{exc.msg}")
        return JSONResponse(content=fail(msg=exc.msg, code=exc.code).model_dump())

    @app.exception_handler(Exception)
    async def global_err_handler(request: Request, exc: Exception):
        log.error(f"系统异常：{str(exc)}")
        return JSONResponse(content=fail(msg="服务器内部错误", code=500).model_dump())