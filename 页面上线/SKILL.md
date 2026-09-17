---
name: pages-deploy
description: '中文名：页面上线。把本地 Web 项目部署到 GitHub Pages，含构建方式探测、GitHub Actions workflow 编写、Pages 启用、线上验证与白屏排障全流程。Use when: 页面上线、部署到 GitHub Pages、发布网页、给项目加在线访问、让仓库变成网站、pages 部署不了、构建失败 EUNSUPPORTEDPROTOCOL。'
---

# 页面上线

## 目标

把一个仓库里的前端项目稳定部署到 `https://<owner>.github.io/<repo>/`，并线上验证真实可访问。支持 npm、pnpm workspace、Jekyll、纯静态四种构建类型。

## 输入

- 必需：仓库名（owner/repo）。
- 可选：目标分支、构建命令、产物目录、已知异常。

## 工作流

### 1. 探测构建方式（先摸清再动手，禁止假设）

| 仓库特征 | 构建方式 |
|---|---|
| 有 `package-lock.json` + Vite/React | npm：`npm ci` → `npm run build` |
| 有 `pnpm-lock.yaml` 或依赖含 `workspace:^` | pnpm workspace（见 2） |
| 有 `.github/workflows/deploy.yml`（Jekyll Pages） | 直接复用仓库自带 workflow |
| 纯 HTML/CSS/JS 无构建 | 静态上传 main 分支 |
| 已有 `.github/workflows/pages.yml` | 直接启用 + dispatch |

**pnpm workspace 关键坑**：子包依赖 `workspace:^` 协议时 `npm ci` 必失败（EUNSUPPORTEDPROTOCOL）。必须：

```bash
pnpm install --frozen-lockfile
pnpm --filter @<scope>/shared build   # 先构建被依赖包
pnpm --filter client build            # 再构建入口包
```

### 2. 编写 workflow（`<repo>/.github/workflows/pages.yml`）

```yaml
name: Deploy to GitHub Pages
on:
  push: { branches: [main] }
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # npm 项目：
      # - uses: actions/setup-node@v4
      #   with: { node-version: 20, cache: npm }
      # - run: npm ci && npm run build -- --base=/<repo>/
      # pnpm 项目（换包管理器）：
      # - uses: pnpm/action-setup@v4
      # - run: pnpm install --frozen-lockfile && pnpm --filter @scope/shared build && pnpm --filter client build
      - uses: actions/upload-pages-artifact@v3
        with: { path: ./dist }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

**关键点**：
- 子路径部署必须 `--base=/<repo>/`（Vite）或等价 base 配置，否则资源 404 白屏。
- 产物目录：Vite 默认 `dist`；子包构建看 `client/dist`；Jekyll 用 `upload-pages-artifact` 默认。
- 静态 HTML 中的资源路径用相对路径（`src="live2d/..."`），不要用 `/live2d/...` 绝对路径。

### 3. 启用与触发

```bash
# 启用 Pages（build_type=workflow 表示用 Actions 构建）
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/<owner>/<repo>/pages \
  -d '{"build_type":"workflow"}'

# 手动触发一次构建
curl -X POST -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/<owner>/<repo>/actions/workflows/pages.yml/dispatches \
  -d '{"ref":"main"}'
```

### 4. 白屏/失败排障

| 症状 | 原因 | 修复 |
|---|---|---|
| 构建失败 `EUNSUPPORTEDPROTOCOL workspace:^` | npm 处理 pnpm workspace | 换 pnpm + `--frozen-lockfile` |
| 页面白屏、控制台 404 | 资源绝对路径 / base 未配置 | 加 `--base=/<repo>/`，改相对路径 |
| 引用的本地大文件不存在 | 仓库未包含该资源 | 下载官方文件放到 `public/` 再提交 |
| 部署成功但 404 | Pages 未启用或 build_type 不对 | 确认 `build_type: workflow` 且 workflow 在默认分支 |
| 构建成功但页面空白 | 依赖缺失或运行时错误 | 查 Actions 日志 + 浏览器控制台 |

## 检查清单

- [ ] 已确认构建方式与产物目录（不靠猜）
- [ ] workflow 推送后触发成功（查 actions/runs）
- [ ] 页面 200 可访问，核心资源（JS/CSS/大文件）非 404
- [ ] 浏览器打开验证真实渲染，不是只看构建成功
- [ ] 失败时按上表定位根因，不绕过问题
