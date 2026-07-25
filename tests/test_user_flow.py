# -*- coding: utf-8 -*-
"""端到端流程测试：模拟用户完整操作链路"""

import os
import pytest
import sys

# 把项目根目录加入 sys.path，确保能 import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import ApiClient, assert_status, assert_json_has_keys, load_json_file


# ===== Fixtures =====

@pytest.fixture(scope="class")
def api_client():
    """创建ApiClient实例，整个测试类共享一个"""
    client = ApiClient()
    yield client
    client.session.close()


@pytest.fixture(scope="module")
def test_data():
    """加载测试数据文件"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    filepath = os.path.join(data_dir, "test_data.json")
    return load_json_file(filepath)


# ===== 第一步：健康检查 =====

class TestHealthCheck:
    """确认后端服务正常运行"""

    def test_server_is_alive(self, api_client):
        resp = api_client.get("/api/health")
        assert_status(resp, 200)
        data = assert_json_has_keys(resp, "status")
        assert data["status"] == "ok"


# ===== 第二步：登录流程 =====

class TestLoginFlow:
    """登录功能验证"""

    def test_login_success(self, api_client):
        resp = api_client.login("admin", "123456")
        assert_status(resp, 200)
        data = resp.json()
        assert "登录成功" in data.get("message", "")

    def test_login_wrong_password(self, api_client):
        resp = api_client.login("admin", "wrong_password")
        assert_status(resp, 401)

    def test_login_empty_fields(self, api_client):
        resp = api_client.login("", "123456")
        assert_status(resp, 400)


# ===== 第三步：用户数据验证 =====

class TestUserData:
    """用户数据接口验证"""

    def test_get_all_users(self, api_client):
        resp = api_client.get_users()
        assert_status(resp)
        users = resp.json()
        assert isinstance(users, list), f"期望返回列表，实际类型: {type(users)}"
        assert len(users) > 0, "用户列表不应为空"

    def test_get_user_by_id(self, api_client, test_data):
        for case in test_data["user_check_cases"]:
            resp = api_client.get_user(case["user_id"])
            assert_status(resp)
            user = resp.json()
            assert user["name"] == case["expected_name"], \
                f"用户ID={case['user_id']}，期望名称={case['expected_name']}，实际={user['name']}"

    def test_get_user_has_required_fields(self, api_client):
        resp = api_client.get_user(1)
        assert_status(resp)
        user = resp.json()
        required_fields = ["id", "name", "email"]
        for field in required_fields:
            assert field in user, \
                f"用户对象缺少字段 '{field}'，当前字段: {list(user.keys())}"


# ===== 第四步：Echo + 端到端链路 =====

class TestEchoAndFlow:
    """Echo接口 + 完整业务链路"""

    def test_echo_post(self, api_client, test_data):
        payload = test_data["echo_test_data"]
        resp = api_client.echo(payload)
        assert_status(resp)
        echoed = resp.json()
        assert echoed["data"]["message"] == payload["message"]
        assert echoed["data"]["timestamp"] == payload["timestamp"]

    def test_complete_user_flow(self, api_client, test_data):
        """端到端流程：登录→查用户→验证数据一致性"""
        # 步骤1：健康检查
        health = api_client.get("/api/health")
        assert_status(health)

        # 步骤2：登录
        login_resp = api_client.login()
        assert_status(login_resp)

        # 步骤3：获取用户列表
        users_resp = api_client.get_users()
        assert_status(users_resp)
        users = users_resp.json()
        assert len(users) > 0

        # 步骤4：用列表里第一个用户的ID去查详情
        first_user_id = users[0]["id"]
        detail_resp = api_client.get_user(first_user_id)
        assert_status(detail_resp)
        detail = detail_resp.json()

        # 步骤5：验证列表和详情里的用户信息一致
        assert detail["id"] == first_user_id
        assert detail["name"] == users[0]["name"], \
            f"列表中的用户名和详情不一致：'{users[0]['name']}' vs '{detail['name']}'"

        # 步骤6：echo接口也在整体链路中验证
        echo_resp = api_client.echo({"step": "flow_complete"})
        assert_status(echo_resp)