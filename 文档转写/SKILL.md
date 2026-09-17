---
name: doc-to-markdown
description: '中文名：文档转写。把 PDF、Word、Excel、PPT、图片等文件转成干净的 Markdown 文本，便于阅读、喂给大模型、存档或二次加工。Use when: 文档转写、PDF 转 Markdown、Word 转 Markdown、Excel 转 Markdown、PPT 转文字、把文件转成文字、处理上传的文档。'
---

# 文档转写

## 目标

把用户提供的文档文件（PDF / DOCX / XLSX / PPTX / 图片等）转换成干净、可用的 Markdown 文本。

## 核心工具

本 Skill 基于 **MarkItDown**（微软开源，MIT 许可，185k+ star）实现：
- GitHub: https://github.com/microsoft/markitdown
- 安装：`pip install markitdown`

## 工作流

### 1. 接收文件

- 支持：PDF、DOCX、XLSX、PPTX、图片（OCR）、HTML、CSV、JSON、XML、ZIP 等。
- 文件路径：使用用户上传的本地路径；若为链接先下载到本地。

### 2. 转换命令

```bash
# 单文件转换
markitdown <input-file> -o <output.md>

# 输出到 stdout（便于直接阅读）
markitdown <input-file>
```

### 3. 转换后处理（重要）

- **表格**：Excel/CSV 转出的表格保留 Markdown 表格语法；若内容过长，检查是否截断。
- **长文档**：PDF 超长时分段转换或截取关键部分，注明页码范围。
- **图片 OCR**：确认 OCR 结果可读，专有名词/数字核对。
- **乱码/空结果**：换方案（如 PDF 用 `pdftotext` 兜底、图片提高分辨率后重试），不静默跳过。

### 4. 输出

- 直接输出 Markdown 内容（用户可复制），或保存为 `.md` 文件交付。
- 保留原文档标题层级与列表结构；OCR 类内容标注"图片转写"。
- 转换失败时说明原因与已尝试的方案，不伪造成功。

## 检查清单

- [ ] 转换结果非空、无乱码
- [ ] 表格/代码块结构完整
- [ ] 长文档未静默截断（注明范围）
- [ ] 转换失败有明确原因说明
