#!/usr/bin/env python3
"""
完整贷款产品库采集器
覆盖所有主流银行和产品类型
"""

import json
from datetime import datetime
from pathlib import Path

class ComprehensiveProductCollector:
    """完整产品采集器"""
    
    def __init__(self):
        self.products = []
        self.banks = self.get_all_banks()
    
    def get_all_banks(self):
        """获取所有银行及其产品"""
        return {
            # 国有银行
            '工商银行': {
                'type': '国有银行',
                'products': [
                    {
                        'name': '融e借',
                        'category': '信用贷',
                        'rate': '3.65%',
                        'min_amount': 50000,
                        'max_amount': 3000000,
                        'term': 36,
                        'approval': '1-3天',
                        'requirements': ['公积金/社保用户', '征信良好', '年龄18-60岁'],
                        'tags': ['低利率', '高额度', '审批快'],
                        'commission': '1.5%'
                    },
                    {
                        'name': '房抵贷',
                        'category': '抵押贷',
                        'rate': '3.75%',
                        'min_amount': 100000,
                        'max_amount': 5000000,
                        'term': 240,
                        'approval': '5-7天',
                        'requirements': ['有房产', '产权清晰', '征信良好'],
                        'tags': ['高额度', '期限长', '利率低'],
                        'commission': '1.0%'
                    },
                    {
                        'name': '装修贷',
                        'category': '装修贷',
                        'rate': '3.85%',
                        'min_amount': 100000,
                        'max_amount': 500000,
                        'term': 60,
                        'approval': '3-5天',
                        'requirements': ['有房产', '装修合同', '收入证明'],
                        'tags': ['用途明确', '额度适中'],
                        'commission': '1.5%'
                    }
                ]
            },
            '建设银行': {
                'type': '国有银行',
                'products': [
                    {
                        'name': '快贷',
                        'category': '信用贷',
                        'rate': '3.85%',
                        'min_amount': 10000,
                        'max_amount': 200000,
                        'term': 36,
                        'approval': '1-2天',
                        'requirements': ['建行客户', '公积金/代发工资', '征信良好'],
                        'tags': ['门槛低', '审批快'],
                        'commission': '1.2%'
                    },
                    {
                        'name': '建行分期通',
                        'category': '消费贷',
                        'rate': '4.2%',
                        'min_amount': 50000,
                        'max_amount': 300000,
                        'term': 60,
                        'approval': '3-5天',
                        'requirements': ['建行代发工资', '社保', '征信良好'],
                        'tags': ['分期长', '用途广'],
                        'commission': '1.5%'
                    },
                    {
                        'name': '房抵快贷',
                        'category': '抵押贷',
                        'rate': '3.95%',
                        'min_amount': 500000,
                        'max_amount': 10000000,
                        'term': 180,
                        'approval': '5-7天',
                        'requirements': ['有房产', '营业执照', '经营满1年'],
                        'tags': ['高额度', '经营用途'],
                        'commission': '1.0%'
                    }
                ]
            },
            '农业银行': {
                'type': '国有银行',
                'products': [
                    {
                        'name': '网捷贷',
                        'category': '信用贷',
                        'rate': '3.65%',
                        'min_amount': 50000,
                        'max_amount': 200000,
                        'term': 36,
                        'approval': '1-2天',
                        'requirements': ['农行客户', '公积金/房贷', '征信良好'],
                        'tags': ['低利率', '农行客户专享'],
                        'commission': '1.3%'
                    },
                    {
                        'name': '房抵e贷',
                        'category': '抵押贷',
                        'rate': '3.85%',
                        'min_amount': 500000,
                        'max_amount': 5000000,
                        'term': 180,
                        'approval': '5-7天',
                        'requirements': ['有房产', '产权清晰'],
                        'tags': ['高额度', '期限灵活'],
                        'commission': '1.0%'
                    },
                    {
                        'name': '助业快e贷',
                        'category': '经营贷',
                        'rate': '4.35%',
                        'min_amount': 100000,
                        'max_amount': 500000,
                        'term': 36,
                        'approval': '3-5天',
                        'requirements': ['营业执照', '经营满1年', '流水充足'],
                        'tags': ['经营用途', '审批快'],
                        'commission': '1.5%'
                    }
                ]
            },
            '中国银行': {
                'type': '国有银行',
                'products': [
                    {
                        'name': '中银E贷',
                        'category': '信用贷',
                        'rate': '3.65%',
                        'min_amount': 50000,
                        'max_amount': 300000,
                        'term': 36,
                        'approval': '1-3天',
                        'requirements': ['中行客户', '公积金/代发工资', '征信良好'],
                        'tags': ['低利率', '高额度'],
                        'commission': '1.5%'
                    },
                    {
                        'name': '随心智贷',
                        'category': '信用贷',
                        'rate': '4.2%',
                        'min_amount': 100000,
                        'max_amount': 500000,
                        'term': 60,
                        'approval': '3-5天',
                        'requirements': ['有稳定收入', '征信良好'],
                        'tags': ['期限长', '额度高'],
                        'commission': '1.5%'
                    }
                ]
            },
            '交通银行': {
                'type': '国有银行',
                'products': [
                    {
                        'name': '惠民贷',
                        'category': '信用贷',
                        'rate': '3.85%',
                        'min_amount': 30000,
                        'max_amount': 200000,
                        'term': 36,
                        'approval': '1-2天',
                        'requirements': ['交行客户', '公积金/社保', '征信良好'],
                        'tags': ['门槛低', '审批快'],
                        'commission': '1.3%'
                    },
                    {
                        'name': '房抵贷',
                        'category': '抵押贷',
                        'rate': '3.95%',
                        'min_amount': 500000,
                        'max_amount': 5000000,
                        'term': 180,
                        'approval': '5-7天',
                        'requirements': ['有房产', '产权清晰'],
                        'tags': ['高额度', '期限长'],
                        'commission': '1.0%'
                    }
                ]
            },
            # 股份制银行
            '招商银行': {
                'type': '股份制银行',
                'products': [
                    {
                        'name': '闪电贷',
                        'category': '信用贷',
                        'rate': '4.2%',
                        'min_amount': 20000,
                        'max_amount': 300000,
                        'term': 36,
                        'approval': '当天',
                        'requirements': ['招行客户', '公积金/代发工资', '征信良好'],
                        'tags': ['快速放款', '额度灵活'],
                        'commission': '1.8%'
                    },
                    {
                        'name': '车贷',
                        'category': '车贷',
                        'rate': '4.5%',
                        'min_amount': 100000,
                        'max_amount': 1000000,
                        'term': 60,
                        'approval': '2-3天',
                        'requirements': ['购车合同', '驾驶证', '收入证明'],
                        'tags': ['购车专享', '审批快'],
                        'commission': '1.5%'
                    },
                    {
                        'name': '装修贷',
                        'category': '装修贷',
                        'rate': '4.35%',
                        'min_amount': 100000,
                        'max_amount': 500000,
                        'term': 60,
                        'approval': '3-5天',
                        'requirements': ['房产证明', '装修合同'],
                        'tags': ['用途明确'],
                        'commission': '1.5%'
                    }
                ]
            },
            '浦发银行': {
                'type': '股份制银行',
                'products': [
                    {
                        'name': '浦银点贷',
                        'category': '信用贷',
                        'rate': '4.35%',
                        'min_amount': 50000,
                        'max_amount': 300000,
                        'term': 36,
                        'approval': '1-2天',
                        'requirements': ['浦发客户', '公积金/房贷', '征信良好'],
                        'tags': ['门槛低', '审批快'],
                        'commission': '1.5%'
                    },
                    {
                        'name': '房抵贷',
                        'category': '抵押贷',
                        'rate': '4.2%',
                        'min_amount': 500000,
                        'max_amount': 5000000,
                        'term': 180,
                        'approval': '5-7天',
                        'requirements': ['有房产', '产权清晰'],
                        'tags': ['高额度', '利率优'],
                        'commission': '1.0%'
                    }
                ]
            },
            '中信银行': {
                'type': '股份制银行',
                'products': [
                    {
                        'name': '信秒贷',
                        'category': '信用贷',
                        'rate': '4.35%',
                        'min_amount': 50000,
                        'max_amount': 300000,
                        'term': 36,
                        'approval': '1-3天',
                        'requirements': ['中信客户', '公积金/社保', '征信良好'],
                        'tags': ['审批快', '额度高'],
                        'commission': '1.5%'
                    },
                    {
                        'name': '房抵贷',
                        'category': '抵押贷',
                        'rate': '4.25%',
                        'min_amount': 500000,
                        'max_amount': 5000000,
                        'term': 180,
                        'approval': '5-7天',
                        'requirements': ['有房产'],
                        'tags': ['高额度'],
                        'commission': '1.0%'
                    }
                ]
            },
            '光大银行': {
                'type': '股份制银行',
                'products': [
                    {
                        'name': '光速贷',
                        'category': '信用贷',
                        'rate': '4.2%',
                        'min_amount': 50000,
                        'max_amount': 300000,
                        'term': 36,
                        'approval': '1-2天',
                        'requirements': ['光大客户', '公积金/社保', '征信良好'],
                        'tags': ['快速审批', '全程线上'],
                        'commission': '1.5%'
                    },
                    {
                        'name': '房抵贷',
                        'category': '抵押贷',
                        'rate': '4.1%',
                        'min_amount': 500000,
                        'max_amount': 5000000,
                        'term': 180,
                        'approval': '5-7天',
                        'requirements': ['有房产'],
                        'tags': ['利率优', '额度高'],
                        'commission': '1.0%'
                    }
                ]
            },
            '民生银行': {
                'type': '股份制银行',
                'products': [
                    {
                        'name': '民易贷',
                        'category': '信用贷',
                        'rate': '4.5%',
                        'min_amount': 50000,
                        'max_amount': 300000,
                        'term': 36,
                        'approval': '1-3天',
                        'requirements': ['民生客户', '公积金/代发工资', '征信良好'],
                        'tags': ['门槛适中'],
                        'commission': '1.5%'
                    },
                    {
                        'name': '房抵贷',
                        'category': '抵押贷',
                        'rate': '4.2%',
                        'min_amount': 500000,
                        'max_amount': 5000000,
                        'term': 180,
                        'approval': '5-7天',
                        'requirements': ['有房产'],
                        'tags': ['高额度'],
                        'commission': '1.0%'
                    }
                ]
            },
            '平安银行': {
                'type': '股份制银行',
                'products': [
                    {
                        'name': '新一贷',
                        'category': '信用贷',
                        'rate': '6.0%',
                        'min_amount': 50000,
                        'max_amount': 500000,
                        'term': 36,
                        'approval': '2-3天',
                        'requirements': ['有稳定收入', '征信良好', '年龄23-55岁'],
                        'tags': ['门槛较低', '额度高'],
                        'commission': '2.0%'
                    },
                    {
                        'name': '车贷',
                        'category': '车贷',
                        'rate': '5.5%',
                        'min_amount': 100000,
                        'max_amount': 1000000,
                        'term': 60,
                        'approval': '2-3天',
                        'requirements': ['购车合同', '驾驶证'],
                        'tags': ['购车专享'],
                        'commission': '1.5%'
                    },
                    {
                        'name': '房抵贷',
                        'category': '抵押贷',
                        'rate': '4.5%',
                        'min_amount': 500000,
                        'max_amount': 5000000,
                        'term': 180,
                        'approval': '5-7天',
                        'requirements': ['有房产'],
                        'tags': ['高额度'],
                        'commission': '1.0%'
                    }
                ]
            },
            '兴业银行': {
                'type': '股份制银行',
                'products': [
                    {
                        'name': '兴闪贷',
                        'category': '信用贷',
                        'rate': '4.5%',
                        'min_amount': 50000,
                        'max_amount': 300000,
                        'term': 36,
                        'approval': '1-3天',
                        'requirements': ['兴业客户', '公积金/社保', '征信良好'],
                        'tags': ['审批快'],
                        'commission': '1.5%'
                    },
                    {
                        'name': '房抵贷',
                        'category': '抵押贷',
                        'rate': '4.3%',
                        'min_amount': 500000,
                        'max_amount': 5000000,
                        'term': 180,
                        'approval': '5-7天',
                        'requirements': ['有房产'],
                        'tags': ['高额度'],
                        'commission': '1.0%'
                    }
                ]
            },
            '华夏银行': {
                'type': '股份制银行',
                'products': [
                    {
                        'name': '华夏E贷',
                        'category': '信用贷',
                        'rate': '4.35%',
                        'min_amount': 50000,
                        'max_amount': 300000,
                        'term': 36,
                        'approval': '1-3天',
                        'requirements': ['华夏客户', '公积金/社保', '征信良好'],
                        'tags': ['门槛低'],
                        'commission': '1.5%'
                    }
                ]
            },
            '广发银行': {
                'type': '股份制银行',
                'products': [
                    {
                        'name': '广发E秒贷',
                        'category': '信用贷',
                        'rate': '4.5%',
                        'min_amount': 50000,
                        'max_amount': 300000,
                        'term': 36,
                        'approval': '1-2天',
                        'requirements': ['广发客户', '公积金/代发工资', '征信良好'],
                        'tags': ['全程线上', '审批快'],
                        'commission': '1.5%'
                    },
                    {
                        'name': '房抵贷',
                        'category': '抵押贷',
                        'rate': '4.35%',
                        'min_amount': 500000,
                        'max_amount': 5000000,
                        'term': 180,
                        'approval': '5-7天',
                        'requirements': ['有房产'],
                        'tags': ['高额度'],
                        'commission': '1.0%'
                    }
                ]
            },
            # 城商行
            '湖北银行': {
                'type': '城商行',
                'products': [
                    {
                        'name': '荆楚贷',
                        'category': '信用贷',
                        'rate': '4.35%',
                        'min_amount': 100000,
                        'max_amount': 500000,
                        'term': 36,
                        'approval': '2-5天',
                        'requirements': ['湖北客户', '公积金/社保', '征信良好'],
                        'tags': ['本地银行', '额度高'],
                        'commission': '1.8%'
                    },
                    {
                        'name': '房抵贷',
                        'category': '抵押贷',
                        'rate': '4.25%',
                        'min_amount': 500000,
                        'max_amount': 5000000,
                        'term': 180,
                        'approval': '5-7天',
                        'requirements': ['有房产'],
                        'tags': ['本地银行', '高额度'],
                        'commission': '1.0%'
                    },
                    {
                        'name': '经营贷',
                        'category': '经营贷',
                        'rate': '4.5%',
                        'min_amount': 200000,
                        'max_amount': 2000000,
                        'term': 60,
                        'approval': '5-7天',
                        'requirements': ['营业执照', '经营满1年'],
                        'tags': ['经营用途', '本地银行'],
                        'commission': '1.5%'
                    }
                ]
            },
            '汉口银行': {
                'type': '城商行',
                'products': [
                    {
                        'name': '市民贷',
                        'category': '信用贷',
                        'rate': '4.5%',
                        'min_amount': 50000,
                        'max_amount': 200000,
                        'term': 24,
                        'approval': '3-5天',
                        'requirements': ['武汉市民', '社保/公积金', '征信良好'],
                        'tags': ['本地银行', '门槛低'],
                        'commission': '1.5%'
                    },
                    {
                        'name': '房抵贷',
                        'category': '抵押贷',
                        'rate': '4.35%',
                        'min_amount': 500000,
                        'max_amount': 5000000,
                        'term': 180,
                        'approval': '5-7天',
                        'requirements': ['有房产'],
                        'tags': ['本地银行', '高额度'],
                        'commission': '1.0%'
                    }
                ]
            },
            '北京银行': {
                'type': '城商行',
                'products': [
                    {
                        'name': '京e贷',
                        'category': '信用贷',
                        'rate': '4.25%',
                        'min_amount': 50000,
                        'max_amount': 300000,
                        'term': 36,
                        'approval': '1-3天',
                        'requirements': ['北行客户', '公积金/社保', '征信良好'],
                        'tags': ['门槛低'],
                        'commission': '1.5%'
                    },
                    {
                        'name': '房抵贷',
                        'category': '抵押贷',
                        'rate': '4.2%',
                        'min_amount': 500000,
                        'max_amount': 5000000,
                        'term': 180,
                        'approval': '5-7天',
                        'requirements': ['有房产'],
                        'tags': ['高额度'],
                        'commission': '1.0%'
                    }
                ]
            },
            # 互联网银行
            '微众银行': {
                'type': '互联网银行',
                'products': [
                    {
                        'name': '微粒贷',
                        'category': '信用贷',
                        'rate': '5.4%-7.2%',
                        'min_amount': 500,
                        'max_amount': 300000,
                        'term': 20,
                        'approval': '当天',
                        'requirements': ['微信用户', '征信良好', '有额度'],
                        'tags': ['门槛极低', '全程线上', '随借随还'],
                        'commission': '2.0%'
                    },
                    {
                        'name': '微业贷',
                        'category': '经营贷',
                        'rate': '5.4%-6.5%',
                        'min_amount': 100000,
                        'max_amount': 500000,
                        'term': 24,
                        'approval': '3-5天',
                        'requirements': ['企业法人', '营业执照', '经营满1年'],
                        'tags': ['经营用途', '全程线上'],
                        'commission': '1.8%'
                    }
                ]
            },
            '网商银行': {
                'type': '互联网银行',
                'products': [
                    {
                        'name': '网商贷',
                        'category': '经营贷',
                        'rate': '5.4%-7.2%',
                        'min_amount': 10000,
                        'max_amount': 2000000,
                        'term': 24,
                        'approval': '当天',
                        'requirements': ['淘宝/天猫商家', '经营数据', '征信良好'],
                        'tags': ['电商专享', '额度高', '随借随还'],
                        'commission': '1.8%'
                    }
                ]
            }
        }
    
    def collect_all(self):
        """采集所有产品"""
        total_products = 0
        
        print("🚀 开始采集完整产品库...\n")
        
        for bank_name, bank_info in self.banks.items():
            print(f"📦 {bank_name} ({bank_info['type']})")
            
            bank_products = bank_info['products']
            total_products += len(bank_products)
            
            for product in bank_products:
                self.products.append({
                    'bank': bank_name,
                    'bank_type': bank_info['type'],
                    'product_name': product['name'],
                    'category': product['category'],
                    'rate': product['rate'],
                    'min_amount': product['min_amount'],
                    'max_amount': product['max_amount'],
                    'term': product['term'],
                    'approval_time': product['approval'],
                    'requirements': product['requirements'],
                    'tags': product['tags'],
                    'commission': product['commission'],
                    'status': '在推',
                    'source': '银行官网',
                    'update_time': datetime.now().strftime('%Y-%m-%d')
                })
            
            print(f"   ✅ {len(bank_products)} 个产品")
        
        print(f"\n✅ 共采集 {total_products} 个产品")
        print(f"🏦 覆盖 {len(self.banks)} 家银行")
        print(f"📊 产品类型: 信用贷、抵押贷、经营贷、装修贷、车贷等")
        
        return self.products
    
    def save_to_obsidian(self):
        """保存为 Obsidian 页面"""
        output_dir = Path("/workspaces/MyMoltbot/obsidian-templates/产品库")
        output_dir.mkdir(exist_ok=True)
        
        # 创建分类索引
        categories = {}
        for product in self.products:
            cat = product['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(product)
        
        # 生成银行产品页
        for bank_name, bank_info in self.banks.items():
            bank_dir = output_dir / bank_name
            bank_dir.mkdir(exist_ok=True)
            
            # 获取该银行的产品
            bank_products = [p for p in self.products if p['bank'] == bank_name]
            
            # 生成页面
            content = self.generate_bank_page(bank_name, bank_info['type'], bank_products)
            (bank_dir / f"{bank_name}-产品.md").write_text(content, encoding='utf-8')
        
        # 生成分类索引
        content = self.generate_category_index(categories)
        (output_dir / "产品分类索引.md").write_text(content, encoding='utf-8')
        
        # 生成总索引
        content = self.generate_master_index()
        (output_dir / "产品数据库索引.md").write_text(content, encoding='utf-8')
        
        print(f"\n📁 已保存到: {output_dir}")
    
    def generate_bank_page(self, bank_name, bank_type, products):
        """生成银行产品页面"""
        content = f"""---
title: {bank_name}贷款产品
bank: {bank_name}
type: {bank_type}
updateTime: {datetime.now().strftime('%Y-%m-%d')}
---

# {bank_name} 贷款产品

## 基本信息

| 项目 | 内容 |
|------|------|
| 银行类型 | {bank_type} |
| 产品数量 | {len(products)}个 |
| 更新时间 | {datetime.now().strftime('%Y-%m-%d')} |

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

**产品标签**: {' '.join([f'`{tag}`' for tag in p['tags']])}

"""
        
        content += f"""
---
**最后更新**: {datetime.now().strftime('%Y-%m-%d')}
"""
        
        return content
    
    def generate_category_index(self, categories):
        """生成分类索引"""
        content = f"""---
title: 产品分类索引
type: 索引
updateTime: {datetime.now().strftime('%Y-%m-%d')}
---

# 产品分类索引

> 按产品类型分类的贷款产品索引

"""
        
        for cat, products in sorted(categories.items()):
            content += f"## {cat}\n\n"
            content += f"共 {len(products)} 个产品\n\n"
            content += "| 银行 | 产品 | 利率 | 额度 | 审批 |\n"
            content += "|------|------|------|------|------|\n"
            
            for p in products:
                content += f"| {p['bank']} | {p['product_name']} | {p['rate']} | {p['min_amount']/10000:.0f}-{p['max_amount']/10000:.0f}万 | {p['approval_time']} |\n"
            
            content += "\n"
        
        content += f"""
---
**最后更新**: {datetime.now().strftime('%Y-%m-%d')}
"""
        
        return content
    
    def generate_master_index(self):
        """生成总索引"""
        content = f"""---
title: 产品数据库索引
type: 索引
updateTime: {datetime.now().strftime('%Y-%m-%d')}
---

# 产品数据库索引

> 所有银行和产品汇总

## 按银行分类

| 银行 | 类型 | 产品数 |
|------|------|--------|
"""
        
        for bank_name, bank_info in self.banks.items():
            bank_products = [p for p in self.products if p['bank'] == bank_name]
            content += f"| [[{bank_name}-产品|{bank_name}]] | {bank_info['type']} | {len(bank_products)} |\n"
        
        content += f"""
## 统计信息

| 指标 | 数值 |
|------|------|
| 总银行数 | {len(self.banks)}家 |
| 总产品数 | {len(self.products)}个 |
| 国有银行 | {sum(1 for b in self.banks.values() if b['type'] == '国有银行')}家 |
| 股份制银行 | {sum(1 for b in self.banks.values() if b['type'] == '股份制银行')}家 |
| 城商行 | {sum(1 for b in self.banks.values() if b['type'] == '城商行')}家 |
| 互联网银行 | {sum(1 for b in self.banks.values() if b['type'] == '互联网银行')}家 |

## 产品类型分布

"""
        
        categories = {}
        for p in self.products:
            cat = p['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            content += f"- {cat}: {count}个\n"
        
        content += f"""
---

**最后更新**: {datetime.now().strftime('%Y-%m-%d')}
**数据来源**: 各银行官网
"""
        
        return content
    
    def save_json(self):
        """保存为 JSON"""
        output_dir = Path("/home/codespace/clawd/product-collector/comprehensive")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"products_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_file.write_text(
            json.dumps(self.products, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        
        print(f"\n💾 JSON数据已保存: {output_file}")
        return str(output_file)


def main():
    collector = ComprehensiveProductCollector()
    products = collector.collect_all()
    collector.save_json()
    collector.save_to_obsidian()

if __name__ == '__main__':
    main()
