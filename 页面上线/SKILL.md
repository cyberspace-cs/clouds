---
name: pages-deploy
description: 把本地 Web 项目部署上线到 GitHub Pages，含构建方式探测、GitHub Actions workflow 编写、Pages 启用与线上验证全流程。当用户要求"部署到 GitHub Pages / 上线 / 发布网页 / 给我的项目加个在线访问 / 让仓库变成网站 / pages 部署不了怎么办"时使用。支持 npm、pnpm workspace、Jekyll、纯静态四种构建类型，包含白屏排障。
---

# 页面上线

## 目标

把一个仓库里的前端项目稳定部署到 `https://<owner>.github.io/<repo>/`，并线上验证可用。

## 核心流程

### 1. 探测项目构建方式（先摸清再动手）

| 仓库特征 | 构建方式 |
|---|---|
| 有 `package-lock.json` + Vite/React | npm：`npm ci` → `npm run build` |
| 有 `pnpm-lock.yaml` 或依赖含 `workspace:^` | pnpm workspace（见下） |
| 有 `.github/workflows/deploy.yml`（Jekyll Pages） | 直接用仓库自带 workflow |
| 纯 HTML/CSS/JS 无构建 | 静态上传 `main` 分支 |
| `.github/workflows/pages.yml` 已存在 | 直接启用 + dispatch |

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

## 检查清单

- [ ] 已确认构建方式与产物目录
- [ ] workflow 推送后触发成功（查 actions/runs）
- [ ] 页面 200 可访问，核心资源（JS/CSS/大文件）非 404
- [ ] 浏览器打开验证真实渲染，不是只看构建成功
- [ ] 失败时按上表定位根因，不绕过问题
