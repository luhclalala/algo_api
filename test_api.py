import requests
import time

BASE_URL = "http://localhost/query"

def health_check():
    """检查服务是否正常"""
    url = f"{BASE_URL}/health"
    response = requests.get(url)
    print("✅ 健康检查:", response.json())

def submit_task(query):
    """提交异步任务"""
    url = f"{BASE_URL}/submit"
    data = {"query": query}
    response = requests.post(url, json=data)
    print("📌 提交任务:", response.json())
    return response.json().get("task_id")

def poll_task(task_id):
    """轮询查询任务结果"""
    url = f"{BASE_URL}/poll/{task_id}"
    while True:
        response = requests.get(url)
        result = response.json()
        print("⏳ 任务状态:", result)

        if result.get("status") == "completed":
            print("🎯 任务完成，最终结果:", result)
            break

        elif result.get("status") == "failed":
            print("❌ 任务失败")
            break

        time.sleep(2)

if __name__ == "__main__":
    # 1. 健康检查
    health_check()

    # 3. 提交异步任务
    task_id = submit_task("测试异步任务")

    # 4. 轮询获取结果
    if task_id:
        poll_task(task_id)