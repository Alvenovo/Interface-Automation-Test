# utils/mysql_helper.py —— MySQL 数据库工具模块
import pymysql

# 数据库连接配置（集中管理）
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "test_dev",
    "charset": "utf8mb4",
}


def get_connection():
    """创建 MySQL 连接"""
    return pymysql.connect(**DB_CONFIG)


def query_all(sql, params=None):
    """执行 SELECT，返回全部结果"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()  # 无论是否出错，保证连接关闭


def query_one(sql, params=None):
    """执行 SELECT，返回第一条结果"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor.fetchone()
    finally:
        conn.close()


def count_rows(table_name):
    """统计表的行数"""
    result = query_one(f"SELECT COUNT(*) FROM {table_name}")
    return result[0] if result else 0