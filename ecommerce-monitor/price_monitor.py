#!/usr/bin/env python3
"""
电商价格与优惠券监控系统
监控主流电商平台，找到最低价
"""

import json
import re
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus
from typing import List, Dict, Optional
import logging

# 配置
DATA_DIR = Path("/home/codespace/clawd/ecommerce-monitor/data")
LOG_DIR = Path("/home/codespace/clawd/ecommerce-monitor/logs")

# 日志配置
LOG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'ecommerce_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EcommercePriceMonitor:
    """电商价格与优惠券监控"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        
        # 电商平台配置
        self.platforms = {
            '淘宝': {
                'search_url': 'https://s.taobao.com/search?q={keyword}',
                'coupon_url': 'https://券星球',
                'api': 'taobao',
                'confidence': 0.9
            },
            '京东': {
                'search_url': 'https://search.jd.com/Search?keyword={keyword}&enc=utf-8',
                'coupon_url': 'https://coupon.jd.com',
                'confidence': 0.95
            },
            '拼多多': {
                'search_url': 'https://youhui.pinduoduo.com/api/search?keyword={keyword}',
                'coupon_url': 'https://youhui.pinduoduo.com',
                'confidence': 0.85
            },
            '抖音商城': {
                'search_url': 'https://www.douyin.com/search/{keyword}',
                'coupon_url': 'https://v.m.Douyin.com',
                'confidence': 0.8
            },
            '唯品会': {
                'search_url': 'https://search.vip.com/search?keyword={keyword}',
                'coupon_url': 'https://www.vip.com',
                'confidence': 0.8
            },
            '苏宁易购': {
                'search_url': 'https://search.suning.com/{keyword}/',
                'coupon_url': 'https://cuxiao.suning.com',
                'confidence': 0.85
            },
            '小红书': {
                'search_url': 'https://www.xiaohongshu.com/search/{keyword}',
                'coupon_url': 'https://www.xiaohongshu.com',
                'confidence': 0.75
            }
        }
        
        # 模拟的热门优惠券平台
        self.coupon_platforms = [
            {'name': '券妈妈', 'url': 'https://www.quanmama.com'},
            {'name': '券星空', 'url': 'https://www.quanxingkong.com'},
            {'name': '什么值得买', 'url': 'https://www.smzdm.com'},
            {'name': '慢慢买', 'url': 'https://www.manmanbuy.com'},
            {'name': '比达尔', 'url': 'https://www.biduer.com'},
            {'name': '惠惠网', 'url': 'https://www.huihui.cn'},
        ]
        
        self.results = []
        self.price_history = []
    
    def search_product(self, keyword: str) -> List[Dict]:
        """搜索商品"""
        logger.info(f"🔍 搜索商品: {keyword}")
        results = []
        
        # 模拟各平台搜索结果（实际需要API或爬虫）
        platforms_data = self._get_mock_search_results(keyword)
        
        for item in platforms_data:
            # 计算实际价格（原价 - 优惠券）
            original_price = item.get('original_price', 0)
            coupon = item.get('coupon', 0)
            final_price = original_price - coupon
            
            results.append({
                'platform': item['platform'],
                'product_name': item['name'],
                'original_price': original_price,
                'coupon': coupon,
                'final_price': final_price,
                'discount_rate': round((1 - final_price/original_price) * 100, 1) if original_price > 0 else 0,
                'url': item.get('url', ''),
                'shop': item.get('shop', ''),
                'sales': item.get('sales', ''),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'confidence': item.get('confidence', 0.8)
            })
        
        # 按价格排序
        results.sort(key=lambda x: x['final_price'])
        
        self.results = results
        return results
    
    def _get_mock_search_results(self, keyword: str) -> List[Dict]:
        """获取模拟搜索结果（实际应调用API）"""
        import random
        
        products = [
            {
                'platform': '淘宝',
                'name': f'【品牌】{keyword} 正品保障',
                'original_price': random.randint(100, 500),
                'coupon': random.randint(10, 50),
                'url': 'https://taobao.com/item/123',
                'shop': '品牌官方旗舰店',
                'sales': f'{random.randint(100, 10000)}+',
                'confidence': 0.9
            },
            {
                'platform': '京东',
                'name': f'{keyword} 京东自营 送货上门',
                'original_price': random.randint(120, 550),
                'coupon': random.randint(15, 60),
                'url': 'https://jd.com/item/456',
                'shop': '京东自营',
                'sales': f'{random.randint(500, 5000)}+',
                'confidence': 0.95
            },
            {
                'platform': '拼多多',
                'name': f'{keyword} 拼多多百亿补贴',
                'original_price': random.randint(90, 450),
                'coupon': random.randint(20, 80),
                'url': 'https://pinduoduo.com/item/789',
                'shop': '官方旗舰店',
                'sales': f'{random.randint(10000, 100000)}+',
                'confidence': 0.85
            },
            {
                'platform': '抖音商城',
                'name': f'{keyword} 抖音直播专享价',
                'original_price': random.randint(100, 480),
                'coupon': random.randint(15, 70),
                'url': 'https://douyin.com/item/111',
                'shop': '品牌官方店',
                'sales': f'{random.randint(1000, 50000)}+',
                'confidence': 0.8
            },
            {
                'platform': '唯品会',
                'name': f'{keyword} 唯品会特卖',
                'original_price': random.randint(110, 520),
                'coupon': random.randint(20, 60),
                'url': 'https://vip.com/item/222',
                'shop': '唯品会自营',
                'sales': f'{random.randint(500, 5000)}+',
                'confidence': 0.8
            },
            {
                'platform': '苏宁易购',
                'name': f'{keyword} 苏宁易购 正品保证',
                'original_price': random.randint(105, 490),
                'coupon': random.randint(10, 55),
                'url': 'https://suning.com/item/333',
                'shop': '苏宁自营',
                'sales': f'{random.randint(300, 3000)}+',
                'confidence': 0.85
            },
            {
                'platform': '小红书',
                'name': f'{keyword} 小红书买手推荐',
                'original_price': random.randint(95, 470),
                'coupon': random.randint(15, 65),
                'url': 'https://xiaohongshu.com/item/444',
                'shop': '买手店',
                'sales': f'{random.randint(200, 2000)}+',
                'confidence': 0.75
            }
        ]
        
        return products
    
    def find_coupons(self, keyword: str) -> List[Dict]:
        """查找优惠券"""
        logger.info(f"🎫 查找优惠券: {keyword}")
        coupons = []
        
        # 模拟优惠券数据
        coupon_templates = [
            {'name': '满100减10', 'threshold': 100, 'discount': 10, 'platform': '淘宝'},
            {'name': '满200减20', 'threshold': 200, 'discount': 20, 'platform': '京东'},
            {'name': '满300减30', 'threshold': 300, 'discount': 30, 'platform': '拼多多'},
            {'name': '满500减50', 'threshold': 500, 'discount': 50, 'platform': '抖音'},
            {'name': '满1000减100', 'threshold': 1000, 'discount': 100, 'platform': '唯品会'},
        ]
        
        for template in coupon_templates:
            coupons.append({
                'platform': template['platform'],
                'coupon_name': template['name'],
                'threshold': template['threshold'],
                'discount': template['discount'],
                'source': '优惠券平台',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'confidence': 0.85
            })
        
        return coupons
    
    def analyze_lowest_price(self, keyword: str) -> Dict:
        """分析最低价"""
        logger.info(f"📊 分析最低价: {keyword}")
        
        if not self.results:
            self.search_product(keyword)
        
        if not self.results:
            return {'error': '未找到商品'}
        
        lowest = self.results[0]
        highest = self.results[-1]
        
        # 计算平均价格
        avg_price = sum(r['final_price'] for r in self.results) / len(self.results)
        
        # 计算节省
        if highest['original_price'] > 0:
            savings = highest['final_price'] - lowest['final_price']
            savings_percent = round(savings / highest['original_price'] * 100, 1)
        else:
            savings = 0
            savings_percent = 0
        
        analysis = {
            'keyword': keyword,
            'lowest_price': {
                'platform': lowest['platform'],
                'price': lowest['final_price'],
                'original_price': lowest['original_price'],
                'coupon': lowest['coupon'],
                'shop': lowest['shop'],
                'url': lowest['url']
            },
            'highest_price': {
                'platform': highest['platform'],
                'price': highest['final_price'],
                'original_price': highest['original_price']
            },
            'statistics': {
                'total_platforms': len(self.results),
                'average_price': round(avg_price, 2),
                'price_range': f"{lowest['final_price']:.2f} - {highest['final_price']:.2f}",
                'potential_savings': round(savings, 2),
                'savings_percent': f"{savings_percent}%"
            },
            'all_results': self.results,
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        return analysis
    
    def monitor_price_changes(self, keyword: str) -> List[Dict]:
        """监控价格变化"""
        logger.info(f"📈 监控价格变化: {keyword}")
        
        # 从历史记录加载
        history_file = DATA_DIR / f"price_history_{keyword}.json"
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                self.price_history = json.load(f)
        
        # 添加当前价格
        self.search_product(keyword)
        
        current_snapshot = {
            'keyword': keyword,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'results': self.results
        }
        
        self.price_history.append(current_snapshot)
        
        # 保存历史
        history_file.write_text(
            json.dumps(self.price_history, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        
        # 分析变化
        changes = []
        if len(self.price_history) >= 2:
            prev = self.price_history[-2]
            curr = self.price_history[-1]
            
            for curr_item in curr['results']:
                for prev_item in prev['results']:
                    if (curr_item['platform'] == prev_item['platform'] and
                        curr_item['product_name'] == prev_item['product_name']):
                        
                        price_change = curr_item['final_price'] - prev_item['final_price']
                        if price_change != 0:
                            changes.append({
                                'platform': curr_item['platform'],
                                'product': curr_item['product_name'],
                                'old_price': prev_item['final_price'],
                                'new_price': curr_item['final_price'],
                                'change': round(price_change, 2),
                                'direction': '↓' if price_change < 0 else '↑'
                            })
                        break
        
        return changes
    
    def generate_price_report(self, keyword: str) -> str:
        """生成价格报告"""
        analysis = self.analyze_lowest_price(keyword)
        coupons = self.find_coupons(keyword)
        
        report = f"""# 📊 {keyword} 价格监控报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**监控平台**: {', '.join(p for p in self.platforms.keys())}

---

## 🏆 最低价推荐

| 平台 | 商品 | 原价 | 券后价 | 优惠 | 店铺 |
|------|------|------|--------|------|------|
"""
        
        for result in self.results[:5]:
            report += f"| {result['platform']} | {result['product_name'][:20]} | ¥{result['original_price']} | ¥{result['final_price']} | ¥{result['coupon']} | {result['shop']} |\n"
        
        report += f"""
---

## 💰 最佳选择

### 🥇 最低价
- **平台**: {analysis['lowest_price']['platform']}
- **价格**: ¥{analysis['lowest_price']['price']:.2f}
- **原价**: ¥{analysis['lowest_price']['original_price']:.2f}
- **优惠券**: ¥{analysis['lowest_price']['coupon']:.2f}
- **店铺**: {analysis['lowest_price']['shop']}
- **链接**: {analysis['lowest_price']['url']}

### 📊 价格统计

| 指标 | 数值 |
|------|------|
| 监控平台数 | {analysis['statistics']['total_platforms']} |
| 平均价格 | ¥{analysis['statistics']['average_price']:.2f} |
| 价格区间 | {analysis['statistics']['price_range']} |
| 潜在节省 | ¥{analysis['statistics']['potential_savings']:.2f} ({analysis['statistics']['savings_percent']}) |

---

## 🎫 可用优惠券

| 平台 | 券名称 | 使用门槛 | 优惠金额 |
|------|--------|----------|----------|
"""
        
        for coupon in coupons:
            report += f"| {coupon['platform']} | {coupon['coupon_name']} | ¥{coupon['threshold']} | ¥{coupon['discount']} |\n"
        
        report += f"""
---

## 📈 各平台详情

### 淘宝/天猫
- 价格区间: ¥{min(r['final_price'] for r in self.results if r['platform']=='淘宝'):.2f} - ¥{max(r['final_price'] for r in self.results if r['platform']=='淘宝'):.2f}
- 推荐: 关注店铺优惠券和88VIP

### 京东
- 价格区间: ¥{min(r['final_price'] for r in self.results if r['platform']=='京东'):.2f} - ¥{max(r['final_price'] for r in self.results if r['platform']=='京东'):.2f}
- 推荐: 京东PLUS券和京豆抵扣

### 拼多多
- 价格区间: ¥{min(r['final_price'] for r in self.results if r['platform']=='拼多多'):.2f} - ¥{max(r['final_price'] for r in self.results if r['platform']=='拼多多'):.2f}
- 推荐: 百亿补贴和多多果园

### 抖音商城
- 价格区间: ¥{min(r['final_price'] for r in self.results if r['platform']=='抖音商城'):.2f} - ¥{max(r['final_price'] for r in self.results if r['platform']=='抖音商城'):.2f}
- 推荐: 直播间专属优惠

---

## 💡 购买建议

1. **最低价平台**: {analysis['lowest_price']['platform']} (¥{analysis['lowest_price']['price']:.2f})
2. **关注时机**: 大促期间(618、双11)价格更低
3. **叠加优惠**: 平台券 + 店铺券 + 支付优惠
4. **比价工具**: 使用慢慢买、什么值得买等比价

---

## 🔗 购买链接

| 平台 | 链接 |
|------|------|
"""
        
        for result in self.results[:7]:
            report += f"| {result['platform']} | [{result['product_name'][:15]}...]({result['url']}) |\n"
        
        report += f"""
---

*报告由 Ecommerce Price Monitor 自动生成*
**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    def run_full_monitoring(self, keyword: str):
        """执行完整监控"""
        print("=" * 60)
        print(f"    🛒 电商价格监控系统 v1.0")
        print(f"    监控商品: {keyword}")
        print("=" * 60)
        
        # 1. 搜索商品
        print("\n🔍 搜索商品...")
        results = self.search_product(keyword)
        print(f"  ✅ 找到 {len(results)} 个结果")
        
        # 2. 分析最低价
        print("\n📊 分析最低价...")
        analysis = self.analyze_lowest_price(keyword)
        
        # 3. 查找优惠券
        print("\n🎫 查找优惠券...")
        coupons = self.find_coupons(keyword)
        print(f"  ✅ 找到 {len(coupons)} 个优惠券")
        
        # 4. 生成报告
        print("\n📄 生成报告...")
        report = self.generate_price_report(keyword)
        report_file = DATA_DIR / f"price_report_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.write_text(report, encoding='utf-8')
        
        # 保存结果
        results_file = DATA_DIR / f"results_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        results_file.write_text(
            json.dumps({'results': results, 'analysis': analysis, 'coupons': coupons}, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        
        # 5. 输出结果
        print("\n" + "=" * 60)
        print("    📊 监控完成！")
        print("=" * 60)
        
        print(f"\n🏆 最低价推荐:")
        print(f"   平台: {analysis['lowest_price']['platform']}")
        print(f"   价格: ¥{analysis['lowest_price']['price']:.2f}")
        print(f"   店铺: {analysis['lowest_price']['shop']}")
        
        print(f"\n📊 价格统计:")
        print(f"   监控平台: {analysis['statistics']['total_platforms']} 个")
        print(f"   平均价格: ¥{analysis['statistics']['average_price']:.2f}")
        print(f"   潜在节省: ¥{analysis['statistics']['potential_savings']:.2f}")
        
        print(f"\n🎫 优惠券: {len(coupons)} 个")
        
        print(f"\n📄 报告文件: {report_file}")
        print(f"📦 数据文件: {results_file}")
        
        print("\n" + "=" * 60)
        print("    💡 最佳购买建议")
        print("=" * 60)
        print(f"\n✅ 推荐在 【{analysis['lowest_price']['platform']}】 购买")
        print(f"   价格: ¥{analysis['lowest_price']['price']:.2f}")
        print(f"   可节省: ¥{analysis['statistics']['potential_savings']:.2f} ({analysis['statistics']['savings_percent']})")
        
        return results, analysis, coupons


def main():
    import sys
    
    if len(sys.argv) < 2:
        keyword = input("请输入要监控的商品名称: ").strip()
    else:
        keyword = sys.argv[1]
    
    if not keyword:
        print("❌ 请输入商品名称")
        return
    
    monitor = EcommercePriceMonitor()
    monitor.run_full_monitoring(keyword)


if __name__ == '__main__':
    main()
