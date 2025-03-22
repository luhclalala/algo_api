import multiprocessing
import os

# 绑定地址和端口
bind = "0.0.0.0:8000"

# 工作进程数（这里使用 CPU 核心数的 2 倍 + 1）
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 4

# 使用 Uvicorn 作为 worker 进程
worker_class = "uvicorn.workers.UvicornWorker"

# 预加载应用（适用于共享只读资源）
preload_app = True
# lifespan = "on" 

# 允许 keep-alive 连接
keepalive = 5

# 访问日志和错误日志
accesslog = "-"
errorlog = "-"

# 日志级别
loglevel = "info"