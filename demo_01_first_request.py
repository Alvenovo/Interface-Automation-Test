import requests

# 1. 定义接口地址
url = "http://localhost:5000/api/users"

# 2. 发送GET请求
response = requests.get(url)

# 3. 查看状态码
print("状态码：", response.status_code)

# 4. 查看响应头
print("Content-Type:", response.headers.get("Content-Type"))

# 5. 解析JSON——返回的是用户列表
users = response.json()
print("用户数量：", len(users))

# 4.4 打印第一个用户的姓名和邮箱
first_user = users[0]
print(f"第一个用户姓名: {first_user['name']}")
print(f"第一个用户邮箱: {first_user['email']}")

# 打印所有用户的姓名
for user in users:
    print(f"  - {user['name']} ({user['email']})")

#查看返回值类型
print(type(response.json()))
print(type(users))

response2 = requests.post("http://localhost:5000/api/echo",json={
    "title": "我的第一个POST请求",
    "body": "接口自动化测试学习中",
    "userId": 1
})
print(response2.json())