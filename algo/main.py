from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from pyprojroot import here
import sys
sys.path.append(str(here()))

from api.routers import questions
from api.routers.preload import preload_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"[PID {os.getpid()}] FastAPI 启动")
    await preload_manager.preload_all()
    yield
    await preload_manager.cleanup()

# 创建 FastAPI 实例，并注册 lifespan
app = FastAPI(lifespan=lifespan)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions.router)

# 仅测试单独启用 FastAPI 时使用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)