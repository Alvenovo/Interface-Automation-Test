# tests/test_db_verify.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.mysql_helper import query_all, query_one, count_rows


class TestMySQLVerify:
    """MySQL 数据校验"""

    def test_users_table_has_data(self):
        """users 表不能为空"""
        assert count_rows("users") > 0

    def test_user_count_is_4(self):
        """应该有4条数据"""
        assert count_rows("users") == 4

    def test_zhangsan_exists(self):
        """张三应该在数据库中"""
        user = query_one("SELECT name, email FROM users WHERE id = %s", (1,))
        assert user is not None
        name, email = user
        assert name == "张三"
        assert email == "zhangsan@test.com"

    def test_all_emails_valid(self):
        """所有邮箱包含 @"""
        for uid, email in query_all("SELECT id, email FROM users"):
            assert "@" in email, f"用户{uid}邮箱错误: {email}"

    def test_all_users_have_name(self):
        """所有用户 name 不为空"""
        for uid, name in query_all("SELECT id, name FROM users"):
            assert name, f"用户{uid}的name为空"