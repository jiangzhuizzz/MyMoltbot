# 飞书CRM + Clawdbot集成方案

> 目标：用飞书CRM管理客户 + 我自动化处理数据
> 
> 最后更新: 2026-02-01

---

## 🎯 方案总览

```
┌─────────────────────────────────────────────────────────────────┐
│                        整体架构                                  │
│                                                                 │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │ 客户搜索    │      │  Clawdbot   │      │  飞书CRM    │     │
│  │ (我自动)    │ ───→ │  (AI协调)   │ ───→ │  (你管理)   │     │
│  └─────────────┘      └──────┬──────┘      └─────────────┘     │
│                              │                                    │
│                              ▼                                    │
│                       ┌─────────────┐                             │
│                       │  定时任务    │                             │
│                       │  数据同步    │                             │
│                       └─────────────┘                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 一、飞书CRM配置

### 1.1 创建飞书CRM

**步骤**：
1. 访问 https://www.feishu.cn
2. 注册/登录飞书账号
3. 打开"应用中心"
4. 搜索"CRM"或"多维表格"
5. 选择"飞书多维表格"创建

### 1.2 推荐的数据表结构

建议创建3个表：

#### 表1：客户信息表
```
字段列表：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| 客户ID | 文本 | 唯一标识 |
| 姓名 | 单行文本 | 客户姓名 |
| 电话 | 电话 | 联系电话 |
| 微信号 | 单行文本 | 微信号 |
| 来源渠道 | 单选 | 抖音/小红书/百度/转介绍/其他 |
| 意向产品 | 单选 | 信用贷/抵押贷/车贷/经营贷 |
| 意向金额 | 数字 | 贷款金额 |
| 意向等级 | 单选 | 高/中/低 |
| 贷款状态 | 单选 | 新客户/已联系/跟进中/方案沟通/谈判中/成交/流失 |
| 创建时间 | 日期时间 | 创建日期 |
| 最后联系 | 日期时间 | 最后联系时间 |
| 下次跟进 | 日期时间 | 下次跟进时间 |
| 备注 | 多行文本 | 其他信息 |
| 标签 | 多选 | 标签 |
| 搜索关键词 | 单行文本 | 来自哪个搜索 |
| 同步状态 | 单选 | 已同步/待同步/同步失败 |
```

#### 表2：跟进记录表
```
字段列表：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| 记录ID | 文本 | 唯一标识 |
| 客户ID | 关联客户 | 关联客户表 |
| 跟进方式 | 单选 | 电话/微信/面谈/其他 |
| 跟进内容 | 多行文本 | 跟进描述 |
| 跟进结果 | 单选 | 有意向/无意向/待考虑/已拒绝 |
| 下次行动 | 单行文本 | 下次做什么 |
| 下次时间 | 日期时间 | 下次跟进时间 |
| 跟进时间 | 日期时间 | 本次跟进时间 |
| 跟进人 | 用户 | 谁跟进的 |
```

#### 表3：成交记录表
```
字段列表：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| 成交ID | 文本 | 唯一标识 |
| 客户ID | 关联客户 | 关联客户表 |
| 产品名称 | 单行文本 | 贷款产品 |
| 银行 | 单行文本 | 放款银行 |
| 贷款金额 | 数字 | 放款金额 |
| 利率 | 数字 | 年利率 |
| 期限 | 数字 | 月数 |
| 佣金 | 数字 | 佣金金额 |
| 成交时间 | 日期时间 | 放款时间 |
| 状态 | 单选 | 已放款/已取消 |
```

### 1.3 获取API凭证

**步骤**：
1. 飞书开放平台 https://open.feishu.cn
2. 创建企业应用
3. 获取 App ID 和 App Secret
4. 开通以下权限：
   - 表格数据读写
   - 表格元数据读写
   - 多维表格权限

---

## 🔄 二、数据流设计

### 2.1 数据同步流程

```
┌─────────────────────────────────────────────────────────────────┐
│                      数据同步流程                                │
│                                                                 │
│  Step 1: 客户搜索                                               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│  │ 我搜索   │ → │ 生成线索 │ → │ 过滤有效 │                 │
│  │ 线索     │   │ 数据     │   │ 线索     │                 │
│  └──────────┘    └──────────┘    └──────────┘                 │
│                                              │                  │
│                                              ▼                  │
│  Step 2: 同步到飞书CRM                                           │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│  │ API调用  │ → │ 创建记录 │ → │ 更新状态 │                 │
│  │ 飞书     │   │ 客户表   │   │ 同步成功 │                 │
│  └──────────┘    └──────────┘    └──────────┘                 │
│                                              │                  │
│                                              ▼                  │
│  Step 3: 跟进提醒                                               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│  │ 检查到期 │ → │ 发送提醒 │ → │ 提醒成功 │                 │
│  │ 客户     │   │ 给你     │   │          │                 │
│  └──────────┘    └──────────┘    └──────────┘                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 数据字段映射

| 搜索线索字段 | → | 飞书CRM字段 |
|-------------|---|-------------|
| name | → | 姓名 |
| phone | → | 电话 |
| source | → | 来源渠道 |
| intent_level | → | 意向等级 |
| content | → | 备注 |
| keyword | → | 搜索关键词 |

---

## 🤖 三、我能帮你做的事情

### 3.1 自动化功能

| 功能 | 说明 | 触发方式 |
|------|------|----------|
| **自动导入线索** | 搜索到的客户自动导入飞书 | 每次搜索后 |
| **定时检查** | 检查到期未跟进的客户 | 每天早上 |
| **提醒通知** | 发送跟进提醒 | 定时 |
| **数据统计** | 生成统计报表 | 每周 |
| **批量更新** | 批量更新客户状态 | 手动触发 |

### 3.2 命令示例

**搜索客户并导入飞书**：
```
你："帮我搜索贷款客户并导入飞书"

我：
1. 执行客户搜索
2. 过滤有效线索
3. 调用飞书API导入
4. 返回导入结果
```

**检查待跟进客户**：
```
你："检查今天需要跟进的客户"

我：
1. 查询飞书CRM
2. 找出到期未跟进的客户
3. 生成提醒列表
4. 发给你
```

**生成统计报表**：
```
你："本周客户统计"

我：
1. 查询飞书CRM数据
2. 统计新增/跟进/成交
3. 生成报表
4. 发送给你
```

---

## 💻 四、实现方案

### 4.1 技术架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        技术实现                                  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Clawdbot (我)                        │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │  客户搜索模块                                     │  │   │
│  │  │  飞书集成模块                                     │  │   │
│  │  │  定时任务模块                                     │  │   │
│  │  │  统计报表模块                                     │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    飞书API                               │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │  多维表格API / CRM API                            │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    飞书CRM                               │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                │   │
│  │  │客户信息 │  │跟进记录 │  │成交记录 │                │   │
│  │  └─────────┘  └─────────┘  └─────────┘                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 飞书集成模块代码结构

```
feishu-integration/
├── feishu_client.py      # 飞书API客户端
├── sync_service.py       # 同步服务
├── reminder_service.py   # 提醒服务
├── stats_service.py      # 统计服务
├── config.yaml           # 配置文件
└── main.py               # 主程序
```

### 4.3 核心代码示例

#### 飞书API客户端
```python
import requests
from typing import List, Dict

class FeishuClient:
    """飞书API客户端"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open.feishu.cn/open-apis"
        self.token = None
    
    def get_access_token(self):
        """获取access_token"""
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        resp = requests.post(url, json=data)
        self.token = resp.json().get("tenant_access_token")
        return self.token
    
    def create_record(self, table_id: str, fields: Dict) -> str:
        """创建记录"""
        url = f"{self.base_url}/bitable/v1/apps/{self.app_id}/tables/{table_id}/records"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"fields": fields}
        resp = requests.post(url, headers=headers, json=data)
        return resp.json().get("data", {}).get("record", {}).get("id")
    
    def query_records(self, table_id: str, filter_obj: Dict = None) -> List[Dict]:
        """查询记录"""
        url = f"{self.base_url}/bitable/v1/apps/{self.app_id}/tables/{table_id}/records"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {}
        if filter_obj:
            params["filter"] = str(filter_obj)
        resp = requests.get(url, headers=headers, params=params)
        return resp.json().get("data", {}).get("items", [])
    
    def update_record(self, table_id: str, record_id: str, fields: Dict):
        """更新记录"""
        url = f"{self.base_url}/bitable/v1/apps/{self.app_id}/tables/{table_id}/records/{record_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"fields": fields}
        requests.put(url, headers=headers, json=data)
```

#### 同步服务
```python
class SyncService:
    """同步服务"""
    
    def __init__(self, feishu_client: FeishuClient):
        self.client = feishu_client
        self.table_id = "客户表ID"
    
    def sync_lead_to_feishu(self, lead: Dict) -> bool:
        """同步线索到飞书"""
        # 检查是否已存在
        existing = self.client.query_records(
            self.table_id,
            {"conjunction": "and", "conditions": [{"field_name": "电话", "operator": "is", "value": [lead['phone']]}]}
        )
        
        if existing:
            # 已存在，跳过
            return False
        
        # 创建新记录
        fields = {
            "姓名": lead.get('name', '客户'),
            "电话": lead.get('phone', ''),
            "来源渠道": lead.get('source', '搜索'),
            "意向等级": lead.get('intent_level', '中'),
            "备注": lead.get('content', '')[:500],
            "搜索关键词": ','.join(lead.get('keywords', [])),
            "贷款状态": "新客户",
            "创建时间": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "同步状态": "已同步"
        }
        
        record_id = self.client.create_record(self.table_id, fields)
        return record_id is not None
    
    def sync_batch(self, leads: List[Dict]) -> Dict:
        """批量同步"""
        synced = 0
        skipped = 0
        failed = 0
        
        for lead in leads:
            try:
                if self.sync_lead_to_feishu(lead):
                    synced += 1
                else:
                    skipped += 1
            except Exception as e:
                failed += 1
        
        return {"synced": synced, "skipped": skipped, "failed": failed}
```

#### 提醒服务
```python
class ReminderService:
    """提醒服务"""
    
    def __init__(self, feishu_client: FeishuClient):
        self.client = feishu_client
        self.table_id = "客户表ID"
    
    def get_pending_followups(self) -> List[Dict]:
        """获取待跟进客户"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        records = self.client.query_records(
            self.table_id,
            {"conjunction": "and", "conditions": [
                {"field_name": "贷款状态", "operator": "not_is", "value": ["成交", "流失"]},
                {"field_name": "下次跟进", "operator": "is_not_empty", "value": []}
            ]}
        )
        
        pending = []
        for record in records:
            fields = record.get('fields', {})
            next_followup = fields.get('下次跟进', '')
            if next_followup and next_followup <= today:
                pending.append({
                    'id': record.get('record_id'),
                    'name': fields.get('姓名', ''),
                    'phone': fields.get('电话', ''),
                    'intent': fields.get('意向等级', ''),
                    'next_followup': next_followup,
                    'status': fields.get('贷款状态', '')
                })
        
        return pending
    
    def send_reminder(self) -> str:
        """发送提醒"""
        pending = self.get_pending_followups()
        
        if not pending:
            return "✅ 今天没有需要跟进的客户"
        
        message = f"📋 待跟进客户 ({len(pending)}个)\n\n"
        for p in pending[:10]:
            message += f"• {p['name']} - {p['phone']} - {p['intent']} - {p['next_followup']}\n"
        
        if len(pending) > 10:
            message += f"\n...还有其他 {len(pending) - 10} 个"
        
        return message
```

---

## 📅 五、使用流程

### 5.1 日常使用流程

```
早上
├── 我自动检查待跟进客户 → 发提醒给你
│
日常工作
├── 你在飞书CRM管理客户
│   ├── 查看客户列表
│   ├── 记录跟进
│   ├── 更新状态
│
你需要时
├── "帮我搜索贷款客户" → 我搜索 → 自动导入飞书
├── "本周统计" → 我查询飞书 → 发统计报表
├── "检查待跟进" → 我查询飞书 → 发提醒列表
```

### 5.2 触发方式

| 触发方式 | 说明 | 示例 |
|----------|------|------|
| 手动触发 | 你告诉我 | "搜索客户并导入飞书" |
| 定时触发 | 我自动执行 | 每天早上检查待跟进 |
| 事件触发 | 特定事件 | 搜索完成后自动导入 |

---

## ⚙️ 六、配置步骤

### 步骤1：飞书配置
- [ ] 注册飞书账号
- [ ] 创建多维表格
- [ ] 设计客户表结构
- [ ] 创建应用获取API凭证

### 步骤2：环境配置
```bash
# 安装依赖
pip install requests pyyaml

# 配置环境变量
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
```

### 步骤3：测试运行
- [ ] 测试API连接
- [ ] 测试创建记录
- [ ] 测试查询功能
- [ ] 测试同步功能

### 步骤4：日常使用
- [ ] 首次同步现有客户
- [ ] 设置定时任务
- [ ] 开始日常使用

---

## 💰 成本分析

| 项目 | 成本 | 说明 |
|------|------|------|
| 飞书CRM | 免费 | 多维表格免费版够用 |
| Clawdbot | 免费 | 自己部署 |
| 飞书应用 | 免费 | 基础API免费 |
| **总成本** | **0元** | 完全免费 |

---

## 🎯 七、预期效果

### 效率提升
| 场景 | 之前 | 之后 |
|------|------|------|
| 搜索客户 | 手动搜索 | 我自动搜索+导入 |
| 导入CRM | 手动复制粘贴 | 自动同步 |
| 检查跟进 | 翻表格查看 | 自动提醒 |
| 数据统计 | 手动统计 | 自动报表 |

### 工作流程对比

**之前**：
```
1. 手动搜索客户
2. 复制客户信息
3. 打开飞书
4. 手动粘贴到CRM
5. 手动检查跟进
6. 手动统计数据
```

**之后**：
```
1. 我："搜索贷款客户并导入"
2. 自动完成所有步骤
3. 你直接去跟进客户
```

---

## 📋 八、下一步行动

### 本周任务
- [ ] 注册飞书账号
- [ ] 创建CRM多维表格
- [ ] 配置字段
- [ ] 获取API凭证

### 下周任务
- [ ] 集成飞书API
- [ ] 测试同步功能
- [ ] 设置定时任务
- [ ] 开始日常使用

---

## 💡 常见问题

### Q1: 飞书CRM收费吗？
A: 免费版多维表格够用，不收费

### Q2: 数据安全吗？
A: 飞书是阿里系，数据在云端。如需完全本地，可用飞书导出后本地存储

### Q3: 我需要学编程吗？
A: 不需要，我帮你集成好，你直接用飞书界面

### Q4: 手机上能用吗？
A: 能，飞书有手机App

---

*文档由 AI 自动生成*
