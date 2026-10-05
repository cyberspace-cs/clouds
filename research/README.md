# research/ — 科研全流程 Skills（第三方聚合）

本目录汇集了微信公众号《告别科研内耗！GPT-6 Astra skills 汇总》一文中提到的科研类 Skill 的**真实可下载源**，按文章「选题 → 验证 → 文献 → 实验 → 绘图 → 写作 → 投稿」的 7 大环节归类，统一从 3 个公开仓库拉取并保留其原始目录结构。

> ⚠️ **许可证提醒**：本目录下 6 个 Skill 来自 **非商业（NonCommercial）** 许可的仓库，仅供个人非商用使用，请勿用于商业场景。详见 [../LICENSES.md](./LICENSES.md)。

## 目录结构

```
research/
├── nature-skills/            # 来源 Hanny126/nature-skills（上游未声明许可证）
│   ├── nature-academic-search
│   ├── nature-reader
│   ├── nature-paper-card
│   ├── nature-proposal-writer
│   ├── nature-figure
│   ├── nature-ref-verifier
│   └── nature-response
├── supervisor-skills/        # 来源 HKUSTDial/Supervisor-Skills（CC BY-NC-SA 4.0）
│   ├── idea-evaluator
│   ├── figure-designer
│   ├── paper-writer
│   └── pre-submission-reviewer
└── academic-research-skills/ # 来源 Imbad0202/academic-research-skills（CC BY-NC 4.0）
    ├── academic-pipeline
    └── academic-paper
```

## 与原文章节的对应

| 科研环节 | 本目录中的 Skill | 来源 |
| --- | --- | --- |
| 文献检索 | nature-academic-search | nature-skills |
| 文献精读 | nature-reader、nature-paper-card | nature-skills |
| Idea 验证 | idea-evaluator | supervisor-skills |
| 实验设计 | academic-pipeline、nature-proposal-writer | academic / nature |
| 科研绘图 | nature-figure、figure-designer | nature / supervisor |
| 论文写作 | paper-writer、academic-paper | supervisor / academic |
| 投稿返修 | nature-ref-verifier、pre-submission-reviewer、nature-response | nature / supervisor |

## 来源与许可证

| Skill | 许可 | 来源仓库 |
| --- | --- | --- |
| nature-*（7 个） | 未声明（上游无 LICENSE） | [Hanny126/nature-skills](https://github.com/Hanny126/nature-skills) |
| idea-evaluator / figure-designer / paper-writer / pre-submission-reviewer | CC BY-NC-SA 4.0 | [HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) |
| academic-pipeline / academic-paper | CC BY-NC 4.0 | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) |

## 未收录说明

原文章还提到以下 4 个 Skill，因**未能在公开仓库中精确定位来源 / 搜索无结果**，本次未下载：

- `Supervisor Deep Research`、`Socratic Deep Research`（文章未标注来源仓库）
- `ResearchStudio-Idea`（仅在个别仓库零散出现，无法确认对应）
- `USTC Academic-Search`（GitHub 代码搜索 0 结果）

另外 `Draw.io 流程` 是通用绘图工具的使用建议，并非可下载的 Skill 包，故未单独收录。

若后续获得权威来源或作者提供的安装包（文章引流的「B902 资料包」），可补充进本目录。
