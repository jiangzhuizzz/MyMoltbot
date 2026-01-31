#!/usr/bin/env python3
"""
客户搜索与监控系统
主动寻找有贷款需求的潜在客户
"""

import json
import re
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging

# 配置
DATA_DIR = Path("/home/codespace/clawd/customer-monitor/data")
LOG_DIR = Path("/home/codespace/clawd/customer-monitor/logs")
TEMPLATE_DIR = Path("/home/codespace/clawd/customer-monitor/templates")

# 创建目录
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'customer_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class IntentLevel(Enum):
    """意向等级"""
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"
    NONE = "无"


class LeadStatus(Enum):
    """线索状态"""
    NEW = "新线索"
    CONTACTED = "已联系"
    FOLLOWING = "跟进中"
    CONVERTED = "已转化"
    INVALID = "无效"


class Source(Enum):
    """数据来源"""
    BAIDU = "百度搜索"
    ZHIHU = "知乎"
    DOUYIN = "抖音搜索"
    XIAOHONGSHU = "小红书"
    TIEBA = "贴吧"
    LIANJIA = "链家"
    C58 = "58同城"
    MEITUAN = "美团"
    AUTO = "自动生成"


@dataclass
class Lead:
    """客户线索"""
    id: str
    name: str                      # 客户称呼/昵称
    source: str                    # 来源
    keywords: List[str]            # 触发关键词
    intent_level: str              # 意向等级
    intent_score: float            # 意向评分 0-100
    status: str                    # 状态
    content: str                   # 原文内容
    url: str                       # 原文链接
    contact_info: str              # 联系方式
    remark: str                    # 备注
    tags: List[str] = field(default_factory=list)  # 标签
    created_at: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M'))
    updated_at: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M'))
    followed_at: str = ""          # 最后跟进时间
    converted_at: str = ""         # 转化时间


@dataclass
class SearchConfig:
    """搜索配置"""
    keywords: List[str]            # 关键词列表
    exclude_words: List[str]       # 排除词
    sources: List[str]             # 数据来源
    intent_threshold: int = 60     # 意向阈值
    max_results: int = 50          # 最大结果数


class CustomerSearchMonitor:
    """客户搜索监控"""
    
    def __init__(self):
        self.leads: List[Lead] = []
        self.config = self._load_config()
        
        # 关键词配置
        self.keyword_config = {
            '高意向': [
                '急需贷款', '征信逾期', '贷款被拒', '急需资金',
                '征信不好', '黑户贷款', '无条件贷款', '当天放款',
                '贷款下不来', '征信花了', '贷款审批', '贷款需要什么'
            ],
            '中意向': [
                '贷款利息', '哪个银行', '贷款条件', '怎么贷款',
                '贷款利率', '能贷多少', '首次贷款', '信用贷款',
                '贷款流程', '贷款要求', '商业贷款', '公积金贷款'
            ],
            '低意向': [
                '贷款', '借钱', '资金', '周转', '买房',
                '装修', '买车', '创业', '投资', '分期'
            ]
        }
        
        # 排除词
        self.exclude_words = [
            '诈骗', '骗子', '骗子贷款', '黑中介', '套路贷',
            '不要相信', '警惕', '骗局', '虚假', '违法'
        ]
        
        # 触达模板
        self.templates = self._load_templates()
    
    def _load_config(self) -> SearchConfig:
        """加载配置"""
        config_file = DATA_DIR / "config.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return SearchConfig(**data)
        return SearchConfig(
            keywords=['贷款'],
            exclude_words=[],
            sources=['百度搜索', '知乎', '抖音搜索'],
            intent_threshold=60,
            max_results=50
        )
    
    def _load_templates(self) -> Dict:
        """加载触达模板"""
        template_file = TEMPLATE_DIR / "templates.json"
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认模板
        return {
            '私信': {
                '高意向': '您好，看到您在咨询贷款问题。我这边专业从事贷款服务，可以帮您匹配最适合的产品，利息低、审批快。需要的话可以私信我，帮您免费评估。',
                '中意向': '您好，看到您在了解贷款相关。我这边整理了各银行的贷款产品对比资料，可能对您有帮助，需要的话可以私信我。',
                '低意向': '您好，看到您的提问。我这边有贷款方面的资料可以分享给您，如有需要可以私信交流。'
            },
            '评论': {
                '高意向': '这个问题我之前研究过，可以帮您分析一下哪个方案更适合。',
                '中意向': '贷款问题可以问我，我帮您对比一下各银行的方案。',
                '低意向': '这个问题我有经验，可以分享给您一些建议。'
            },
            '短信': {
                '高意向': '【贷款顾问】看到您近期在了解贷款，我司可提供免费咨询和方案匹配服务，咨询热线：XXX',
                '中意向': '【贷款顾问】您好，我司整理了最新的银行贷款产品对比资料，如有需要可回复Y获取。',
                '低意向': '【贷款顾问】您好，关注贷款资讯可回复TD退订。'
            }
        }
    
    def _generate_lead_id(self) -> str:
        """生成线索ID"""
        import hashlib
        timestamp = str(datetime.now().timestamp()).encode()
        return hashlib.md5(timestamp).hexdigest()[:8]
    
    def calculate_intent(self, content: str, keywords: List[str]) -> tuple:
        """计算意向评分"""
        content_lower = content.lower()
        score = 0
        triggered = []
        matched_keywords = []
        
        # 匹配高意向关键词
        for kw in self.keyword_config['高意向']:
            if kw in content_lower:
                score += 30
                triggered.append(f"高:{kw}")
                matched_keywords.append(kw)
        
        # 匹配中意向关键词
        for kw in self.keyword_config['中意向']:
            if kw in content_lower:
                score += 15
                triggered.append(f"中:{kw}")
                matched_keywords.append(kw)
        
        # 匹配低意向关键词
        for kw in self.keyword_config['低意向']:
            if kw in content_lower:
                score += 5
                triggered.append(f"低:{kw}")
                matched_keywords.append(kw)
        
        # 排除词扣分
        for word in self.exclude_words:
            if word in content_lower:
                score = max(0, score - 50)
                triggered.append(f"排:{word}")
        
        # 计算关键词匹配度
        keyword_bonus = min(len(set(matched_keywords)) * 5, 30)
        score = min(score + keyword_bonus, 100)
        
        # 意向等级
        if score >= 70:
            level = IntentLevel.HIGH.value
        elif score >= 40:
            level = IntentLevel.MEDIUM.value
        elif score >= 10:
            level = IntentLevel.LOW.value
        else:
            level = IntentLevel.NONE.value
        
        return score, level, triggered, matched_keywords
    
    def search_baidu(self, keyword: str) -> List[Lead]:
        """百度搜索结果"""
        logger.info(f"🔍 百度搜索: {keyword}")
        leads = []
        
        # 模拟搜索结果（实际需要API或爬虫）
        search_results = [
            {
                'title': f'急！征信有逾期能贷款吗？{keyword}',
                'content': '我征信有两次逾期，现在急需一笔资金周转，想问一下还能不能贷款...',
                'url': 'https://zhidao.baidu.com/question/123',
                'author': '李先生'
            },
            {
                'title': f'哪个银行利息低？{keyword}',
                'content': '准备买房首付不够，想了解一下哪个银行贷款利息比较低，手续简单...',
                'url': 'https://zhidao.baidu.com/question/456',
                'author': '张女士'
            },
            {
                'title': f'征信花了能贷多少？{keyword}',
                'content': '之前信用卡逾期过几次，现在征信花了，但是急用钱，不知道能不能贷到款...',
                'url': 'https://zhidao.baidu.com/question/789',
                'author': '王同学'
            }
        ]
        
        for result in search_results:
            score, level, triggered, matched = self.calculate_intent(
                result['content'], [keyword]
            )
            
            lead = Lead(
                id=self._generate_lead_id(),
                name=result['author'],
                source=Source.BAIDU.value,
                keywords=[keyword],
                intent_level=level,
                intent_score=score,
                status=LeadStatus.NEW.value,
                content=result['content'],
                url=result['url'],
                contact_info='',
                remark=f"触发词: {', '.join(triggered)}",
                tags=['搜索', keyword]
            )
            leads.append(lead)
        
        logger.info(f"  ✅ 找到 {len(leads)} 条线索")
        return leads
    
    def search_zhihu(self, keyword: str) -> List[Lead]:
        """知乎搜索结果"""
        logger.info(f"🔍 知乎搜索: {keyword}")
        leads = []
        
        # 模拟知乎结果
        search_results = [
            {
                'title': f'征信不好怎么贷款？{keyword}',
                'content': '坐标武汉，征信有几次逾期记录，想问问这种情况还能申请信用贷吗？',
                'url': 'https://www.zhihu.com/question/123',
                'author': '匿名用户'
            },
            {
                'title': f'首次贷款需要注意什么？{keyword}',
                'content': '第一次贷款什么都不懂，怕被坑，想问一下有什么注意事项...',
                'url': 'https://www.zhihu.com/question/456',
                'author': '贷款小白'
            }
        ]
        
        for result in search_results:
            score, level, triggered, matched = self.calculate_intent(
                result['content'], [keyword]
            )
            
            lead = Lead(
                id=self._generate_lead_id(),
                name=result['author'],
                source=Source.ZHIHU.value,
                keywords=[keyword],
                intent_level=level,
                intent_score=score,
                status=LeadStatus.NEW.value,
                content=result['content'],
                url=result['url'],
                contact_info='',
                remark=f"触发词: {', '.join(triggered)}",
                tags=['知乎', keyword]
            )
            leads.append(lead)
        
        logger.info(f"  ✅ 找到 {len(leads)} 条线索")
        return leads
    
    def search_douyin(self, keyword: str) -> List[Lead]:
        """抖音搜索结果"""
        logger.info(f"🔍 抖音搜索: {keyword}")
        leads = []
        
        # 模拟抖音搜索结果
        search_results = [
            {
                'title': f'征信逾期还能贷款吗？在线等急',
                'content': '征信有逾期，但是急用钱装修房子，有没有不看征信的口子？',
                'url': 'https://www.douyin.com/discover/123',
                'author': '武汉租房小王'
            },
            {
                'title': f'公积金贷款怎么贷？求科普',
                'content': '公积金交了3年了，第一次用公积金贷款，不知道需要什么条件...',
                'url': 'https://www.douyin.com/discover/456',
                'author': '刚需买房族'
            }
        ]
        
        for result in search_results:
            score, level, triggered, matched = self.calculate_intent(
                result['content'], [keyword]
            )
            
            lead = Lead(
                id=self._generate_lead_id(),
                name=result['author'],
                source=Source.DOUYIN.value,
                keywords=[keyword],
                intent_level=level,
                intent_score=score,
                status=LeadStatus.NEW.value,
                content=result['content'],
                url=result['url'],
                contact_info='',
                remark=f"触发词: {', '.join(triggered)}",
                tags=['抖音', keyword]
            )
            leads.append(lead)
        
        logger.info(f"  ✅ 找到 {len(leads)} 条线索")
        return leads
    
    def search_xiaohongshu(self, keyword: str) -> List[Lead]:
        """小红书搜索结果"""
        logger.info(f"🔍 小红书搜索: {keyword}")
        leads = []
        
        # 模拟小红书结果
        search_results = [
            {
                'title': f'征信不好怎么贷款？急！',
                'content': '之前信用卡逾期过几次，现在征信花了，但是急用钱，有没有办法贷款？',
                'url': 'https://www.xiaohongshu.com/explore/123',
                'author': '小仙女'
            },
            {
                'title': f'装修贷款哪个银行好？',
                'content': '新房下来要装修了，想问一下装修贷款哪个银行利息低一点？',
                'url': 'https://www.xiaohongshu.com/explore/456',
                'author': '新房主'
            }
        ]
        
        for result in search_results:
            score, level, triggered, matched = self.calculate_intent(
                result['content'], [keyword]
            )
            
            lead = Lead(
                id=self._generate_lead_id(),
                name=result['author'],
                source=Source.XIAOHONGSHU.value,
                keywords=[keyword],
                intent_level=level,
                intent_score=score,
                status=LeadStatus.NEW.value,
                content=result['content'],
                url=result['url'],
                contact_info='',
                remark=f"触发词: {', '.join(triggered)}",
                tags=['小红书', keyword]
            )
            leads.append(lead)
        
        logger.info(f"  ✅ 找到 {len(leads)} 条线索")
        return leads
    
    def search_all_sources(self, keyword: str) -> List[Lead]:
        """全平台搜索"""
        logger.info(f"🌐 全平台搜索: {keyword}")
        
        all_leads = []
        
        # 百度搜索
        if '百度搜索' in self.config.sources:
            all_leads.extend(self.search_baidu(keyword))
        
        # 知乎搜索
        if '知乎' in self.config.sources:
            all_leads.extend(self.search_zhihu(keyword))
        
        # 抖音搜索
        if '抖音搜索' in self.config.sources:
            all_leads.extend(self.search_douyin(keyword))
        
        # 小红书搜索
        if '小红书' in self.config.sources:
            all_leads.extend(self.search_xiaohongshu(keyword))
        
        # 去重
        seen = set()
        unique_leads = []
        for lead in all_leads:
            key = (lead.name, lead.source, lead.content[:50])
            if key not in seen:
                seen.add(key)
                unique_leads.append(lead)
        
        # 按意向评分排序
        unique_leads.sort(key=lambda x: x.intent_score, reverse=True)
        
        self.leads = unique_leads
        return unique_leads
    
    def generate_leads_report(self, keyword: str) -> str:
        """生成线索报告"""
        # 按意向分组
        high_intent = [l for l in self.leads if l.intent_level == IntentLevel.HIGH.value]
        medium_intent = [l for l in self.leads if l.intent_level == IntentLevel.MEDIUM.value]
        low_intent = [l for l in self.leads if l.intent_level == IntentLevel.LOW.value]
        
        report = f"""# 📊 客户线索报告

**搜索关键词**: {keyword}
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**数据来源**: {', '.join(self.config.sources)}

---

## 📈 统计摘要

| 指标 | 数值 |
|------|------|
| 总线索数 | {len(self.leads)} |
| 高意向 | {len(high_intent)} |
| 中意向 | {len(medium_intent)} |
| 低意向 | {len(low_intent)} |
| 平均意向评分 | {sum(l.intent_score for l in self.leads)/len(self.leads):.1f} |

---

## 🔥 高意向线索（{len(high_intent)}个）

| 来源 | 客户 | 评分 | 内容 | 触发词 |
|------|------|------|------|--------|
"""
        
        for lead in high_intent[:10]:
            content_short = lead.content[:30] + '...' if len(lead.content) > 30 else lead.content
            report += f"| {lead.source} | {lead.name} | {lead.intent_score} | {content_short} | {lead.remark[:50]} |\n"
        
        report += f"""
---

## 📊 中意向线索（{len(medium_intent)}个）

| 来源 | 客户 | 评分 | 内容 |
|------|------|------|------|
"""
        
        for lead in medium_intent[:10]:
            content_short = lead.content[:30] + '...' if len(lead.content) > 30 else lead.content
            report += f"| {lead.source} | {lead.name} | {lead.intent_score} | {content_short} |\n"
        
        report += f"""
---

## 📉 低意向线索（{len(low_intent)}个）

| 来源 | 客户 | 评分 | 内容 |
|------|------|------|------|
"""
        
        for lead in low_intent[:10]:
            content_short = lead.content[:30] + '...' if len(lead.content) > 30 else lead.content
            report += f"| {lead.source} | {lead.name} | {lead.intent_score} | {content_short} |\n"
        
        report += f"""
---

## 🎯 触达建议

### 高优先级（{len(high_intent)}个）

"""
        
        for lead in high_intent[:5]:
            template = self.templates['私信'].get(lead.intent_level, self.templates['私信']['中意向'])
            report += f"""#### {lead.source} - {lead.name}
- **内容**: {lead.content[:50]}...
- **意向**: {lead.intent_level} ({lead.intent_score}分)
- **建议话术**:
> {template}

- **链接**: [查看原文]({lead.url})

"""
        
        report += f"""
---

## 📋 行动计划

1. **立即跟进**: {len(high_intent)} 个高意向客户（建议今天联系）
2. **本周跟进**: {len(medium_intent)} 个中意向客户
3. **培育转化**: {len(low_intent)} 个低意向客户（定期推送资讯）

---

## 💡 关键词优化建议

| 关键词 | 找到线索数 | 平均意向 |
|--------|------------|----------|
"""
        
        # 按关键词统计
        keyword_stats = {}
        for lead in self.leads:
            for kw in lead.keywords:
                if kw not in keyword_stats:
                    keyword_stats[kw] = {'count': 0, 'total_score': 0}
                keyword_stats[kw]['count'] += 1
                keyword_stats[kw]['total_score'] += lead.intent_score
        
        for kw, stats in keyword_stats.items():
            avg = stats['total_score'] / stats['count']
            report += f"| {kw} | {stats['count']} | {avg:.1f} |\n"
        
        report += f"""
---

*报告由 Customer Search Monitor 自动生成*
**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    def run_full_search(self, keyword: str):
        """执行完整搜索"""
        print("=" * 60)
        print(f"    🔍 客户搜索系统 v1.0")
        print(f"    搜索关键词: {keyword}")
        print("=" * 60)
        
        # 1. 全平台搜索
        print("\n🌐 全平台搜索...")
        leads = self.search_all_sources(keyword)
        print(f"  ✅ 找到 {len(leads)} 条线索")
        
        # 2. 统计
        high = len([l for l in leads if l.intent_level == IntentLevel.HIGH.value])
        medium = len([l for l in leads if l.intent_level == IntentLevel.MEDIUM.value])
        
        print("\n📊 线索统计:")
        print(f"  - 高意向: {high} 个")
        print(f"  - 中意向: {medium} 个")
        print(f"  - 低意向: {len(leads) - high - medium} 个")
        
        # 3. 生成报告
        print("\n📄 生成报告...")
        report = self.generate_leads_report(keyword)
        report_file = DATA_DIR / f"leads_report_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.write_text(report, encoding='utf-8')
        
        # 4. 保存数据
        leads_file = DATA_DIR / f"leads_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        leads_data = [asdict(l) for l in leads]
        leads_file.write_text(json.dumps(leads_data, ensure_ascii=False, indent=2), encoding='utf-8')
        
        # 5. 输出结果
        print("\n" + "=" * 60)
        print("    📊 搜索完成！")
        print("=" * 60)
        
        print(f"\n🔍 搜索结果:")
        print(f"   总线索: {len(leads)} 个")
        print(f"   高意向: {high} 个")
        print(f"   中意向: {medium} 个")
        
        print(f"\n📄 报告文件: {report_file}")
        print(f"📦 数据文件: {leads_file}")
        
        print("\n" + "=" * 60)
        print("    💡 建议行动")
        print("=" * 60)
        print(f"\n✅ 优先跟进 {high} 个高意向客户")
        print("   - 今天完成首次联系")
        print("   - 使用个性化话术")
        print("   - 记录客户反馈")
        
        return leads, report
    
    def export_leads_for_outreach(self, keyword: str):
        """导出线索用于外呼"""
        high_intent = [l for l in self.leads if l.intent_level == IntentLevel.HIGH.value]
        
        export_data = {
            'keyword': keyword,
            'export_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'total': len(high_intent),
            'leads': []
        }
        
        for lead in high_intent:
            template = self.templates['私信'].get(lead.intent_level, '')
            export_data['leads'].append({
                'id': lead.id,
                'name': lead.name,
                'source': lead.source,
                'intent_level': lead.intent_level,
                'intent_score': lead.intent_score,
                'content': lead.content,
                'url': lead.url,
                'message_template': template,
                'status': lead.status
            })
        
        export_file = DATA_DIR / f"outreach_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        export_file.write_text(json.dumps(export_data, ensure_ascii=False, indent=2), encoding='utf-8')
        
        return export_file


def main():
    import sys
    
    if len(sys.argv) < 2:
        keyword = input("请输入搜索关键词: ").strip()
    else:
        keyword = sys.argv[1]
    
    if not keyword:
        print("❌ 请输入关键词")
        return
    
    monitor = CustomerSearchMonitor()
    leads, report = monitor.run_full_search(keyword)
    
    # 导出外呼数据
    export_file = monitor.export_leads_for_outreach(keyword)
    print(f"\n📤 外呼数据已导出: {export_file}")


if __name__ == '__main__':
    main()
