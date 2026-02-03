#!/bin/bash
while true; do
    WEATHER=$(curl -s --max-time 10 "https://wttr.in/汉阳?format=%C|%t|%w" 2>/dev/null || echo "获取失败")
    if [ "$WEATHER" != "获取失败" ]; then
        echo "🌤️ 武汉汉阳: $WEATHER"
    else
        echo "🌤️ 武汉汉阳天气获取失败"
    fi
    sleep 3600
done
