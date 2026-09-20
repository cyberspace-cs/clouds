---
name: browser-recorder-replayer
description: 浏览器录制与回放技能。使用当你需要录制用户在浏览器上的操作、自动化测试生成、用户行为分析、Bug 复现、或者需要把浏览器操作导出成可执行脚本时。支持 rrweb 会话录制、Playwright Codegen 代码生成、Puppeteer 自动化。
---

# 浏览器录制与回放

## 概述

浏览器录制与回放技术可以把用户在浏览器上的操作（点击、输入、滚动、DOM 变化）录制下来，然后回放或者导出成可执行的自动化脚本。

**核心能力**：
- 🎥 **会话录制**：录制用户在网页上的所有操作和 DOM 变化
- ▶️ **像素级回放**：像看视频一样回放用户操作
- 🤖 **代码生成**：把录制的操作导出成 Playwright/Puppeteer 脚本
- 🐛 **Bug 复现**：记录用户操作，远程复现 Bug

---

## 🛠️ 三大开源方案

### 1. rrweb（推荐：会话录制回放）

**GitHub**：https://github.com/rrweb-io/rrweb
**⭐ Star**：16k+
**License**：MIT

**是什么**：
- Record and Replay the Web 的缩写
- 录制 DOM 变化和用户操作，不录视频
- 回放是像素级的，比录视频清晰得多
- 体积小，可嵌入到任何网页

**适合场景**：
- 用户行为分析
- 远程 Bug 复现
- 产品体验优化
- 客服会话回放

**快速开始**：

```javascript
// 1. 安装
npm install rrweb rrweb-player

// 2. 录制
import { record } from 'rrweb';

let events = [];
record({
  emit: (event) => {
    events.push(event);
    // 可以实时传到服务器
  },
});

// 3. 回放
import rrwebPlayer from 'rrweb-player';
import 'rrweb-player/dist/style.css';

new rrwebPlayer({
  target: document.body,
  data: {
    events: events,
  },
});
```

**核心 API**：
```javascript
// 录制配置
record({
  emit: (event) => {},          // 事件回调
  recordDOM: true,              // 录制 DOM 变化
  recordCanvas: false,          // 录制 Canvas
  collectFonts: true,           // 收集字体
  slimDOMOptions: {},           // DOM 瘦身选项
  maskAllInputs: true,          // 屏蔽输入（隐私）
  maskInputOptions: {},         // 哪些输入要屏蔽
});

// 快照 + 增量事件
// 第一个事件是全量快照，后面都是增量
```

---

### 2. Playwright Codegen（推荐：自动化测试代码生成）

**GitHub**：https://github.com/microsoft/playwright
**⭐ Star**：70k+
**License**：Apache 2.0

**是什么**：
- 微软出品的浏览器自动化工具
- `codegen` 命令可以录制你的操作，自动生成测试代码
- 支持 Chromium / Firefox / WebKit
- 录制的是操作流程，不是 DOM 快照

**适合场景**：
- E2E 自动化测试
- 爬虫脚本生成
- 重复操作自动化
- API 测试辅助

**快速开始**：

```bash
# 1. 安装
npm init playwright@latest

# 2. 录制（打开浏览器，你操作，它生成代码）
npx playwright codegen https://example.com

# 3. 录制并保存到文件
npx playwright codegen https://example.com -o tests/example.spec.ts

# 4. 录制时模拟不同设备
npx playwright codegen --device="iPhone 14" https://example.com

# 5. 录制时模拟不同语言
npx playwright codegen --lang="zh-CN" https://example.com
```

**生成的代码示例**：
```typescript
import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://example.com/');
  await page.getByRole('link', { name: 'Get started' }).click();
  await page.getByText('Installation').click();
  await page.getByRole('button', { name: 'Search' }).click();
});
```

**高级功能**：
```bash
# 录制时记录网络请求
npx playwright codegen --save-storage=auth.json

# 录制时复用登录状态
npx playwright codegen --load-storage=auth.json

# 录制并生成 POM（Page Object Model）
npx playwright codegen --pom https://example.com
```

---

### 3. Puppeteer Recorder（备选）

**GitHub**：https://github.com/puppeteer/puppeteer
**⭐ Star**：90k+
**License**：Apache 2.0

**是什么**：
- Google 出品的 Headless Chrome 工具
- 官方的 Recorder 扩展可以录制操作
- 导出 Puppeteer / Playwright 脚本

**适合场景**：
- Chrome 生态用户
- 已有 Puppeteer 项目
- 轻量级自动化

**快速开始**：

```bash
# 1. 安装
npm install puppeteer

# 2. 使用 Chrome 自带的 Recorder
# Chrome DevTools → More tools → Recorder
# 点击 "Start new recording" → 操作 → "Stop recording"
# 可以导出为 Puppeteer 脚本

# 3. 用 Puppeteer 写脚本
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://example.com');
  await page.click('button');
  await browser.close();
})();
```

---

## 🎯 选型对比

| 维度 | rrweb | Playwright Codegen | Puppeteer Recorder |
| --- | --- | --- | --- |
| **定位** | 会话录制回放 | 测试代码生成 | 自动化脚本生成 |
| **录制内容** | DOM 变化 + 用户操作 | 用户操作流程 | 用户操作流程 |
| **回放方式** | 像素级回放（像看视频） | 重新执行操作 | 重新执行操作 |
| **输出格式** | JSON 事件流 | TypeScript/JS 测试代码 | JS Puppeteer 脚本 |
| **体积** | 小（~50KB） | 中 | 中 |
| **隐私保护** | 强（可屏蔽输入） | 弱（录操作） | 弱（录操作） |
| **浏览器支持** | 所有现代浏览器 | Chromium/Firefox/WebKit | 主要 Chrome |
| **最佳场景** | 用户分析、Bug 复现 | E2E 测试 | 爬虫、自动化 |

---

## 📋 选型建议

### 选 rrweb 如果你：
- ✅ 需要记录用户真实操作，远程复现 Bug
- ✅ 做用户行为分析、产品体验优化
- ✅ 需要把录屏做成可嵌入的组件
- ✅ 关心隐私，需要屏蔽敏感输入

### 选 Playwright Codegen 如果你：
- ✅ 写 E2E 自动化测试
- ✅ 想快速生成测试脚本
- ✅ 需要跨浏览器测试
- ✅ 用 TypeScript 写测试

### 选 Puppeteer Recorder 如果你：
- ✅ 已有 Puppeteer 项目
- ✅ 只需要 Chrome 自动化
- ✅ 轻量级脚本生成

---

## 🔧 高级用法

### 1. rrweb 隐私保护

```javascript
record({
  emit: (event) => {},
  // 屏蔽所有输入框
  maskAllInputs: true,
  
  // 只屏蔽特定输入
  maskInputOptions: {
    password: true,      // 屏蔽密码
    email: true,         // 屏蔽邮箱
    phone: true,         // 屏蔽电话
  },
  
  // 屏蔽特定元素（比如个人信息区域）
  maskSelector: '.user-info',
});
```

### 2. Playwright 录制时调试

```bash
# 录制时打开 Trace Viewer
npx playwright codegen --trace on https://example.com

# 录制后查看 trace
npx playwright show-trace trace.zip
```

### 3. 录制 + AI 分析

```python
# 用 rrweb 录制后，把事件流发给 AI 分析
import openai

events_json = json.dumps(recorded_events)

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "分析用户的浏览器操作，找出问题"},
        {"role": "user", "content": f"用户操作事件：{events_json}"}
    ]
)
```

---

## 🚀 快速决策

```
你想做什么？
├── 记录用户操作，远程复现 Bug → rrweb
├── 写自动化测试脚本 → Playwright Codegen
├── 做用户行为分析 → rrweb
├── 生成爬虫脚本 → Puppeteer / Playwright
└── 录屏做成可嵌入组件 → rrweb
```

---

## 📚 参考链接

- rrweb 官网：https://www.rrweb.io/
- rrweb GitHub：https://github.com/rrweb-io/rrweb
- Playwright 官网：https://playwright.dev/
- Playwright Codegen 文档：https://playwright.dev/docs/codegen
- Puppeteer 官网：https://pptr.dev/
- Chrome Recorder 文档：https://developer.chrome.com/docs/devtools/recorder
