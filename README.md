# ☁️ buleboy 的 clouds —— 专属 Skill 集合

> **Everything is Skill-Composable.** 把常用工作流打包成可随时调用的 Skill，配合豆包工作任务模式 / AI Agent 一键安装即用。

每个中文目录就是一个独立的 Skill（`SKILL.md` 含触发描述与完整流程），按需调用，随取随用。

## 🚀 快速开始

在豆包（工作任务模式）或任意支持 Skills 的 Agent 中直接说：

> 帮我安装 GitHub 上 cyberspace-cs 的 clouds，直接用「xxx Skill」帮我处理 …

或者按目录读取对应 Skill 的 `SKILL.md` 即可获得完整工作流。

## 📦 Skill 列表

### 🖥️ 编程

| Skill | 一句话说明 | 来源 |
| --- | --- | --- |
| [排障](./排障/) | 硬 bug 诊断：先建反馈回路再定位，二分/属性/差分等 10 种循环构建法 | mattpocock/skills（MIT） |
| [测试驱动](./测试驱动/) | TDD 红绿循环：好的测试长什么样、测试缝、反模式 | mattpocock/skills（MIT） |
| [刷题教练](./刷题教练/) | LeetCode 刷题：定制路线、逐题精讲、遗忘曲线复习 | 自研（buleboy） |
| [页面上线](./页面上线/) | 一键部署 GitHub Pages：构建探测 + workflow + pnpm 坑 + 白屏排障 | 自研（buleboy） |

### 📄 展示与内容

| Skill | 一句话说明 | 来源 |
| --- | --- | --- |
| [主页美化](./主页美化/) | 生成 liyupi 风格的 GitHub 个人主页 README | 自研（buleboy） |
| [简历制作](./简历制作/) | 制作可部署的个人简历/作品集网页 | 自研（buleboy） |
| [项目拆解](./项目拆解/) | 深度拆解开源项目，产出中文学习指南 | 自研（buleboy） |
| [图表](./图表/) | 根据数据生成准确、可访问的 HTML 图表与报告 | lvy010/clouds（MIT） |
| [人话](./人话/) | 保留事实与观点，把生硬中文改得自然易读 | lvy010/clouds（MIT） |

### 🎨 UI 与输出风格

| Skill | 一句话说明 | 来源 |
| --- | --- | --- |
| [前端设计](./前端设计/) | 有辨识度的前端视觉设计：美学方向、字体、布局，拒绝模板感 | anthropics/skills（Apache 2.0） |
| [直给回答](./直给回答/) | ADHD 友好输出：先给行动、编号步骤、每轮重述、抑制废话 | ayghri/i-have-adhd（MIT） |

## 🧩 目录结构

```text
clouds/
├── README.md          # 本说明
├── LICENSES.md        # 各 Skill 许可证与来源
├── 排障/SKILL.md       # 每个中文目录 = 一个 Skill
├── 测试驱动/SKILL.md
├── 刷题教练/SKILL.md
├── 页面上线/SKILL.md
├── 主页美化/SKILL.md
├── 简历制作/SKILL.md
├── 项目拆解/SKILL.md
├── 图表/SKILL.md
├── 人话/SKILL.md
├── 前端设计/SKILL.md   # 含 LICENSE.txt（Apache 2.0）
└── 直给回答/SKILL.md
```

## 🛠️ Skill 规范

每个 Skill 遵循标准格式：

- `SKILL.md` 必备，含 YAML frontmatter（`name` + `description` 触发条件）与 Markdown 流程正文
- 可选 `scripts/`（可执行脚本）、`references/`（参考文档）、`assets/`（模板资产）
- 描述清晰，Agent 读到描述即可判断何时调用

## ⭐ 来源与致谢

- 4 个 Skill 直接复用 GitHub 高星项目（MIT / Apache 2.0）：mattpocock/skills、anthropics/skills、lvy010/clouds、ayghri/i-have-adhd，均保留原许可证与版权声明，详见 [LICENSES.md](./LICENSES.md)。
- 5 个 Skill 为 buleboy 实战沉淀（GitHub 主页整理、Pages 部署、ShiftX 拆解、刷题平台、简历网页）。

欢迎 Star ⭐、Fork、提 Issue 共建你的专属 Skill。
