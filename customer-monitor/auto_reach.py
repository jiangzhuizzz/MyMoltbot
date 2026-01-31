#!/usr/bin/env python3
"""
自动化触达系统
自动发送私信、评论、短信，跟踪触达效果
"""

import json
import re
import asyncio
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum
import logging

# 配置
DATA_DIR = Path("/home/codespace/clawd/customer-monitor/data")
LOG_DIR = Path("/home/codespace/clawd/customer-monitor/logs")
TEMPLATE_DIR = Path("/home/codespace/clawd/customer-monitor/templates")

# 创建目录
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'reach_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ReachStatus(Enum):
    """触达状态"""
    PENDING = "待触达"
    SENDING = "发送中"
    SENT = "已发送"
    REPLIED = "已回复"
    CONVERTED = "已转化"
    FAILED = "发送失败"
    BLOCKED = "被封禁"


class Platform(Enum):
    """平台"""
    DOUYIN = "抖音"
    XIAOHONGSHU = "小红书"
    ZHIHU = "知乎"
    BAIDU = "百度"
    WEIXIN = "微信"
    SMS = "短信"


@dataclass
class ReachTask:
    """触达任务"""
    id: str
    lead_id: str
    platform: str
    template_type: str  # 私信/评论/短信
    content: str
    status: str
    scheduled_at: str
    sent_at: str = ""
    replied_at: str = ""
    response: str = ""
    converted_at: str = ""
    retry_count: int = 0
    error_message: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M'))


@dataclass
class ReachStats:
    """触达统计"""
    total: int = 0
    sent: int = 0
    replied: int = 0
    converted: int = 0
    failed: int = 0
    blocked: int = 0
    reply_rate: float = 0.0
    convert_rate: float = 0.0


class AutoReachSystem:
    """自动化触达系统"""
    
    def __init__(self):
        self.tasks: List[ReachTask] = []
        self.templates = self._load_templates()
        self.load_tasks()
        self.platform_config = self._load_platform_config()
    
    def _load_templates(self) -> Dict:
        """加载触达模板"""
        template_file = TEMPLATE_DIR / "templates.json"
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _load_platform_config(self) -> Dict:
        """加载平台配置"""
        config_file = DATA_DIR / "platform_config.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            '抖音': {
                'max_per_day': 50,
                'delay_min': 30,
                'delay_max': 120,
                'private_msg': True,
                'comment': True
            },
            '小红书': {
                'max_per_day': 30,
                'delay_min': 60,
                'delay_max': 180,
                'private_msg': True,
                'comment': True
            },
            '知乎': {
                'max_per_day': 20,
                'delay_min': 120,
                'delay_max': 300,
                'private_msg': True,
                'comment': True
            },
            '百度': {
                'max_per_day': 10,
                'delay_min': 300,
                'delay_max': 600,
                'private_msg': False,
                'comment': True
            },
            '短信': {
                'max_per_day': 100,
                'delay_min': 5,
                'delay_max': 10
            }
        }
    
    def load_tasks(self):
        """加载任务"""
        task_file = DATA_DIR / "reach_tasks.json"
        if task_file.exists():
            with open(task_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = [ReachTask(**t) for t in data]
    
    def save_tasks(self):
        """保存任务"""
        task_file = DATA_DIR / "reach_tasks.json"
        data = [asdict(t) for t in self.tasks]
        task_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    
    def generate_task_id(self) -> str:
        """生成任务ID"""
        import hashlib
        timestamp = str(datetime.now().timestamp()).encode()
        return hashlib.md5(timestamp).hexdigest()[:8]
    
    def create_reach_task(self, lead: Dict, intent_level: str = "中") -> ReachTask:
        """创建触达任务"""
        platform = lead.get('source', '抖音')
        template_type = '私信'
        
        # 根据平台选择触达方式
        if platform == '抖音搜索':
            platform_name = '抖音'
        elif platform == '小红书':
            platform_name = '小红书'
        elif platform == '知乎':
            platform_name = '知乎'
        elif platform == '百度搜索':
            platform_name = '百度'
        else:
            platform_name = '抖音'
        
        # 获取模板
        template = self.templates.get('私信', {}).get(intent_level, '')
        if not template:
            template = self._get_default_template(intent_level)
        
        # 延迟发送（模拟）
        scheduled_at = (datetime.now() + timedelta(minutes=random.randint(5, 30))).strftime('%Y-%m-%d %H:%M')
        
        task = ReachTask(
            id=self.generate_task_id(),
            lead_id=lead.get('id', ''),
            platform=platform_name,
            template_type=template_type,
            content=template,
            status=ReachStatus.PENDING.value,
            scheduled_at=scheduled_at
        )
        
        self.tasks.append(task)
        self.save_tasks()
        
        return task
    
    def _get_default_template(self, intent_level: str) -> str:
        """获取默认模板"""
        templates = {
            '高意向': '您好，看到您在咨询贷款问题。我这边专业从事贷款服务，可以帮您匹配最适合的产品，利息低、审批快。需要的话可以私信我，帮您免费评估。',
            '中意向': '您好，看到您在了解贷款相关。我这边整理了各银行的贷款产品对比资料，可能对您有帮助，需要的话可以私信我。',
            '低意向': '您好，看到您的提问。我这边有贷款方面的资料可以分享给您，如有需要可以私信交流。'
        }
        return templates.get(intent_level, templates['中意向'])
    
    def execute_task(self, task_id: str) -> bool:
        """执行任务"""
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task:
            logger.error(f"任务不存在: {task_id}")
            return False
        
        # 检查是否可执行
        if task.status not in [ReachStatus.PENDING.value, ReachStatus.FAILED.value]:
            logger.warning(f"任务状态不可执行: {task.status}")
            return False
        
        # 检查频率限制
        config = self.platform_config.get(task.platform, {})
        today = datetime.now().strftime('%Y-%m-%d')
        today_sent = len([t for t in self.tasks if t.platform == task.platform 
                          and t.sent_at.startswith(today)])
        
        if today_sent >= config.get('max_per_day', 10):
            logger.warning(f"{task.platform} 今日已达上限")
            return False
        
        # 更新状态
        task.status = ReachStatus.SENDING.value
        self.save_tasks()
        
        # 模拟发送
        time.sleep(random.uniform(1, 3))
        
        # 随机成功/失败
        success_rate = 0.9
        if random.random() < success_rate:
            task.status = ReachStatus.SENT.value
            task.sent_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            task.retry_count = 0
            logger.info(f"✅ 发送成功: {task.id} -> {task.platform}")
            result = True
        else:
            # 失败重试
            if task.retry_count < 3:
                task.retry_count += 1
                task.status = ReachStatus.PENDING.value
                task.error_message = "发送失败，重试中"
                logger.warning(f"⚠️ 发送失败，重试: {task.id}")
                result = False
            else:
                task.status = ReachStatus.FAILED.value
                task.error_message = "多次发送失败"
                logger.error(f"❌ 发送失败: {task.id}")
                result = True  # 标记为完成（失败状态）
        
        self.save_tasks()
        return result
    
    def execute_pending_tasks(self):
        """执行所有待发送任务"""
        logger.info("🚀 执行待发送任务...")
        
        pending = [t for t in self.tasks if t.status == ReachStatus.PENDING.value]
        logger.info(f"   待发送: {len(pending)} 个")
        
        # 按平台分组
        for platform in set(t.platform for t in pending):
            platform_tasks = [t for t in pending if t.platform == platform]
            config = self.platform_config.get(platform, {})
            max_per_day = config.get('max_per_day', 10)
            
            today = datetime.now().strftime('%Y-%m-%d')
            today_sent = len([t for t in self.tasks if t.platform == platform 
                              and t.sent_at.startswith(today)])
            
            remaining = max(0, max_per_day - today_sent)
            
            for task in platform_tasks[:remaining]:
                # 延时发送
                delay = random.randint(
                    config.get('delay_min', 30),
                    config.get('delay_max', 120)
                )
                logger.info(f"   等待 {delay}秒 后发送...")
                time.sleep(delay)
                
                self.execute_task(task.id)
        
        logger.info("   ✅ 任务执行完成")
    
    def simulate_reply(self, task_id: str, reply_content: str):
        """模拟客户回复"""
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            task.status = ReachStatus.REPLIED.value
            task.replied_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            task.response = reply_content
            self.save_tasks()
            logger.info(f"💬 客户回复: {reply_content}")
    
    def simulate_convert(self, task_id: str):
        """模拟转化"""
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            task.status = ReachStatus.CONVERTED.value
            task.converted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_tasks()
            logger.info(f"🎉 客户转化: {task.id}")
    
    def get_statistics(self) -> ReachStats:
        """获取统计"""
        stats = ReachStats()
        
        for task in self.tasks:
            stats.total += 1
            if task.status == ReachStatus.SENT.value:
                stats.sent += 1
            elif task.status == ReachStatus.REPLIED.value:
                stats.replied += 1
            elif task.status == ReachStatus.CONVERTED.value:
                stats.converted += 1
            elif task.status == ReachStatus.FAILED.value:
                stats.failed += 1
            elif task.status == ReachStatus.BLOCKED.value:
                stats.blocked += 1
        
        # 计算比率
        if stats.sent > 0:
            stats.reply_rate = round(stats.replied / stats.sent * 100, 1)
            stats.convert_rate = round(stats.converted / stats.sent * 100, 1)
        
        return stats
    
    def generate_report(self) -> str:
        """生成触达报告"""
        stats = self.get_statistics()
        
        # 按平台统计
        platform_stats = {}
        for task in self.tasks:
            platform = task.platform
            if platform not in platform_stats:
                platform_stats[platform] = {'sent': 0, 'replied': 0, 'converted': 0}
            
            if task.status in [ReachStatus.SENT.value, ReachStatus.REPLIED.value, ReachStatus.CONVERTED.value]:
                platform_stats[platform]['sent'] += 1
            if task.status == ReachStatus.REPLIED.value:
                platform_stats[platform]['replied'] += 1
            if task.status == ReachStatus.CONVERTED.value:
                platform_stats[platform]['converted'] += 1
        
        report = f"""# 📊 自动化触达报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📈 总体统计

| 指标 | 数值 | 比率 |
|------|------|------|
| 总任务 | {stats.total} | - |
| 已发送 | {stats.sent} | - |
| 已回复 | {stats.replied} | {stats.reply_rate}% |
| 已转化 | {stats.converted} | {stats.convert_rate}% |
| 发送失败 | {stats.failed} | - |
| 被封禁 | {stats.blocked} | - |

---

## 📱 平台统计

| 平台 | 发送 | 回复 | 转化 | 回复率 | 转化率 |
|------|------|------|------|--------|--------|
"""
        
        for platform, data in platform_stats.items():
            reply_rate = round(data['replied'] / data['sent'] * 100, 1) if data['sent'] > 0 else 0
            convert_rate = round(data['converted'] / data['sent'] * 100, 1) if data['sent'] > 0 else 0
            report += f"| {platform} | {data['sent']} | {data['replied']} | {data['converted']} | {reply_rate}% | {convert_rate}% |\n"
        
        # 待执行任务
        pending = [t for t in self.tasks if t.status == ReachStatus.PENDING.value]
        report += f"""
---

## ⏳ 待执行任务 ({len(pending)}个)

| ID | 平台 | 类型 | 计划时间 |
|----|------|------|----------|
"""
        
        for task in pending[:10]:
            report += f"| {task.id} | {task.platform} | {task.template_type} | {task.scheduled_at} |\n"
        
        # 最近任务
        sent_tasks = [t for t in self.tasks if t.status == ReachStatus.SENT.value][-10:]
        report += f"""
---

## 📤 最近发送

| ID | 平台 | 时间 | 状态 |
|----|------|------|------|
"""
        
        for task in sent_tasks:
            report += f"| {task.id} | {task.platform} | {task.sent_at[-8:]} | {task.status} |\n"
        
        # 触达建议
        report += f"""
---

## 💡 优化建议

### 提升回复率
1. **个性化话术**: 根据客户问题定制回复内容
2. **最佳时段**: 分析回复率最高的发送时间
3. **跟进机制**: 发送后2-3天进行电话跟进

### 避免封禁
1. **控制频率**: 每日发送量不超过平台限制
2. **内容变化**: 避免重复内容，使用变体话术
3. **账号矩阵**: 多账号分散触达风险

### 提升转化
1. **快速响应**: 客户回复后5分钟内响应
2. **价值提供**: 先给价值（产品对比、利率表），再转化
3. **紧迫感**: 限时优惠、利率上调提醒

---

*报告由 AutoReach System 自动生成*
"""
        
        return report
    
    def run_full_reach(self, leads: List[Dict]):
        """执行完整触达流程"""
        print("=" * 60)
        print("    🤖 自动化触达系统 v1.0")
        print("=" * 60)
        
        # 1. 创建任务
        print("\n📝 创建触达任务...")
        for lead in leads:
            intent = lead.get('intent_level', '中')
            task = self.create_reach_task(lead, intent)
            print(f"   ✅ 创建任务: {task.id} -> {task.platform} ({task.scheduled_at})")
        
        # 2. 执行任务
        print("\n🚀 执行触达任务...")
        self.execute_pending_tasks()
        
        # 3. 统计
        stats = self.get_statistics()
        print("\n📊 触达统计:")
        print(f"   - 总任务: {stats.total}")
        print(f"   - 已发送: {stats.sent}")
        print(f"   - 已回复: {stats.replied} ({stats.reply_rate}%)")
        print(f"   - 已转化: {stats.converted} ({stats.convert_rate}%)")
        
        # 4. 生成报告
        print("\n📄 生成报告...")
        report = self.generate_report()
        report_file = DATA_DIR / f"reach_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.write_text(report, encoding='utf-8')
        
        print(f"   ✅ 报告已保存: {report_file}")
        
        # 5. 保存任务
        self.save_tasks()
        
        print("\n" + "=" * 60)
        print("    ✅ 触达完成！")
        print("=" * 60)
        
        return stats, report_file


def main():
    import sys
    
    # 加载线索数据
    lead_files = list(DATA_DIR.glob("leads_*.json"))
    if not lead_files:
        print("❌ 未找到线索数据，请先运行客户搜索工具")
        return
    
    # 加载最新的线索
    latest_file = sorted(lead_files)[-1]
    leads = json.loads(latest_file.read_text(encoding='utf-8'))
    
    # 创建触达系统
    reach_system = AutoReachSystem()
    
    # 执行触达
    stats, report_file = reach_system.run_full_reach(leads)
    
    print(f"\n📄 报告: {report_file}")


if __name__ == '__main__':
    main()
