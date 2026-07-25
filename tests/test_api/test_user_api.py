import requests
import pytest
import allure


# ===== 原有测试用例 =====

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


# ===== 第13课：Allure 装饰器示例 =====

@allure.feature("用户管理")
@allure.story("用户注册")
@allure.severity(allure.severity_level.CRITICAL)
class TestUserRegistration:

    @allure.title("正常注册——有效邮箱和密码")
    @allure.description("使用符合规则的邮箱和密码进行注册")
    def test_register_success(self, api):
        with allure.step("步骤1：发送注册请求"):
            response = api.register(
                email="user@example.com",
                password="SecureP@ss123"
            )

        with allure.step("步骤2：验证响应状态码"):
            assert response.status_code == 201

        with allure.step("步骤3：验证返回的用户数据"):
            data = response.json()
            assert data["email"] == "user@example.com"
            assert "id" in data

    @allure.title("注册失败——邮箱格式无效")
    def test_register_invalid_email(self, api):
        response = api.register(
            email="not-an-email",
            password="SecureP@ss123"
        )
        assert response.status_code == 400
