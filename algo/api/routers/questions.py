from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import uuid
from datetime import timedelta
from pyprojroot import here
import sys
sys.path.append(str(here()))

from api.database.curd import get_db
from api.database import models
import api.routers.schemas as schemas
from api.routers.tasks import async_algorithm
from api.routers.preload import preload_manager

router = APIRouter(prefix="/query", tags=["query"])

@router.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok"}

@router.post(
    "/submit", 
    response_model=schemas.TaskResponse,
    summary="异步提交任务",
    description="提交 query 创建异步任务，并返回 task_id"
)
async def start_task(request: schemas.QuestionRequest, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    task_id = str(uuid.uuid4())

    # 任务初始状态写入 Redis
    preload_manager.redis_conn.hset(f"task:{task_id}", mapping={"status": "processing"})
    preload_manager.redis_conn.expire(f"task:{task_id}", timedelta(hours=1))

    # 添加异步任务
    background_tasks.add_task(async_algorithm, request.query, task_id, db)
    
    return {"task_id": task_id}

@router.get(
    "/poll/{task_id}",
    response_model=schemas.PollResponse,
    summary="查询任务状态",
    description="通过 task_id 查询任务执行状态"
)
async def get_task_result(task_id: str, db: AsyncSession = Depends(get_db)):
    status = preload_manager.redis_conn.hget(f"task:{task_id}", "status")

    if status == b"processing":
        return {"task_id": task_id, "status": "processing"}
    
    if status == b"completed":
        result = preload_manager.redis_conn.hget(f"task:{task_id}", "result").decode("utf-8")
        result = preload_manager.global_config.get("log_level", "未找到结果")
        return {"task_id": task_id, "status": "completed", "result": result}

    # 从数据库查询
    query = select(models.QueryAnswer).where(models.QueryAnswer.task_id == task_id)
    result = await db.execute(query)
    task = result.scalar()

    if task:
        preload_manager.redis_conn.hset(f"task:{task_id}", mapping={"result": task.result, "status": "completed"})
        preload_manager.redis_conn.expire(f"task:{task_id}", timedelta(hours=1))
        return {"task_id": task_id, "status": "completed", "result": task.result}

    return {"task_id": task_id, "status": "failed"}
