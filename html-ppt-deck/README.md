# HTML PPT 汇报场景 Skill 包

> ☁️ 归档于 clouds 仓库 · 2026-09-21 · 用途：**HTML → 演示文稿 / 汇报卡片 / PPTX** 全链路

## 场景定位

需要做「汇报 / 分享 / 汇报页」时，按下面两条流水线组合调用：

- **网页 PPT 流水线**：`frontend-slides` 或 `guizang-ppt-skill` 生成单文件 HTML deck → 浏览器直接翻页演示
- **真 PPTX 流水线**：`frontend-slides` / `deck-guizang-editorial` 出 HTML → `html2pptx` 转原生可编辑 .pptx（文字/形状可编辑，非贴图）
- **卡片 / 信息图**：`editorial-card-screenshot` 出杂志风 HTML 卡片 + 定比例 PNG 封面
- **文档收尾**：`md-to-pdf-cjk` / `minimax-pdf` 出中文 PDF 报告

## Skill 清单

| 文件夹 | 名称 | 来源 | 用途 |
|---|---|---|---|
| `frontend-slides/` | Frontend Slides | skills.sh `zarazhangrui/frontend-slides`（977 installs） | 零依赖、带动画的单文件 HTML 演示文稿，支持 PPTX 转 web |
| `frontend-slides-builtin/` | frontend-slides | WorkBuddy 内置市场 v1.0.2 | 同名内置版（与本机已装版本一致），二选一使用 |
| `guizang-ppt-skill/` | 歸藏 PPT Skills | WorkBuddy 内置市场 v1.0.0 | 电子杂志风 + 瑞士国际主义两套视觉系统，横向翻页网页 PPT |
| `deck-guizang-editorial/` | 贵赞编辑墨水 Deck | skills.sh `nexu-io/html-anything`（guizang 编辑风规范） | 电子杂志 × 电子墨水，10 版面 + 5 调色板，16:9 |
| `editorial-card-screenshot/` | Editorial Card | skills.sh `shaom/infocard-skills` | 杂志/瑞士国际主义风格高密度信息卡，3:4/16:9 等 8 种比例 + PNG 截图 |
| `html2pptx/` | html2pptx | skills.sh `microsoft/researchstudio` | HTML → 原生可编辑 PPTX（DOM 提取文字块/形状，视觉审计闭环，~95% 保真） |
| `md-to-pdf-cjk/` | MD to PDF CJK | 本地自制 | Markdown → 中文专业 PDF（reportlab，CJK 无乱码） |
| `minimax-pdf/` | MiniMax PDF | 本地自制 | 高设计感 PDF 生成 |

## 调用方式

1. **WorkBuddy 本机**：`editorial-card-screenshot`、`deck-guizang-editorial`、`html2pptx` 已装入 `~/.workbuddy/skills/`，直接对话触发；其余本机已有。
2. **其他机器 / 其他 Agent**：把对应文件夹整个拷到该 Agent 的 skills 目录（含 SKILL.md 即为标准 Agent Skill 格式）。
3. **html2pptx 依赖**：Python + headless chromium；视觉审计需 `ANTHROPIC_AUTH_TOKEN`（可用 `--no-vision-audit` 关闭）。

## 安全审计

4 个外部 skill 于 2026-09-21 下载源码后扫描（curl|bash / eval / base64 解码 / 反弹 shell / 外传 webhook 等模式）：**未发现恶意模式**，来源均为可验证公开仓库。

## 版本记录

- 2026-09-21：建包。收录 8 skills（4 社区 + 4 本地）；官方市场当时无 infocard-skills / myclaw-frontend-slides / html2pptx 独立版，改由 skills.sh 渠道收录；`myclaw-frontend-slides` 在 skills.sh 无精确匹配，以 `zarazhangrui/frontend-slides`（同描述：HTML 演示文稿生成，安装量最高）替代。
