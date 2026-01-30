---
tags: [产品, 信用贷, {{bank}}]
type: 贷款产品
bank: {{bank}}
rate: {{rate}}
minAmount: {{minAmount}}
maxAmount: {{maxAmount}}
term: {{term}}
status: {{status}}
updated: {{date}}
---

# {{bank}} - {{productName}}

## 基本信息

| 项目 | 内容 |
|------|------|
| 银行 | {{bank}} |
| 产品名称 | {{productName}} |
| 产品类型 | {{productType}} |
| 利率 | {{rate}}% |
| 额度范围 | {{minAmount}}-{{maxAmount}}万 |
| 最长期限 | {{term}}个月 ({{term/12}}年) |
| 审批时间 | {{approvalTime}} |
| 通过率 | {{successRate}} |

## 申请条件

### 必要条件
{{#each requiredConditions}}
- [ ] {{this}}
{{/each}}

### 加分项（满足更容易通过）
{{#each bonusConditions}}
- [ ] {{this}}
{{/each}}

### 禁止条件（这些情况不能申请）
{{#each forbiddenConditions}}
- [ ] {{this}}
{{/each}}

## 申请要求

{{requirements}}

## 申请流程

{{#each applicationProcess}}
{{@index}}. {{this}}
{{/each}}

## 所需材料

{{#each requiredDocuments}}
- [ ] {{this}}
{{/each}}

## 优势

{{#each pros}}
1. {{this}}
{{/each}}

## 劣势

{{#each cons}}
1. {{this}}
{{/each}}

## 佣金信息

| 项目 | 金额 |
|------|------|
| 佣金比例 | {{commission}}% |
| 预估佣金 | {{estimatedCommission}}元 |
| 结算方式 | {{settlementMethod}} |

## 适合人群

{{#each targetAudience}}
- [ ] {{this}}
{{/each}}

## 适合场景

{{suitableScenarios}}

## 注意事项

⚠️ {{warnings}}

## 常见问题

**Q: 这个产品适合什么样的人？**
A: {{faq1}}

**Q: 审批需要多长时间？**
A: {{faq2}}

**Q: 如果被拒了怎么办？**
A: {{faq3}}

## 申请链接

[立即申请]({{applyLink}})

## 相关产品

- [[{{relatedProduct1}}]]
- [[{{relatedProduct2}}]]
- [[{{relatedProduct3}}]]

## 备注

{{notes}}

---

**最后更新**: {{updated}}
**作者**: {{author}}
**版本**: {{version}}
