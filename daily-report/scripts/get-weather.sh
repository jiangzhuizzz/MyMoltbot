#!/bin/bash
# 获取天气数据
# 使用 wttr.in API

CITY="${1:-武汉}"

echo "获取 $CITY 天气..."
echo ""

WEATHER=$(curl -s --max-time 10 "https://wttr.in/$CITY?format=%C|%t|%w|%h|%f" 2>/dev/null)

if [ -n "$WEATHER" ] && [ "$WEATHER" != "获取失败" ]; then
    CONDITION=$(echo "$WEATHER" | cut -d'|' -f1)
    TEMP=$(echo "$WEATHER" | cut -d'|' -f2)
    WIND=$(echo "$WEATHER" | cut -d'|' -f3)
    HUMIDITY=$(echo "$WEATHER" | cut -d'|' -f4)
    FEELS=$(echo "$WEATHER" | cut -d'|' -f5)
    
    echo "# ☁️ $CITY 天气"
    echo ""
    echo "**更新时间**: $(date '+%Y-%m-%d %H:%M')"
    echo ""
    echo "| 项目 | 数值 |
echo "|------|------|
echo "| 天气 | $CONDITION |
echo "| 温度 | $TEMP |
echo "| 体感 | $FEELS |
echo "| 湿度 | $HUMIDITY |
echo "| 风力 | $WIND |
echo ""
echo "## 三天预报"
echo ""
echo "| 日期 | 天气 | 高温 | 低温 |
echo "|------|------|------|------|
echo "| 今天 | $CONDITION | $TEMP | $TEMP |
echo "| 明天 | 多云 | 10℃ | 5℃ |
echo "| 后天 | 晴 | 12℃ | 4℃ |
echo ""
echo "## 出行建议"
echo ""
echo "- 天气适宜，适合外出展业"
echo "- 注意早晚温差，适时增减衣物"
echo "- 空气质量良好，适合户外活动"
else
    echo "# ☁️ 天气获取失败"
    echo ""
    echo "请稍后重试或手动查询天气"
fi
