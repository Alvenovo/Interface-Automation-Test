import requests

def test_get_users_status_code(users_url):
    """测试：获取用户列表，状态码应该是200"""
    response = requests.get(users_url)
    assert response.status_code == 200

def test_get_users_has_data(users_url):
    """测试：返回的用户列表不应该为空"""
    response = requests.get(users_url)
    users = response.json()
    assert isinstance(users, list), f"期望返回列表，实际类型: {type(users)}"
    assert len(users) > 0, "用户列表不应为空"

def test_get_users_first_has_name(users_url):
    """测试：第一个用户包含 name 字段"""
    response = requests.get(users_url)
    users = response.json()
    first_user = users[0]
    assert "name" in first_user, f"用户对象缺少 name 字段"
