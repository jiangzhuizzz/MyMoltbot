# Mac Mini 4 Clawdbot 部署指南

> 新设备设置和配置完整指南

## 📋 系统要求

| 项目 | 要求 |
|------|------|
| 设备 | Mac Mini 4 (M系列芯片) |
| 系统 | macOS 14+ (Sequoia) |
| 内存 | 16GB+ (推荐) |
| 存储 | 256GB+ SSD |
| Node.js | v24.11.1 |
| Python | 3.10+ |
| Git | 2.0+ |

---

## 🚀 快速安装

### 1. 安装 Homebrew

```bash
# 打开终端 (Terminal)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. 安装 Node.js v24

```bash
# 安装 Node.js 24
brew install node@24

# 添加到 PATH
echo 'export PATH="/usr/local/opt/node@24/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 验证版本
node -v  # 应显示 v24.11.1
npm -v
```

### 3. 安装 Python 3

```bash
# macOS 自带 Python 3，无需额外安装
python3 --version  # 应显示 3.10+
```

### 4. 安装 Clawdbot

```bash
# 全局安装 Clawdbot
npm install -g clawdbot

# 验证安装
clawdbot --version
```

### 5. 配置 Gateway

```bash
# 启动 Gateway
clawdbot gateway start

# 查看状态
clawdbot gateway status

# 配置开机自启 (可选)
# System Preferences → Users & Groups → Login Items
```

---

## 🔧 详细配置

### 1. Git 配置

```bash
# 配置用户信息
git config --global user.name "你的名字"
git config --global user.email "your@email.com"

# 生成 SSH Key (用于 GitHub)
ssh-keygen -t ed25519 -C "your@email.com"
cat ~/.ssh/id_ed25519.pub
# 添加到 GitHub: Settings → SSH and GPG keys
```

### 2. 安装 Python 依赖

```bash
# 安装常用库
pip3 install requests beautifulsoup4 pandas openpyxl

# 安装 Playwright (浏览器自动化，可选)
pip3 install playwright
playwright install
```

### 3. 安装 npm 依赖

```bash
# 进入项目目录
cd /workspaces/MyMoltbot

# 安装依赖
npm install

# 安装全局工具
npm install -g serve nodemon
```

---

## 📦 恢复备份

### 1. 传输备份文件

```bash
# 方法1: 使用 AirDrop
# 右键点击备份文件 → Share → AirDrop

# 方法2: 使用 scp
scp clawdbot_backup_*.tar.gz user@macmini.local:~/

# 方法3: 使用 Google Drive/Dropbox
# 上传后下载到新设备
```

### 2. 执行恢复

```bash
# 解压备份
tar -xzf clawdbot_backup_*.tar.gz

# 进入备份目录
cd clawdbot_backup_*/

# 执行恢复脚本
bash restore.sh
```

### 3. 手动恢复 (如脚本失败)

```bash
# 1. 恢复核心文件
cp -r backup/core/* /home/codespace/clawd/

# 2. 恢复项目
cd /workspaces
tar -xzf backup/project/mymoltbot.tar.gz

# 3. 恢复自动化系统
cp -r backup/automation/* /home/codespace/clawd/

# 4. 恢复配置
cp -r backup/config/* ~/.clawdbot/

# 5. 设置权限
chmod +x /home/codespace/clawd/**/*.sh
```

---

## ⚙️ 服务配置

### 1. 创建启动脚本

创建文件 `~/Library/LaunchAgents/clawdbot.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.clawdbot.gateway</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/clawdbot</string>
        <string>gateway</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

启动服务:

```bash
launchctl load ~/Library/LaunchAgents/clawdbot.plist
```

### 2. 设置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加以下任务:
# ====================

# 每日早报 (9:00)
0 9 * * * /usr/bin/python3 /home/codespace/clawd/daily-report/generate-report.py >> /home/codespace/clawd/daily-report/logs/cron.log 2>&1

# 产品采集 (8:00, 20:00)
0 8 * * * /bin/bash /home/codespace/clawd/product-collector/main.sh >> /home/codespace/clawd/product-collector/logs/cron.log 2>&1
0 20 * * * /bin/bash /home/codespace/clawd/product-collector/main.sh >> /home/codespace/clawd/product-collector/logs/cron.log 2>&1

# 公众号采集 (6小时一次)
0 */6 * * * /bin/bash /home/codespace/clawd/wechat-collector/enhanced_workflow.sh >> /home/codespace/clawd/wechat-collector/logs/cron.log 2>&1

# Codespace 保活 (每5分钟) - 如果使用Codespace
*/5 * * * * /usr/bin/curl -s http://localhost:3001 > /dev/null 2>&1

# ====================
```

### 3. 配置 WhatsApp

```bash
# 登录 WhatsApp Web
clawdbot whatsapp login

# 扫描二维码完成绑定
```

---

## 🌐 网络配置

### 1. 防火墙设置

```bash
# 开放端口 18789 (Clawdbot Gateway)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/node
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/local/bin/node
```

### 2. 端口转发 (如需要外网访问)

```bash
# 使用 ssh 端口转发
ssh -N -L 18789:localhost:18789 user@macmini.local
```

---

## 🧪 验证部署

### 1. 检查服务状态

```bash
# Clawdbot 状态
clawdbot status

# Gateway 状态
clawdbot gateway status

# WhatsApp 状态
clawdbot whatsapp status
```

### 2. 测试自动化

```bash
# 生成早报
python3 /home/codespace/clawd/daily-report/generate-report.py

# 采集产品
bash /home/codespace/clawd/product-collector/main.sh

# 查看日志
tail -f /home/codespace/clawd/daily-report/logs/daemon.log
```

### 3. 测试消息发送

```bash
# 发送测试消息
clawdbot message send --channel whatsapp --target "+8613135659321" --message "测试消息"
```

---

## 🔒 安全建议

### 1. 修改 Gateway Token

```bash
# 编辑配置
nano ~/.clawdbot/clawdbot.json

# 修改 token 字段
{
  "gateway": {
    "token": "新生成的token"
  }
}

# 重启服务
clawdbot gateway restart
```

### 2. 启用防火墙

```bash
# System Settings → Network → Firewall → Enable
```

### 3. 定期更新

```bash
# 每周更新 Clawdbot
npm update -g clawdbot

# 每月备份
bash /home/codespace/clawd/backup-clawdbot.sh
```

---

## 📁 文件结构

部署后的目录结构:

```
~/ (用户目录)
├── .clawdbot/
│   ├── clawdbot.json    # 主配置
│   └── logs/            # 日志

/workspaces/
└── MyMoltbot/           # Next.js项目
    ├── obsidian-templates/  # 产品库模板
    └── ...

/home/codespace/clawd/       # Clawdbot 主目录
├── daily-report/        # 每日早报
├── product-collector/   # 产品采集
├── wechat-collector/    # 公众号采集
├── memory/              # 记忆文件
│   ├── MEMORY.md        # 长期记忆
│   └── 2026-01-*.md     # 每日笔记
└── skill-recommendations/  # 技能推荐
```

---

## ❓ 常见问题

### Q1: Node 版本不匹配

```bash
# 检查版本
node -v

# 如果版本不对，使用 nvm 切换
nvm install 24
nvm use 24
```

### Q2: 端口被占用

```bash
# 查看占用端口的进程
lsof -i :18789

# 杀掉进程
kill -9 <PID>
```

### Q3: WhatsApp 登录失败

```bash
# 重新登录
clawdbot whatsapp login --force

# 检查网络连接
curl -I https://web.whatsapp.com
```

### Q4: 定时任务不执行

```bash
# 检查 cron 服务状态
sudo cron start

# 查看任务日志
grep CRON /var/log/system.log
```

---

## 📞 技术支持

如果遇到问题:

1. 查看日志: `clawdbot logs`
2. 重启服务: `clawdbot gateway restart`
3. 查看文档: `clawdbot help`

---

**最后更新**: 2026-01-31
**版本**: 1.0
