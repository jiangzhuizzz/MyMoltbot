#!/bin/bash
# 每日早报后台运行脚本
# 每小时检查一次，如果超过9点就生成今日早报并发送到WhatsApp

REPORT_DIR="/home/codespace/clawd/daily-report"
LOG_FILE="$REPORT_DIR/logs/daemon.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "📰 每日早报守护进程启动"

while true; do
    CURRENT_HOUR=$(date '+%H')
    TODAY=$(date '+%Y-%m-%d')
    
    # 检查是否需要生成早报（9点-10点之间运行）
    if [ "$CURRENT_HOUR" = "09" ] || [ "$CURRENT_HOUR" = "10" ]; then
        REPORT_FILE="$REPORT_DIR/$TODAY/daily-report.md"
        
        # 如果报告不存在或已超过12小时，则重新生成
        if [ ! -f "$REPORT_FILE" ] || [ $(stat -c %Y "$REPORT_FILE" 2>/dev/null || echo 0) -lt $(($(date +%s) - 43200)) ]; then
            log "🕘 生成每日早报..."
            bash "$REPORT_DIR/generate-daily-report.sh" >> "$LOG_FILE" 2>&1
            log "✅ 早报生成完成"
            
            # 发送到 WhatsApp
            log "📤 发送到 WhatsApp..."
            bash "$REPORT_DIR/send-to-whatsapp.sh" >> "$LOG_FILE" 2>&1
        else
            log "⏭️ 早报已存在，跳过生成"
        fi
    fi
    
    sleep 3600  # 每小时检查一次
done
