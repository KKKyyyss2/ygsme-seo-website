#!/bin/bash
# 每日SEO更新脚本 - 自动运行
# 计划任务配置：每天9:00运行

cd /home/tenbox/ygsme-seo-website

echo "========================================"
echo "每日SEO更新脚本 - $(date)"
echo "========================================"

# 激活Python环境（如果需要）
# source /path/to/venv/bin/activate

# 运行更新脚本
python3 scripts/daily_seo_update.py

# 检查执行结果
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 脚本执行成功"
else
    echo "❌ 脚本执行失败，退出码: $EXIT_CODE"
fi

echo "========================================"
echo "运行完成 - $(date)"
echo "========================================"

exit $EXIT_CODE