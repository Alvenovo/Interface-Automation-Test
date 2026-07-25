# Interface-Automation-Test

🚀 基于 Python + pytest + Requests 的接口自动化测试框架

[![CI](https://github.com/Alvenovo/Interface-Automation-Test/actions/workflows/test.yml/badge.svg)](https://github.com/Alvenovo/Interface-Automation-Test/actions)

## 📋 项目简介

独立设计并实现的接口自动化测试框架，包含：
- 用户管理 API 的 CRUD 测试
- 登录功能的多场景参数化测试
- MySQL 数据库一致性验证
- 端到端业务流程测试
- pytest-html / Allure 双报告体系
- GitHub Actions CI/CD 自动化流水线

## 🛠 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | Python 3.8+ |
| 测试框架 | pytest 8.0+ |
| HTTP 库 | Requests |
| 数据库 | MySQL 8.0 + PyMySQL |
| 报告 | pytest-html + Allure |
| CI/CD | GitHub Actions |
| 后端 | Flask |

## 📂 项目结构

```
Interface-Automation-Test/
├── tests/                  # 测试用例
│   ├── test_users_api.py   # 用户API测试（3条）
│   ├── test_login.py       # 登录参数化测试（4条）
│   ├── test_user_flow.py   # 端到端流程测试（9条）
│   ├── test_db_verify.py   # 数据库验证测试（5条）
│   ├── test_api/           # 扩展API测试（5条）
│   └── conftest.py         # pytest fixture 配置
├── utils/                  # 工具模块
│   ├── helpers.py          # HTTP客户端 + 断言工具
│   └── mysql_helper.py     # MySQL数据库工具
├── data/                   # 测试数据
├── backend_server.py       # Flask 后端模拟服务
├── pytest.ini              # pytest 配置
├── requirements.txt        # 项目依赖
└── .github/workflows/      # CI/CD 配置
    └── test.yml            # GitHub Actions 工作流
```

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/Alvenovo/Interface-Automation-Test.git
cd Interface-Automation-Test
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置 MySQL（数据库验证测试需要）
```sql
CREATE DATABASE IF NOT EXISTS test_dev;
USE test_dev;
```
然后运行 `python data/init_mysql_db.py` 初始化测试数据。

### 4. 启动后端
```bash
python backend_server.py
```

### 5. 运行测试
```bash
# 基础运行
python -m pytest tests/ -v

# 生成 pytest-html 报告
python -m pytest tests/ -v --html=reports/report.html --self-contained-html

# 生成 Allure 报告
python -m pytest tests/ -v --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## ✅ 测试覆盖

| 测试模块 | 用例数 | 覆盖场景 |
|----------|--------|----------|
| test_users_api | 3 | GET 用户列表 - 状态码/数据类型/字段完整性 |
| test_login | 4 | 登录成功/密码错误/用户名为空/密码为空 |
| test_user_flow | 9 | 健康检查/登录流程/用户数据/Echo/端到端流程 |
| test_db_verify | 5 | 表数据存在/用户数量/字段完整性/邮箱格式 |
| test_api | 5 | 用户注册/邮箱校验/扩展API |

## 📊 CI/CD

每次推送到 main 分支自动触发 GitHub Actions：
1. 拉取代码
2. 安装 Python 3.8
3. 安装项目依赖
4. 启动后端服务
5. 运行全部测试
6. 生成 Allure 报告
7. 上传报告为 Artifact

## 📄 License

MIT
