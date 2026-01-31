#!/usr/bin/env python3
"""
客户线索管理工作台
看板式管理所有客户和工具状态
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum

# 配置
WORKSPACE_DIR = Path("/home/codespace/clawd")
DATA_DIR = WORKSPACE_DIR / "customer-monitor" / "data"
TASK_FILE = WORKSPACE_DIR / "TASKS.md"

# 颜色配置
COLORS = {
    'GREEN': '🟢',
    'YELLOW': '🟡', 
    'RED': '🔴',
    'GRAY': '⚪',
    'BLUE': '🔵',
    'PURPLE': '🟣'
}

# 工具状态
class ToolStatus(Enum):
    RUNNING = "运行中"
    PENDING = "待完善"
    ISSUES = "有问题"
    PLANNED = "规划中"

# 客户状态
class CustomerStatus(Enum):
    NEW = "新线索"
    CONTACTED = "已联系"
    FOLLOWING = "跟进中"
    CONVERTED = "已转化"
    INVALID = "无效"


@dataclass
class Tool:
    """工具"""
    name: str
    status: str
    description: str
    last_update: str
    next_action: str
    priority: int = 1


@dataclass
class Customer:
    """客户"""
    id: str
    name: str
    source: str
    status: str
    intent: str
    last_contact: str
    next_followup: str
    amount: str
    product: str
    remark: str


class Workbench:
    """工作台"""
    
    def __init__(self):
        self.tools: List[Tool] = []
        self.customers: List[Customer] = []
        self.load_tools()
        self.load_customers()
    
    def load_tools(self):
        """加载工具列表"""
        self.tools = [
            Tool(
                name="早报系统",
                status=ToolStatus.RUNNING.value,
                description="每日9点自动生成早报，发送至WhatsApp",
                last_update="2026-01-30",
                next_action="完善内容模板",
                priority=2
            ),
            Tool(
                name="贷款产品库",
                status=ToolStatus.RUNNING.value,
                description="Obsidian模板，包含55+个贷款产品",
                last_update="2026-01-31",
                next_action="公众号采集功能",
                priority=3
            ),
            Tool(
                name="产品对比更新",
                status=ToolStatus.RUNNING.value,
                description="自动对比各银行产品，生成更新报告",
                last_update="2026-01-31",
                next_action="接入更多数据源",
                priority=3
            ),
            Tool(
                name="电商价格监控",
                status=ToolStatus.RUNNING.value,
                description="监控7大电商平台价格，找到最低价",
                last_update="2026-01-31",
                next_action="接入真实API",
                priority=2
            ),
            Tool(
                name="客户搜索工具",
                status=ToolStatus.RUNNING.value,
                description="主动搜索有贷款需求的潜在客户",
                last_update="2026-01-31",
                next_action="接入更多搜索源",
                priority=5
            ),
            Tool(
                name="小红书矩阵",
                status=ToolStatus.PENDING.value,
                description="多账号矩阵运营，低风险内容策略",
                last_update="2026-01-31",
                next_action="制定内容SOP",
                priority=4
            ),
            Tool(
                name="客户CRM",
                status=ToolStatus.PLANNED.value,
                description="客户全生命周期管理",
                last_update="-",
                next_action="需求调研",
                priority=4
            ),
            Tool(
                name="自动获客系统",
                status=ToolStatus.PLANNED.value,
                description="自动化获客流程",
                last_update="-",
                next_action="完成客户搜索工具",
                priority=5
            )
        ]
    
    def load_customers(self):
        """加载客户数据"""
        # 从客户搜索结果加载
        customer_files = list(DATA_DIR.glob("leads_*.json"))
        for cf in customer_files[-3:]:  # 最近3个文件
            try:
                data = json.loads(cf.read_text(encoding='utf-8'))
                for item in data[:5]:  # 每个文件取前5个
                    if isinstance(item, dict):
                        self.customers.append(Customer(
                            id=item.get('id', ''),
                            name=item.get('name', '客户'),
                            source=item.get('source', ''),
                            status=CustomerStatus.NEW.value,
                            intent=item.get('intent_level', '中'),
                            last_contact=item.get('created_at', ''),
                            next_followup=(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                            amount="待确认",
                            product="待匹配",
                            remark=item.get('remark', '')[:30]
                        ))
            except Exception as e:
                pass
    
    def generate_dashboard(self) -> str:
        """生成仪表盘"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # 统计
        running = len([t for t in self.tools if t.status == ToolStatus.RUNNING.value])
        pending = len([t for t in self.tools if t.status == ToolStatus.PENDING.value])
        issues = len([t for t in self.tools if t.status == ToolStatus.ISSUES.value])
        planned = len([t for t in self.tools if t.status == ToolStatus.PLANNED.value])
        
        new_customers = len([c for c in self.customers if c.status == CustomerStatus.NEW.value])
        following = len([c for c in self.customers if c.status == CustomerStatus.FOLLOWING.value])
        converted = len([c for c in self.customers if c.status == CustomerStatus.CONVERTED.value])
        
        dashboard = f"""# 📊 工作台看板

**更新时间**: {now}

---

## 🎯 快速统计

| 指标 | 数值 | 状态 |
|------|------|------|
| 🛠️ 工具总数 | {len(self.tools)} | 运行{running} / 待完善{pending} / 有问题{issues} / 规划{planned} |
| 👥 客户线索 | {len(self.customers)} | 新{new_customers} / 跟进{following} / 转化{converted} |
| 📈 本周新增 | {new_customers} | - |

---

## 🛠️ 工具状态看板

### 🟢 运行中 ({running})

| 工具 | 描述 | 最后更新 | 下一步 |
|------|------|----------|--------|
"""
        
        for tool in [t for t in self.tools if t.status == ToolStatus.RUNNING.value]:
            dashboard += f"| {COLORS['GREEN']} {tool.name} | {tool.description} | {tool.last_update} | {tool.next_action} |\n"
        
        dashboard += f"""
### 🟡 待完善 ({pending})

| 工具 | 描述 | 最后更新 | 下一步 |
|------|------|----------|--------|
"""
        
        for tool in [t for t in self.tools if t.status == ToolStatus.PENDING.value]:
            dashboard += f"| {COLORS['YELLOW']} {tool.name} | {tool.description} | {tool.last_update} | {tool.next_action} |\n"
        
        dashboard += f"""
### 🔴 有问题 ({issues})

| 工具 | 描述 | 最后更新 | 问题 |
|------|------|----------|------|
"""
        
        for tool in [t for t in self.tools if t.status == ToolStatus.ISSUES.value]:
            dashboard += f"| {COLORS['RED']} {tool.name} | {tool.description} | {tool.last_update} | {tool.next_action} |\n"
        
        dashboard += f"""
### ⚪ 规划中 ({planned})

| 工具 | 描述 | 优先级 |
|------|------|--------|
"""
        
        for tool in sorted([t for t in self.tools if t.status == ToolStatus.PLANNED.value], key=lambda x: x.priority, reverse=True):
            priority_emoji = "🔥" if tool.priority >= 4 else "📌"
            dashboard += f"| {COLORS['GRAY']} {tool.name} | {tool.description} | {priority_emoji} P{tool.priority} |\n"
        
        dashboard += f"""
---

## 👥 客户线索看板

### 新线索 ({new_customers})

| 来源 | 客户 | 意向 | 备注 | 操作 |
|------|------|------|------|------|
"""
        
        for customer in [c for c in self.customers if c.status == CustomerStatus.NEW.value][:5]:
            dashboard += f"| {customer.source} | {customer.name} | {customer.intent} | {customer.remark} | [联系] |\n"
        
        dashboard += f"""
### 跟进中 ({following})

| 来源 | 客户 | 意向 | 产品 | 备注 |
|------|------|------|------|------|
"""
        
        for customer in [c for c in self.customers if c.status == CustomerStatus.FOLLOWING.value][:5]:
            dashboard += f"| {customer.source} | {customer.name} | {customer.intent} | {customer.product} | {customer.remark} |\n"
        
        dashboard += f"""
### 已转化 ({converted})

| 来源 | 客户 | 金额 | 产品 | 时间 |
|------|------|------|------|------|
"""
        
        for customer in [c for c in self.customers if c.status == CustomerStatus.CONVERTED.value][:5]:
            dashboard += f"| {customer.source} | {customer.name} | {customer.amount} | {customer.product} | {customer.last_contact[:10]} |\n"
        
        dashboard += f"""
---

## 📋 本周计划

### 🔥 优先级任务

| 优先级 | 任务 | 状态 | 截止 |
|--------|------|------|------|
| P1 | 客户搜索工具完善 | 进行中 | - |
| P1 | 小红书内容策略 | 待开始 | - |
| P2 | 产品库公众号采集 | 待开始 | - |
| P2 | 电商监控接入API | 待开始 | - |
| P3 | 早报系统完善 | 进行中 | - |

### 📌 日常任务

- [ ] 每日客户搜索（关键词轮换）
- [ ] 跟进高意向客户
- [ ] 更新产品库
- [ ] 发布自媒体内容
- [ ] 检查工具运行状态

---

## 💡 效率建议

### 获客渠道优先级

| 渠道 | 投入 | 见效 | 推荐度 |
|------|------|------|--------|
| 老客户转介绍 | 低 | 快 | ⭐⭐⭐⭐⭐ |
| 同行渠道 | 低 | 快 | ⭐⭐⭐⭐ |
| **客户搜索工具** | 中 | 中 | ⭐⭐⭐⭐ |
| **自媒体矩阵** | 高 | 慢 | ⭐⭐⭐⭐ |

### 时间分配建议

| 活动 | 时间占比 | 说明 |
|------|----------|------|
| 客户跟进 | 40% | 转化现有客户 |
| 客户搜索 | 20% | 主动获客 |
| 内容创作 | 20% | 自媒体运营 |
| 产品学习 | 10% | 更新知识库 |
| 工具维护 | 10% | 保持工具运转 |

---

*工作台由 Workbench 自动生成*
**生成时间**: {now}
"""
        
        return dashboard
    
    def generate_tasks_markdown(self):
        """生成任务清单"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        tasks = f"""# TASKS.md - 待办任务清单

*自动生成的任务清单，用于跟踪工作进度*

---

## 📋 今日待办

- [ ] 客户搜索（轮换关键词）
- [ ] 跟进高意向客户（至少3个）
- [ ] 检查早报系统运行状态
- [ ] 更新一条自媒体内容

## 📅 本周计划

### 高优先级
- [ ] 完善客户搜索工具（接入更多数据源）
- [ ] 制定小红书内容SOP
- [ ] 测试房产号内容方向

### 中优先级
- [ ] 开发产品库公众号采集功能
- [ ] 优化电商监控数据准确性
- [ ] 整理贷款产品话术

### 低优先级
- [ ] 早报系统内容完善
- [ ] 工具文档整理
- [ ] 历史数据整理归档

---

## 🎯 长期目标

### 短期（1-2周）
- [ ] 客户搜索工具上线
- [ ] 小红书矩阵开始运营
- [ ] 获客效率提升50%

### 中期（1个月）
- [ ] 客户CRM系统上线
- [ ] 自媒体流量稳定
- [ ] 获客成本降低30%

### 长期（3个月）
- [ ] 自动化获客体系
- [ ] 客户量翻倍
- [ ] 被动流量占比50%

---

*最后更新: {now}*
"""
        
        return tasks


def main():
    workbench = Workbench()
    
    # 生成仪表盘
    dashboard = workbench.generate_dashboard()
    dashboard_file = WORKSPACE_DIR / "WORKBENCH.md"
    dashboard_file.write_text(dashboard, encoding='utf-8')
    
    # 生成任务清单
    tasks = workbench.generate_tasks_markdown()
    TASK_FILE.write_text(tasks, encoding='utf-8')
    
    print("=" * 60)
    print("    📊 工作台看板生成完成")
    print("=" * 60)
    print(f"\n📄 看板文件: {dashboard_file}")
    print(f"📋 任务文件: {TASK_FILE}")
    print(f"\n🛠️ 工具统计: {len(workbench.tools)} 个")
    print(f"👥 客户线索: {len(workbench.customers)} 个")


if __name__ == '__main__':
    main()
