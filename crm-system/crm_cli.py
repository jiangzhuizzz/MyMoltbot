#!/usr/bin/env python3
"""
CRM命令行工具
快速执行CRM操作
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from crm import CRMSystem, CustomerStatus, IntentLevel

DATA_DIR = Path("/home/codespace/clawd/crm-system/data")


def print_help():
    print("""
CRM命令行工具

用法: python crm_cli.py <命令> [参数]

命令:
  list                          列出所有客户
  add <姓名> <电话> [来源]       添加客户
  get <客户ID>                  查看客户详情
  update <客户ID> <字段>=<值>   更新客户
  delete <客户ID>               删除客户
  search <关键词>               搜索客户
  follow <客户ID> <方式> <内容>  添加跟进记录
  pending                       待跟进客户
  import <文件>                 从搜索结果导入
  stats                         统计数据
  report                        生成报告
  export                        导出CSV
  pipeline                      销售漏斗

示例:
  python crm_cli.py add 张三 13800138000 抖音
  python crm_cli.py update C123456 status=跟进中
  python crm_cli.py search 贷款
  python crm_cli.py follow ABCD1234 电话 客户有意向
""")


def cmd_list(args):
    """列出客户"""
    crm = CRMSystem()
    
    status = args[0] if args else ""
    intent = args[1] if len(args) > 1 else ""
    
    customers = crm.search_customers(status=status, intent=intent)
    
    print(f"\n客户列表 ({len(customers)}个):")
    print("-" * 80)
    print(f"{'ID':<10} {'姓名':<10} {'电话':<15} {'状态':<10} {'意向':<8} {'产品':<15}")
    print("-" * 80)
    
    for c in customers:
        print(f"{c.id:<10} {c.name:<10} {c.phone:<15} {c.status:<10} {c.intent_level:<8} {c.product_type[:15] if c.product_type else '-':<15}")


def cmd_add(args):
    """添加客户"""
    if len(args) < 2:
        print("❌ 需要提供姓名和电话")
        return
    
    name, phone = args[0], args[1]
    source = args[2] if len(args) > 2 else ""
    
    crm = CRMSystem()
    customer = crm.add_customer(name=name, phone=phone, source=source)
    print(f"✅ 添加成功: {customer.id}")


def cmd_get(args):
    """查看客户"""
    if not args:
        print("❌ 需要提供客户ID")
        return
    
    crm = CRMSystem()
    customer = crm.get_customer(args[0])
    
    if not customer:
        print("❌ 客户不存在")
        return
    
    print(f"\n客户详情:")
    print(f"  ID: {customer.id}")
    print(f"  姓名: {customer.name}")
    print(f"  电话: {customer.phone}")
    print(f"  来源: {customer.source}")
    print(f"  状态: {customer.status}")
    print(f"  意向: {customer.intent_level}")
    print(f"  产品: {customer.product_type}")
    print(f"  金额: ¥{customer.amount:,.0f}" if customer.amount else "  金额: -")
    print(f"  描述: {customer.description}")
    print(f"  创建: {customer.created_at}")
    print(f"  最后联系: {customer.last_contact}")
    
    # 跟进记录
    followups = crm.get_customer_followups(customer.id)
    if followups:
        print(f"\n跟进记录 ({len(followups)}条):")
        for f in followups[-5:]:
            print(f"  - [{f.type}] {f.content[:30]}... ({f.created_at})")


def cmd_update(args):
    """更新客户"""
    if len(args) < 2:
        print("❌ 需要提供客户ID和字段")
        return
    
    customer_id = args[0]
    update_data = {}
    
    for arg in args[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            update_data[key] = value
    
    crm = CRMSystem()
    if crm.update_customer(customer_id, **update_data):
        print(f"✅ 更新成功")
    else:
        print("❌ 客户不存在")


def cmd_search(args):
    """搜索客户"""
    if not args:
        print("❌ 需要提供关键词")
        return
    
    keyword = args[0]
    crm = CRMSystem()
    customers = crm.search_customers(keyword=keyword)
    
    print(f"\n搜索结果 '{keyword}' ({len(customers)}个):")
    print("-" * 80)
    for c in customers:
        print(f"  {c.id} | {c.name} | {c.phone} | {c.status} | {c.intent_level}")


def cmd_follow(args):
    """添加跟进"""
    if len(args) < 3:
        print("❌ 需要提供客户ID、跟进方式、内容")
        return
    
    customer_id, type_, content = args[0], args[1], args[2]
    
    crm = CRMSystem()
    followup = crm.add_followup(customer_id, type_, content)
    print(f"✅ 跟进记录已添加: {followup.id}")


def cmd_pending(args):
    """待跟进"""
    crm = CRMSystem()
    pending = crm.get_pending_followups()
    
    print(f"\n待跟进客户 ({len(pending)}个):")
    print("-" * 60)
    for customer, time in pending:
        print(f"  {customer.name} | {customer.phone} | {customer.status} | 计划: {time}")


def cmd_import(args):
    """导入客户"""
    if not args:
        print("❌ 需要提供文件")
        return
    
    crm = CRMSystem()
    count = crm.import_from_search(args[0])
    print(f"✅ 成功导入 {count} 个客户")


def cmd_stats(args):
    """统计"""
    crm = CRMSystem()
    stats = crm.get_statistics()
    
    print("\n📊 统计数据:")
    print(f"  总客户: {stats['customers']['total']}")
    print(f"  新客户: {stats['customers']['new']}")
    print(f"  跟进中: {stats['customers']['following']}")
    print(f"  已成交: {stats['customers']['closed_won']}")
    print(f"  转化率: {stats['conversion']['rate']}%")
    print(f"  总佣金: ¥{stats['deals']['total_commission']:,.0f}")


def cmd_report(args):
    """生成报告"""
    crm = CRMSystem()
    stats, report_file = crm.run_full_report()
    print(f"\n✅ 报告已生成: {report_file}")


def cmd_export(args):
    """导出"""
    crm = CRMSystem()
    csv_file = crm.export_to_csv()
    print(f"✅ 数据已导出: {csv_file}")


def cmd_pipeline(args):
    """销售漏斗"""
    crm = CRMSystem()
    pipeline = crm.get_pipeline()
    
    print("\n🔄 销售漏斗:")
    total = sum(pipeline.values())
    for stage, count in pipeline.items():
        bar = "█" * int(count / max(total, 1) * 30)
        print(f"  {stage:<10} {count:<5} {bar}")


def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    commands = {
        'list': cmd_list,
        'add': cmd_add,
        'get': cmd_get,
        'update': cmd_update,
        'search': cmd_search,
        'follow': cmd_follow,
        'pending': cmd_pending,
        'import': cmd_import,
        'stats': cmd_stats,
        'report': cmd_report,
        'export': cmd_export,
        'pipeline': cmd_pipeline,
    }
    
    if command in commands:
        commands[command](args)
    else:
        print(f"❌ 未知命令: {command}")
        print_help()


if __name__ == '__main__':
    main()
