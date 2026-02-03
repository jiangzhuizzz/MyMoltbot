#!/bin/bash
# 发送每日早报到 WhatsApp
# 使用 Clawdbot Gateway API

# 配置
GATEWAY_URL="http://127.0.0.1:18789"
REPORT_DIR="/home/codespace/clawd/daily-report"
TODAY=$(date '+%Y-%m-%d')
MESSAGE_FILE="$REPORT_DIR/$TODAY/daily-report.md"
TARGET="+8613135659321"

# 读取配置
CONFIG_FILE="$REPORT_DIR/config/config.json"
if [ -f "$CONFIG_FILE" ]; then
    TOKEN=$(cat "$CONFIG_FILE" | python3 -c "import sys,json;print(json.load(sys.stdin).get('token',''))" 2>/dev/null)
fi

# 如果没有配置token，尝试从Clawdbot配置获取
if [ -z "$TOKEN" ] || [ "$TOKEN" = "None" ]; then
    TOKEN=$(cat ~/.clawdbot/clawdbot.json 2>/dev/null | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
fi

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "📤 准备发送早报到 WhatsApp..."

# 检查报告是否存在
if [ ! -f "$MESSAGE_FILE" ]; then
    log "❌ 早报文件不存在: $MESSAGE_FILE"
    exit 1
fi

# 读取报告内容
REPORT_CONTENT=$(cat "$MESSAGE_FILE")

# 转换为简洁的文本消息（移除Markdown格式）
MESSAGE=$(echo "$REPORT_CONTENT" | \
    sed 's/# 📰 //' | \
    sed 's/^## /📌 /' | \
    sed 's/^### /• /' | \
    sed 's/| /| /g' | \
    sed 's/\*\*//g' | \
    sed 's/`//g' | \
    sed 's/>/✅ /g' | \
    tr -s '\n' ' ' | \
    sed 's/  */ /g' | \
    head -c 4000)

# 分割长消息（WhatsApp限制4096字符）
MAX_LENGTH=3500

if [ ${#MESSAGE} -gt $MAX_LENGTH ]; then
    log "📝 消息较长，将分段发送..."
    
    # 发送第一部分
    PART1=$(echo "$MESSAGE" | head -c $MAX_LENGTH)
    
    # 发送第一部分
    send_message "$PART1" "（1/2）"
    
    # 发送第二部分
    sleep 2
    PART2=$(echo "$MESSAGE" | tail -c +$((MAX_LENGTH + 1)))
    send_message "$PART2" "（2/2）"
else
    send_message "$MESSAGE" ""
fi

log "✅ 早报发送完成！"

# 发送消息函数
send_message() {
    local content="$1"
    local suffix="$2"
    
    if [ -n "$TOKEN" ]; then
        curl -s -X POST "$GATEWAY_URL/api/v1/messages/send" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -d "{
                \"channel\": \"whatsapp\",
                \"target\": \"$TARGET\",
                \"message\": \"📰 每日早报 $suffix

$content\"
            }" > /dev/null 2>&1
        
        log "✅ 消息$suffix发送成功"
    else
        log "⚠️ 未配置Token，无法发送消息"
        log "💡 请配置TOKEN或手动复制以下内容："
        echo "$content" | head -c 500
        echo "..."
    fi
}
