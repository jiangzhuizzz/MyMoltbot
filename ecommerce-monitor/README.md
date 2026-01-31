# 🛒 电商价格监控系统

监控主流国内电商平台，自动收集优惠券，找到最低价！

## ✨ 功能特性

- 🔍 **商品搜索** - 同时搜索淘宝、京东、拼多多、抖音等7大平台
- 💰 **价格对比** - 自动比较各平台价格，找出最低价
- 🎫 **优惠券收集** - 汇总各平台优惠券信息
- 📊 **价格分析** - 提供价格统计和购买建议
- 📈 **价格监控** - 跟踪价格变化趋势
- 📄 **报告生成** - 自动生成Markdown格式的价格报告

## 🚀 快速开始

### 安装依赖

```bash
pip install requests beautifulsoup4
```

### 使用方法

#### 命令行方式

```bash
python price_monitor.py
```

然后输入商品名称即可。

#### 指定商品

```bash
python price_monitor.py "iPhone 15"
```

#### Python调用

```python
from price_monitor import EcommercePriceMonitor

monitor = EcommercePriceMonitor()

# 搜索商品
results = monitor.search_product("iPhone 15")

# 分析最低价
analysis = monitor.analyze_lowest_price("iPhone 15")

# 生成报告
report = monitor.generate_price_report("iPhone 15")
```

## 📊 监控平台

| 平台 | 搜索 | 优惠券 | 置信度 |
|------|------|--------|--------|
| 淘宝/天猫 | ✅ | ✅ | 90% |
| 京东 | ✅ | ✅ | 95% |
| 拼多多 | ✅ | ✅ | 85% |
| 抖音商城 | ✅ | ✅ | 80% |
| 唯品会 | ✅ | ✅ | 80% |
| 苏宁易购 | ✅ | ✅ | 85% |
| 小红书 | ✅ | ✅ | 75% |

## 📁 输出文件

监控结果保存在 `data/` 目录：

```
data/
├── price_report_商品名称_时间戳.md    # 价格报告
├── results_商品名称_时间戳.json       # 结构化数据
└── price_history_商品名称.json        # 价格历史
```

## 💡 使用建议

### 最佳购买时机

1. **大促期间**: 618、双11、雙12价格最低
2. **关注店铺**: 品牌官方旗舰店优惠更多
3. **叠加优惠**: 平台券 + 店铺券 + 支付优惠

### 常用比价网站

- [什么值得买](https://www.smzdm.com) - 购物攻略和优惠信息
- [慢慢买](https://www.manmanbuy.com) - 历史价格查询
- [券妈妈](https://www.quanmama.com) - 优惠券聚合

## ⚠️ 注意事项

1. **数据真实性**: 当前版本使用模拟数据，实际使用需要接入真实API
2. **价格波动**: 商品价格实时变动，建议多次查询
3. **优惠券有效性**: 优惠券可能有使用限制和有效期

## 🔧 扩展功能

### 接入真实API

要接入真实数据，需要：

1. **淘宝/天猫**: 使用淘宝联盟API或爬虫
2. **京东**: 使用京东宙斯API
3. **拼多多**: 使用多多客API
4. **抖音**: 使用抖音精选联盟API

### 添加新平台

在 `platforms` 字典中添加：

```python
'新平台': {
    'search_url': 'https://example.com/search?q={keyword}',
    'coupon_url': 'https://example.com/coupon',
    'confidence': 0.8
}
```

## 📝 License

MIT License
