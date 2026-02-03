# 产品库自动化完善系统

> 自动采集产品数据，创建PR供审核，定期互动讨论

## 📁 文件结构

```
product-collector/
├── 📄 main.sh              # 主脚本（整合所有功能）
├── 📄 collector.py         # 产品数据采集器
├── 📄 git-workflow.sh      # Git工作流（创建PR）
├── 📄 import-manual.sh     # 产品手册导入工具
├── 📄 interaction.py       # 互动讨论系统
├── 📄 notify-user.py       # 用户通知系统
├── 📁 data/                # 数据存储
├── 📁 logs/                # 日志文件
├── 📁 manuals/             # 产品手册目录
└── 📁 scripts/             # 辅助脚本
```

## 🚀 快速开始

### 1. 运行完整流程

```bash
cd /home/codespace/clawd/product-collector
bash main.sh
```

### 2. 单独运行

```bash
# 采集产品数据
python3 collector.py

# 导入手册
bash import-manual.sh --dir

# 创建PR
bash git-workflow.sh

# 检查是否需要讨论
python3 interaction.py
```

## 📦 功能说明

### 1. 自动采集

从以下来源采集产品数据：
- 银行官网
- 贷款资讯网站（融360等）
- 微信公众号

**支持的银行**：
- 工商银行、招商银行、建设银行、农业银行、中国银行、交通银行、平安银行等

### 2. Git工作流

自动创建 PR 供审核：

1. 采集新产品数据
2. 创建新分支
3. 生成 Obsidian 页面
4. 提交更改
5. 创建 Pull Request

### 3. 产品手册导入

支持格式：
- PDF (.pdf) - 需要手动提取
- Word (.docx) - 自动解析
- Excel (.xlsx, .xls) - 自动解析
- CSV (.csv) - 自动解析
- Markdown (.md) - 直接导入
- JSON (.json) - 自动解析

**使用方法**：
```bash
# 导入单个文件
bash import-manual.sh ./产品手册.pdf

# 导入目录下所有文件
bash import-manual.sh --dir
```

### 4. 互动讨论

定期与用户讨论产品库完善：

- 数据完整度检查
- 新产品建议
- 数据更新提醒
- 合作银行拓展

## ⚙️ 配置

### 环境变量

```bash
# GitHub 配置
export GITHUB_TOKEN="your-token"

# 工作目录
export REPO_DIR="/workspaces/MyMoltbot"
```

### GitHub Token

需要设置 GitHub Personal Access Token：

1. GitHub → Settings → Developer settings → Personal access tokens
2. 生成新 token（需要 repo 权限）
3. 设置环境变量或配置 gh CLI

## 📅 定时任务

### 自动运行（每天2次）

```bash
# 添加到 crontab
0 8 * * * cd /home/codespace/clawd/product-collector && bash main.sh
0 20 * * * cd /home/codespace/clawd/product-collector && bash main.sh
```

### 手动运行

```bash
# 每天早上8点、晚上8点自动执行
```

## 💬 互动流程

### 1. 定期讨论

- 每3天检查一次是否需要讨论
- 发送讨论话题到 WhatsApp
- 用户回复后处理相应话题

### 2. PR 审核

1. 系统创建 PR
2. 发送通知到 WhatsApp
3. 用户在 GitHub 审核
4. 合并后数据自动更新

### 3. 紧急事项

- 利率重大变化
- 新产品上线
- 政策调整

## 📊 工作流程

```
┌─────────────────────────────────────────────────────┐
│                   产品库完善流程                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1️⃣ 采集数据  →  2️⃣ 整理格式  →  3️⃣ 创建PR        │
│       ↓                    ↓              ↓        │
│  银行官网/资讯     Obsidian模板        GitHub审核   │
│                                                     │
│  4️⃣ 合并更新  →  5️⃣ 通知用户  →  6️⃣ 定期讨论      │
│       ↓                    ↓              ↓        │
│  主分支更新       WhatsApp通知        优化建议      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 🔧 自定义

### 添加新银行

编辑 `collector.py`：

```python
def parse_new_bank(self):
    """采集新银行产品"""
    product = {
        'bank': '新银行名',
        'productName': '产品名',
        'rate': '利率',
        # ... 其他字段
    }
    self.products.append(product)
```

### 修改模板

编辑 `collector.py` 中的 `generate_obsidian_page()` 方法。

### 调整采集频率

编辑 `main.sh` 中的 crontab 设置。

## 📝 日志

- `logs/collector.log` - 采集日志
- `logs/git.log` - Git操作日志
- `logs/interaction.log` - 互动日志

## ❓ 常见问题

### Q: 采集失败怎么办？

A: 检查日志 `logs/collector.log`，常见原因：
- 网络问题
- 网站结构变化
- 需要登录认证

### Q: PR 没有自动创建？

A: 可能原因：
- 没有新的产品数据
- GitHub Token 未配置
- gh CLI 未安装

### Q: 如何手动触发PR？

```bash
cd /workspaces/MyMoltbot
git add -A
git commit -m "手动更新"
git push
# 然后手动在 GitHub 创建 PR
```

## 📞 支持

有问题请在 GitHub Issues 反馈。

---

**最后更新**: 2026-01-30
**版本**: 1.0
