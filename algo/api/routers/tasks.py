from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from api.database import models
from api.routers.preload import preload_manager

async def async_algorithm(query: str, task_id: str, db: AsyncSession):
    """异步执行算法，并存储结果到 Redis 和数据库"""
    await asyncio.sleep(10)  # 模拟耗时任务
    result = f"Processed result for query: {query}"

    # 更新 Redis
    preload_manager.redis_conn.hset(f"task:{task_id}", mapping={"result": result, "status": "completed"})

    # 存储到数据库
    db_task = models.QueryAnswer(task_id=task_id, query=query, result=result)
    async with db.begin():
        db.add(db_task)