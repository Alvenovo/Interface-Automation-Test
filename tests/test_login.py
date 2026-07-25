import pytest
import requests

@pytest.mark.parametrize("username,password,expected_code", [
    ("admin",  "123456", 200),   # 第1组：正确登录
    ("admin",  "wrong",  401),   # 第2组：密码错误
    ("",       "123456", 400),   # 第3组：用户名为空
    ("admin",  "",       400),   # 第4组：密码为空
])
def test_login(base_url, username, password, expected_code):
    """登录接口参数化测试"""
    response = requests.post(base_url + "/api/login",
        json={"username": username, "password": password})
    assert response.status_code == expected_code
