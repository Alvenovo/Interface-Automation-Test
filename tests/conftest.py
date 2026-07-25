import pytest

@pytest.fixture
def base_url():
    """返回后端基础地址"""
    return "http://localhost:5001"

@pytest.fixture
def users_url(base_url):
    """返回用户接口完整URL"""
    return base_url + "/api/users"

@pytest.fixture
def login_url(base_url):
    """返回登录接口完整URL"""
    return base_url + "/api/login"

@pytest.fixture(scope="session")
def db_connection():
    """MySQL 连接（整个测试会话只创建一次）"""
    import pymysql
    conn = pymysql.connect(
        host="localhost", port=3306,
        user="root", password="123456",
        database="test_dev", charset="utf8mb4"
    )
    yield conn
    conn.close()

# ===== 第13课：Allure 失败截图钩子 =====
import allure

def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="失败截图",
                attachment_type=allure.attachment_type.PNG
            )
