#!/bin/bash
# Clawdbot 完整备份脚本
# 用于迁移到新设备

BACKUP_DIR="/home/codespace/clawd/backup_$(date '+%Y%m%d_%H%M%S')"
DATE=$(date '+%Y-%m-%d %H:%M')

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "🚀 开始 Clawdbot 完整备份..."

# 创建备份目录
mkdir -p "$BACKUP_DIR"

echo ""
echo "=========================================="
echo "    Clawdbot 备份清单"
echo "=========================================="
echo ""
echo "1. 💾 核心记忆文件"
echo "2. 📁 项目文件 (MyMoltbot)"
echo "3. 🔧 自动化系统"
echo "4. ⚙️ 配置文件"
echo "5. 🔑 密钥配置"
echo ""

# 1. 备份核心记忆文件
log "📦 备份核心记忆文件..."
mkdir -p "$BACKUP_DIR/core"

cp -r /home/codespace/clawd/MEMORY.md "$BACKUP_DIR/core/"
cp -r /home/codespace/clawd/USER.md "$BACKUP_DIR/core/"
cp -r /home/codespace/clawd/SOUL.md "$BACKUP_DIR/core/"
cp -r /home/codespace/clawd/IDENTITY.md "$BACKUP_DIR/core/"
cp -r /home/codespace/clawd/AGENTS.md "$BACKUP_DIR/core/"
cp -r /home/codespace/clawd/TOOLS.md "$BACKUP_DIR/core/"
cp -r /home/codespace/clawd/memory/ "$BACKUP_DIR/core/"
log "✅ 核心记忆文件已备份"

# 2. 备份项目文件
log "📦 备份项目文件..."
mkdir -p "$BACKUP_DIR/project"

# 备份 MyMoltbot（排除 node_modules 和 .git）
cd /workspaces/MyMoltbot
tar --exclude='node_modules' --exclude='.git' --exclude='.next' -czf "$BACKUP_DIR/project/mymoltbot.tar.gz" .
log "✅ MyMoltbot 已备份"

# 3. 备份自动化系统
log "📦 备份自动化系统..."
mkdir -p "$BACKUP_DIR/automation"

cp -r /home/codespace/clawd/daily-report/ "$BACKUP_DIR/automation/"
cp -r /home/codespace/clawd/product-collector/ "$BACKUP_DIR/automation/"
cp -r /home/codespace/clawd/wechat-collector/ "$BACKUP_DIR/automation/"
cp -r /home/codespace/clawd/skill-recommendations/ "$BACKUP_DIR/automation/"
cp -r /home/codespace/codespace-keepalive.sh "$BACKUP_DIR/automation/"
cp -r /home/codespace/find-skills.py "$BACKUP_DIR/automation/"
log "✅ 自动化系统已备份"

# 4. 备份配置文件
log "📦 备份配置文件..."
mkdir -p "$BACKUP_DIR/config"

# Clawdbot 配置
cp -r ~/.clawdbot/clawdbot.json "$BACKUP_DIR/config/"
if [ -f ~/.clawdbot/clawdbot.conf ]; then
    cp -r ~/.clawdbot/clawdbot.conf "$BACKUP_DIR/config/"
fi

# Git 配置（可选）
if [ -f ~/.gitconfig ]; then
    cp -r ~/.gitconfig "$BACKUP_DIR/config/"
fi

log "✅ 配置文件已备份"

# 5. 创建恢复脚本
log "📝 创建恢复脚本..."
cat > "$BACKUP_DIR/restore.sh" << 'EOF'
#!/bin/bash
# Clawdbot 恢复脚本
# 在新设备上运行

BACKUP_DIR=$(dirname "$0")
DATE=$(date '+%Y-%m-%d %H:%M')

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "🚀 开始恢复 Clawdbot..."

# 1. 恢复核心记忆文件
log "📦 恢复核心记忆文件..."
cp -r "$BACKUP_DIR/core/"* /home/codespace/clawd/
log "✅ 核心记忆文件已恢复"

# 2. 恢复项目文件
log "📦 恢复项目文件..."
cd /workspaces
tar -xzf "$BACKUP_DIR/project/mymoltbot.tar.gz"
log "✅ 项目文件已恢复"

# 3. 恢复自动化系统
log "📦 恢复自动化系统..."
cp -r "$BACKUP_DIR/automation/"* /home/codespace/clawd/
log "✅ 自动化系统已恢复"

# 4. 恢复配置文件
log "📦 恢复配置文件..."
cp -r "$BACKUP_DIR/config/"* ~/.clawdbot/
log "✅ 配置文件已恢复"

# 5. 设置权限
log "🔧 设置权限..."
chmod +x /home/codespace/clawd/daily-report/*.sh
chmod +x /home/codespace/clawd/product-collector/**/*.sh
chmod +x /home/codespace/clawd/wechat-collector/**/*.sh
chmod +x /home/codespace/clawd/codespace-keepalive.sh

log "✅ 权限已设置"

# 6. 安装依赖
log "📦 安装依赖..."
cd /workspaces/MyMoltbot && npm install
cd /home/codespace/clawd/daily-report && pip3 install -r requirements.txt 2>/dev/null || true
cd /home/codespace/clawd/product-collector && pip3 install -r requirements.txt 2>/dev/null || true

log "✅ 依赖已安装"

log ""
log "=========================================="
log "    恢复完成！"
log "=========================================="
log ""
log "下一步操作:"
log "1. 重启 Clawdbot: clawdbot gateway restart"
log "2. 验证系统: clawdbot status"
log "3. 测试自动化: bash /home/codespace/clawd/daily-report/generate-report.py"
log ""
log "建议设置定时任务:"
log "- crontab -e"
log "- 添加: 0 9 * * * /home/codespace/clawd/daily-report/generate-report.py"
log ""
EOF

chmod +x "$BACKUP_DIR/restore.sh"
log "✅ 恢复脚本已创建"

# 6. 创建备份清单
cat > "$BACKUP_DIR/BACKUP_INFO.md" << EOF
# Clawdbot 备份信息

**备份时间**: $DATE
**备份目录**: $BACKUP_DIR

## 备份内容

### 1. 核心记忆文件
- MEMORY.md - 长期记忆
- USER.md - 用户信息
- SOUL.md - 角色设定
- IDENTITY.md - 身份信息
- AGENTS.md - 代理配置
- TOOLS.md - 工具配置
- memory/*.md - 每日笔记

### 2. 项目文件
- MyMoltbot - Next.js项目
  - 贷款产品知识库
  - Obsidian模板
  - 配置文件

### 3. 自动化系统
- daily-report - 每日早报
- product-collector - 产品采集
- wechat-collector - 公众号采集
- skill-recommendations - 技能推荐

### 4. 配置文件
- ~/.clawdbot/clawdbot.json - Clawdbot配置
- ~/.gitconfig - Git配置

## 恢复方法

1. 复制整个备份目录到新设备
2. 执行恢复脚本:
```bash
cd /path/to/backup
bash restore.sh
```

3. 重启 Clawdbot:
```bash
clawdbot gateway restart
```

## 新设备设置

### 系统要求
- macOS (M系列芯片)
- Node.js v24.11.1
- Python 3.10+
- Git

### 安装步骤
1. 安装 Homebrew
2. 安装 Node.js: brew install node@24
3. 安装 Clawdbot: npm install -g clawdbot
4. 配置 Gateway: clawdbot gateway start
5. 运行恢复脚本
6. 设置定时任务

## 定时任务建议

```bash
# 每日早报 (9:00)
0 9 * * * /home/codespace/clawd/daily-report/generate-report.py

# 产品采集 (8:00, 20:00)
0 8 * * * /home/codespace/clawd/product-collector/main.sh
0 20 * * * /home/codespace/clawd/product-collector/main.sh

# 公众号采集 (6小时一次)
0 */6 * * * /home/codespace/clawd/wechat-collector/enhanced_workflow.sh

# 保活心跳 (每5分钟)
*/5 * * * * curl -s http://localhost:3001 > /dev/null
```

## 注意事项

1. 确保新设备有足够的磁盘空间 (>10GB)
2. 备份文件包含敏感信息，请妥善保管
3. 恢复后建议修改 Gateway token
4. 定期更新备份 (建议每周一次)

---
**备份时间**: $DATE
EOF

log "✅ 备份清单已创建"

# 7. 打包备份
log "📦 打包备份文件..."
cd /home/codespace/clawd
tar -czf "clawdbot_backup_${DATE}.tar.gz" "backup_$(date '+%Y%m%d_%H%M%S')" --exclude='backup_*/*.log'
BACKUP_FILE="clawdbot_backup_${DATE}.tar.gz"

log ""
log "=========================================="
log "    备份完成！"
log "=========================================="
log ""
log "📁 备份文件: $BACKUP_FILE"
log "📊 备份大小: $(ls -lh "$BACKUP_FILE" | awk '{print $5}')"
log "📦 备份内容:"
echo "   - 核心记忆文件"
echo "   - 项目文件 (MyMoltbot)"
echo "   - 自动化系统"
echo "   - 配置文件"
echo "   - 恢复脚本"
echo ""
log "💡 下一步:"
log "   1. 下载备份文件到本地"
log "   2. 复制到新 Mac Mini"
log "   3. 执行恢复脚本"
log ""
log "恢复命令:"
log "   cd /path/to/backup"
log "   bash restore.sh"
