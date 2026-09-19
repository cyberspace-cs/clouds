---
name: agent-optimization
description: |
  中文名：智能体优化。基于 ECC (Everything Claude Code, 261k★) 最佳实践，优化 AI 编程智能体的上下文预算、性能表现和代码质量。English: Optimize AI coding agent performance using ECC best practices (context budget, performance tuning, security scanning). Use when: 智能体优化、agent 慢、上下文不够用、coding agent 性能差、ECC、everything claude code、优化 Claude Code、优化 Cursor。
---

# Agent Optimization (ECC 沉淀)

基于 **Everything Claude Code (ECC, 261k★)** 的生产级最佳实践，优化你的 AI 编程智能体。

> 来源：affaan-m/everything-claude-code — Anthropic 黑客松获胜项目，10+ 个月日常使用打磨

## 三大核心优化维度

### 1. 上下文预算优化 (Context Budget)

**问题**：上下文窗口不够用，agent 越跑越慢、越跑越笨

**ECC 最佳实践**：

- **按需加载**：不要把所有文件都读进上下文，只读当前任务相关的
- **渐进式披露**：
  - 第一层：文件列表 + 函数签名（永远在上下文里）
  - 第二层：函数体（需要时才读）
  - 第三层：完整实现 + 注释（debug 时才读）
- **记忆压缩**：长对话里旧的内容自动摘要，保留关键结论
- **工具调用结果裁剪**：大输出只保留前 N 行 + 末尾 N 行

**自查清单**：
- [ ] 当前任务真的需要读这个文件吗？
- [ ] 能不能用 grep 代替 read？
- [ ] 能不能把旧对话总结成 3 行？

### 2. 性能优化 (Performance)

**问题**：agent 执行太慢、token 烧钱

**ECC 最佳实践**：

- **批量操作**：能一次做完的不要分三次
  - ❌ 先读文件 → 再写文件 → 再验证
  - ✅ 直接写 + 验证（如果模式明确）
- **缓存命中**：
  - 重复用的 prompt 模板存下来
  - 常用的正则/解析逻辑写成脚本
- **并行工具调用**：独立的 API 调用并行发，不要串行等
- **减少"确认"轮次**：简单操作直接做，不要问"我可以改这个吗？"

**自查清单**：
- [ ] 这个操作能不能脚本化？
- [ ] 这些调用有没有依赖关系？能不能并行？
- [ ] 我是不是在问"我可以做 X 吗"而不是直接做 X？

### 3. 安全扫描 (Security Review)

**问题**：AI 生成的代码有安全漏洞

**ECC + OCR 最佳实践**：

**自动检查清单**（每次生成代码后跑）：
- [ ] 有没有硬编码的密钥/Token？
- [ ] 有没有 SQL 注入风险？
- [ ] 有没有 XSS 风险？
- [ ] 有没有路径遍历风险？
- [ ] 有没有 bare except？
- [ ] 有没有 eval/exec？
- [ ] 有没有不安全的 pickle？

**OCR (alibaba/open-code-review, 34k★) 集成**：
```bash
# 如果你装了 OCR CLI，跑一遍代码审查
ocr review --staged
```

## 什么时候触发这个 skill

- 你觉得 agent 跑的越来越慢
- 上下文窗口经常爆
- 生成的代码有安全漏洞
- 想优化 coding agent 的工作流

## 和其他 skill 的配合

| 场景 | 配合哪个 skill |
| --- | --- |
| 代码写完了要审查 | + code-review-and-quality |
| 发布前要安全检查 | + pre-publish-security-check |
| 写新 skill 要规范 | + writing-skills |
