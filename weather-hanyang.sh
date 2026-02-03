#!/bin/bash
# 武汉汉阳天气预报 - 每小时自动发送

WEATHER=$(curl -s "https://wttr.in/汉阳?format=温度:%C|风力:%w|天气:%c")

echo "🌤️ 武汉汉阳天气: $WEATHER"
