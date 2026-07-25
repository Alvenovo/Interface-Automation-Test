# -*- coding: utf-8 -*-
"""接口自动化测试 - 工具模块"""

import requests
import json
import os


class ApiClient:
    """HTTP API 客户端"""

    def __init__(self, base_url=None):
        self.base_url = base_url or "http://localhost:5001"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def get(self, path, **kwargs):
        url = self.base_url + path
        return self.session.get(url, **kwargs)

    def post(self, path, **kwargs):
        url = self.base_url + path
        return self.session.post(url, **kwargs)

    def put(self, path, **kwargs):
        url = self.base_url + path
        return self.session.put(url, **kwargs)

    def delete(self, path, **kwargs):
        url = self.base_url + path
        return self.session.delete(url, **kwargs)

    def login(self, username, password):
        """用户登录"""
        return self.post("/api/login", json={"username": username, "password": password})

    def get_users(self):
        """获取所有用户"""
        return self.get("/api/users")

    def get_user(self, user_id):
        """获取单个用户"""
        return self.get("/api/users/" + str(user_id))

    def echo(self, data):
        """Echo 测试"""
        return self.post("/api/echo", json=data)

    def register(self, **kwargs):
        """注册用户"""
        return self.post("/api/users", json=kwargs)


def assert_status(response, expected_code=200):
    """断言 HTTP 状态码"""
    assert response.status_code == expected_code,         "Expected status %d, got %d. Body: %s" % (expected_code, response.status_code, response.text[:200])


def assert_json_has_keys(data, keys):
    """断言 JSON 数据包含指定字段"""
    if isinstance(data, list):
        data = data[0] if data else {}
    if isinstance(keys, str):
        keys = [k.strip() for k in keys.split(",")]
    for key in keys:
        assert key in data, "Key '%s' not found in response data" % key


def load_json_file(filepath):
    """加载 JSON 文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
