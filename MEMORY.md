# MEMORY.md - Long-Term Memory

*Curated memories, distilled from daily notes. This is your "long-term memory" — the essence of what matters.*

---

## 关于用户

**企业主** - 单人运营，工作时间长（从醒来到入睡）
**位置**: 武汉汉阳
**目标**: 自动化工作流程、增加营收、减少工作量

**业务**:
- **主业**: 武汉贷款中介
- **发展方向**: 自媒体（小红书、抖音等）

**项目**: MyMoltbot
- 技术栈: Next.js + React + TypeScript + Tailwind CSS
- 仓库: https://github.com/jiangzhuizzz/MyMoltbot
- CodeSpace: https://automatic-space-halibut-qgjx69w7gwr2x9wx-18789.app.github.dev:3001

**偏好**:
- 中文优先
- 避免蓝紫渐变色配色
- 使用 GitHub Codespace 开发
- 端口避免与 18789 冲突
- 编程小白，需要简单易用的工具

**沟通风格**:
- 正常文字回复，不需要语音
- 完成工作后创建 PR 供审核，不实时推送
- 希望 AI 主动发现问题并提出解决方案

## 待完成/思考

**已完成**（2026-01-30 更新）:
1. ✅ **Obsidian贷款产品知识库模板**
   - 路径：/workspaces/MyMoltbot/obsidian-templates/
   - 包含：产品数据库、知识库、工具箱、模板系统
   - 文档：OBSIDIAN使用指南.md

2. ✅ **每日早报系统**
   - 路径：/home/codespace/clawd/daily-report/
   - 内容：贷款产品、自媒体热点、行业新闻、天气、LPR
   - 功能：每天9点自动生成并发送到WhatsApp
   - WhatsApp 测试消息已发送成功

3. ✅ **Codespace 保活脚本**
   - 路径：/home/codespace/codespace-keepalive.sh
   - 功能：每5分钟发送心跳，保持Codespace活跃
   - PID: 20776
   - 限制：免费版最长30分钟无操作超时，Pro版60分钟

**技术债务/考虑**:
1. **Codespace 永不掉线方案**
   - 当前方案：保活脚本（每5分钟心跳）
   - 根本方案：升级 GitHub 计划 或 迁移到云服务器
   - 云服务器选项：AWS EC2 / Google Cloud / 阿里云（$5-20/月）
   - 平台选项：Railway / Render / Fly.io（免费/付费）

**业务需求**（2026-01-29 18:27 更新）:
1. **贷款产品库** - 整理各银行贷款产品信息，方便快速查找和匹配 ✅ (模板完成)
2. **自媒体运营** - 小红书、抖音内容创作和发布 📅 (选题推荐已集成)
3. **客户获取** - 提高寻找目标客户（贷款需求者）的效率 📋 (待开发)
4. **生产力工具** - 自动化重复工作，减少手动操作 ✅ (早报系统)
