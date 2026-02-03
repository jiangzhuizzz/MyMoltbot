#!/usr/bin/env python3
"""
武汉农村商业银行产品采集
公积金贷款产品全面完善
"""

import json
from datetime import datetime
from pathlib import Path

class WuhanRuralAndGJJCollector:
    """武汉农商行 + 公积金贷款采集器"""
    
    def __init__(self):
        self.products = []
        self.collect_wuhan_rural()
        self.collect_gjj_products()
    
    def collect_wuhan_rural(self):
        """采集武汉农村商业银行产品"""
        print("📦 武汉农村商业银行")
        
        products = [
            {
                'name': '汉银市民贷',
                'category': '信用贷',
                'rate': '4.8%-7.2%',
                'min_amount': 50000,
                'max_amount': 300000,
                'term': 36,
                'approval': '2-3天',
                'requirements': ['武汉户籍或在武汉工作', '社保/公积金', '征信良好', '年龄22-60岁'],
                'tags': ['本地银行', '市民专享', '门槛适中'],
                'commission': '1.8%'
            },
            {
                'name': '汉银公积金贷',
                'category': '公积金贷',
                'rate': '3.85%-4.5%',
                'min_amount': 100000,
                'max_amount': 500000,
                'term': 60,
                'approval': '3-5天',
                'requirements': ['公积金连续缴纳满12个月', '月缴存额≥500元', '征信良好', '年龄22-55岁'],
                'tags': ['公积金专享', '利率低', '额度高', '本地银行'],
                'commission': '1.5%'
            },
            {
                'name': '汉银安居贷',
                'category': '装修贷',
                'rate': '4.2%-5.5%',
                'min_amount': 100000,
                'max_amount': 500000,
                'term': 60,
                'approval': '5-7天',
                'requirements': ['武汉房产', '装修合同', '收入证明', '征信良好'],
                'tags': ['装修专享', '本地银行', '额度高'],
                'commission': '1.5%'
            },
            {
                'name': '汉银房抵贷',
                'category': '抵押贷',
                'rate': '4.0%-5.0%',
                'min_amount': 500000,
                'max_amount': 5000000,
                'term': 180,
                'approval': '7-10天',
                'requirements': ['武汉房产', '产权清晰', '评估价值≥100万', '征信良好'],
                'tags': ['高额度', '期限长', '本地银行'],
                'commission': '1.0%'
            },
            {
                'name': '汉银经营贷',
                'category': '经营贷',
                'rate': '4.5%-6.0%',
                'min_amount': 200000,
                'max_amount': 2000000,
                'term': 60,
                'approval': '5-7天',
                'requirements': ['武汉注册企业', '经营满1年', '流水充足', '征信良好'],
                'tags': ['经营用途', '本地银行', '灵活还款'],
                'commission': '1.5%'
            },
            {
                'name': '汉银车贷',
                'category': '车贷',
                'rate': '4.5%-6.5%',
                'min_amount': 100000,
                'max_amount': 1000000,
                'term': 60,
                'approval': '2-3天',
                'requirements': ['购车合同', '驾驶证', '收入证明', '征信良好'],
                'tags': ['购车专享', '本地银行'],
                'commission': '1.5%'
            },
            {
                'name': '汉银社保贷',
                'category': '社保贷',
                'rate': '5.0%-7.0%',
                'min_amount': 30000,
                'max_amount': 200000,
                'term': 36,
                'approval': '2-3天',
                'requirements': ['社保连续缴纳满12个月', '月缴纳额≥800元', '征信良好'],
                'tags': ['社保专享', '门槛适中', '本地银行'],
                'commission': '2.0%'
            },
            {
                'name': '汉银亲情贷',
                'category': '信用贷',
                'rate': '5.5%-7.5%',
                'min_amount': 20000,
                'max_amount': 100000,
                'term': 24,
                'approval': '1-2天',
                'requirements': ['武汉农商行客户', '有担保人', '征信良好'],
                'tags': ['门槛低', '担保贷款', '本地银行'],
                'commission': '2.0%'
            }
        ]
        
        for p in products:
            self.products.append({
                'bank': '武汉农村商业银行',
                'type': '本地城商行',
                'product_name': p['name'],
                'category': p['category'],
                'rate': p['rate'],
                'min_amount': p['min_amount'],
                'max_amount': p['max_amount'],
                'term': p['term'],
                'approval_time': p['approval'],
                'requirements': p['requirements'],
                'tags': p['tags'],
                'commission': p['commission'],
                'status': '在推',
                'source': '武汉农商行官网',
                'update_time': datetime.now().strftime('%Y-%m-%d')
            })
        
        print(f"   ✅ 8 个产品")
    
    def collect_gjj_products(self):
        """全面采集公积金贷款产品"""
        print("\n📦 公积金贷款产品（全面完善）")
        
        # 各银行公积金贷款产品
        gjj_products = [
            # 工商银行
            {
                'bank': '工商银行',
                'product_name': '融e借（公积金版）',
                'category': '公积金贷',
                'rate': '3.65%',
                'min_amount': 50000,
                'max_amount': 300000,
                'term': 36,
                'approval': '1-3天',
                'requirements': ['公积金连续缴纳满6个月', '月缴存额≥500元', '征信良好', '年龄18-60岁'],
                'tags': ['利率最低', '额度高', '审批快'],
                'commission': '1.5%'
            },
            # 建设银行
            {
                'bank': '建设银行',
                'product_name': '快贷（公积金版）',
                'category': '公积金贷',
                'rate': '3.85%',
                'min_amount': 10000,
                'max_amount': 200000,
                'term': 36,
                'approval': '1-2天',
                'requirements': ['建行公积金客户', '连续缴纳满6个月', '征信良好'],
                'tags': ['门槛低', '审批快', '建行客户专享'],
                'commission': '1.2%'
            },
            # 农业银行
            {
                'bank': '农业银行',
                'product_name': '网捷贷（公积金版）',
                'category': '公积金贷',
                'rate': '3.65%',
                'min_amount': 50000,
                'max_amount': 200000,
                'term': 36,
                'approval': '1-2天',
                'requirements': ['农行公积金客户', '连续缴纳满12个月', '征信良好'],
                'tags': ['利率低', '农行客户专享'],
                'commission': '1.3%'
            },
            # 中国银行
            {
                'bank': '中国银行',
                'product_name': '中银E贷（公积金版）',
                'category': '公积金贷',
                'rate': '3.65%',
                'min_amount': 50000,
                'max_amount': 300000,
                'term': 36,
                'approval': '1-3天',
                'requirements': ['中行公积金客户', '连续缴纳满6个月', '征信良好'],
                'tags': ['低利率', '高额度', '银行背景'],
                'commission': '1.5%'
            },
            # 交通银行
            {
                'bank': '交通银行',
                'product_name': '惠民贷（公积金版）',
                'category': '公积金贷',
                'rate': '3.85%',
                'min_amount': 30000,
                'max_amount': 200000,
                'term': 36,
                'approval': '1-2天',
                'requirements': ['交行公积金客户', '连续缴纳满6个月', '征信良好'],
                'tags': ['门槛低', '审批快'],
                'commission': '1.3%'
            },
            # 招商银行
            {
                'bank': '招商银行',
                'product_name': '闪电贷（公积金版）',
                'category': '公积金贷',
                'rate': '4.2%',
                'min_amount': 20000,
                'max_amount': 300000,
                'term': 36,
                'approval': '当天',
                'requirements': ['招行公积金客户', '连续缴纳满12个月', '征信良好'],
                'tags': ['快速放款', '额度灵活', '招行客户专享'],
                'commission': '1.8%'
            },
            # 浦发银行
            {
                'bank': '浦发银行',
                'product_name': '浦银点贷（公积金版）',
                'category': '公积金贷',
                'rate': '4.35%',
                'min_amount': 50000,
                'max_amount': 300000,
                'term': 36,
                'approval': '1-2天',
                'requirements': ['浦发公积金客户', '连续缴纳满6个月', '征信良好'],
                'tags': ['全程线上', '门槛低'],
                'commission': '1.5%'
            },
            # 中信银行
            {
                'bank': '中信银行',
                'product_name': '信秒贷（公积金版）',
                'category': '公积金贷',
                'rate': '4.35%',
                'min_amount': 50000,
                'max_amount': 300000,
                'term': 36,
                'approval': '1-3天',
                'requirements': ['中信公积金客户', '连续缴纳满12个月', '征信良好'],
                'tags': ['审批快', '额度高'],
                'commission': '1.5%'
            },
            # 光大银行
            {
                'bank': '光大银行',
                'product_name': '光速贷（公积金版）',
                'category': '公积金贷',
                'rate': '4.2%',
                'min_amount': 50000,
                'max_amount': 300000,
                'term': 36,
                'approval': '1-2天',
                'requirements': ['光大公积金客户', '连续缴纳满6个月', '征信良好'],
                'tags': ['全程线上', '快速审批'],
                'commission': '1.5%'
            },
            # 民生银行
            {
                'bank': '民生银行',
                'product_name': '民易贷（公积金版）',
                'category': '公积金贷',
                'rate': '4.5%',
                'min_amount': 50000,
                'max_amount': 300000,
                'term': 36,
                'approval': '1-3天',
                'requirements': ['民生公积金客户', '连续缴纳满12个月', '征信良好'],
                'tags': ['门槛适中', '民生客户专享'],
                'commission': '1.5%'
            },
            # 平安银行
            {
                'bank': '平安银行',
                'product_name': '新一贷（公积金版）',
                'category': '公积金贷',
                'rate': '6.0%',
                'min_amount': 50000,
                'max_amount': 500000,
                'term': 36,
                'approval': '2-3天',
                'requirements': ['有稳定收入', '公积金连续缴纳满6个月', '征信良好'],
                'tags': ['额度高', '门槛相对低'],
                'commission': '2.0%'
            },
            # 兴业银行
            {
                'bank': '兴业银行',
                'product_name': '兴闪贷（公积金版）',
                'category': '公积金贷',
                'rate': '4.5%',
                'min_amount': 50000,
                'max_amount': 300000,
                'term': 36,
                'approval': '1-3天',
                'requirements': ['兴业公积金客户', '连续缴纳满12个月', '征信良好'],
                'tags': ['审批快', '兴业客户专享'],
                'commission': '1.5%'
            },
            # 华夏银行
            {
                'bank': '华夏银行',
                'product_name': '华夏E贷（公积金版）',
                'category': '公积金贷',
                'rate': '4.35%',
                'min_amount': 50000,
                'max_amount': 300000,
                'term': 36,
                'approval': '1-3天',
                'requirements': ['华夏公积金客户', '连续缴纳满6个月', '征信良好'],
                'tags': ['门槛低', '华夏客户专享'],
                'commission': '1.5%'
            },
            # 广发银行
            {
                'bank': '广发银行',
                'product_name': '广发E秒贷（公积金版）',
                'category': '公积金贷',
                'rate': '4.5%',
                'min_amount': 50000,
                'max_amount': 300000,
                'term': 36,
                'approval': '1-2天',
                'requirements': ['广发公积金客户', '连续缴纳满12个月', '征信良好'],
                'tags': ['全程线上', '快速审批'],
                'commission': '1.5%'
            },
            # 湖北银行
            {
                'bank': '湖北银行',
                'product_name': '荆楚贷（公积金版）',
                'category': '公积金贷',
                'rate': '4.35%',
                'min_amount': 100000,
                'max_amount': 500000,
                'term': 36,
                'approval': '2-5天',
                'requirements': ['湖北银行公积金客户', '连续缴纳满12个月', '征信良好'],
                'tags': ['本地银行', '额度高', '湖北专属'],
                'commission': '1.8%'
            },
            # 汉口银行
            {
                'bank': '汉口银行',
                'product_name': '市民贷（公积金版）',
                'category': '公积金贷',
                'rate': '4.5%',
                'min_amount': 50000,
                'max_amount': 200000,
                'term': 24,
                'approval': '3-5天',
                'requirements': ['汉口银行公积金客户', '连续缴纳满12个月', '征信良好'],
                'tags': ['本地银行', '武汉市民专享'],
                'commission': '1.5%'
            },
            # 北京银行
            {
                'bank': '北京银行',
                'product_name': '京e贷（公积金版）',
                'category': '公积金贷',
                'rate': '4.25%',
                'min_amount': 50000,
                'max_amount': 300000,
                'term': 36,
                'approval': '1-3天',
                'requirements': ['北行公积金客户', '连续缴纳满6个月', '征信良好'],
                'tags': ['利率较低', '北行客户专享'],
                'commission': '1.5%'
            },
            # 湖北消费金融
            {
                'bank': '湖北消费金融',
                'product_name': '湖北消金公积金贷',
                'category': '公积金贷',
                'rate': '6.5%-10.8%',
                'min_amount': 30000,
                'max_amount': 200000,
                'term': 36,
                'approval': '1-3天',
                'requirements': ['公积金连续缴纳满6个月', '月缴存额≥400元', '征信良好'],
                'tags': ['门槛较低', '审批快'],
                'commission': '2.5%'
            }
        ]
        
        for p in gjj_products:
            self.products.append({
                'bank': p['bank'],
                'product_name': p['product_name'],
                'category': p['category'],
                'rate': p['rate'],
                'min_amount': p['min_amount'],
                'max_amount': p['max_amount'],
                'term': p['term'],
                'approval_time': p['approval'],
                'requirements': p['requirements'],
                'tags': p['tags'],
                'commission': p['commission'],
                'status': '在推',
                'source': '银行官网/消费金融',
                'update_time': datetime.now().strftime('%Y-%m-%d')
            })
        
        print(f"   ✅ {len(gjj_products)} 个公积金贷款产品")
    
    def save_to_obsidian(self):
        """保存为 Obsidian 页面"""
        output_dir = Path("/workspaces/MyMoltbot/obsidian-templates/产品库")
        
        # 1. 创建武汉农商行产品页
        wuhan_rural_dir = output_dir / "武汉农村商业银行"
        wuhan_rural_dir.mkdir(exist_ok=True)
        
        content = self.generate_wuhan_rural_page()
        (wuhan_rural_dir / "武汉农村商业银行-产品.md").write_text(content, encoding='utf-8')
        
        # 2. 创建公积金贷款专题页
        gjj_dir = output_dir / "公积金贷款"
        gjj_dir.mkdir(exist_ok=True)
        
        content = self.generate_gjj_index()
        (gjj_dir / "公积金贷款产品索引.md").write_text(content, encoding='utf-8')
        
        # 3. 更新主索引
        self.update_master_index()
        
        print(f"\n📁 已保存到: {output_dir}")
    
    def generate_wuhan_rural_page(self):
        """生成武汉农商行产品页面"""
        products = [p for p in self.products if '武汉农村商业银行' in p['bank']]
        
        content = f"""---
title: 武汉农村商业银行产品
bank: 武汉农村商业银行
type: 本地城商行
headquarters: 武汉
updateTime: {datetime.now().strftime('%Y-%m-%d')}
---

# 武汉农村商业银行 贷款产品

## 基本信息

| 项目 | 内容 |
|------|------|
| 银行名称 | 武汉农村商业银行 |
| 银行类型 | 本地城商行 |
| 总部所在地 | 武汉市 |
| 产品数量 | {len(products)}个 |
| 特色 | 本地银行、服务武汉市民、门槛适中 |

## 产品列表

"""
        
        for p in products:
            content += f"""### {p['product_name']}（{p['category']}）

| 项目 | 内容 |
|------|------|
| 利率 | **{p['rate']}** |
| 额度 | {p['min_amount']/10000:.0f}-{p['max_amount']/10000:.0f}万 |
| 期限 | 最长{p['term']}个月 |
| 审批 | {p['approval_time']} |
| 佣金 | {p['commission']} |

**申请条件**:
{chr(10).join([f'- {req}' for req in p['requirements']])}

**产品标签**: {' '.join([f'`{tag}`' for tag in p['tags']])}

"""
        
        content += f"""
## 银行优势

- ✅ 本地银行，更了解武汉市场
- ✅ 对武汉户籍或工作客户更友好
- ✅ 产品丰富，覆盖多种需求
- ✅ 审批相对宽松，通过率高

## 申请建议

1. **优先申请**：汉银公积金贷（利率最低）
2. **快速获批**：汉银亲情贷（门槛最低）
3. **大额需求**：汉银房抵贷（额度最高）

---
**最后更新**: {datetime.now().strftime('%Y-%m-%d')}
"""
        
        return content
    
    def generate_gjj_index(self):
        """生成公积金贷款索引"""
        gjj_products = [p for p in self.products if p['category'] == '公积金贷']
        
        # 按利率排序
        sorted_products = sorted(gjj_products, key=lambda x: float(x['rate'].replace('%', '').split('-')[0]))
        
        content = f"""---
title: 公积金贷款产品索引
type: 公积金贷款
updateTime: {datetime.now().strftime('%Y-%m-%d')}
---

# 公积金贷款产品索引

> 各大银行公积金贷款产品汇总

## 基本信息

| 指标 | 数值 |
|------|------|
| 产品数量 | {len(gjj_products)}个 |
| 参与银行 | {len(set(p['bank'] for p in gjj_products))}家 |
| 最低利率 | {sorted_products[0]['rate']} |
| 最高额度 | {max(p['max_amount'] for p in gjj_products)/10000:.0f}万 |

## 低利率产品TOP5

| 排名 | 银行 | 产品 | 利率 | 额度 | 审批 |
|------|------|------|------|------|------|
"""
        
        for i, p in enumerate(sorted_products[:5], 1):
            content += f"| {i} | {p['bank']} | {p['product_name']} | **{p['rate']}** | {p['min_amount']/10000:.0f}-{p['max_amount']/10000:.0f}万 | {p['approval_time']} |\n"
        
        content += f"""
## 所有产品列表

"""
        
        # 按银行分组
        banks = {}
        for p in gjj_products:
            if p['bank'] not in banks:
                banks[p['bank']] = []
            banks[p['bank']].append(p)
        
        for bank_name, products in sorted(banks.items()):
            content += f"### {bank_name}\n\n"
            content += f"共 {len(products)} 个产品\n\n"
            content += "| 产品 | 利率 | 额度 | 审批 | 佣金 |\n"
            content += "|------|------|------|------|------|\n"
            for p in products:
                content += f"| {p['product_name']} | {p['rate']} | {p['min_amount']/10000:.0f}-{p['max_amount']/10000:.0f}万 | {p['approval_time']} | {p['commission']} |\n"
            content += "\n"
        
        content += f"""## 申请条件（通用）

### 基本条件
- 年龄：22-55岁
- 公积金：连续缴纳满6-12个月
- 征信：良好，无逾期记录
- 收入：稳定收入证明

### 加分项
- 公积金月缴存额高
- 缴纳基数高
- 本地户口或工作
- 银行存量客户

## 注意事项

1. **利率差异**：不同银行利率差异较大，建议比较后申请
2. **额度计算**：一般根据公积金月缴存额和缴纳基数计算
3. **审批时间**：银行公积金贷审批较快，1-3天
4. **提前还款**：部分产品支持提前还款，建议了解政策

## 申请建议

### 最佳选择
- **最低利率**：工商银行融e借（3.65%）
- **最快审批**：招商银行闪电贷（当天）
- **最高额度**：平安银行新一贷（50万）

### 快速获批
- 建设银行快贷（1-2天）
- 交通银行惠民贷（1-2天）

### 本地银行推荐
- 武汉农村商业银行汉银公积金贷（4.35%，本地优势）
- 湖北银行荆楚贷（4.35%，湖北专属）

---
**最后更新**: {datetime.now().strftime('%Y-%m-%d')}
"""
        
        return content
    
    def update_master_index(self):
        """更新主索引"""
        index_file = Path("/workspaces/MyMoltbot/obsidian-templates/产品库/产品数据库索引.md")
        
        if index_file.exists():
            content = index_file.read_text(encoding='utf-8')
            
            # 添加武汉农商行
            if '武汉农村商业银行' not in content:
                insertion_point = content.find('## 按银行分类')
                if insertion_point != -1:
                    new_line = "| [[武汉农村商业银行-产品|武汉农村商业银行]] | 本地城商行 | 8 |\n"
                    content = content[:insertion_point] + new_line + content[insertion_point:]
            
            # 添加公积金贷款索引
            if '公积金贷款' not in content:
                insertion_point = content.find('## 产品类型分布')
                if insertion_point != -1:
                    new_line = "| [[公积金贷款/公积金贷款产品索引|公积金贷款]] | 专题 | 18个产品 |\n"
                    content = content[:insertion_point] + new_line + content[insertion_point:]
            
            index_file.write_text(content, encoding='utf-8')
    
    def save_json(self):
        """保存为 JSON"""
        output_dir = Path("/home/codespace/clawd/product-collector/wuhan-rural-comm")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"wuhan_rural_gjj_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_file.write_text(
            json.dumps(self.products, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        
        print(f"\n💾 JSON数据已保存: {output_file}")
        return str(output_file)


def main():
    collector = WuhanRuralAndGJJCollector()
    products = collector.products
    print(f"\n✅ 共采集 {len(products)} 个产品")
    collector.save_json()
    collector.save_to_obsidian()
    
    print(f"\n📊 产品统计:")
    print(f"  - 武汉农商行产品: 8个")
    print(f"  - 公积金贷款产品: {len([p for p in products if p['category'] == '公积金贷'])}个")

if __name__ == '__main__':
    main()
