#!/usr/bin/env python3
"""
客户关系管理系统(CRM) - 基础版
管理客户全生命周期
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum
import logging

# 配置
DATA_DIR = Path("/home/codespace/clawd/crm-system/data")
LOG_DIR = Path("/home/codespace/clawd/crm-system/logs")
TEMPLATE_DIR = Path("/home/codespace/clawd/crm-system/templates")

# 创建目录
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'crm_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CustomerStatus(Enum):
    """客户状态"""
    NEW = "新客户"
    CONTACTED = "已联系"
    FOLLOWING = "跟进中"
    QUALIFIED = "已筛选"
    PROPOSAL = "方案沟通"
    NEGOTIATION = "谈判中"
    CLOSED_WON = "成交"
    CLOSED_LOST = "流失"


class IntentLevel(Enum):
    """意向等级"""
    HIGH = "高意向"
    MEDIUM = "中意向"
    LOW = "低意向"
    NONE = "无意向"


class ProductType(Enum):
    """产品类型"""
    PERSONAL_LOAN = "个人信用贷"
    MORTGAGE = "房产抵押贷"
    CAR_LOAN = "车贷"
    BUSINESS_LOAN = "经营贷"
    CREDIT_CARD = "信用卡"
    INSURANCE = "保险"
    OTHER = "其他"


@dataclass
class Customer:
    """客户"""
    id: str
    name: str                    # 客户姓名
    phone: str                   # 联系电话
    wechat: str = ""             # 微信号
    source: str = ""             # 来源渠道
    status: str = CustomerStatus.NEW.value
    intent_level: str = IntentLevel.MEDIUM.value
    product_type: str = ""       # 意向产品
    amount: float = 0            # 贷款金额
    term: int = 0                # 期限(月)
    description: str = ""        # 客户描述
    tags: List[str] = field(default_factory=list)
    
    # 征信相关
    has_credit_issue: bool = False
    credit_issue_desc: str = ""
    
    # 房产相关
    has_property: bool = False
    property_value: float = 0
    property_loan: float = 0
    
    # 时间字段
    created_at: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M'))
    updated_at: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M'))
    last_contact: str = ""
    next_followup: str = ""
    converted_at: str = ""
    lost_reason: str = ""


@dataclass
class Followup:
    """跟进记录"""
    id: str
    customer_id: str
    type: str                   # 跟进方式(电话/微信/面谈)
    content: str                # 跟进内容
    result: str = ""            # 跟进结果
    next_action: str = ""       # 下次行动
    next_time: str = ""         # 下次跟进时间
    created_at: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M'))
    created_by: str = "系统"


@dataclass
class Deal:
    """成交记录"""
    id: str
    customer_id: str
    product_name: str           # 产品名称
    bank: str                   # 银行/机构
    amount: float               # 贷款金额
    commission: float           # 佣金
    rate: float                 # 利率
    term: int                   # 期限
    closed_at: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M'))
    status: str = "已放款"


class CRMSystem:
    """CRM系统"""
    
    def __init__(self):
        self.customers: List[Customer] = []
        self.followups: List[Followup] = []
        self.deals: List[Deal] = []
        self.load_data()
    
    # ========== 数据加载/保存 ==========
    
    def load_data(self):
        """加载所有数据"""
        self._load_customers()
        self._load_followups()
        self._load_deals()
        logger.info(f"Loaded {len(self.customers)} customers, {len(self.followups)} followups, {len(self.deals)} deals")
    
    def _load_customers(self):
        """加载客户"""
        file_path = DATA_DIR / "customers.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.customers = [Customer(**c) for c in data]
    
    def _load_followups(self):
        """加载跟进记录"""
        file_path = DATA_DIR / "followups.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.followups = [Followup(**f) for f in data]
    
    def _load_deals(self):
        """加载成交记录"""
        file_path = DATA_DIR / "deals.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.deals = [Deal(**d) for d in data]
    
    def save_all(self):
        """保存所有数据"""
        self._save_customers()
        self._save_followups()
        self._save_deals()
    
    def _save_customers(self):
        """保存客户"""
        file_path = DATA_DIR / "customers.json"
        data = [asdict(c) for c in self.customers]
        file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    
    def _save_followups(self):
        """保存跟进记录"""
        file_path = DATA_DIR / "followups.json"
        data = [asdict(f) for f in self.followups]
        file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    
    def _save_deals(self):
        """保存成交记录"""
        file_path = DATA_DIR / "deals.json"
        data = [asdict(d) for d in self.deals]
        file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # ========== 客户管理 ==========
    
    def generate_id(self) -> str:
        """生成ID"""
        import hashlib
        timestamp = str(datetime.now().timestamp()).encode()
        return hashlib.md5(timestamp).hexdigest()[:8]
    
    def add_customer(self, name: str, phone: str, source: str = "", 
                     product_type: str = "", amount: float = 0,
                     description: str = "", **kwargs) -> Customer:
        """添加客户"""
        customer = Customer(
            id=self.generate_id(),
            name=name,
            phone=phone,
            source=source,
            product_type=product_type,
            amount=amount,
            description=description,
            **kwargs
        )
        self.customers.append(customer)
        self.save_all()
        logger.info(f"Added customer: {name} ({phone})")
        return customer
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """获取客户"""
        for c in self.customers:
            if c.id == customer_id:
                return c
        return None
    
    def search_customers(self, keyword: str = "", status: str = "", 
                        intent: str = "", source: str = "") -> List[Customer]:
        """搜索客户"""
        results = self.customers
        
        if keyword:
            keyword = keyword.lower()
            results = [c for c in results if 
                      keyword in c.name.lower() or 
                      keyword in c.phone or 
                      keyword in c.description.lower()]
        
        if status:
            results = [c for c in results if c.status == status]
        
        if intent:
            results = [c for c in results if c.intent_level == intent]
        
        if source:
            results = [c for c in results if c.source == source]
        
        return results
    
    def update_customer(self, customer_id: str, **kwargs) -> bool:
        """更新客户"""
        customer = self.get_customer(customer_id)
        if not customer:
            return False
        
        for key, value in kwargs.items():
            if hasattr(customer, key):
                setattr(customer, key, value)
        
        customer.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.save_all()
        return True
    
    def delete_customer(self, customer_id: str) -> bool:
        """删除客户"""
        customer = self.get_customer(customer_id)
        if not customer:
            return False
        
        self.customers.remove(customer)
        self.save_all()
        return True
    
    # ========== 跟进管理 ==========
    
    def add_followup(self, customer_id: str, type: str, content: str,
                    result: str = "", next_action: str = "", next_time: str = "") -> Followup:
        """添加跟进记录"""
        followup = Followup(
            id=self.generate_id(),
            customer_id=customer_id,
            type=type,
            content=content,
            result=result,
            next_action=next_action,
            next_time=next_time
        )
        self.followups.append(followup)
        
        # 更新客户状态
        self.update_customer(customer_id, 
                           status=CustomerStatus.FOLLOWING.value,
                           last_contact=datetime.now().strftime('%Y-%m-%d %H:%M'),
                           next_followup=next_time)
        
        self.save_all()
        return followup
    
    def get_customer_followups(self, customer_id: str) -> List[Followup]:
        """获取客户跟进记录"""
        return [f for f in self.followups if f.customer_id == customer_id]
    
    def get_pending_followups(self) -> List[tuple]:
        """获取待跟进客户"""
        today = datetime.now().strftime('%Y-%m-%d')
        pending = []
        
        for c in self.customers:
            if c.next_followup and c.next_followup <= today:
                if c.status not in [CustomerStatus.CLOSED_WON.value, CustomerStatus.CLOSED_LOST.value]:
                    pending.append((c, c.next_followup))
        
        return sorted(pending, key=lambda x: x[1])
    
    # ========== 成交管理 ==========
    
    def add_deal(self, customer_id: str, product_name: str, bank: str,
                amount: float, commission: float, rate: float, term: int) -> Deal:
        """添加成交记录"""
        deal = Deal(
            id=self.generate_id(),
            customer_id=customer_id,
            product_name=product_name,
            bank=bank,
            amount=amount,
            commission=commission,
            rate=rate,
            term=term
        )
        self.deals.append(deal)
        
        # 更新客户状态
        self.update_customer(customer_id, 
                           status=CustomerStatus.CLOSED_WON.value,
                           converted_at=datetime.now().strftime('%Y-%m-%d'))
        
        self.save_all()
        return deal
    
    def get_customer_deal(self, customer_id: str) -> Optional[Deal]:
        """获取客户成交记录"""
        for d in self.deals:
            if d.customer_id == customer_id:
                return d
        return None
    
    # ========== 统计分析 ==========
    
    def get_statistics(self) -> Dict:
        """获取统计"""
        # 客户统计
        total_customers = len(self.customers)
        new_customers = len([c for c in self.customers if c.status == CustomerStatus.NEW.value])
        following = len([c for c in self.customers if c.status == CustomerStatus.FOLLOWING.value])
        qualified = len([c for c in self.customers if c.status == CustomerStatus.QUALIFIED.value])
        closed_won = len([c for c in self.customers if c.status == CustomerStatus.CLOSED_WON.value])
        closed_lost = len([c for c in self.customers if c.status == CustomerStatus.CLOSED_LOST.value])
        
        # 意向分布
        high_intent = len([c for c in self.customers if c.intent_level == IntentLevel.HIGH.value])
        medium_intent = len([c for c in self.customers if c.intent_level == IntentLevel.MEDIUM.value])
        low_intent = len([c for c in self.customers if c.intent_level == IntentLevel.LOW.value])
        
        # 金额统计
        total_amount = sum(d.amount for d in self.deals)
        total_commission = sum(d.commission for d in self.deals)
        avg_commission = total_commission / len(self.deals) if self.deals else 0
        
        # 转化率
        contacted = len([c for c in self.customers if c.status in [
            CustomerStatus.CONTACTED.value, CustomerStatus.FOLLOWING.value,
            CustomerStatus.QUALIFIED.value, CustomerStatus.PROPOSAL.value,
            CustomerStatus.NEGOTIATION.value, CustomerStatus.CLOSED_WON.value
        ]])
        conversion_rate = (closed_won / contacted * 100) if contacted > 0 else 0
        
        return {
            'customers': {
                'total': total_customers,
                'new': new_customers,
                'following': following,
                'qualified': qualified,
                'closed_won': closed_won,
                'closed_lost': closed_lost
            },
            'intent': {
                'high': high_intent,
                'medium': medium_intent,
                'low': low_intent
            },
            'deals': {
                'total': len(self.deals),
                'total_amount': total_amount,
                'total_commission': total_commission,
                'avg_commission': avg_commission
            },
            'conversion': {
                'contacted': contacted,
                'closed_won': closed_won,
                'rate': round(conversion_rate, 1)
            }
        }
    
    def get_pipeline(self) -> Dict:
        """获取销售漏斗"""
        pipeline = {
            '新客户': len([c for c in self.customers if c.status == CustomerStatus.NEW.value]),
            '已联系': len([c for c in self.customers if c.status == CustomerStatus.CONTACTED.value]),
            '跟进中': len([c for c in self.customers if c.status == CustomerStatus.FOLLOWING.value]),
            '已筛选': len([c for c in self.customers if c.status == CustomerStatus.QUALIFIED.value]),
            '方案沟通': len([c for c in self.customers if c.status == CustomerStatus.PROPOSAL.value]),
            '谈判中': len([c for c in self.customers if c.status == CustomerStatus.NEGOTIATION.value]),
            '成交': len([c for c in self.customers if c.status == CustomerStatus.CLOSED_WON.value]),
            '流失': len([c for c in self.customers if c.status == CustomerStatus.CLOSED_LOST.value]),
        }
        return pipeline
    
    def get_source_stats(self) -> Dict:
        """获取来源统计"""
        stats = {}
        for c in self.customers:
            source = c.source or '未知'
            if source not in stats:
                stats[source] = {'total': 0, 'won': 0}
            stats[source]['total'] += 1
            if c.status == CustomerStatus.CLOSED_WON.value:
                stats[source]['won'] += 1
        
        # 计算转化率
        for source, data in stats.items():
            data['rate'] = round(data['won'] / data['total'] * 100, 1) if data['total'] > 0 else 0
        
        return stats
    
    # ========== 导入导出 ==========
    
    def import_from_search(self, leads_file: str):
        """从搜索结果导入客户"""
        file_path = DATA_DIR / leads_file
        if not file_path.exists():
            logger.error(f"File not found: {leads_file}")
            return 0
        
        with open(file_path, 'r', encoding='utf-8') as f:
            leads = json.load(f)
        
        count = 0
        for lead in leads:
            # 检查是否已存在
            exists = any(c.phone == lead.get('phone', '') for c in self.customers)
            if not exists:
                self.add_customer(
                    name=lead.get('name', lead.get('author', '客户')),
                    phone=lead.get('phone', ''),
                    source=lead.get('source', ''),
                    description=lead.get('content', '')[:200],
                    intent_level=lead.get('intent_level', '中意向'),
                    amount=lead.get('amount', 0)
                )
                count += 1
        
        logger.info(f"Imported {count} customers from {leads_file}")
        return count
    
    def export_to_csv(self, filename: str = "customers.csv"):
        """导出客户数据"""
        import csv
        
        file_path = DATA_DIR / filename
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 标题行
            writer.writerow(['ID', '姓名', '电话', '来源', '状态', '意向', '产品', '金额', '创建时间', '最后联系'])
            # 数据行
            for c in self.customers:
                writer.writerow([
                    c.id, c.name, c.phone, c.source, c.status, 
                    c.intent_level, c.product_type, c.amount,
                    c.created_at, c.last_contact
                ])
        
        return file_path
    
    # ========== 报告生成 ==========
    
    def generate_report(self) -> str:
        """生成CRM报告"""
        stats = self.get_statistics()
        pipeline = self.get_pipeline()
        source_stats = self.get_source_stats()
        
        report = f"""# 📊 CRM客户管理报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📈 总体统计

| 指标 | 数值 |
|------|------|
| 总客户数 | {stats['customers']['total']} |
| 新客户 | {stats['customers']['new']} |
| 跟进中 | {stats['customers']['following']} |
| 已筛选 | {stats['customers']['qualified']} |
| 已成交 | {stats['customers']['closed_won']} |
| 已流失 | {stats['customers']['closed_lost']} |

---

## 🎯 意向分布

| 等级 | 数量 | 占比 |
|------|------|------|
| 高意向 | {stats['intent']['high']} | {stats['intent']['high']/stats['customers']['total']*100 if stats['customers']['total']>0 else 0:.1f}% |
| 中意向 | {stats['intent']['medium']} | {stats['intent']['medium']/stats['customers']['total']*100 if stats['customers']['total']>0 else 0:.1f}% |
| 低意向 | {stats['intent']['low']} | {stats['intent']['low']/stats['customers']['total']*100 if stats['customers']['total']>0 else 0:.1f}% |

---

## 🔄 销售漏斗

| 阶段 | 数量 | 转化率 |
|------|------|--------|
"""
        
        prev_count = stats['customers']['total']
        for stage, count in pipeline.items():
            rate = round(count / prev_count * 100, 1) if prev_count > 0 else 0
            report += f"| {stage} | {count} | {rate}% |\n"
            prev_count = count if count > 0 else prev_count
        
        report += f"""
---

## 📊 来源分析

| 来源 | 总数 | 成交 | 转化率 |
|------|------|------|--------|
"""
        
        for source, data in sorted(source_stats.items(), key=lambda x: x[1]['total'], reverse=True):
            report += f"| {source} | {data['total']} | {data['won']} | {data['rate']}% |\n"
        
        report += f"""
---

## 💰 成交统计

| 指标 | 数值 |
|------|------|
| 总成交数 | {stats['deals']['total']} |
| 总放款金额 | ¥{stats['deals']['total_amount']:,.0f} |
| 总佣金 | ¥{stats['deals']['total_commission']:,.0f} |
| 平均佣金 | ¥{stats['deals']['avg_commission']:,.0f} |

---

## 📋 今日待跟进

| 客户 | 计划时间 | 状态 |
|------|----------|------|
"""
        
        pending = self.get_pending_followups()
        for customer, time in pending[:10]:
            report += f"| {customer.name} | {time} | {customer.status} |\n"
        
        report += f"""
---

## 💡 优化建议

### 提升转化率
1. 跟进频率: 保证每周至少跟进1次
2. 及时响应: 客户咨询后5分钟内响应
3. 价值提供: 先给方案，再谈价格

### 减少流失
1. 原因分析: 记录每次流失原因
2. 定期回访: 流失客户定期回访
3. 差异化服务: 针对不同意向等级提供不同服务

---

*报告由 CRM System 自动生成*
"""
        
        return report
    
    def run_full_report(self):
        """执行完整报告"""
        print("=" * 60)
        print("    📊 CRM客户管理系统 v1.0")
        print("=" * 60)
        
        # 统计
        stats = self.get_statistics()
        print("\n📈 总体统计:")
        print(f"   总客户数: {stats['customers']['total']}")
        print(f"   已成交: {stats['customers']['closed_won']}")
        print(f"   转化率: {stats['conversion']['rate']}%")
        
        print("\n💰 成交统计:")
        print(f"   总放款: ¥{stats['deals']['total_amount']:,.0f}")
        print(f"   总佣金: ¥{stats['deals']['total_commission']:,.0f}")
        
        # 待跟进
        pending = self.get_pending_followups()
        print(f"\n⏰ 待跟进: {len(pending)} 个")
        
        # 生成报告
        report = self.generate_report()
        report_file = DATA_DIR / f"crm_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.write_text(report, encoding='utf-8')
        
        # 导出数据
        csv_file = self.export_to_csv()
        
        print(f"\n📄 报告文件: {report_file}")
        print(f"📊 数据导出: {csv_file}")
        
        print("\n" + "=" * 60)
        print("    ✅ 报告生成完成！")
        print("=" * 60)
        
        return stats, report_file


def main():
    crm = CRMSystem()
    stats, report_file = crm.run_full_report()


if __name__ == '__main__':
    main()
