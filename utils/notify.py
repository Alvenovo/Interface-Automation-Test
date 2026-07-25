# 第13课：企业微信通知（可选）
import requests

def send_wecom_notification(webhook_url, test_result):
    passed = test_result.get("passed", 0)
    failed = test_result.get("failed", 0)
    total = passed + failed
    emoji = "✅" if failed == 0 else "❌"
    pass_rate = passed / total * 100 if total > 0 else 0

    content = f"""## {emoji} 自动化测试报告
> 总用例数: **{total}**
> 通过: <font color="info">{passed}</font>
> 失败: <font color="warning">{failed}</font>
> 通过率: **{pass_rate:.1f}%**"""

    requests.post(webhook_url, json={
        "msgtype": "markdown",
        "markdown": {"content": content}
    })
