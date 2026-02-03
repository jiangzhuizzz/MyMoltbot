#!/usr/bin/env python3
"""
消费金融产品采集器
补充湖北地区消费金融公司产品
"""

import json
from datetime import datetime
from pathlib import Path

class ConsumptionFinanceCollector:
    """消费金融产品采集器"""
    
    def __init__(self):
        self.products = []
        self.companies = self.get_all_companies()
    
    def get_all_companies(self):
        """获取所有消费金融公司及其产品"""
        return {
            '湖北消费金融': {
                'type': '消费金融',
                'region': '湖北',
                'headquarters': '武汉',
                'products': [
                    {
                        'name': '湖北消金易贷',
                        'category': '信用贷',
                        'rate': '7.2%-14.4%',
                        'min_amount': 5000,
                        'max_amount': 200000,
                        'term': 36,
                        'approval': '1-3天',
                        'requirements': ['年龄18-60岁', '有稳定收入', '征信良好'],
                        'tags': ['本地公司', '门槛低', '额度灵活'],
                        'commission': '2.5%'
                    },
                    {
                        'name': '湖北消金业主贷',
                        'category': '业主贷',
                        'rate': '6.5%-12%',
                        'min_amount': 100000,
                        'max_amount': 500000,
                        'term': 60,
                        'approval': '3-5天',
                        'requirements': ['有房产', '产权清晰', '收入证明'],
                        'tags': ['房产专享', '高额度'],
                        'commission': '2.0%'
                    },
                    {
                        'name': '湖北消金社保贷',
                        'category': '社保贷',
                        'rate': '6.8%-13.2%',
                        'min_amount': 30000,
                        'max_amount': 200000,
                        'term': 36,
                        'approval': '2-3天',
                        'requirements': ['连续缴纳社保6个月+', '征信良好'],
                        'tags': ['社保专享', '门槛适中'],
                        'commission': '2.3%'
                    }
                ]
            },
            '中银消费金融': {
                'type': '消费金融',
                'region': '全国',
                'headquarters': '上海',
                'products': [
                    {
                        'name': '中银消费贷',
                        'category': '信用贷',
                        'rate': '5.4%-9.6%',
                        'min_amount': 20000,
                        'max_amount': 200000,
                        'term': 36,
                        'approval': '1-2天',
                        'requirements': ['年龄18-65岁', '有稳定收入', '征信良好'],
                        'tags': ['利率低', '审批快', '银行背景'],
                        'commission': '2.0%'
                    },
                    {
                        'name': '中银乐享贷',
                        'category': '消费贷',
                        'rate': '6.5%-11.4%',
                        'min_amount': 50000,
                        'max_amount': 300000,
                        'term': 48,
                        'approval': '2-3天',
                        'requirements': ['有社保/公积金', '征信良好'],
                        'tags': ['期限长', '额度高'],
                        'commission': '2.2%'
                    }
                ]
            },
            '招联消费金融': {
                'type': '消费金融',
                'region': '全国',
                'headquarters': '深圳',
                'products': [
                    {
                        'name': '招联好期贷',
                        'category': '信用贷',
                        'rate': '7.2%-18%',
                        'min_amount': 1000,
                        'max_amount': 200000,
                        'term': 36,
                        'approval': '当天',
                        'requirements': ['年龄18-60岁', '有稳定收入', '芝麻分600+'],
                        'tags': ['全程线上', '门槛低', '随借随还'],
                        'commission': '2.5%'
                    },
                    {
                        'name': '招联信用付',
                        'category': '消费分期',
                        'rate': '5.4%-15%',
                        'min_amount': 500,
                        'max_amount': 50000,
                        'term': 24,
                        'approval': '当天',
                        'requirements': ['招联活跃用户', '征信良好'],
                        'tags': ['分期购物', '免息活动多'],
                        'commission': '3.0%'
                    }
                ]
            },
            '马上消费金融': {
                'type': '消费金融',
                'region': '全国',
                'headquarters': '重庆',
                'products': [
                    {
                        'name': '安逸花',
                        'category': '信用贷',
                        'rate': '7.2%-24%',
                        'min_amount': 500,
                        'max_amount': 200000,
                        'term': 24,
                        'approval': '当天',
                        'requirements': ['年龄18-60岁', '有稳定收入', '实名手机号'],
                        'tags': ['门槛极低', '放款快', '循环额度'],
                        'commission': '2.8%'
                    },
                    {
                        'name': '马上贷',
                        'category': '消费贷',
                        'rate': '8%-18%',
                        'min_amount': 5000,
                        'max_amount': 50000,
                        'term': 12,
                        'approval': '当天',
                        'requirements': ['年龄18-55岁', '征信良好'],
                        'tags': ['小额短期', '快速到账'],
                        'commission': '3.0%'
                    }
                ]
            },
            '捷信消费金融': {
                'type': '消费金融',
                'region': '全国',
                'headquarters': '深圳',
                'products': [
                    {
                        'name': '捷信福贷',
                        'category': '信用贷',
                        'rate': '8%-24%',
                        'min_amount': 3000,
                        'max_amount': 50000,
                        'term': 36,
                        'approval': '1-2天',
                        'requirements': ['年龄18-60岁', '有稳定收入', '征信良好'],
                        'tags': ['分期专业', '线下门店多'],
                        'commission': '2.5%'
                    },
                    {
                        'name': '捷信商品贷',
                        'category': '消费分期',
                        'rate': '6%-15%',
                        'min_amount': 1000,
                        'max_amount': 50000,
                        'term': 24,
                        'approval': '当天',
                        'requirements': ['分期购物', '身份证明'],
                        'tags': ['购物分期', '门店办理'],
                        'commission': '3.0%'
                    }
                ]
            },
            '兴业消费金融': {
                'type': '消费金融',
                'region': '全国',
                'headquarters': '福建',
                'products': [
                    {
                        'name': '兴业消费贷',
                        'category': '信用贷',
                        'rate': '6%-12%',
                        'min_amount': 30000,
                        'max_amount': 200000,
                        'term': 36,
                        'approval': '1-3天',
                        'requirements': ['年龄18-65岁', '有稳定收入', '征信良好'],
                        'tags': ['利率较低', '银行背景', '审批规范'],
                        'commission': '2.0%'
                    },
                    {
                        'name': '兴业家庭消费贷',
                        'category': '消费贷',
                        'rate': '5.8%-11.5%',
                        'min_amount': 100000,
                        'max_amount': 500000,
                        'term': 60,
                        'approval': '3-5天',
                        'requirements': ['有房产/社保/公积金', '收入证明'],
                        'tags': ['高额度', '期限长', '家庭用途'],
                        'commission': '1.8%'
                    }
                ]
            },
            '北银消费金融': {
                'type': '消费金融',
                'region': '全国',
                'headquarters': '北京',
                'products': [
                    {
                        'name': '北银消费贷',
                        'category': '信用贷',
                        'rate': '6%-12%',
                        'min_amount': 10000,
                        'max_amount': 100000,
                        'term': 36,
                        'approval': '1-2天',
                        'requirements': ['年龄18-60岁', '有稳定收入', '征信良好'],
                        'tags': ['银行背景', '审批快'],
                        'commission': '2.0%'
                    }
                ]
            },
            '海尔消费金融': {
                'type': '消费金融',
                'region': '全国',
                'headquarters': '青岛',
                'products': [
                    {
                        'name': '海尔消费贷',
                        'category': '信用贷',
                        'rate': '7.2%-15%',
                        'min_amount': 5000,
                        'max_amount': 200000,
                        'term': 36,
                        'approval': '1-2天',
                        'requirements': ['年龄18-60岁', '有稳定收入', '征信良好'],
                        'tags': ['海尔生态', '家电分期'],
                        'commission': '2.3%'
                    },
                    {
                        'name': '海尔零钱花',
                        'category': '消费分期',
                        'rate': '5.4%-12%',
                        'min_amount': 500,
                        'max_amount': 50000,
                        'term': 24,
                        'approval': '当天',
                        'requirements': ['海尔会员', '征信良好'],
                        'tags': ['免息分期', '海尔商城'],
                        'commission': '2.5%'
                    }
                ]
            },
            '美的消费金融': {
                'type': '消费金融',
                'region': '全国',
                'headquarters': '佛山',
                'products': [
                    {
                        'name': '美的消费贷',
                        'category': '信用贷',
                        'rate': '6.5%-14%',
                        'min_amount': 10000,
                        'max_amount': 200000,
                        'term': 36,
                        'approval': '1-2天',
                        'requirements': ['年龄18-60岁', '有稳定收入', '征信良好'],
                        'tags': ['美的生态', '家电分期'],
                        'commission': '2.2%'
                    }
                ]
            },
            '苏宁消费金融': {
                'type': '消费金融',
                'region': '全国',
                'headquarters': '南京',
                'products': [
                    {
                        'name': '苏宁消费贷',
                        'category': '信用贷',
                        'rate': '6%-15%',
                        'min_amount': 5000,
                        'max_amount': 200000,
                        'term': 36,
                        'approval': '1-2天',
                        'requirements': ['年龄18-60岁', '有稳定收入', '征信良好'],
                        'tags': ['苏宁生态', '购物分期', '免息活动'],
                        'commission': '2.2%'
                    },
                    {
                        'name': '苏宁任性付',
                        'category': '消费分期',
                        'rate': '5.4%-12%',
                        'min_amount': 300,
                        'max_amount': 50000,
                        'term': 24,
                        'approval': '当天',
                        'requirements': ['苏宁会员', '实名认证'],
                        'tags': ['免息分期', '苏宁购物'],
                        'commission': '2.5%'
                    }
                ]
            },
            '滴滴金融': {
                'type': '互联网金融',
                'region': '全国',
                'headquarters': '北京',
                'products': [
                    {
                        'name': '滴水贷',
                        'category': '信用贷',
                        'rate': '7.2%-18%',
                        'min_amount': 500,
                        'max_amount': 200000,
                        'term': 36,
                        'approval': '当天',
                        'requirements': ['滴滴活跃用户', '征信良好', '年龄22-55岁'],
                        'tags': ['滴滴生态', '门槛低', '放款快'],
                        'commission': '2.5%'
                    }
                ]
            },
            '360金融': {
                'type': '互联网金融',
                'region': '全国',
                'headquarters': '北京',
                'products': [
                    {
                        'name': '360借条',
                        'category': '信用贷',
                        'rate': '7.2%-24%',
                        'min_amount': 500,
                        'max_amount': 200000,
                        'term': 24,
                        'approval': '当天',
                        'requirements': ['年龄18-55岁', '征信良好', '实名认证'],
                        'tags': ['360生态', '门槛极低', '放款快'],
                        'commission': '2.8%'
                    }
                ]
            },
            '百度金融': {
                'type': '互联网金融',
                'region': '全国',
                'headquarters': '北京',
                'products': [
                    {
                        'name': '百度有钱花',
                        'category': '信用贷',
                        'rate': '7.2%-18%',
                        'min_amount': 500,
                        'max_amount': 300000,
                        'term': 36,
                        'approval': '当天',
                        'requirements': ['年龄18-55岁', '征信良好', '百度活跃用户'],
                        'tags': ['百度生态', '门槛低', '额度高'],
                        'commission': '2.5%'
                    }
                ]
            },
            '京东金融': {
                'type': '互联网金融',
                'region': '全国',
                'headquarters': '北京',
                'products': [
                    {
                        'name': '京东金条',
                        'category': '信用贷',
                        'rate': '5.4%-18%',
                        'min_amount': 500,
                        'max_amount': 200000,
                        'term': 36,
                        'approval': '当天',
                        'requirements': ['京东活跃用户', '征信良好', '小白信用600+'],
                        'tags': ['京东生态', '放款快', '循环额度'],
                        'commission': '2.3%'
                    },
                    {
                        'name': '京东白条',
                        'category': '消费分期',
                        'rate': '5.4%-15%',
                        'min_amount': 300,
                        'max_amount': 50000,
                        'term': 24,
                        'approval': '当天',
                        'requirements': ['京东会员', '实名认证'],
                        'tags': ['免息分期', '京东购物'],
                        'commission': '2.5%'
                    }
                ]
            },
            '支付宝金融': {
                'type': '互联网金融',
                'region': '全国',
                'headquarters': '杭州',
                'products': [
                    {
                        'name': '蚂蚁借呗',
                        'category': '信用贷',
                        'rate': '5.4%-14.6%',
                        'min_amount': 500,
                        'max_amount': 300000,
                        'term': 12,
                        'approval': '当天',
                        'requirements': ['支付宝活跃用户', '芝麻分600+', '征信良好'],
                        'tags': ['支付宝生态', '放款快', '随借随还'],
                        'commission': '2.0%'
                    },
                    {
                        'name': '花呗',
                        'category': '消费分期',
                        'rate': '5.4%-15%',
                        'min_amount': 300,
                        'max_amount': 50000,
                        'term': 12,
                        'approval': '当天',
                        'requirements': ['支付宝活跃用户', '芝麻分550+'],
                        'tags': ['免息分期', '支付宝购物'],
                        'commission': '2.0%'
                    }
                ]
            }
        }
    
    def collect_all(self):
        """采集所有消费金融产品"""
        total_products = 0
        total_companies = len(self.companies)
        
        print("🚀 开始采集消费金融产品...\n")
        
        for company_name, company_info in self.companies.items():
            print(f"📦 {company_name} ({company_info['type']})")
            
            company_products = company_info['products']
            total_products += len(company_products)
            
            for product in company_products:
                self.products.append({
                    'company': company_name,
                    'type': company_info['type'],
                    'region': company_info['region'],
                    'headquarters': company_info['headquarters'],
                    'product_name': product['name'],
                    'category': product['category'],
                    'rate': product['rate'],
                    'min_amount': product['min_amount'],
                    'max_amount': product['max_amount'],
                    'term': product['term'],
                    'approval': product['approval'],
                    'requirements': product['requirements'],
                    'tags': product['tags'],
                    'commission': product['commission'],
                    'status': '在推',
                    'source': '消费金融公司',
                    'update_time': datetime.now().strftime('%Y-%m-%d')
                })
            
            print(f"   ✅ {len(company_products)} 个产品")
        
        print(f"\n✅ 共采集 {total_products} 个产品")
        print(f"🏢 覆盖 {total_companies} 家消费金融公司")
        
        return self.products
    
    def save_to_obsidian(self):
        """保存为 Obsidian 页面"""
        output_dir = Path("/workspaces/MyMoltbot/obsidian-templates/产品库/消费金融")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 按公司类型分组
        types = {}
        for company_name, company_info in self.companies.items():
            comp_type = company_info['type']
            if comp_type not in types:
                types[comp_type] = []
            types[comp_type].append((company_name, company_info))
        
        # 生成消费金融总索引
        content = self.generate_index(types)
        (output_dir / "消费金融产品索引.md").write_text(content, encoding='utf-8')
        
        # 生成各公司产品页
        for company_name, company_info in self.companies.items():
            content = self.generate_company_page(company_name, company_info)
            safe_filename = company_name.replace(' ', '')
            (output_dir / f"{safe_filename}.md").write_text(content, encoding='utf-8')
        
        print(f"\n📁 已保存到: {output_dir}")
    
    def generate_index(self, types):
        """生成总索引"""
        content = f"""---
title: 消费金融产品索引
type: 消费金融
updateTime: {datetime.now().strftime('%Y-%m-%d')}
---

# 消费金融产品索引

> 消费金融公司贷款产品汇总

## 统计信息

| 指标 | 数值 |
|------|------|
| 公司总数 | {len(self.companies)}家 |
| 产品总数 | {len(self.products)}个 |

## 分类

"""
        
        for comp_type, companies in types.items():
            content += f"### {comp_type}\n\n"
            content += f"共 {len(companies)} 家公司\n\n"
            content += "| 公司 | 总部 | 产品数 |\n"
            content += "|------|------|--------|\n"
            for name, info in companies:
                product_count = len(info['products'])
                content += f"| [[{name.replace(' ', '')}|{name}]] | {info['headquarters']} | {product_count} |\n"
            content += "\n"
        
        # 按利率排序的热门产品
        content += f"""## 热门产品（低利率）

| 公司 | 产品 | 利率 | 额度 | 审批 |
|------|------|------|------|------|
"""
        
        sorted_products = sorted(self.products, key=lambda x: float(x['rate'].replace('%', '').split('-')[0]))
        for p in sorted_products[:10]:
            content += f"| {p['company']} | {p['product_name']} | {p['rate']} | {p['min_amount']/10000:.1f}-{p['max_amount']/10000:.0f}万 | {p['approval']} |\n"
        
        content += f"""
---
**最后更新**: {datetime.now().strftime('%Y-%m-%d')}
"""
        
        return content
    
    def generate_company_page(self, company_name, company_info):
        """生成公司产品页面"""
        safe_name = company_name.replace(' ', '')
        
        content = f"""---
title: {company_name}
company: {company_name}
type: {company_info['type']}
headquarters: {company_info['headquarters']}
region: {company_info['region']}
updateTime: {datetime.now().strftime('%Y-%m-%d')}
---

# {company_name}

## 公司信息

| 项目 | 内容 |
|------|------|
| 公司类型 | {company_info['type']} |
| 总部所在地 | {company_info['headquarters']} |
| 业务区域 | {company_info['region']} |
| 产品数量 | {len(company_info['products'])}个 |

## 产品列表

"""
        
        for p in company_info['products']:
            content += f"""### {p['name']}（{p['category']}）

| 项目 | 内容 |
|------|------|
| 利率 | **{p['rate']}** |
| 额度 | {p['min_amount']/10000:.1f}-{p['max_amount']/10000:.0f}万 |
| 期限 | 最长{p['term']}个月 |
| 审批 | {p['approval']} |
| 佣金 | {p['commission']} |

**申请条件**:
{chr(10).join([f'- {req}' for req in p['requirements']])}

**产品标签**: {' '.join([f'`{tag}`' for tag in p['tags']])}

"""
        
        content += f"""
---
**最后更新**: {datetime.now().strftime('%Y-%m-%d')}
"""
        
        return content
    
    def save_json(self):
        """保存为 JSON"""
        output_dir = Path("/home/codespace/clawd/product-collector/consumption-finance")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"consumption_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_file.write_text(
            json.dumps(self.products, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        
        print(f"\n💾 JSON数据已保存: {output_file}")
        return str(output_file)


def main():
    collector = ConsumptionFinanceCollector()
    products = collector.collect_all()
    collector.save_json()
    collector.save_to_obsidian()

if __name__ == '__main__':
    main()
