---
name: github-profile-beautify
description: 生成或优化 GitHub 个人主页 README（profile README），打造 liyupi（程序员鱼皮）风格的开发者主页。当用户要求"整理 GitHub 主页 / 美化个人主页 / 写 profile README / 参考鱼皮风格做主页 / 主页像 xxx 一样好看"时使用。适用于 cyberspace-cs.github.io 或任意 GitHub 账号的 README.md 创作与重构。
---

# GitHub 主页美化

## 目标

把 GitHub 个人主页 README 从"普通列表"升级为"专业开发者名片"：一眼看清身份、方向、核心项目与在线作品，参考 liyupi（程序员鱼皮）风格。

## 核心流程

### 1. 摸底数据（先取证再动笔）

- 用 GitHub API 拉用户信息与仓库列表：
  ```bash
  curl -s -H "Authorization: Bearer $TOKEN" https://api.github.com/users/<username>
  curl -s -H "Authorization: Bearer $TOKEN" https://api.github.com/users/<username>/repos?per_page=100&sort=updated
  ```
- 记录：昵称、粉丝数、仓库数、语言分布、按 updated 与 created 两个维度的仓库排序、star 分布、fork 的重点仓库。
- 若目标账号没有 profile 仓库（`<username>/<username>`），需要先创建（POST /user/repos，name 与用户名一致，auto_init=true）。

### 2. 参考风格对照（liyupi 式结构）

| 区块 | 内容要点 |
|---|---|
| 标题行 | `# 👋 Hi, I'm <昵称>` 一句话身份定位 |
| 徽章栏 | followers / stars / repos 数量徽章 + 技术栈徽章，用 `img.shields.io/badge` |
| 一句话简介 | 定位 + 关注领域 + 学习方法 |
| emoji 分节 | 🧑💻 关于我 / 🛠️ 技术栈 / 🚀 正在做什么 / 🌐 在线作品 / 📂 精选项目 / 📊 统计卡片 |
| 项目表格 | 双列表：项目名(链接) + 一句话说明，重点项目放最前或加醒目区块 |
| 统计卡片 | `https://github-readme-stats.vercel.app/api?username=xxx` |

### 3. 写作规则

- **置顶重点项目**：如果用户有获奖/重磅项目（如黑客松获奖），用专门区块放"关于我"之后、其他内容之前，表格维度：在线预览 / 核心创意 / 架构亮点 / 学习指南 / 源码仓库。
- **在线展示页区块**：凡有 GitHub Pages 站点，单独一节列出：站点名 + 链接 + 一句话说明。
- **项目分两类**：自建项目（用户自己写的）与精选 fork（拆解学习的），fork 项目标注"fork 自 xxx"。
- **内容真实**：所有数字、链接、获奖信息必须来自 API/仓库实测，禁止编造；不确定的标注待补充。
- 全中文为主，英文标题可保留，保持简洁，不堆砌。

### 4. 提交推送

- 先 GET `repos/<owner>/<owner>/contents/README.md` 拿 sha，再 PUT 覆盖（message 写明改动）。
- 推送后必须用浏览器访问 `github.com/<owner>` 验证渲染：徽章、表格、链接均正常显示。

## 检查清单

- [ ] 徽章栏渲染正常
- [ ] 重点/获奖项目置顶且有完整五维度表格
- [ ] 在线展示页链接可点击且地址正确
- [ ] 所有数字来自 API 实测
- [ ] 浏览器验证主页渲染无异常
