# 增强版公众号采集系统 v2.0

> 自动监控、智能提取、同步更新

## 新增功能

### 1. 增强版监控（14个公众号）

| 公众号 | 类型 | 优先级 | 监控关键词 |
|--------|------|--------|-----------|
| 武汉贷款通 | 产品推荐 | ⭐⭐⭐ | 利率、额度、审批、佣金 |
| 汉口贷款助手 | 产品评测 | ⭐⭐⭐ | 测评、案例、通过率 |
| 湖北金融通 | 政策解读 | ⭐⭐ | 政策、新规、补贴 |
| 光谷贷款指南 | 产品推荐 | ⭐⭐ | 科技企业、创业、高新 |
| 武汉房抵专家 | 抵押贷款 | ⭐⭐⭐ | 房产抵押、利率 |
| 汉口银行微服务 | 银行官方 | ⭐⭐⭐ | 官方、新产品 |
| 湖北银行微银行 | 银行官方 | ⭐⭐⭐ | 官方、新产品 |
| 公积金查询武汉 | 公积金资讯 | ⭐⭐⭐ | 公积金贷款、提取 |
| 武汉信贷联盟 | 行业资讯 | ⭐⭐ | 市场动态、佣金 |
| 贷款中介联盟 | 行业资讯 | ⭐⭐ | 获客技巧、案例 |
| 银行产品大全 | 产品聚合 | ⭐⭐⭐ | 产品汇总、对比 |
| 武汉房贷通 | 房贷专项 | ⭐⭐⭐ | 房贷、二手房、转贷 |
| 企业贷助手 | 企业贷款 | ⭐⭐ | 企业贷、税贷 |
| 征信修复指南 | 征信服务 | ⭐ | 征信修复、逾期 |

### 2. 智能关键词提取

- **产品关键词**: 贷款、信用贷、抵押贷、公积金贷等
- **利率关键词**: 利率、利息、年化、月息
- **额度关键词**: 额度、最高、最低、可贷
- **条件关键词**: 条件、要求、资格、审批
- **佣金关键词**: 佣金、返点、提成

### 3. 变化检测

- 自动检测新产品上线
- 利率变化提醒
- 产品信息更新通知

### 4. 自动同步

- 自动同步到产品库
- 自动创建PR
- 自动发送通知

## 使用方法

### 快速开始

```bash
# 运行增强版采集
python3 /home/codespace/clawd/wechat-collector/enhanced_collector.py

# 或运行完整工作流（采集+同步+PR）
bash /home/codespace/clawd/wechat-collector/enhanced_workflow.sh
```

### 配置文件

```bash
/home/codespace/clawd/wechat-collector/config/accounts_enhanced.json
```

可以配置：
- 公众号账号
- 监控关键词
- 检查频率
- 自动同步开关

## 定时任务

### 每6小时运行一次

```bash
# crontab -e
0 */6 * * * cd /home/codespace/clawd/wechat-collector && bash enhanced_workflow.sh
```

### 每天运行3次（推荐）

```bash
# crontab -e
0 8 * * * cd /home/codespace/clawd/wechat-collector && bash enhanced_workflow.sh
0 14 * * * cd /home/codespace/clawd/wechat-collector && bash enhanced_workflow.sh
0 20 * * * cd /home/codespace/clawd/wechat-collector && bash enhanced_workflow.sh
```

## 工作流程

```
┌─────────────────────────────────────────────────────┐
│              增强版公众号采集流程 v2.0                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1️⃣ 关键词监控                                       │
│     ↓                                               │
│  14个公众号 → 智能提取 → 产品信息                     │
│                                                     │
│  2️⃣ 变化检测                                         │
│     ↓                                               │
│  新产品上线 → 利率变化 → 信息更新                     │
│                                                     │
│  3️⃣ 自动同步                                         │
│     ↓                                               │
│  产品库 → PR创建 → WhatsApp通知                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 与产品库集成

```
公众号数据 → 变化检测 → PR创建 → 审核合并 → 产品库更新
```

## 监控指标

- 采集成功率
- 新产品数量
- 利率变化次数
- 同步状态

## 故障排除

### 采集失败
```bash
# 检查日志
tail -f /home/codespace/clawd/wechat-collector/logs/enhanced_collector.log
```

### PR未创建
```bash
# 检查是否有新数据
ls -la /home/codespace/clawd/wechat-collector/data/wechat_products_*.json
```

### 关键词不匹配
```bash
# 检查配置文件
cat /home/codespace/clawd/wechat-collector/config/accounts_enhanced.json
```

## 下一步优化

1. ✅ 14个公众号监控
2. ✅ 智能关键词提取
3. ✅ 变化自动检测
4. ⏳ 接入真实微信API
5. ⏳ 内容全文搜索
6. ⏳ 竞品分析报告

## 相关文件

```
wechat-collector/
├── enhanced_collector.py    # 增强版采集器
├── enhanced_workflow.sh     # 完整工作流
├── config/
│   └── accounts_enhanced.json  # 增强配置
├── data/                    # 采集数据
└── logs/                    # 日志
```
