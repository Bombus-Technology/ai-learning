# AI Learning — 團隊學習筆記網站

## 架構

靜態網站產生器，Python build script + HTML templates。

```
content/*.md → build.py → site/ (Nginx serve on port 3002)
```

## 開發指令

```bash
python3 build.py          # 建置全站
python3 dev.py             # 開發伺服器 (auto-rebuild + livereload)
python3 dev.py 8080        # 指定 port
```

## 目錄結構

- `content/` — Markdown 原始檔 (frontmatter + body)
- `templates/` — HTML 模板 (`{placeholder}` 語法)
- `static/` — CSS/JS (build 時複製到 site/)
- `site/` — 建置輸出 (gitignored)
- `deploy/` — Nginx config + Git hook

## Frontmatter 格式

```yaml
---
title: "文章標題"
url: "https://original-url"
author: "Allen"
date: 2026-03-15
tags: [LLM, RAG]
category: "AI 基礎"
series: "LLM 系列"           # 選填
series_order: 1               # 選填
draft: true                   # 選填，跳過建置
source_title: "原文標題"
source_author: "原文作者"
---
```

## 新增文章

1. 使用 `/ai-learning <url>` skill (推薦)
2. 或手動建立 `content/YYYY-MM-DD-slug.md`
3. 執行 `python3 build.py`
4. Commit + push

## 部署

- Nginx port 3002，root 指向 `site/`
- Git push 自動觸發 build (post-receive hook)
- Config: `deploy/nginx/ai-learning.conf`

## 技術選型

- Markdown: mistune 3.x
- Frontmatter: PyYAML
- 語法高亮: Prism.js (CDN)
- 搜尋: Fuse.js (CDN)
- 模板: Python str.format 變體 (自訂 render 函式)

## 回應語言

所有返回給使用者的結論、摘要、說明，一律使用**繁體中文**描述。
程式碼中的變數名稱、註解可維持英文，但對話輸出必須是中文。
