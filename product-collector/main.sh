#!/bin/bash
# 产品库完善主脚本
# 整合采集、导入、Git工作流

set -e

REPO_DIR="/workspaces/MyMoltbot"
COLLECTOR_DIR="/home/codespace/clawd/product-collector"
LOG_DIR="$COLLECTOR_DIR/logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_DIR/main.log"
}

log "🚀 启动产品库完善流程"

# 1. 采集产品数据
log "📡 步骤1: 采集产品数据..."
if [ -f "$COLLECTOR_DIR/collector.py" ]; then
    python3 "$COLLECTOR_DIR/collector.py" >> "$LOG_DIR/collector.log" 2>&1
    log "✅ 数据采集完成"
else
    log "⚠️ 采集脚本不存在"
fi

# 2. 检查是否有待导入的手册
log "📁 步骤2: 检查产品手册..."
if [ "$(ls -A $COLLECTOR_DIR/manuals 2>/dev/null)" ]; then
    log "发现手册文件，需要手动处理"
    bash "$COLLECTOR_DIR/import-manual.sh" --dir >> "$LOG_DIR/import.log" 2>&1
else
    log "⏭️ 没有发现手册文件"
fi

# 3. 创建 PR
log "🔗 步骤3: 创建 Pull Request..."
cd "$REPO_DIR"

# 检查是否有更改
if git status --porcelain | grep -q .; then
    log "发现有更新，运行 Git 工作流..."
    bash "$COLLECTOR_DIR/git-workflow.sh" >> "$LOG_DIR/git.log" 2>&1
    
    # 获取 PR 编号
    PR_BRANCH=$(cat "$COLLECTOR_DIR/last-pr-branch.txt" 2>/dev/null)
    if [ -n "$PR_BRANCH" ]; then
        log "✅ PR 已创建: $PR_BRANCH"
        
        # 发送通知
        python3 "$COLLECTOR_DIR/notify-user.py" "pr_created" "$PR_BRANCH" >> "$LOG_DIR/notify.log" 2>&1
    fi
else
    log "⏭️ 没有新的更新"
fi

# 4. 检查是否需要讨论
log "💬 步骤4: 检查是否需要讨论..."
python3 "$COLLECTOR_DIR/interaction.py" >> "$LOG_DIR/interaction.log" 2>&1

log ""
log "✅ 产品库完善流程完成！"
log ""
log "📊 本次执行摘要:"
log "  - 数据采集: 完成"
log "  - 手册导入: 检查完成"
log "  - PR创建: 如有更新则创建"
log "  - 互动讨论: 已检查"

# 显示待处理事项
echo ""
echo "📋 待处理事项:"
echo "  1. 查看 GitHub PR（如有）"
echo "  2. 审核产品数据"
echo "  3. 合并 PR 到 main 分支"
echo ""
echo "💡 手动运行:"
echo "  - 采集数据: python3 $COLLECTOR_DIR/collector.py"
echo "  - 导入手册: bash $COLLECTOR_DIR/import-manual.sh"
echo "  - 创建PR: bash $COLLECTOR_DIR/git-workflow.sh"
echo "  - 讨论话题: python3 $COLLECTOR_DIR/interaction.py"
