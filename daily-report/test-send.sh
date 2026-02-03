#!/bin/bash
# 手动测试发送早报到 WhatsApp
# 仅用于测试，实际运行由守护进程自动执行

REPORT_DIR="/home/codespace/clawd/daily-report"
TODAY=$(date '+%Y-%m-%d')
MESSAGE_FILE="$REPORT_DIR/$TODAY/daily-report.md"

echo "🧪 测试发送早报到 WhatsApp"
echo "日期: $TODAY"
echo "报告文件: $MESSAGE_FILE"
echo ""

# 读取配置文件
CONFIG_FILE="$REPORT_DIR/config/config.json"
if [ -f "$CONFIG_FILE" ]; then
    TOKEN=$(cat "$CONFIG_FILE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('token',''))" 2>/dev/null)
    GATEWAY_URL=$(cat "$CONFIG_FILE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('gateway_url','http://127.0.0.1:18789'))" 2>/dev/null)
    ENABLED=$(cat "$CONFIG_FILE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('enabled',False))" 2>/dev/null)
fi

echo "配置信息:"
echo "- Token: ${TOKEN:0:10}... (已隐藏)"
echo "- Gateway: $GATEWAY_URL"
echo "- 启用: $ENABLED"
echo ""

if [ "$ENABLED" != "True" ] && [ "$ENABLED" != "true" ] && [ "$ENABLED" != "TRUE" ]; then
    echo "⚠️ 发送功能未启用"
    echo "请编辑 $CONFIG_FILE 将 enabled 设为 true"
    exit 1
fi

if [ ! -f "$MESSAGE_FILE" ]; then
    echo "❌ 报告文件不存在，先运行生成脚本"
    python3 "$REPORT_DIR/generate-report.py" > /dev/null 2>&1
fi

# 读取报告并发送测试消息
TEST_MESSAGE="📰 每日早报测试

✅ 每日早报系统已配置完成！
- 每天早上9:00自动生成
- 自动发送到WhatsApp
- 包含贷款产品、自媒体热点、行业资讯

完整版早报将于明天9:00发送！

---
由 Clawdbot 自动生成"

echo "📤 发送测试消息..."
curl -s -X POST "$GATEWAY_URL/api/v1/messages/send" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"channel\": \"whatsapp\",
        \"target\": \"+8613135659321\",
        \"message\": \"$TEST_MESSAGE\"
    }" > /dev/null 2>&1

echo "✅ 测试消息已发送！"
echo ""
echo "📝 如果你收到了测试消息，说明配置正确。"
echo "明天早上9:00将自动发送完整版早报！"
