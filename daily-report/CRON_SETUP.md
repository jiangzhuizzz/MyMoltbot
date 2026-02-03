# 每日早报 Cron 配置
# 运行时间: 每天早上 9:00

# 由于系统环境限制，建议使用以下方式之一：

## 方式1: 使用 systemd timer（推荐）
# 创建 /etc/systemd/system/daily-report.service
# 创建 /etc/systemd/system/daily-report.timer

## 方式2: 使用 nohup 后台运行
nohup bash /home/codespace/clawd/daily-report/generate-daily-report.sh > /home/codespace/clawd/daily-report/logs/cron.log 2>&1 &
echo $! > /home/codespace/clawd/daily-report/daily-report.pid

## 方式3: 手动添加 cron
# 运行: crontab -e
# 添加: 0 9 * * * /home/codespace/clawd/daily-report/generate-daily-report.sh >> /home/codespace/clawd/daily-report/logs/cron.log 2>&1

## 当前状态
# 由于 Codespace 环境限制，建议使用 nohup 方式运行
# 或者手动触发生成
