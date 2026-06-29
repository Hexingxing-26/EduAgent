from fastapi import FastAPI
from database.connect import engine, Base
from routers import user

# 自动创建表（本地已有表不会重复生成）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduAgent学习助手后端")

# 注册路由
app.include_router(user.router)

@app.get("/")
def root():
    return {"msg":"后端服务启动成功，访问 /docs 查看接口文档"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)