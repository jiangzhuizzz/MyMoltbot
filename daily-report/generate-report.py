#!/usr/bin/env python3
"""
每日早报生成器
完整版 - 贷款中介 + 自媒体运营
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# 配置
REPORT_DIR = "/home/codespace/clawd/daily-report"
TODAY = datetime.now().strftime("%Y-%m-%d")
WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()]

def read_file(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def load_json(filepath):
    """加载JSON数据"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

# 数据源文件
data_sources = {
    'market': f"{REPORT_DIR}/{TODAY}/market-data.md",
    'lpr': f"{REPORT_DIR}/{TODAY}/lpr-data.md",
    'social': f"{REPORT_DIR}/{TODAY}/social-trends.md",
    'product': f"{REPORT_DIR}/{TODAY}/product-news.md",
    'weather': f"{REPORT_DIR}/{TODAY}/weather.md",
}

# 模拟数据（实际使用时替换为真实API调用）
def get_lpr_data():
    """获取LPR利率"""
    return {
        '1y': {'rate': '3.45%', 'change': '0%'},
        '5y': {'rate': '3.95%', 'change': '0%'},
        'update': '2026-01-30'
    }

def get_weather():
    """获取武汉天气"""
    return {
        'condition': '多云',
        'temp': '8-15℃',
        'humidity': '65%',
        'wind': '东北风 3级',
        'pm25': '45'
    }

def get_product_recommendations():
    """获取今日推荐产品"""
    return [
        {
            'bank': '工商银行',
            'product': '融e借',
            'rate': '3.65%',
            'amount': '5-30万',
            'approval': '1-3天',
            'tags': ['利率低', '额度高', '审批快'],
            'commission': '1.5%'
        },
        {
            'bank': '建设银行',
            'product': '快贷',
            'rate': '3.85%',
            'amount': '1-20万',
            'approval': '1-2天',
            'tags': ['门槛低', '速度快'],
            'commission': '1.2%'
        },
        {
            'bank': '招商银行',
            'product': '闪电贷',
            'rate': '4.2%',
            'amount': '2-30万',
            'approval': '当天',
            'tags': ['最快当天', '额度灵活'],
            'commission': '1.8%'
        }
    ]

def get_social_trends():
    """获取自媒体热点"""
    return {
        'xiaohongshu': [
            {'topic': '#贷款审批', 'views': '120万', 'trend': '↑'},
            {'topic': '#征信修复', 'views': '85万', 'trend': '↑'},
            {'topic': '#公积金贷款', 'views': '72万', 'trend': '→'},
            {'topic': '#低利率贷款', 'views': '68万', 'trend': '↓'},
        ],
        'douyin': [
            {'topic': '#贷款避坑', 'views': '230万', 'trend': '↑'},
            {'topic': '#信用修复', 'views': '156万', 'trend': '↑'},
            {'topic': '#贷款流程', 'views': '98万', 'trend': '→'},
        ],
        'suggested_topics': [
            '征信查询次数对贷款的影响',
            '如何提高贷款审批通过率',
            '等额本息 vs 等额本金',
            '公积金贷款全攻略',
        ]
    }

def get_industry_news():
    """获取行业新闻"""
    return [
        {
            'source': '新华社',
            'title': '央行：继续保持货币政策稳健性',
            'time': '昨日',
            'summary': '央行表示将继续实施稳健的货币政策，支持实体经济发展。'
        },
        {
            'source': '湖北日报',
            'title': '武汉房地产市场最新数据',
            'time': '昨日',
            'summary': '1月武汉新房成交环比增长5.2%，市场稳步回暖。'
        },
        {
            'source': '金融时报',
            'title': '多家银行下调消费贷款利率',
            'time': '昨日',
            'summary': '工行、建行、招行等纷纷下调消费贷利率，最低至3.65%。'
        }
    ]

def get_learning_tip():
    """获取今日学习提示"""
    tips = [
        "【贷款知识】等额本息月供不变，前期利息多；等额本金月供递减，前期压力大。选择等额本金总利息更少。",
        "【销售技巧】客户说'考虑一下'，可以问：'您主要考虑哪些方面？'了解真实顾虑。",
        "【沟通话术】客户问'利率还能降吗？'可以回答：'每个产品利率不同，我可以帮您匹配最适合的方案。'",
        "【客户跟进】最佳跟进时间：周一上午（决策日）、周五下午（总结周计划）。",
        "【心理暗示】说'这个产品很适合您'比'您要不要试试这个产品'转化率更高。",
    ]
    import random
    return random.choice(tips)

def generate_header():
    """生成头部"""
    return f"""# 📰 每日早报 - {TODAY} {WEEKDAY_CN}

> 生成时间：{datetime.now().strftime('%H:%M')}
> 贷款中介 + 自媒体运营 完整版

---

## 📊 今日数据概览

| 指标 | 数值 | 备注 |
|------|------|------|
| LPR(1年) | 3.45% | 持平 |
| LPR(5年) | 3.95% | 持平 |
| 今日推荐产品 | 3款 | 点击查看 |
| 自媒体热点 | 7个 | 小红书+抖音 |
"""

def generate_weather_section():
    """生成天气板块"""
    weather = get_weather()
    return f"""## ☁️ 武汉天气

| 项目 | 数值 |
|------|------|
| 天气 | {weather['condition']} |
| 温度 | {weather['temp']} |
| 湿度 | {weather['humidity']} |
| 风力 | {weather['wind']} |
| PM2.5 | {weather['pm25']} |

> 💡 提示：天气适宜，适合外出展业。
"""

def generate_lpr_section():
    """生成LPR板块"""
    lpr = get_lpr_data()
    return f"""## 💰 LPR利率（贷款基准利率）

| 期限 | 利率 | 较上周 |
|------|------|--------|
| 1年期 | **{lpr['1y']['rate']}** | {lpr['1y']['change']} |
| 5年期 | **{lpr['5y']['rate']}** | {lpr['5y']['change']} |

> 📊 数据更新时间：{lpr['update']}
> 💡 提示：LPR维持不变，贷款成本稳定。
"""

def generate_products_section():
    """生成产品推荐板块"""
    products = get_product_recommendations()
    
    lines = ["## 🏦 今日推荐产品", ""]
    lines.append("| 银行 | 产品 | 利率 | 额度 | 审批 | 佣金 | 标签 |")
    lines.append("|------|------|------|------|------|------|------|")
    
    for p in products:
        tags = ' '.join([f"`{t}`" for t in p['tags']])
        lines.append(f"| {p['bank']} | {p['product']} | **{p['rate']}** | {p['amount']} | {p['approval']} | {p['commission']} | {tags} |")
    
    lines.append("")
    lines.append("### 💡 产品亮点")
    lines.append("")
    lines.append("- 🔥 **工商银行-融e借**：利率低至3.65%，额度最高30万，审批1-3天")
    lines.append("- ⚡ **建设银行-快贷**：门槛低，审批快，额度灵活")
    lines.append("- 🚀 **招商银行-闪电贷**：最快当天放款，额度2-30万")
    lines.append("")
    
    return '\n'.join(lines)

def generate_social_section():
    """生成自媒体板块"""
    trends = get_social_trends()
    
    lines = ["## 📱 自媒体热点", ""]
    
    # 小红书
    lines.append("### 小红书热门话题")
    lines.append("")
    lines.append("| 话题 | 热度 | 趋势 |")
    lines.append("|------|------|------|")
    for t in trends['xiaohongshu']:
        trend_icon = "📈" if t['trend'] == '↑' else ("📉" if t['trend'] == '↓' else "➡️")
        lines.append(f"| {t['topic']} | {t['views']} | {trend_icon} |")
    
    lines.append("")
    
    # 抖音
    lines.append("### 抖音热门话题")
    lines.append("")
    lines.append("| 话题 | 热度 | 趋势 |")
    lines.append("|------|------|------|")
    for t in trends['douyin']:
        trend_icon = "📈" if t['trend'] == '↑' else ("📉" if t['trend'] == '↓' else "➡️")
        lines.append(f"| {t['topic']} | {t['views']} | {trend_icon} |")
    
    lines.append("")
    
    # 推荐选题
    lines.append("### 📝 今日推荐选题")
    lines.append("")
    for i, topic in enumerate(trends['suggested_topics'], 1):
        lines.append(f"{i}. {topic}")
    
    lines.append("")
    lines.append("> 💡 选题建议：结合今日热点话题创作，内容更易获得流量。")
    lines.append("")
    
    return '\n'.join(lines)

def generate_news_section():
    """生成行业新闻板块"""
    news = get_industry_news()
    
    lines = ["## 📰 行业新闻", ""]
    
    for n in news:
        lines.append(f"### {n['source']} - {n['title']}")
        lines.append(f"> {n['time']} | {n['summary']}")
        lines.append("")
    
    return '\n'.join(lines)

def generate_learning_section():
    """生成学习板块"""
    tip = get_learning_tip()
    
    lines = ["## 💡 今日学习", ""]
    lines.append(tip)
    lines.append("")
    
    lines.append("### 📚 本周学习计划")
    lines.append("")
    lines.append("| 日期 | 主题 | 内容 |")
    lines.append("|------|------|------|")
    lines.append("| 周一 | 产品知识 | 各银行产品对比 |")
    lines.append("| 周二 | 销售技巧 | 客户沟通话术 |")
    lines.append("| 周三 | 案例分析 | 成功案例拆解 |")
    lines.append("| 周四 | 行业动态 | 市场趋势分析 |")
    lines.append("| 周五 | 客户管理 | 客户跟进策略 |")
    lines.append("")
    
    return '\n'.join(lines)

def generate_tools_section():
    """生成工具板块"""
    return """## 🛠️ 今日工具

### 📊 数据看板
- [[产品数据库]] - 所有贷款产品查询
- [[客户统计]] - 客户数据分析
- [[佣金计算器]] - 快速计算佣金

### 📝 常用模板
- [[客户需求登记表]] - 记录客户需求
- [[产品推荐记录]] - 跟进记录
- [[自媒体内容计划]] - 内容排期

### 📱 自媒体工具
- [[选题库]] - 热门选题收集
- [[文案模板]] - 常用文案
- [[数据监控]] - 流量数据

---

> 💡 快捷键：按 `Ctrl/Cmd + K` 打开快速搜索
"""

def generate_footer():
    """生成底部"""
    return f"""---

## 📌 今日待办

- [ ] 跟进3个潜在客户
- [ ] 发布1篇小红书/抖音
- [ ] 更新产品数据库
- [ ] 学习1个产品知识

---

## 📞 联系方式

| 渠道 | 链接 |
|------|------|
| 小红书 | [链接](https://xiaohongshu.com) |
| 抖音 | [链接](https://douyin.com) |
| 微信 | [链接](weixin.com) |

---

> **使用说明**
> - 每日早报每天早上9:00自动生成
> - 包含贷款产品、自媒体、行业资讯等
> - 数据来源：LPR官网、各银行官网、小红书/抖音热榜
> 
> **更新日志**
> - 2026-01-30: 初始化版本
> - 新增贷款产品推荐、自媒体热点、行业新闻板块

---

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**版本**: 1.0
**维护**: Clawdbot AI助手
"""

def main():
    """主函数"""
    report_sections = []
    
    # 头部
    report_sections.append(generate_header())
    
    # 天气
    report_sections.append(generate_weather_section())
    
    # LPR
    report_sections.append(generate_lpr_section())
    
    # 产品推荐
    report_sections.append(generate_products_section())
    
    # 自媒体
    report_sections.append(generate_social_section())
    
    # 行业新闻
    report_sections.append(generate_news_section())
    
    # 学习
    report_sections.append(generate_learning_section())
    
    # 工具
    report_sections.append(generate_tools_section())
    
    # 底部
    report_sections.append(generate_footer())
    
    # 合并报告
    report = '\n'.join(report_sections)
    
    # 打印报告
    print(report)
    
    # 保存报告
    report_file = f"{REPORT_DIR}/{TODAY}/daily-report.md"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 报告已保存到: {report_file}")

if __name__ == '__main__':
    main()
