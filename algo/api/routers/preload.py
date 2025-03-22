import json
import os
from redis import Redis
import logging


def log_with_pid(message: str):
    pid = os.getpid()
    print(f"[PID {pid}] {message}", flush=True)

class PreloadManager:
    def __init__(self):
        self.config_path = "config.json"
        self.global_config = {}
        self.ai_model = None
        self.redis_conn = None

    async def preload_all(self):
        """ 执行所有预加载任务 """
        self.load_config()
        self.load_model()
        self.connect_redis()

    def load_config(self):
        """ 加载全局配置 """
        try:
            log_with_pid("加载配置")
            with open(self.config_path, "r") as f:
                self.global_config = json.load(f)
            print(self.global_config)
            log_with_pid("加载配置成功")
        except FileNotFoundError:
            log_with_pid("配置文件不存在，请检查 config.json 文件是否存在")
            exit(1)

    def load_model(self):
        """ 加载 AI 模型 """
        pass

    def connect_redis(self):
        """ 连接 Redis """
        try:
            log_with_pid("连接 Redis")
            self.redis_conn = Redis(host="redis", port=6379, db=0)
            log_with_pid("Redis 连接成功")
        except Exception as e:
            log_with_pid(f"Redis 连接失败: {e}")

    async def cleanup(self):
        """ 清理资源 """
        log_with_pid("释放 AI 模型 & 清理配置")
        self.global_config.clear()
        self.ai_model = None
        await self.redis_conn.close()

preload_manager = PreloadManager()
