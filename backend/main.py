from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connect import engine, Base
from api import user
from utils.exception import register_exception
from utils.logger import log

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduAgent后端")

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

# 路由
app.include_router(user.router)

@app.get("/")
def root():
    return {"msg": "服务正常，访问 /docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)