---
name: github-profile-beautify
description: '中文名：主页美化。把 GitHub 个人主页 README 从普通列表升级为专业开发者名片：徽章栏、定位句、置顶重点、在线作品、统计卡片，参考 liyupi（程序员鱼皮）风格。Use when: 主页美化、美化 GitHub 主页、写 profile README、参考鱼皮风格做主页、主页像 xxx 一样好看。'
---

# GitHub 主页美化

## 目标

让 profile README 在 3 秒内传达三件事：**你是谁、你做什么、你最值得看什么**。风格参考 liyupi（程序员鱼皮）：徽章开头、一句话定位、emoji 分节、表格导航、统计卡片收尾。

## 输入

- 必需：GitHub 用户名。
- 可选：目标风格、希望置顶的项目、在线展示站点、偏好语言。

## 工作流

### 1. 取证（先摸底再动笔，不凭印象）

用 GitHub API 拉取用户真实数据：

```bash
# 用户信息
curl -s -H "Authorization: Bearer $TOKEN" https://api.github.com/users/<username>
# 仓库列表（按更新时间与创建时间两个维度）
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/users/<username>/repos?per_page=100&sort=updated"
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/users/<username>/repos?per_page=100&sort=created"
```

记录：昵称、粉丝数、仓库数、语言分布、重点项目（自研 vs fork）、star 情况、是否有可用的 GitHub Pages 站点。

若账号没有 profile 仓库（`<username>/<username>`），先创建：`POST /user/repos`，`name` 与用户名一致，`auto_init: true`。

### 2. 结构（liyupi 式区块）

```markdown
# 👋 Hi, I'm <昵称>（<用户名>）

> 一句话定位：领域 + 角色 + 独特标签
> 副句：在做什么、关注什么

<div align="center">  徽章行（数量徽章 + 技术栈徽章）  </div>

---

## 🧑💻 关于我
- 主攻方向 / 技术栈 / 学习方法 / 目标

## 🚀 正在做什么        ← 表格：板块 | 说明
## 🌐 在线展示页面       ← 表格：站点 | 地址 | 说明（有 Pages 才写）
## 📂 精选项目           ← 自研项目表 + fork 精选表（标注来源）
## 📈 GitHub 统计        ← github-readme-stats 卡片
## 📫 联系我             ← 一句交流意愿 + Star 邀请
```

### 3. 写作规则

- **置顶重点**：获奖 / 重磅项目（如黑客松获奖）放"关于我"之后，用五维度表格：在线预览 / 核心创意 / 架构亮点 / 学习指南 / 源码仓库。
- **数量真实**：粉丝数、star 数、仓库数来自 API 实测，禁止编造；不确定的标注"待补充"。
- **分类清晰**：自研项目与 fork 精选分开；fork 标注"fork 自 <upstream>"，体现"拆解学习"的路径。
- **表格优先**：项目列表一律用表格（项目链接 + 一句话说明），不用散列表述。
- **保持克制**：徽章 6-10 枚足够，不堆砌；分节用 emoji + 中文短标题。

### 4. 推送与验证

- 先 `GET repos/<owner>/<owner>/contents/README.md` 拿 `sha`，再 `PUT` 覆盖提交（message 写明改动内容）。
- 浏览器打开 `github.com/<owner>` 验证：徽章渲染、表格对齐、链接可点、统计卡片加载。

## 检查清单

- [ ] 首屏 3 秒能看出身份与方向
- [ ] 徽章行渲染正常（数量来自 API）
- [ ] 重点/获奖项目置顶且有完整表格
- [ ] 在线展示页链接逐一可访问
- [ ] 自研与 fork 分类清晰、来源标注
- [ ] 浏览器验证主页渲染无异常
