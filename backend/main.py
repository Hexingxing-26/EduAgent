from api.resource_router import router as resource_router
from api.portrait_router import router as portrait_router
from api.conversation_router import router as conv_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connect import engine, Base
from api import user
from utils.exception import register_exception
from utils.logger import log
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="个性化学习多智能体系统")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常
register_exception(app)

# 注册全部路由
app.include_router(resource_router)
app.include_router(conv_router)
app.include_router(portrait_router)

@app.get("/")
def root():
    return {"msg": "服务正常，访问 /docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from api import all_v1_routers
for r in all_v1_routers:
    app.include_router(r)