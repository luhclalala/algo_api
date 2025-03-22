### 使用说明
1. 在docker desktop中下载以下镜像：
```
nginx:latest
redis:alpine
mysql:8.0
```
2. 进入algo目录，执行构建镜像：
```
docker build -t algo_server .
```
3. 在根目录下执行命令启动容器：
```
docker-compose up
```

### 文件结构
```
.
├── README.md
├── algo
│   ├── Dockerfile
│   ├── api
│   │   ├── __init__.py
│   │   ├── database
│   │   │   ├── __init__.py
│   │   │   ├── curd.py # 建立数据库引擎，创建会话工厂
│   │   │   └── models.py # 定义数据库模型
│   │   └── routers
│   │       ├── __init__.py
│   │       ├── questions.py # 定义路由
│   │       ├── schemas.py # 定义接口数据模型
│   │       └── tasks.py # 模拟算法任务
│   ├── config.py
│   ├── main.py
│   └── requirements.txt
├── docker-compose.yml
├── mysql
│   └── init.sql
├── nginx.conf
├── static # 静态文件
└── test_api.py
```