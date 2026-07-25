import requests
def test_get_users_status():
    """测试：获取用户列表，状态码应该为200"""
    url = "http://localhost:5000/api/users"
    response = requests.get(url)
    assert response.status_code == 200

def test_get_users_data():
    """测试：返回的用户数据列表不应该为空"""
    url = "http://localhost:5000/api/users"
    response = requests.get(url)
    users = response.json()
    assert len(users) > 0