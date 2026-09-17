# ☁️ buleboy 的 clouds —— 我的专属 Skill 集合

> **Everything is Skill-Composable.** 把常用工作流打包成可随时调用的 Skill，配合豆包工作任务模式 / AI Agent 一键安装即用。

每个中文目录就是一个独立的 Skill（`SKILL.md` 含触发描述与完整流程），按需调用，随取随用。

## 🚀 快速开始

在豆包（工作任务模式）或任意支持 Skills 的 Agent 中直接说：

> 帮我安装 GitHub 上 cyberspace-cs 的 clouds，直接用「xxx Skill」帮我处理 …

或者按目录读取对应 Skill 的 `SKILL.md` 即可获得完整工作流。

## 📦 Skill 列表

| 方向 | Skill | 一句话说明 |
| --- | --- | --- |
| 🖥️ 编程 | [代码评审](./代码评审/) | 五维度代码审查：正确性 / 安全 / 性能 / 可读性 / 架构，输出分级修改建议 |
| 🖥️ 编程 | [刷题教练](./刷题教练/) | LeetCode / 算法刷题：定制路线、逐题精讲、遗忘曲线复习 |
| 🖥️ 编程 | [页面上线](./页面上线/) | 一键把项目部署到 GitHub Pages：构建探测 + workflow + 白屏排障 |
| 📄 展示 | [主页美化](./主页美化/) | 生成 liyupi 风格的 GitHub 个人主页 README（徽章/表格/置顶项目） |
| 📄 展示 | [简历制作](./简历制作/) | 制作可部署的个人简历/作品集网页（单页 HTML 或 React 工程） |
| 📄 展示 | [项目拆解](./项目拆解/) | 深度拆解开源项目，产出中文学习指南（名片/创意/架构/学习路线） |
| 🎨 UI 设计 | [界面设计](./界面设计/) | 前端界面设计落地规范：设计原则 / 设计系统 / 组件规范 / 交付检查 |

## 🧩 目录结构

```text
clouds/
├── README.md          # 本说明
├── 代码评审/SKILL.md   # 每个中文目录 = 一个 Skill
├── 刷题教练/SKILL.md
├── 页面上线/SKILL.md
├── 主页美化/SKILL.md
├── 简历制作/SKILL.md
├── 项目拆解/SKILL.md
└── 界面设计/SKILL.md
```

## 🛠️ Skill 规范

每个 Skill 遵循标准格式：

- `SKILL.md` 必备，含 YAML frontmatter（`name` + `description` 触发条件）与 Markdown 流程正文
- 可选 `scripts/`（可执行脚本）、`references/`（参考文档）、`assets/`（模板资产）
- 描述清晰，Agent 读到描述即可判断何时调用

## ⭐ 说在后面

这套 Skill 全部来自真实项目实战沉淀（GitHub 主页整理、Pages 部署、ShiftX 拆解、刷题平台、简历网页），不是通用模板——用的时候你会感受到"有人踩过坑"的细节。

欢迎 Star ⭐、Fork、提 Issue 共建你的专属 Skill。
