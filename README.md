# ☁️ buleboy's clouds — Personal Skill Collection

> **Everything is Skill-Composable.** 常用工作流打包成可随时调用的 Skill，配合豆包工作任务模式 / AI Agent 一键安装即用。

每个英文目录就是一个独立的 Skill（`SKILL.md` 含触发描述与完整流程），按需调用，随取随用。

## 🚀 快速开始

在豆包（工作任务模式）或任意支持 Skills 的 Agent 中直接说：

> 帮我安装 GitHub 上 cyberspace-cs 的 clouds，直接用「knowledge-cards Skill」帮我处理 …

或者按目录读取对应 Skill 的 `SKILL.md` 即可获得完整工作流。

## 📦 Skill 列表

> ⭐ = 来源仓库 GitHub Star 数（实时可查）；「自研」为 buleboy 实战沉淀。

### 🖥️ 编程 Coding

| Skill | 说明 Description | 来源 Source |
| --- | --- | --- |
| [diagnosing-bugs](./diagnosing-bugs/) | 硬 bug 诊断：先建反馈回路再定位，10 种循环构建法 · Hard-bug diagnosis loop | mattpocock/skills ⭐264k |
| [tdd](./tdd/) | TDD 红绿循环：好测试标准、测试缝、反模式 · Test-driven development | mattpocock/skills ⭐264k |
| [code-review-and-quality](./code-review-and-quality/) | 五轴代码评审：正确性/可读性/架构/安全/性能 + 质量门 · Five-axis code review | addyosmani/agent-skills ⭐96k |
| [code-simplification](./code-simplification/) | 代码简化：删冗余、降复杂度、保持行为不变 · Simplify without changing behavior | addyosmani/agent-skills ⭐96k |
| [security-and-hardening](./security-and-hardening/) | 安全加固：审查输入/会话/第三方集成，对照 OWASP Top 10 · Harden against vulnerabilities | addyosmani/agent-skills ⭐96k |
| [performance-optimization](./performance-optimization/) | 全栈性能优化：前后端/查询/数据库，N+1、Core Web Vitals · Optimize performance | addyosmani/agent-skills ⭐96k |
| [vercel-react-best-practices](./vercel-react-best-practices/) | React/Next.js 性能优化：40+ 规则 8 大类（waterfall/包体积/重渲染）· Performance guidelines | vercel-labs/agent-skills ⭐31k |
| [leetcode-coach](./leetcode-coach/) | LeetCode 刷题：定制路线、逐题精讲、遗忘曲线复习 · LeetCode learning coach | 自研 buleboy |

### 🛠️ 工程流程 Engineering Workflow

| Skill | 说明 Description | 来源 Source |
| --- | --- | --- |
| [verification-before-completion](./verification-before-completion/) | 完成前验证：无新鲜验证证据不得声称完成 · Evidence before claims | obra/superpowers ⭐288k |
| [brainstorming](./brainstorming/) | 创意先构思再动手：分类需求、设计方案、获准后才实现 · Design before implementation | obra/superpowers ⭐288k |
| [writing-skills](./writing-skills/) | 写 Skill 的 Skill：TDD 式创作、子代理压测、验证后部署 · Create & test skills | obra/superpowers ⭐288k |
| [planning-and-task-breakdown](./planning-and-task-breakdown/) | 任务拆解：规格 → 有序可执行任务、估算范围、并行推进 · Plan & break down tasks | addyosmani/agent-skills ⭐96k |
| [spec-driven-development](./spec-driven-development/) | 规格先行：先写规格/PRD/能力地图再编码 · Spec before code | addyosmani/agent-skills ⭐96k |
| [git-workflow-and-versioning](./git-workflow-and-versioning/) | Git 规范：原子提交、分支、冲突、PR、版本号与 CHANGELOG · Git workflow & versioning | addyosmani/agent-skills ⭐96k |
| [documentation-and-adrs](./documentation-and-adrs/) | 架构决策记录（ADR）与文档沉淀 · Document decisions & ADRs | addyosmani/agent-skills ⭐96k |
| [ci-cd-and-automation](./ci-cd-and-automation/) | CI/CD 自动化：流水线、质量门、测试运行器、部署策略 · Automate CI/CD | addyosmani/agent-skills ⭐96k |
| [observability-and-instrumentation](./observability-and-instrumentation/) | 可观测性：日志/指标/追踪/告警，生产可诊断 · Observability & instrumentation | addyosmani/agent-skills ⭐96k |
| [pages-deploy](./pages-deploy/) | 一键部署 GitHub Pages：构建探测 + workflow + pnpm 坑 + 白屏排障 · Deploy to Pages | 自研 buleboy |

### 📄 展示与内容 Showcase & Content

| Skill | 说明 Description | 来源 Source |
| --- | --- | --- |
| [github-profile-beautify](./github-profile-beautify/) | 生成 liyupi 风格的 GitHub 主页 README · Profile README beautifier | 自研 buleboy |
| [portfolio-builder](./portfolio-builder/) | 个人简历/作品集网页制作 · Portfolio website builder | 自研 buleboy |
| [project-deep-dive](./project-deep-dive/) | 深度拆解开源项目，产出中文学习指南 · Open-source project teardown | 自研 buleboy |
| [knowledge-cards](./knowledge-cards/) | 文章/本地文档 → 5~8 张知识卡片 · Turn articles into knowledge cards | 自研 buleboy |
| [charts](./charts/) | 根据数据生成准确、可访问的 HTML 图表与报告 · Data charts & reports | lvy010/clouds ⭐8 |
| [prose](./prose/) | 保留事实与观点，把生硬中文改得自然易读 · Natural Chinese editing | lvy010/clouds ⭐8 |

### 📄 文档处理 Documents

| Skill | 说明 Description | 来源 Source |
| --- | --- | --- |
| [doc-to-markdown](./doc-to-markdown/) | PDF/Word/Excel/PPT → 干净 Markdown，基于 MarkItDown · Docs to Markdown | microsoft/markitdown ⭐185k |

### 🎨 UI 与输出风格 UI & Output Style

| Skill | 说明 Description | 来源 Source |
| --- | --- | --- |
| [frontend-design](./frontend-design/) | 有辨识度的前端视觉设计，拒绝模板感 · Distinctive frontend design | anthropics/skills ⭐177k |
| [i-have-adhd](./i-have-adhd/) | ADHD 友好输出：先给行动、编号步骤、抑制废话 · Action-first output | ayghri/i-have-adhd ⭐47k |
| [humanizer](./humanizer/) | 去除 AI 写作痕迹：改写 AI 味文本、保留原意 · Remove AI writing tells | blader/humanizer ⭐49k |
| [no-ai-slop](./no-ai-slop/) | 检测或编辑 AI 味：保留个人文风、最小有效编辑 · Edit or detect AI slop | petergyang/no-ai-slop ⭐10k |

### 🔒 安全 Security

| Skill | 说明 Description | 来源 Source |
| --- | --- | --- |
| [security-and-hardening](./security-and-hardening/) | 安全加固：审查输入/会话/第三方集成，对照 OWASP Top 10 · Harden against vulnerabilities | addyosmani/agent-skills ⭐96k |
| [pre-publish-security-check](./pre-publish-security-check/) | 发布前检查：Token/隐私/绝对路径/临时文件，先报告不执行 Git · Pre-publish security scan | 自研 buleboy |

## 🧩 目录结构

```text
clouds/
├── README.md                  # 本说明
├── LICENSES.md                # 各 Skill 许可证与来源
├── diagnosing-bugs/SKILL.md    # 每个英文目录 = 一个 Skill
├── tdd/SKILL.md + tests.md + mocking.md
├── code-review-and-quality/SKILL.md
├── code-simplification/SKILL.md
├── security-and-hardening/SKILL.md
├── performance-optimization/SKILL.md
├── vercel-react-best-practices/SKILL.md + rules/（72 条规则）
├── verification-before-completion/SKILL.md
├── brainstorming/SKILL.md
├── writing-skills/SKILL.md + examples/ + references/
├── planning-and-task-breakdown/SKILL.md
├── spec-driven-development/SKILL.md
├── git-workflow-and-versioning/SKILL.md
├── documentation-and-adrs/SKILL.md
├── ci-cd-and-automation/SKILL.md
├── observability-and-instrumentation/SKILL.md
├── leetcode-coach/SKILL.md
├── pages-deploy/SKILL.md
├── github-profile-beautify/SKILL.md
├── portfolio-builder/SKILL.md
├── project-deep-dive/SKILL.md
├── knowledge-cards/SKILL.md
├── charts/SKILL.md
├── prose/SKILL.md
├── doc-to-markdown/SKILL.md
├── frontend-design/SKILL.md    # 含 LICENSE.txt（Apache 2.0）
├── i-have-adhd/SKILL.md
├── humanizer/SKILL.md + LICENSE
├── no-ai-slop/SKILL.md
└── pre-publish-security-check/SKILL.md
```

## 🛠️ Skill 规范

每个 Skill 遵循标准格式：

- `SKILL.md` 必备，含 YAML frontmatter（`name` + `description` 触发条件）与 Markdown 流程正文
- 可选 `scripts/`（可执行脚本）、`references/`（参考文档）、`assets/`（模板资产）
- 描述清晰，Agent 读到描述即可判断何时调用

## ✅ CI 自动校验

仓库内置 GitHub Actions（`.github/workflows/skill-validation.yml`），每次 push/PR 自动校验所有 Skill：

- `SKILL.md` 存在且含合法 YAML frontmatter
- frontmatter 仅允许 `name / description / license / allowed-tools / metadata`
- `name` 必须与目录名一致
- 任一 Skill 不合规则 CI 失败（质量门）

## ⭐ 来源与致谢

| 来源仓库 | Star | 许可 | 采用 Skill |
| --- | --- | --- | --- |
| [obra/superpowers](https://github.com/obra/superpowers) | 288k | MIT | verification-before-completion, brainstorming, writing-skills |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 264k | MIT | diagnosing-bugs, tdd |
| [microsoft/markitdown](https://github.com/microsoft/markitdown) | 185k | MIT | doc-to-markdown（封装 CLI） |
| [anthropics/skills](https://github.com/anthropics/skills) | 177k | Apache 2.0 | frontend-design |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 96k | MIT | code-review-and-quality, code-simplification, security-and-hardening, performance-optimization, git-workflow-and-versioning, documentation-and-adrs, planning-and-task-breakdown, spec-driven-development, ci-cd-and-automation, observability-and-instrumentation |
| [blader/humanizer](https://github.com/blader/humanizer) | 49k | MIT | humanizer |
| [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) | 47k | MIT | i-have-adhd |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 31k | MIT（SKILL.md 标注） | vercel-react-best-practices |
| [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) | 10k | MIT | no-ai-slop |
| [lvy010/clouds](https://github.com/lvy010/clouds) | 8 | MIT（各 skill 标注） | charts, prose |

- 21 个 Skill 直接复用/基于高星项目（保留原许可证与版权声明），详见 [LICENSES.md](./LICENSES.md)。
- 8 个 Skill 为 buleboy 实战沉淀（GitHub 主页整理、Pages 部署、ShiftX 拆解、刷题平台、简历网页、知识卡片、安全检查、文档转写）。

欢迎 Star ⭐、Fork、提 Issue 共建你的专属 Skill。
