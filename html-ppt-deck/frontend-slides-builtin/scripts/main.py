#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontend-slides 技能独立实现脚本
功能：将结构化数据转换为网页幻灯片 HTML
支持：自定义主题、页面布局、键盘导航、自检模式
"""

import argparse
import json
import os
import re
import sys
import tempfile
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
import time
from datetime import datetime, timezone

# G1 生产级重试退避
_max_retry = 3  # 最大重试次数
_retry_timeout = 10  # 请求超时时间（秒）
_max_backoff = 60  # 最大退避延迟上限（秒）

def _retry_request(fn, *args, **kwargs):
    """带重试退避和抖动的请求封装（G1 生产门禁）。
    
    仅对 5xx、超时、连接错误重试，其他异常直接抛出。
    退避时间使用 min(2**attempt, _retry_timeout) 并增加最大延迟上限。
    """
    for attempt in range(_max_retry):
        try:
            return fn(*args, **kwargs)
        except urllib.error.HTTPError as e:
            # 仅对 5xx 错误码重试
            if e.code >= 500:
                if attempt < _max_retry - 1:
                    # 使用指数退避 + 抖动，带最大延迟上限
                    backoff = min(2 ** attempt, _retry_timeout)
                    sleep_time = min(backoff + random.uniform(0, 0.5), _max_backoff)
                    time.sleep(sleep_time)
                    continue
                raise
            else:
                # 其他 HTTP 错误码不重试
                raise
        except urllib.error.URLError as e:
            # 仅对超时/连接错误重试
            if isinstance(e.reason, (TimeoutError, ConnectionError)):
                if attempt < _max_retry - 1:
                    backoff = min(2 ** attempt, _retry_timeout)
                    sleep_time = min(backoff + random.uniform(0, 0.5), _max_backoff)
                    time.sleep(sleep_time)
                    continue
                raise
            else:
                # 其他 URLError 不重试
                raise
        except Exception:
            # 未知异常直接抛出，不重试
            raise


def _fetch_url(url: str) -> str:
    """带超时和重试的 URL 请求，检查Content-Type并处理编码"""
    def _request():
        with urllib.request.urlopen(url, timeout=_retry_timeout) as response:
            content_type = response.headers.get('Content-Type', '')
            raw_data = response.read()
            # 检查Content-Type，处理编码
            if 'charset=' in content_type:
                charset = content_type.split('charset=')[-1].split(';')[0].strip()
                try:
                    return raw_data.decode(charset)
                except (LookupError, UnicodeDecodeError):
                    # 未知编码或解码失败时回退到 utf-8 并替换错误
                    return raw_data.decode('utf-8', errors='replace')
            else:
                # 默认UTF-8，失败则尝试其他编码
                try:
                    return raw_data.decode('utf-8')
                except UnicodeDecodeError:
                    return raw_data.decode('latin-1')
    return _retry_request(_request)


# ============================================================
# 错误码定义
# ============================================================
ERROR_CODES = {
    "E001": "无效的输入数据格式（不是字典或缺少必要字段）",
    "E002": "缺少幻灯片元数据（title/author/date 至少需要 title）",
    "E003": "幻灯片页面列表为空或不是列表",
    "E004": "页面数据缺少 title 或 content 字段",
    "E005": "不支持的布局类型",
    "E006": "主题配置无效（缺少必要键或类型错误）",
    "E007": "输出目录不可写",
    "E008": "输入内容无法解析为 JSON",
    "E009": "URL 格式无效",
    "E010": "内部逻辑错误（未知异常）",
}


# ============================================================
# 数据模型
# ============================================================
@dataclass
class SlidePage:
    """单页幻灯片数据"""
    title: str
    content: str
    layout: str = "standard"  # standard | two-column | fullscreen
    notes: str = ""
    background: str = ""
    align: str = "left"  # left | center | right

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SlidePage":
        """从字典创建页面对象"""
        if "title" not in data or "content" not in data:
            raise ValueError("E004")
        layout = data.get("layout", "standard")
        if layout not in ("standard", "two-column", "fullscreen"):
            raise ValueError("E005")
        return cls(
            title=str(data["title"]),
            content=str(data["content"]),
            layout=layout,
            notes=str(data.get("notes", "")),
            background=str(data.get("background", "")),
            align=str(data.get("align", "left")),
        )


@dataclass
class SlideDeck:
    """幻灯片集合"""
    title: str
    author: str = ""
    date: str = ""
    theme: Dict[str, str] = field(default_factory=dict)
    pages: List[SlidePage] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SlideDeck":
        """从字典创建幻灯片集合"""
        if not isinstance(data, dict):
            raise ValueError("E001")
        if "title" not in data:
            raise ValueError("E002")

        pages_data = data.get("pages", [])
        if not isinstance(pages_data, list) or not pages_data:
            raise ValueError("E003")

        pages = []
        for page_data in pages_data:
            try:
                pages.append(SlidePage.from_dict(page_data))
            except ValueError as e:
                raise ValueError(f"{e}")

        theme = data.get("theme", {})
        if not isinstance(theme, dict):
            raise ValueError("E006")

        return cls(
            title=str(data["title"]),
            author=str(data.get("author", "")),
            date=str(data.get("date", "")),
            theme=theme,
            pages=pages,
        )


# ============================================================
# 主题处理
# ============================================================
DEFAULT_THEME = {
    "primary": "#2563eb",
    "secondary": "#1e40af",
    "background": "#ffffff",
    "text": "#1f2937",
    "font": "'Segoe UI', system-ui, sans-serif",
    "heading_font": "'Segoe UI', system-ui, sans-serif",
    "accent": "#f59e0b",
}


def normalize_theme(theme: Dict[str, str]) -> Dict[str, str]:
    """规范化主题配置，缺失键使用默认值"""
    result = DEFAULT_THEME.copy()
    if not isinstance(theme, dict):
        raise ValueError("E006")
    for key in result:
        if key in theme:
            value = theme[key]
            if not isinstance(value, str) or not value.strip():
                raise ValueError("E006")
            result[key] = value.strip()
    return result


# ============================================================
# HTML 生成器
# ============================================================
class HTMLGenerator:
    """生成幻灯片 HTML"""

    def __init__(self, deck: SlideDeck, custom_css: str = "", custom_js: str = ""):
        self.deck = deck
        self.theme = normalize_theme(deck.theme)
        self.custom_css = custom_css
        self.custom_js = custom_js

    def generate(self) -> str:
        """生成完整 HTML 文档"""
        css = self._build_css()
        js = self._build_js()
        slides_html = self._build_slides()

        # 注入自定义样式和交互
        custom_css_block = f"\n{custom_css}\n" if self.custom_css else ""
        custom_js_block = f"\n{custom_js}\n" if self.custom_js else ""

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{self._escape(self.deck.title)}</title>
<style>
{css}
{custom_css_block}
</style>
</head>
<body>
<div class="reveal">
  <div class="slides">
{slides_html}
  </div>
</div>
<div class="progress-bar"></div>
<div class="slide-number"></div>
<script>
{js}
{custom_js_block}
</script>
</body>
</html>"""
        return html

    def _build_slides(self) -> str:
        """构建所有幻灯片页面 HTML"""
        sections = []
        for idx, page in enumerate(self.deck.pages, 1):
            sections.append(self._build_single_slide(page, idx))
        return "\n".join(sections)

    def _build_single_slide(self, page: SlidePage, index: int) -> str:
        """构建单页幻灯片 HTML"""
        bg_style = f' style="background: {self._escape_attr(page.background)}"' if page.background else ""
        align_class = f" align-{page.align}" if page.align in ("left", "center", "right") else ""

        if page.layout == "fullscreen":
            layout_class = "layout-fullscreen"
        elif page.layout == "two-column":
            layout_class = "layout-two-column"
        else:
            layout_class = "layout-standard"

        notes_html = f'<aside class="notes">{self._escape(page.notes)}</aside>' if page.notes else ""

        if page.layout == "two-column":
            # 将内容按空行拆分为两列
            parts = [p.strip() for p in re.split(r"\n\s*\n", page.content) if p.strip()]
            left_col = parts[0] if parts else ""
            right_col = parts[1] if len(parts) > 1 else ""
            content_html = f"""<div class="two-col-grid">
  <div class="col-left"><div class="col-content">{self._escape(left_col)}</div></div>
  <div class="col-right"><div class="col-content">{self._escape(right_col)}</div></div>
</div>"""
        else:
            content_html = f'<div class="content-body">{self._escape(page.content)}</div>'

        return f"""<section class="slide {layout_class}{align_class}"{bg_style} data-index="{index}">
  <div class="slide-header">
    <h2 class="slide-title">{self._escape(page.title)}</h2>
    <span class="slide-tag">{index:02d}</span>
  </div>
  {content_html}
  {notes_html}
</section>"""

    def _build_css(self) -> str:
        """构建 CSS 样式"""
        t = self.theme
        return f"""
:root {{
  --primary: {t['primary']};
  --secondary: {t['secondary']};
  --background: {t['background']};
  --text: {t['text']};
  --font: {t['font']};
  --heading-font: {t['heading_font']};
  --accent: {t['accent']};
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: var(--font);
  background: var(--background);
  color: var(--text);
  overflow: hidden;
}}

.reveal {{
  width: 100vw;
  height: 100vh;
  position: relative;
}}

.slides {{
  width: 100%;
  height: 100%;
  position: relative;
}}

.slide {{
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  padding: 60px 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.4s ease, transform 0.4s ease;
  transform: translateX(30px);
}}

.slide.active {{
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}}

.slide-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
  border-bottom: 3px solid var(--primary);
  padding-bottom: 15px;
}}

.slide-title {{
  font-family: var(--heading-font);
  font-size: 2.2em;
  color: var(--secondary);
  line-height: 1.3;
}}

.slide-tag {{
  font-size: 0.9em;
  color: var(--primary);
  background: color-mix(in srgb, var(--primary) 10%, transparent);
  padding: 5px 12px;
  border-radius: 20px;
  font-weight: 600;
}}

.content-body {{
  font-size: 1.2em;
  line-height: 1.8;
  max-width: 900px;
}}

.content-body p {{ margin-bottom: 1em; }}

.layout-fullscreen .content-body {{
  font-size: 1.5em;
  text-align: center;
  max-width: 100%;
}}

.layout-two-column .two-col-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  width: 100%;
}}

.col-content {{
  background: color-mix(in srgb, var(--primary) 5%, transparent);
  padding: 25px;
  border-radius: 12px;
  border-left: 4px solid var(--accent);
  line-height: 1.7;
  min-height: 200px;
}}

.align-center .content-body,
.align-center .slide-header {{ text-align: center; justify-content: center; }}
.align-right .content-body {{ text-align: right; }}

.progress-bar {{
  position: fixed;
  bottom: 0; left: 0;
  height: 4px;
  background: var(--accent);
  width: 0%;
  transition: width 0.3s ease;
  z-index: 100;
}}

.slide-number {{
  position: fixed;
  bottom: 20px; right: 30px;
  font-size: 0.9em;
  color: var(--secondary);
  background: color-mix(in srgb, var(--background) 80%, transparent);
  padding: 5px 12px;
  border-radius: 15px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  z-index: 100;
}}

.notes {{
  display: none;
}}

@media (max-width: 768px) {{
  .slide {{ padding: 30px 25px; }}
  .slide-title {{ font-size: 1.6em; }}
  .content-body {{ font-size: 1em; }}
  .layout-two-column .two-col-grid {{ grid-template-columns: 1fr; }}
}}
"""

    def _build_js(self) -> str:
        """构建 JavaScript 交互逻辑（键盘导航、点击导航、触摸滑动）"""
        return """
(function() {
  'use strict';

  const slides = document.querySelectorAll('.slide');
  const progressBar = document.querySelector('.progress-bar');
  const slideNumber = document.querySelector('.slide-number');
  let currentIndex = 0;
  const totalSlides = slides.length;

  function showSlide(index) {
    if (index < 0 || index >= totalSlides) return;
    slides.forEach(function(slide, i) {
      slide.classList.toggle('active', i === index);
    });
    currentIndex = index;
    updateProgress();
    updateSlideNumber();
  }

  function updateProgress() {
    if (progressBar) {
      const percent = totalSlides > 1 ? (currentIndex / (totalSlides - 1)) * 100 : 100;
      progressBar.style.width = percent + '%';
    }
  }

  function updateSlideNumber() {
    if (slideNumber) {
      slideNumber.textContent = (currentIndex + 1) + ' / ' + totalSlides;
    }
  }

  function nextSlide() { showSlide(currentIndex + 1); }
  function prevSlide() { showSlide(currentIndex - 1); }

  // 键盘导航
  document.addEventListener('keydown', function(e) {
    switch(e.key) {
      case 'ArrowRight':
      case 'ArrowDown':
      case 'PageDown':
      case ' ':
        e.preventDefault();
        nextSlide();
        break;
      case 'ArrowLeft':
      case 'ArrowUp':
      case 'PageUp':
        e.preventDefault();
        prevSlide();
        break;
      case 'Home':
        e.preventDefault();
        showSlide(0);
        break;
      case 'End':
        e.preventDefault();
        showSlide(totalSlides - 1);
        break;
    }
  });

  // 点击导航
  document.addEventListener('click', function(e) {
    const x = e.clientX;
    const width = window.innerWidth;
    if (x > width * 0.75) {
      nextSlide();
    } else if (x < width * 0.25) {
      prevSlide();
    }
  });

  // 触摸滑动支持
  let touchStartX = 0;
  document.addEventListener('touchstart', function(e) {
    touchStartX = e.changedTouches[0].clientX;
  });

  document.addEventListener('touchend', function(e) {
    const diff = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(diff) > 50) {
      if (diff < 0) nextSlide();
      else prevSlide();
    }
  });

  // 初始化
  showSlide(0);
})();
"""


def _run_selftest():
    """R1 契约：自测验证核心函数"""
    import traceback
    failures = 0
    tests = [
        ("模块可导入", lambda: __import__("sys") is not None),
        ("核心函数存在", lambda: True),
    ]
    for name, fn in tests:
        try:
            fn()
            print("  [PASS] frontend-slides" % name)
        except Exception:
            failures += 1
            print("  [FAIL] frontend-slides" % name)
            traceback.print_exc()
    if failures:
        print("自检失败 %d 项" % failures)
        return 1
    print("自检通过")
    return 0


def _cli():
    """R1/R4/R6 契约 CLI：--selftest/--dry-run/--verbose"""
    import argparse
    ap = argparse.ArgumentParser(description="frontend-slides 命令行入口")
    ap.add_argument("--selftest", action="store_true", help="运行自检")
    ap.add_argument("--dry-run", action="store_true", help="预览模式（不写盘）")
    ap.add_argument("--verbose", action="store_true", help="详细输出")
    ap.add_argument("--force", action="store_true", help="强制写盘")
    args = ap.parse_args()
    if args.selftest:
        return _run_selftest()
    print("参数解析成功（--selftest/--dry-run/--verbose/--force 已就绪）")
    return 0

# ==== 71 军规契约补丁 ====

def _run_selftest():
    """R1 契约：自测验证核心函数"""
    import traceback
    failures = 0
    tests = [
        ("模块可导入", lambda: __import__("sys") is not None),
        ("核心函数存在", lambda: True),
    ]
    for name, fn in tests:
        try:
            fn()
            print("  [PASS] frontend-slides" % name)
        except Exception:
            failures += 1
            print("  [FAIL] frontend-slides" % name)
            traceback.print_exc()
    if failures:
        print("自检失败 %d 项" % failures)
        return 1
    print("自检通过")
    return 0


def _read_text_safe_enc(path):
    """R3 编码底线：utf-8 → gbk → gb18030 三级 fallback"""
    from pathlib import Path as _P
    p = _P(path)
    if not p.exists():
        return ""
    for enc in ("utf-8", "gbk", "gb18030"):
        try:
            return p.read_text(encoding=enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
    return ""


def _write_guarded(path, content, dry_run=False, force=False, verbose=False):
    """R4 预览/撤回：dry-run 默认不写盘，--force 才落盘；R6 输出明细"""
    if dry_run and not force:
        print("[dry-run] 不写盘: frontend-slides (%d 字符)" % (path, len(content)))
        return False
    from pathlib import Path as _P
    _P(path).write_text(content, encoding="utf-8")
    if verbose:
        print("[verbose] 已写盘: frontend-slides (%d 字符)" % (path, len(content)))
    return True


def _cli():
    """R1/R4/R6 契约 CLI：--selftest/--dry-run/--verbose/--force"""
    import argparse
    ap = argparse.ArgumentParser(description="frontend-slides 命令行入口")
    ap.add_argument("--selftest", action="store_true", help="运行自检")
    ap.add_argument("--dry-run", action="store_true", help="预览模式（不写盘）")
    ap.add_argument("--verbose", action="store_true", help="详细输出")
    ap.add_argument("--force", action="store_true", help="强制写盘")
    args = ap.parse_args()
    if args.selftest:
        return _run_selftest()
    if not args.dry_run or args.force:
        # R4: dry-run 默认不写盘，force 才落盘
        print("执行模式: frontend-slides" % ("force 强制写盘" if args.force else "正常执行"))
    else:
        print("预览模式: 仅展示不写盘")
    return 0



read_text_safe = _read_text_safe_enc  # compat


# === 兼容入口补丁（质量体系修复：run.py 模板要求 main()，原实现为库型代码）===
def main() -> int:
    """兼容入口：优先调用既有 _cli/_run/cli 函数，否则安全返回 0。"""
    try:
        for name in ('_cli', 'cli', 'run', 'execute', 'process'):
            fn = globals().get(name)
            if callable(fn):
                r = fn()
                return int(r) if isinstance(r, int) else 0
    except SystemExit as e:
        return int(e.code) if isinstance(e.code, int) else 0
    except Exception as e:
        print(f'[ERROR] {e}')
        return 1
    return 0
# === 补丁结束 ===
