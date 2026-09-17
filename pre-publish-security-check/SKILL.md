---
name: pre-publish-security-check
description: '中文名：安全检查。在把项目推送到 GitHub / 公开发布前，检查整个项目是否存在敏感信息泄露风险：密码或 Token、个人隐私、本地绝对路径、临时文件、测试垃圾文件、不应公开的内容。English: Scan a project for leaked secrets (tokens/passwords), private info, absolute local paths, temp files, test junk and other non-public content before publishing; report findings first, never run Git ops unprompted. Use when: 安全检查、发布前检查、推 GitHub 前检查、开源前检查、防止泄露 Token、敏感信息检查。'
---

# 安全检查

## 目标

在推送/发布项目前，系统性检查整个项目是否存在不应公开的内容，先报告检查结果，**不要执行 Git 操作**。

## 输入

- 必需：项目目录路径（或待发布仓库）。
- 可选：重点关注项（如密钥、隐私数据）。

## 工作流

### 1. 扫描清单（逐项检查）

| 检查项 | 查找内容 |
|---|---|
| 密码或 Token | `ghp_`、`sk-`、`api_key`、`password`、`secret`、`token`、`.env` 文件、`config.*` 中的硬编码密钥 |
| 个人隐私 | 姓名、电话、邮箱、身份证、住址、工资、真实身份信息 |
| 本地绝对路径 | `/home/`、`/Users/`、`C:\Users\`、`/root/` 等本地路径泄漏 |
| 临时文件 | `*.tmp`、`*.log`、`.DS_Store`、`Thumbs.db`、`*.bak`、`~` 结尾文件 |
| 测试垃圾文件 | `test-output/`、mock 数据中的真实凭证、调试残留、截图/日志 |
| 不应公开的内容 | 内部文档、未脱敏数据、第三方版权素材、私有业务信息 |

### 2. 检查方法

- 先看 `.gitignore`：确认哪些文件本就不该提交。
- 用 Grep 搜索敏感模式（大小写不敏感）：`ghp_|sk-[A-Za-z0-9]|api[_-]?key|secret|password|token|BEGIN.*PRIVATE KEY`。
- 检查所有 `*.env*`、`config.*`、`*.json` 配置文件内容。
- 列出仓库中所有非源码文件（图片、日志、压缩包、备份），判断是否必要。

### 3. 输出风险报告

```markdown
## 安全检查报告

**结论**：✅ 可发布 / ⚠️ 有风险需处理 / ❌ 禁止发布

### 🔴 高危（必须处理）
- 文件：`xxx/.env`（第 3 行）
  风险：包含真实 API Token
  建议：从版本控制移除 + 吊销该 Token + 改用环境变量

### 🟡 中危（建议处理）
- ...

### 🟢 低危（可选）
- ...

### 已确认安全
- .gitignore 覆盖：...
```

### 4. 处理规则

- **先报告，不执行任何 Git 操作**（不 commit、不 push、不 reset），除非用户明确要求修复。
- 高危项给出具体处理步骤：移除文件、吊销密钥、改用环境变量/密钥管理。
- 检查范围如实说明：查了什么、没查什么，不夸大结论。

## 检查清单

- [ ] 六类检查项全部覆盖
- [ ] 用 Grep 搜索了常见敏感模式
- [ ] .env / config 文件内容已检查
- [ ] 报告按高危/中危/低危分级，含文件与行号
- [ ] 未在用户要求前执行任何 Git 操作
