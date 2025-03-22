FROM python:3.12-slim
# 后续参考Yintai的Dockerfile进行修改

# 设置工作目录
WORKDIR /app

# 复制并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装工具
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    nmap \
    net-tools \
    iputils-ping \
    vim \
    && rm -rf /var/lib/apt/lists/*

# 拷贝依赖清单并安装 Python 包
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 暴露指定端口
EXPOSE 8000

# 复制应用程序代码
# COPY . .

# 启动应用程序
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app"]
