# Obsidian 贷款产品知识库使用指南

## 📋 目录

- [1. 安装与配置](#1-安装与配置)
- [2. 文件结构](#2-文件结构)
- [3. 核心功能](#3-核心功能)
- [4. 数据查询](#4-数据查询)
- [5. 模板使用](#5-模板使用)
- [6. 插件推荐](#6-插件推荐)
- [7. 数据备份](#7-数据备份)
- [8. 常见问题](#8-常见问题)

---

## 1. 安装与配置

### 1.1 下载安装

1. 访问 https://obsidian.md
2. 下载桌面版（Windows/Mac/Linux）
3. 安装并注册账号

### 1.2 推荐设置

- 主题：浅色模式（工作）
- 字体：系统默认
- 字号：16px
- 行距：宽松

### 1.3 核心插件（需开启）

- **Dataview** - 数据库查询（必需）
- **Templater** - 模板（必需）
- **Obsidian Git** - Git 备份（推荐）
- **Table Editor** - 增强表格（推荐）

---

## 2. 文件结构

```
Obsidian Vault/
├── 📦 贷款产品知识库/
│   ├── 📦 产品库/
│   │   ├── 📦 工商银行/
│   │   │   ├── 融e借.md
│   │   │   └── ...
│   │   ├── 📦 建设银行/
│   │   └── ...
│   ├── 📦 知识库/
│   │   ├── 📚 贷款基础/
│   │   ├── 📚 产品攻略/
│   │   ├── 📚 申请流程/
│   │   ├── 📚 FAQ/
│   │   └── 📚 案例分享/
│   ├── 📦 工具/
│   │   ├── 贷款计算器.md
│   │   └── 产品对比表.md
│   ├── 📦 附件/
│   │   ├── 银行Logo/
│   │   └── 流程图/
│   ├── 📦 Templates/ (模板文件夹)
│   │   ├── TEMPLATE-产品.md
│   │   ├── TEMPLATE-产品攻略.md
│   │   └── ...
│   ├── 📦 .obsidian/ (设置文件夹)
│   └── 📄 贷款产品知识库.md (主入口)
```

### 2.1 如何导入模板

1. 复制 `Templates/` 文件夹到你的 Vault 根目录
2. 在 Obsidian 设置中配置模板文件夹路径：
   - Settings → Templater → Template folder location
   - 设置为 `Templates`

### 2.2 如何使用模板

1. 按 `Ctrl/Cmd + P` 打开命令面板
2. 输入 `Templater: Open Insert Template Modal`
3. 选择模板
4. 自动填充内容

---

## 3. 核心功能

### 3.1 产品数据库查询

使用 Dataview 语法查询产品：

```dataview
TABLE bank, rate, maxAmount, approvalTime
FROM "产品库"
WHERE status = "在推"
SORT rate ASC
```

### 3.2 筛选条件

| 条件 | 语法 | 示例 |
|------|------|------|
| 等于 | `= "值"` | `bank = "工商银行"` |
| 不等于 | `!= "值"` | `status != "暂停"` |
| 小于 | `< 数值` | `rate < 4` |
| 大于 | `> 数值` | `maxAmount > 200000` |
| 包含 | `contains(字段, "值")` | `contains(bank, "工商")` |
| 且 | `AND` | `rate < 4 AND approvalTime = "快"` |
| 或 | `OR` | `bank = "工商" OR bank = "建行"` |

### 3.3 排序

```dataview
TABLE rate, maxAmount
FROM "产品库"
WHERE status = "在推"
SORT rate ASC        # 按利率升序
SORT maxAmount DESC  # 按额度降序
```

### 3.4 限制数量

```dataview
TABLE rate, maxAmount
FROM "产品库"
LIMIT 10  # 只显示前10条
```

---

## 4. 数据查询

### 4.1 常用查询模板

#### 按银行查询

```dataview
TABLE rate, maxAmount, approvalTime, successRate
FROM "产品库"
WHERE bank = "工商银行" AND status = "在推"
SORT rate ASC
```

#### 低利率产品

```dataview
TABLE bank, productName, rate, maxAmount
FROM "产品库"
WHERE rate < 4 AND status = "在推"
SORT rate ASC
```

#### 高佣金产品

```dataview
TABLE bank, productName, commission
FROM "产品库"
WHERE commission > 1.5 AND status = "在推"
SORT commission DESC
```

#### 快速审批产品

```dataview
TABLE bank, productName, rate, approvalTime
FROM "产品库"
WHERE approvalTime = "快" AND status = "在推"
```

### 4.2 客户匹配查询

#### 公积金客户

```dataview
TABLE bank, productName, rate, maxAmount
FROM "产品库"
WHERE contains(requiredConditions, "公积金") AND status = "在推"
```

#### 房贷客户

```dataview
TABLE bank, productName, rate, maxAmount
FROM "产品库"
WHERE contains(requiredConditions, "房贷") AND status = "在推"
```

### 4.3 统计查询

#### 产品数量统计

```dataview
TABLE length(rows) AS "产品数量"
FROM "产品库"
GROUP BY status
```

#### 银行产品分布

```dataview
TABLE length(rows) AS "产品数量"
FROM "产品库"
GROUP BY bank
SORT length(rows) DESC
```

---

## 5. 模板使用

### 5.1 创建新产品

1. 按 `Ctrl/Cmd + P`
2. 输入 `Templater: Open Insert Template Modal`
3. 选择 `TEMPLATE-产品.md`
4. 填写产品信息
5. 保存到对应银行文件夹

### 5.2 模板字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| bank | 银行名称 | 工商银行 |
| productName | 产品名称 | 融e借 |
| rate | 年利率 | 3.65 |
| minAmount | 最低额度 | 50000 |
| maxAmount | 最高额度 | 3000000 |
| term | 期限（月） | 36 |
| commission | 佣金比例 | 1.5 |

### 5.3 自定义模板

如需修改模板：
1. 打开 `TEMPLATE-产品.md`
2. 修改内容
3. 保存
4. 新创建的页面会使用新模板

---

## 6. 插件推荐

### 必需插件

| 插件 | 功能 | 设置 |
|------|------|------|
| Dataview | 数据库查询 | 开启即可 |
| Templater | 模板管理 | 设置模板文件夹 |

### 推荐插件

| 插件 | 功能 | 推荐度 |
|------|------|--------|
| Obsidian Git | Git 备份 | ⭐⭐⭐⭐⭐ |
| Table Editor | 增强表格 | ⭐⭐⭐⭐ |
| QuickAdd | 快速创建 | ⭐⭐⭐⭐ |
| DataviewJS | 高级查询 | ⭐⭐⭐ |
| Calendar | 日历视图 | ⭐⭐⭐ |
| Kanban | 看板视图 | ⭐⭐⭐ |

### 6.1 安装插件

1. Settings → Community plugins
2. 关闭安全模式
3. 浏览搜索插件名
4. 安装并启用

### 6.2 配置 Obsidian Git

1. 安装插件
2. Settings → Git → Initialize repo
3. 设置 GitHub 仓库
4. 设置自动备份频率

---

## 7. 数据备份

### 7.1 使用 Git 备份（推荐）

#### 步骤

1. 在 GitHub 创建仓库
2. Settings → Git → Initialize new repository
3. 设置远程仓库 URL
4. 设置自动备份（如每小时）

#### 备份命令

- **手动备份**: `Ctrl/Cmd + P` → `Git: Commit all changes`
- **自动备份**: 设置中配置

### 7.2 手动备份

1. 复制整个 Vault 文件夹
2. 压缩为 zip
3. 存放到网盘/硬盘

### 7.3 备份频率建议

| 备份类型 | 频率 | 说明 |
|----------|------|------|
| Git 自动 | 每小时 | 增量备份 |
| 本地备份 | 每天 | 完整备份 |
| 异地备份 | 每周 | 存到网盘 |

---

## 8. 常见问题

### Q1: Dataview 不显示数据？

**解决方法**：
1. 确保文件在正确文件夹
2. 确保 frontmatter 格式正确
3. 重启 Obsidian

### Q2: 模板不工作？

**解决方法**：
1. 检查模板文件夹路径设置
2. 确保有 Templater 权限
3. 按 `Ctrl/Cmd + P` 运行命令

### Q3: 查询结果为空？

**解决方法**：
1. 检查文件路径是否正确
2. 检查字段名是否一致
3. 检查条件是否正确

### Q4: 如何分享给客户？

**方法1: 使用 Publish（需付费）**
- Obsidian → Publish
- 选择要分享的页面
- 获取链接分享给客户

**方法2: 导出为 HTML**
- 导出为静态 HTML
- 上传到网站

**方法3: 截图分享**
- 截取表格/页面
- 发送图片给客户

### Q5: 手机上能用吗？

**能！**
- 下载 Obsidian 手机 App
- 登录账号
- 同步后即可使用
- 支持查看和编辑

---

## 📞 获取帮助

- Obsidian 官方文档：https://help.obsidian.md
- Dataview 文档：https://blacksmithgu.github.io/obsidian-dataview/
- Obsidian 中文社区：搜索「Obsidian」

---

## 📁 文件清单

```
obsidian-templates/
├── 📦 产品库/
│   ├── 📦 工商银行/
│   │   └── 融e借.md (示例产品)
│   ├── 📦 建设银行/
│   └── 产品数据库索引.md
├── 📦 知识库/
│   └── 📦 产品攻略/
│       └── TEMPLATE-产品攻略.md
├── 📦 工具/
│   └── 贷款计算器.md
├── 📦 Templates/
│   ├── TEMPLATE-产品.md
│   └── TEMPLATE-产品攻略.md
├── 📄 贷款产品知识库.md (主入口)
└── 📄 OBSIDIAN使用指南.md (本文档)
```

---

**最后更新**: 2026-01-29
**版本**: 1.0
