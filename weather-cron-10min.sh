#!/bin/bash
# 武汉天气定时获取脚本 - 每10分钟执行一次
# 发送到 WhatsApp（通过 Clawdbot API）

API_URL="https://wttr.in/武汉"
INTERVAL=600  # 10分钟 = 600秒

get_weather() {
    curl -s --max-time 10 "$API_URL?format=%C|%t|%w|湿度:%h" 2>/dev/null || echo "获取失败"
}

send_to_clawdbot() {
    local message="$1"
    # 通过 Clawdbot Gateway API 发送消息
    # 注意：这需要 Gateway 运行且有 API token
    local gateway_url="http://127.0.0.1:18789"
    local token=$(cat ~/.clawdbot/clawdbot.json 2>/dev/null | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$token" ]; then
        curl -s -X POST "$gateway_url/api/v1/messages/send" \
            -H "Authorization: Bearer $token" \
            -H "Content-Type: application/json" \
            -d "{\"channel\":\"whatsapp\",\"target\":\"+8613135659321\",\"message\":\"$message\"}" \
            > /dev/null 2>&1
    fi
}

log_weather() {
    local weather
    local datetime
    weather=$(get_weather)
    datetime=$(date "+%Y-%m-%d %H:%M:%S")
    
    if [ "$weather" != "获取失败" ]; then
        echo "[$datetime] 武汉天气: $weather" >> /home/codespace/clawd/logs/weather.log
        # 发送简短版本到 WhatsApp（如果需要）
        # 格式：天气|温度|风力|湿度
        echo "$weather|$datetime"
    else
        echo "[$datetime] 获取天气失败" >> /home/codespace/clawd/logs/weather-error.log
    fi
}

# 创建日志目录
mkdir -p /home/codespace/clawd/logs

# 主循环
echo "[$(date "+%Y-%m-%d %H:%M:%S")] 天气定时任务启动（每10分钟）" >> /home/codespace/clawd/logs/weather.log

while true; do
    log_weather
    sleep $INTERVAL
done
