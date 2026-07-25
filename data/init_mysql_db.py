# data/init_mysql_db.py —— 初始化 MySQL 测试数据库
# 运行：py -3.8 data/init_mysql_db.py
import pymysql

# 第1步：连接 MySQL（先不指定数据库，要建库）
conn = pymysql.connect(
    host="localhost", port=3306,
    user="root", password="123456",
    charset="utf8mb4"
)
cursor = conn.cursor()

# 第2步：建库
cursor.execute("CREATE DATABASE IF NOT EXISTS test_dev CHARACTER SET utf8mb4")
cursor.execute("USE test_dev")

# 第3步：建表
cursor.execute("CREATE TABLE IF NOT EXISTS users ("
               "id INT PRIMARY KEY AUTO_INCREMENT, "
               "name VARCHAR(50) NOT NULL, "
               "email VARCHAR(100) NOT NULL, "
               "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

# 第4步：清空旧数据
cursor.execute("DELETE FROM users")
cursor.execute("ALTER TABLE users AUTO_INCREMENT = 1")

# 第5步：插入测试数据（和后端 USERS 列表一致）
users = [
    (1, "张三", "zhangsan@test.com"),
    (2, "李四", "lisi@test.com"),
    (3, "王五", "wangwu@test.com"),
    (4, "赵六", "zhaoliu@test.com"),
]
cursor.executemany(
    "INSERT INTO users (id, name, email) VALUES (%s, %s, %s)",
    users
)

# 第6步：提交事务
conn.commit()
print("MySQL 初始化完成！test_dev.users 表已就绪")

# 验证
cursor.execute("SELECT COUNT(*) FROM users")
print(f"users 表共 {cursor.fetchone()[0]} 条数据")

cursor.close()
conn.close()