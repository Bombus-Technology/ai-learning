#!/usr/bin/env python3
"""
build.py — Convert content/*.md → site/articles/*.html + articles.json
Run: python3 build.py
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

CONTENT_DIR = Path(__file__).parent / "content"
SITE_DIR = Path(__file__).parent / "site"
ARTICLES_DIR = SITE_DIR / "articles"

def parse_frontmatter(text):
    """Parse YAML-like frontmatter from markdown."""
    fm = {}
    if not text.startswith("---"):
        return fm, text
    end = text.find("---", 3)
    if end == -1:
        return fm, text
    header = text[3:end].strip()
    body = text[end+3:].strip()
    for line in header.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip("'\"") for v in val[1:-1].split(",")]
            fm[key] = val
    return fm, body

def md_to_html(md):
    """Minimal markdown to HTML (no external deps)."""
    lines = md.split("\n")
    html_lines = []
    in_blockquote = False
    in_code = False
    in_table = False

    for line in lines:
        # Code blocks
        if line.strip().startswith("```"):
            if in_code:
                html_lines.append("</code></pre>")
                in_code = False
            else:
                lang = line.strip()[3:]
                html_lines.append(f'<pre><code class="lang-{lang}">')
                in_code = True
            continue
        if in_code:
            html_lines.append(line)
            continue

        # Headers
        if line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
            continue
        if line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
            continue
        if line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
            continue

        # Horizontal rule
        if line.strip() == "---":
            html_lines.append("<hr>")
            continue

        # Table
        if "|" in line and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(set(c) <= set("- :") for c in cells):
                continue  # separator row
            if not in_table:
                html_lines.append("<table>")
                in_table = True
            tag = "th" if not in_table else "td"
            html_lines.append("<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in cells) + "</tr>")
            continue
        elif in_table:
            html_lines.append("</table>")
            in_table = False

        # Blockquote
        if line.startswith("> "):
            if not in_blockquote:
                html_lines.append("<blockquote>")
                in_blockquote = True
            html_lines.append(f"<p>{line[2:]}</p>")
            continue
        elif in_blockquote:
            html_lines.append("</blockquote>")
            in_blockquote = False

        # Bold / Italic / Code / Links
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
        line = re.sub(r'`(.+?)`', r'<code>\1</code>', line)
        line = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', line)

        if line.strip():
            html_lines.append(f"<p>{line}</p>")
        else:
            html_lines.append("")

    if in_blockquote:
        html_lines.append("</blockquote>")
    if in_table:
        html_lines.append("</table>")

    return "\n".join(html_lines)

ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — AI Learning</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#0F1117;--bg2:#161922;--bg3:#1E2230;--bg4:#262A38;--border:#2A2E3E;--text:#E8E8ED;--text2:#A0A4B8;--text3:#6B7084;--sage:#2D6A4F;--sage-xl:#52B788;--font:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans TC',sans-serif;--mono:'SF Mono','Fira Code',monospace}}
body{{font-family:var(--font);background:var(--bg);color:var(--text);min-height:100vh}}
.container{{max-width:800px;margin:0 auto;padding:40px 24px}}
a{{color:var(--sage-xl)}}
.back{{font-size:13px;color:var(--text3);text-decoration:none;display:inline-flex;align-items:center;gap:4px;margin-bottom:24px}}
.back:hover{{color:var(--text)}}
h1{{font-size:24px;font-weight:800;margin-bottom:8px;line-height:1.3}}
.meta{{display:flex;gap:16px;font-size:12px;color:var(--text3);margin-bottom:24px;flex-wrap:wrap}}
.meta a{{color:var(--sage-xl)}}
.tags{{display:flex;gap:4px;margin-bottom:24px}}
.tag{{font-size:10px;padding:2px 8px;border-radius:10px;background:rgba(45,106,79,.15);color:var(--sage-xl)}}
.content{{font-size:14px;color:var(--text2);line-height:1.8}}
.content h2{{font-size:18px;font-weight:700;color:var(--text);margin:28px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--border)}}
.content h3{{font-size:15px;font-weight:700;color:var(--text);margin:20px 0 8px}}
.content p{{margin-bottom:12px}}
.content blockquote{{border-left:3px solid var(--sage);padding:8px 16px;margin:12px 0;background:var(--bg3);border-radius:0 8px 8px 0;color:var(--text3);font-style:italic}}
.content blockquote p{{margin-bottom:4px}}
.content code{{font-family:var(--mono);font-size:12px;background:var(--bg4);padding:1px 5px;border-radius:3px;color:var(--sage-xl)}}
.content pre{{background:var(--bg4);border-radius:8px;padding:14px;overflow-x:auto;margin:12px 0}}
.content pre code{{background:none;padding:0}}
.content table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:13px}}
.content th{{text-align:left;padding:6px 10px;background:var(--bg4);color:var(--text3);font-weight:600;border-bottom:1px solid var(--border)}}
.content td{{padding:6px 10px;border-bottom:1px solid var(--border);color:var(--text2)}}
.content hr{{border:none;border-top:1px solid var(--border);margin:24px 0}}
.content strong{{color:var(--text);font-weight:600}}
</style>
</head>
<body>
<div class="container">
  <a href="../index.html" class="back">← 回到列表</a>
  <h1>{title}</h1>
  <div class="meta">
    <span>{date}</span>
    <span>{author}</span>
    <a href="{url}" target="_blank">閱讀原文 ↗</a>
  </div>
  <div class="tags">{tags_html}</div>
  <div class="content">{content}</div>
</div>
</body>
</html>"""

def build():
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    articles = []

    md_files = sorted(CONTENT_DIR.glob("*.md"))
    if not md_files:
        print("No articles found in content/")
        # Write empty articles.json
        (SITE_DIR / "articles.json").write_text("[]")
        return

    for md_file in md_files:
        print(f"Processing: {md_file.name}")
        text = md_file.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)

        title = fm.get("title", md_file.stem)
        url = fm.get("url", "")
        author = fm.get("author", "Unknown")
        date = fm.get("date", datetime.now().strftime("%Y-%m-%d"))
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]

        slug = md_file.stem
        content_html = md_to_html(body)
        tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)

        # Extract excerpt (first non-empty paragraph)
        excerpt = ""
        for line in body.split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith(">") and not line.startswith("|") and not line.startswith("---"):
                excerpt = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', line)
                excerpt = re.sub(r'[*`]', '', excerpt)
                break

        # Write article HTML
        article_html = ARTICLE_TEMPLATE.format(
            title=title, url=url, author=author, date=date,
            tags_html=tags_html, content=content_html
        )
        (ARTICLES_DIR / f"{slug}.html").write_text(article_html, encoding="utf-8")

        articles.append({
            "slug": slug,
            "title": title,
            "author": author,
            "date": date,
            "tags": tags,
            "excerpt": excerpt[:200],
            "url": url
        })

    # Write articles.json
    (SITE_DIR / "articles.json").write_text(
        json.dumps(articles, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\nBuilt {len(articles)} articles → site/articles/")
    print(f"Index: site/articles.json")

if __name__ == "__main__":
    build()
