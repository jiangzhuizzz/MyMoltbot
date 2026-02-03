#!/bin/bash
# 技能安装和管理脚本

SKILLS_DIR="/usr/local/share/nvm/versions/node/v24.11.1/lib/node_modules/clawdbot/skills"

echo "========================================="
echo "    Clawdbot 技能管理"
echo "========================================="
echo ""

# 列出所有自定义技能
echo "📦 已封装的技能:"
echo ""

custom_skills=("daily-report" "product-collector" "codespace-keepalive" "social-trends")

for skill in "${custom_skills[@]}"; do
    skill_path="$SKILLS_DIR/$skill"
    if [ -d "$skill_path" ]; then
        emoji=$(grep -oP 'emoji.*"\K[^"]+' "$skill_path/SKILL.md" 2>/dev/null || echo "📁")
        echo "  $emoji $skill"
    fi
done

echo ""
echo "========================================="
echo "    推荐安装的技能"
echo "========================================="
echo ""

echo "🔴 高优先级（强烈推荐）:"
echo "  📰 daily-report      - 每日早报生成+发送"
echo "  🏦 product-collector - 产品库自动采集+PR"
echo ""
echo "🟡 中优先级（建议安装）:"
echo "  🟢 codespace-keepalive - Codespace 保活"
echo "  📱 social-trends     - 自媒体热点追踪"
echo ""
echo "🟢 已内置技能（无需安装）:"
echo "  🌤️ weather           - 天气查询"
echo "  📦 github            - GitHub 操作"
echo "  💎 obsidian          - Obsidian 集成"

echo ""
echo "========================================="
echo "    安装说明"
echo "========================================="
echo ""
echo "✅ 这些技能已经封装好，可以直接使用！"
echo ""
echo "使用方法:"
echo "  1. 技能已安装在: $SKILLS_DIR/"
echo "  2. 重启 Clawdbot 使技能生效"
echo "  3. 使用技能前请阅读 SKILL.md 文档"
echo ""
echo "示例命令:"
echo "  # 生成每日早报"
echo "  python3 /home/codespace/clawd/daily-report/generate-report.py"
echo ""
echo "  # 采集产品数据"
echo "  bash /home/codespace/clawd/product-collector/main.sh"
echo ""
echo "  # 查看热点"
echo "  python3 /home/codespace/clawd/product-collector/scripts/get-social-trends.sh"

echo ""
echo "========================================="
echo "    主动推荐"
echo "========================================="
echo ""
echo "💡 根据你的工作，我推荐以下技能组合:"
echo ""
echo "  1️⃣ 每日运营套装:"
echo "     - daily-report + product-collector + social-trends"
echo "     - 自动生成早报 + 更新产品库 + 追踪热点"
echo ""
echo "  2️⃣ 基础设施:"
echo "     - codespace-keepalive"
echo "     - 保持系统在线"
echo ""
echo "需要我帮你配置这些技能吗？"
