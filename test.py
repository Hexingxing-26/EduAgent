import requests
import json

url = "http://localhost:8000/chat/stream"
payload = {
    "user_id": "test001",
    "message": "我想学习机器学习中的决策树算法"
}

# 发送 POST 请求，开启流式接收
response = requests.post(url, json=payload, stream=True)

print("正在等待AI响应...\n")
for line in response.iter_lines():
    if line:
        # 去掉 "data: " 前缀
        raw_data = line.decode('utf-8')
        if raw_data.startswith("data: "):
            try:
                data = json.loads(raw_data[6:])  # 去掉 "data: " 前缀
                print(f"收到: {data}")
            except:
                print(f"原始数据: {raw_data}")