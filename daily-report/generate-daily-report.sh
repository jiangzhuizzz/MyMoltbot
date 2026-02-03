#!/bin/bash
# 每日早报生成脚本
# 运行时间：每天早上9:00

# 配置
REPORT_DIR="/home/codespace/clawd/daily-report"
DATE=$(date "+%Y-%m-%d")
WEEKDAY=$(date "+%A")
TIME=$(date "+%H:%M")

echo "📰 生成每日早报..."
echo "日期: $DATE $WEEKDAY $TIME"

# 创建今日数据目录
mkdir -p "$REPORT_DIR/$DATE"

# 1. 获取市场数据
echo "📈 获取市场数据..."
bash "$REPORT_DIR/scripts/get-market-data.sh" > "$REPORT_DIR/$DATE/market-data.md" 2>&1

# 2. 获取LPR利率
echo "💰 获取LPR利率..."
bash "$REPORT_DIR/scripts/get-lpr.sh" > "$REPORT_DIR/$DATE/lpr-data.md" 2>&1

# 3. 获取自媒体热点
echo "📱 获取自媒体热点..."
bash "$REPORT_DIR/scripts/get-social-trends.sh" > "$REPORT_DIR/$DATE/social-trends.md" 2>&1

# 4. 获取贷款产品动态
echo "🏦 获取贷款产品动态..."
bash "$REPORT_DIR/scripts/get-product-news.sh" > "$REPORT_DIR/$DATE/product-news.md" 2>&1

# 5. 获取天气
echo "☁️ 获取天气..."
bash "$REPORT_DIR/scripts/get-weather.sh" 武汉 > "$REPORT_DIR/$DATE/weather.md" 2>&1

# 6. 生成早报
echo "📝 生成早报..."
python3 "$REPORT_DIR/generate-report.py" > "$REPORT_DIR/$DATE/daily-report.md"

# 7. 发送通知（如果配置了）
if [ -f "$REPORT_DIR/config/send-notification.sh" ]; then
    echo "📤 发送通知..."
    bash "$REPORT_DIR/config/send-notification.sh" "$REPORT_DIR/$DATE/daily-report.md"
fi

echo "✅ 早报生成完成！"
echo "📄 报告位置: $REPORT_DIR/$DATE/daily-report.md"
