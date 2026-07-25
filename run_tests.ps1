# run_tests.ps1
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  接口自动化测试 - 本地 CI 模拟" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

Write-Host "[1/3] 安装依赖..." -ForegroundColor Yellow
pip install -r requirements.txt -q

Write-Host "[2/3] 运行测试..." -ForegroundColor Yellow
py -3.8 -m pytest tests/ -v `
  --html=reports/report.html `
  --self-contained-html `
  --junitxml=reports/junit.xml

Write-Host "[3/3] 完成! 打开 reports/report.html 查看报告" -ForegroundColor Green