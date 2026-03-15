#!/usr/bin/env python3
"""
build.py — AI Learning static site generator

Converts content/*.md → site/ (HTML pages + JSON indexes)
Uses mistune for Markdown, PyYAML for frontmatter, Prism.js for syntax highlighting.

Run: python3 build.py
"""

import json
import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import mistune
import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
SITE_DIR = ROOT / "site"


# ---------------------------------------------------------------------------
# Template Engine
# ---------------------------------------------------------------------------
_template_cache = {}


def load_template(name):
    """Load and cache a template file."""
    if name not in _template_cache:
        path = TEMPLATES_DIR / name
        _template_cache[name] = path.read_text(encoding="utf-8")
    return _template_cache[name]


def render(template_str, **kwargs):
    """Replace {key} placeholders. Only replaces keys present in kwargs."""
    def replacer(match):
        key = match.group(1)
        if key in kwargs:
            return str(kwargs[key])
        return match.group(0)
    return re.sub(r"\{([a-zA-Z_]\w*)\}", replacer, template_str)


def render_page(title, content, root="", extra_scripts=""):
    """Wrap content in base template."""
    base = load_template("base.html")
    return render(base,
                  title=title,
                  content=content,
                  root=root,
                  extra_scripts=extra_scripts)


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------
class PrismRenderer(mistune.HTMLRenderer):
    """Renderer that emits Prism.js-compatible code blocks."""

    def block_code(self, code, info=None, **attrs):
        lang = (info or "").strip().split()[0] if info else ""
        cls = f' class="language-{lang}"' if lang else ""
        escaped = mistune.html(code)
        return f"<pre><code{cls}>{escaped}</code></pre>\n"


def create_markdown():
    return mistune.create_markdown(
        renderer=PrismRenderer(),
        plugins=["table", "strikethrough", "footnotes"],
    )


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------
def parse_frontmatter(text):
    """Parse YAML frontmatter with PyYAML."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    header = text[3:end]
    body = text[end + 3:].strip()
    fm = yaml.safe_load(header) or {}
    return fm, body


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
def reading_time(text):
    """CJK: 500 chars/min, English: 200 words/min."""
    cjk_count = len(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf]", text))
    no_cjk = re.sub(r"[\u4e00-\u9fff\u3400-\u4dbf]", "", text)
    word_count = len(no_cjk.split())
    minutes = cjk_count / 500 + word_count / 200
    return max(1, round(minutes))


def extract_excerpt(body, max_len=200):
    """First non-heading, non-meta paragraph."""
    for line in body.split("\n"):
        line = line.strip()
        if (line
                and not line.startswith("#")
                and not line.startswith(">")
                and not line.startswith("|")
                and not line.startswith("---")
                and not line.startswith("```")):
            text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", line)
            text = re.sub(r"[*`]", "", text)
            return text[:max_len]
    return ""


def slugify(text):
    """URL-safe slug, keeps CJK characters."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s\u4e00-\u9fff\u3400-\u4dbf-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-") or "uncategorized"


def html_escape(text):
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


# ---------------------------------------------------------------------------
# Related Articles (tag overlap)
# ---------------------------------------------------------------------------
def find_related(current, all_articles, max_count=3):
    cur_tags = set(current.get("tags", []))
    if not cur_tags:
        return []
    scored = []
    for a in all_articles:
        if a["slug"] == current["slug"]:
            continue
        overlap = len(cur_tags & set(a.get("tags", [])))
        if overlap > 0:
            scored.append((overlap, a["date"], a))
    scored.sort(key=lambda x: (-x[0], x[1]), reverse=False)
    return [item[2] for item in scored[:max_count]]


# ---------------------------------------------------------------------------
# Render Helpers
# ---------------------------------------------------------------------------
def render_tags_html(tags):
    return "".join(f'<span class="tag">{html_escape(t)}</span>' for t in tags)


def render_article_card(article, root=""):
    tpl = load_template("partials/article-card.html")
    return render(tpl,
                  slug=article["slug"],
                  title=html_escape(article["title"]),
                  date=article["date"],
                  author=html_escape(article["author"]),
                  reading_time=article["reading_time"],
                  excerpt=html_escape(article["excerpt"]),
                  tags_html=render_tags_html(article["tags"]),
                  tags_csv=",".join(article["tags"]),
                  category=html_escape(article.get("category", "")),
                  root=root)


def render_cards(articles, root=""):
    return "\n".join(render_article_card(a, root) for a in articles)


# ---------------------------------------------------------------------------
# Page Generators
# ---------------------------------------------------------------------------
def generate_article_page(article, all_articles, series_map):
    """Generate a single article HTML page."""
    root = "../"
    related = find_related(article, all_articles)

    # Related articles section
    related_html = ""
    if related:
        related_tpl = load_template("partials/related-articles.html")
        related_html = render(related_tpl, cards=render_cards(related, root))

    # Series navigation
    series_nav = ""
    series_name = article.get("series", "")
    if series_name and series_name in series_map:
        s_articles = series_map[series_name]
        total = len(s_articles)
        order = article.get("series_order", 0)
        series_slug = slugify(series_name)
        series_nav = (
            '<div class="series-nav">'
            '<div class="series-nav-title">系列文章</div>'
            f'<div class="series-nav-name"><a href="{root}series/{series_slug}.html">'
            f'{html_escape(series_name)}</a></div>'
            f'<div class="series-nav-pos">第 {order} / {total} 篇</div>'
            '</div>'
        )

    # Tags with links
    tags_html = "".join(
        f'<a href="{root}tags/{slugify(t)}.html" class="tag">{html_escape(t)}</a>'
        for t in article["tags"]
    )

    article_tpl = load_template("article.html")
    content = render(article_tpl,
                     root=root,
                     title=html_escape(article["title"]),
                     date=article["date"],
                     author=html_escape(article["author"]),
                     author_slug=slugify(article["author"]),
                     reading_time=article["reading_time"],
                     source_url=article.get("url", ""),
                     category=html_escape(article.get("category", "未分類")),
                     category_slug=slugify(article.get("category", "未分類")),
                     tags_html=tags_html,
                     series_nav=series_nav,
                     content_html=article["content_html"],
                     related_html=related_html)

    html = render_page(article["title"], content, root=root)
    out = SITE_DIR / "articles" / f'{article["slug"]}.html'
    out.write_text(html, encoding="utf-8")


def generate_tag_pages(tags_map):
    """Generate tag index + individual tag pages."""
    root = "../"

    # Individual tag pages
    for tag_name, articles in tags_map.items():
        tag_slug = slugify(tag_name)
        tpl = load_template("tag.html")
        content = render(tpl,
                         root=root,
                         tag_name=html_escape(tag_name),
                         count=len(articles),
                         articles_html=render_cards(articles, root))
        html = render_page(f"{tag_name}", content, root=root)
        (SITE_DIR / "tags" / f"{tag_slug}.html").write_text(html, encoding="utf-8")

    # Tag index page
    cloud_items = sorted(tags_map.items(), key=lambda x: -len(x[1]))
    cloud_html = "\n".join(
        f'<a href="{root}tags/{slugify(name)}.html" class="tag-cloud-item">'
        f'{html_escape(name)} <span class="tag-cloud-count">{len(arts)}</span></a>'
        for name, arts in cloud_items
    )
    content = (
        '<div class="container">'
        '<div class="page-header">'
        '<h1 class="page-title">Tags</h1>'
        f'<p class="page-subtitle">{len(tags_map)} 個標籤</p>'
        '</div>'
        f'<div class="tag-cloud">{cloud_html}</div>'
        '</div>'
    )
    html = render_page("Tags", content, root=root)
    (SITE_DIR / "tags" / "index.html").write_text(html, encoding="utf-8")


def generate_category_pages(categories_map):
    """Generate category index + individual category pages."""
    root = "../"

    for cat_name, articles in categories_map.items():
        cat_slug = slugify(cat_name)
        tpl = load_template("category.html")
        content = render(tpl,
                         root=root,
                         category_name=html_escape(cat_name),
                         count=len(articles),
                         articles_html=render_cards(articles, root))
        html = render_page(cat_name, content, root=root)
        (SITE_DIR / "categories" / f"{cat_slug}.html").write_text(html, encoding="utf-8")

    # Category index
    cloud_items = sorted(categories_map.items(), key=lambda x: -len(x[1]))
    cloud_html = "\n".join(
        f'<a href="{root}categories/{slugify(name)}.html" class="tag-cloud-item">'
        f'{html_escape(name)} <span class="tag-cloud-count">{len(arts)}</span></a>'
        for name, arts in cloud_items
    )
    content = (
        '<div class="container">'
        '<div class="page-header">'
        '<h1 class="page-title">分類</h1>'
        f'<p class="page-subtitle">{len(categories_map)} 個分類</p>'
        '</div>'
        f'<div class="tag-cloud">{cloud_html}</div>'
        '</div>'
    )
    html = render_page("分類", content, root=root)
    (SITE_DIR / "categories" / "index.html").write_text(html, encoding="utf-8")


def generate_series_pages(series_map):
    """Generate series index + individual series pages."""
    root = "../"

    for series_name, articles in series_map.items():
        series_slug = slugify(series_name)
        items_html = ""
        for a in articles:
            order = a.get("series_order", 0)
            items_html += (
                f'<li class="series-item">'
                f'<span class="series-number">{order}</span>'
                f'<div class="series-item-info">'
                f'<div class="series-item-title">'
                f'<a href="{root}articles/{a["slug"]}.html">{html_escape(a["title"])}</a>'
                f'</div>'
                f'<div class="series-item-meta">{a["date"]} · {a["reading_time"]} min</div>'
                f'</div></li>'
            )
        tpl = load_template("series.html")
        content = render(tpl,
                         root=root,
                         series_name=html_escape(series_name),
                         count=len(articles),
                         articles_html=items_html)
        html = render_page(series_name, content, root=root)
        (SITE_DIR / "series" / f"{series_slug}.html").write_text(html, encoding="utf-8")

    # Series index
    groups_html = ""
    for series_name, articles in sorted(series_map.items()):
        series_slug = slugify(series_name)
        items = "".join(
            f'<li class="series-item">'
            f'<span class="series-number">{a.get("series_order", 0)}</span>'
            f'<div class="series-item-info">'
            f'<div class="series-item-title">'
            f'<a href="{root}articles/{a["slug"]}.html">{html_escape(a["title"])}</a>'
            f'</div></div></li>'
            for a in articles
        )
        groups_html += (
            f'<div class="series-group">'
            f'<div class="series-name">'
            f'<a href="{root}series/{series_slug}.html">{html_escape(series_name)}</a>'
            f' <span class="tag-cloud-count">({len(articles)} 篇)</span></div>'
            f'<ol class="series-articles">{items}</ol></div>'
        )
    content = (
        '<div class="container">'
        '<div class="page-header">'
        '<h1 class="page-title">系列</h1>'
        f'<p class="page-subtitle">{len(series_map)} 個系列</p>'
        '</div>'
        f'<div class="series-list">{groups_html}</div>'
        '</div>'
    )
    html = render_page("系列", content, root=root)
    (SITE_DIR / "series" / "index.html").write_text(html, encoding="utf-8")


def generate_author_pages(authors_map, all_tags_map):
    """Generate author index + individual author pages."""
    root = "../"
    max_articles = max((len(arts) for arts in authors_map.values()), default=1)

    for author_name, articles in authors_map.items():
        author_slug = slugify(author_name)
        avatar = author_name[0] if author_name else "?"

        # Contribution chart: articles per tag
        tag_counts = defaultdict(int)
        for a in articles:
            for t in a["tags"]:
                tag_counts[t] += 1
        top_tags = sorted(tag_counts.items(), key=lambda x: -x[1])[:5]

        max_tag_count = max((c for _, c in top_tags), default=1)
        bars_html = ""
        for tag, count in top_tags:
            pct = round(count / max_tag_count * 100)
            bars_html += (
                f'<div class="contribution-bar">'
                f'<span class="contribution-label">{html_escape(tag)}</span>'
                f'<div class="contribution-track">'
                f'<div class="contribution-fill" style="width:{pct}%"></div>'
                f'</div>'
                f'<span class="contribution-count">{count}</span>'
                f'</div>'
            )

        tpl = load_template("author.html")
        content = render(tpl,
                         root=root,
                         author_name=html_escape(author_name),
                         avatar_letter=avatar,
                         total_articles=len(articles),
                         contribution_html=bars_html,
                         articles_html=render_cards(articles, root))
        html = render_page(author_name, content, root=root)
        (SITE_DIR / "authors" / f"{author_slug}.html").write_text(html, encoding="utf-8")

    # Authors index
    cards_html = ""
    for author_name, articles in sorted(authors_map.items(),
                                         key=lambda x: -len(x[1])):
        author_slug = slugify(author_name)
        avatar = author_name[0] if author_name else "?"
        cards_html += (
            f'<a href="{root}authors/{author_slug}.html" class="author-card">'
            f'<div class="author-card-avatar">{avatar}</div>'
            f'<div><div class="author-card-name">{html_escape(author_name)}</div>'
            f'<div class="author-card-count">{len(articles)} 篇文章</div>'
            f'</div></a>'
        )
    content = (
        '<div class="container">'
        '<div class="page-header">'
        '<h1 class="page-title">作者</h1>'
        f'<p class="page-subtitle">{len(authors_map)} 位作者</p>'
        '</div>'
        f'<div class="authors-grid">{cards_html}</div>'
        '</div>'
    )
    html = render_page("作者", content, root=root)
    (SITE_DIR / "authors" / "index.html").write_text(html, encoding="utf-8")


def generate_index(articles, tags_map, categories_map, series_map, authors_map):
    """Generate index page with dashboard stats."""
    root = ""

    # Stats
    now = datetime.now()
    monthly = sum(
        1 for a in articles
        if a["date"].startswith(f"{now.year}-{now.month:02d}")
    )

    # Filter bar (top tags)
    top_tags = sorted(tags_map.items(), key=lambda x: -len(x[1]))[:10]
    filter_html = ""
    if top_tags:
        btns = "".join(
            f'<button class="filter-btn" data-filter-type="tag" '
            f'data-filter="{html_escape(name)}">{html_escape(name)}</button>'
            for name, _ in top_tags
        )
        filter_html = f'<div class="filter-bar">{btns}</div>'

    # Articles
    articles_html = render_cards(articles, root)

    # Empty state
    empty = ""
    if not articles:
        empty = (
            '<div class="empty">'
            '<div class="empty-icon">📚</div>'
            '<p>還沒有學習筆記。<br>'
            '在 Claude Code 中輸入 <code>/ai-learning &lt;url&gt;</code> 開始第一篇。</p>'
            '</div>'
        )

    tpl = load_template("index.html")
    content = render(tpl,
                     stat_total=len(articles),
                     stat_monthly=monthly,
                     stat_authors=len(authors_map),
                     stat_tags=len(tags_map),
                     filter_bar=filter_html,
                     articles_html=articles_html,
                     empty_state=empty)

    extra = f'<script src="{root}js/filter.js"></script>' if articles else ""
    html = render_page("團隊學習筆記", content, root=root, extra_scripts=extra)
    (SITE_DIR / "index.html").write_text(html, encoding="utf-8")


def generate_json(articles):
    """Generate articles.json and search-index.json."""
    # articles.json (full metadata)
    articles_data = [
        {
            "slug": a["slug"],
            "title": a["title"],
            "author": a["author"],
            "date": a["date"],
            "tags": a["tags"],
            "category": a.get("category", ""),
            "series": a.get("series", ""),
            "reading_time": a["reading_time"],
            "excerpt": a["excerpt"],
            "url": a.get("url", ""),
        }
        for a in articles
    ]
    (SITE_DIR / "articles.json").write_text(
        json.dumps(articles_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # search-index.json (lightweight for Fuse.js)
    search_data = [
        {
            "slug": a["slug"],
            "title": a["title"],
            "author": a["author"],
            "tags": ", ".join(a["tags"]),
            "excerpt": a["excerpt"],
        }
        for a in articles
    ]
    (SITE_DIR / "search-index.json").write_text(
        json.dumps(search_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# Main Build
# ---------------------------------------------------------------------------
def build():
    print("Building AI Learning site...")

    # Clean output
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True)

    # Copy static assets
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, SITE_DIR, dirs_exist_ok=True)

    # Create output directories
    for d in ["articles", "tags", "categories", "series", "authors"]:
        (SITE_DIR / d).mkdir(parents=True, exist_ok=True)

    # Parse all markdown files
    md = create_markdown()
    articles = []

    if not CONTENT_DIR.exists():
        CONTENT_DIR.mkdir(parents=True)

    for md_file in sorted(CONTENT_DIR.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)

        # Skip drafts
        if fm.get("draft", False):
            print(f"  [DRAFT] {md_file.name}")
            continue

        title = fm.get("title", md_file.stem)
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        article = {
            "slug": md_file.stem,
            "title": title,
            "url": fm.get("url", ""),
            "author": fm.get("author", "Unknown"),
            "date": str(fm.get("date", datetime.now().strftime("%Y-%m-%d"))),
            "tags": tags,
            "category": fm.get("category", "未分類"),
            "series": fm.get("series", ""),
            "series_order": fm.get("series_order", 0),
            "source_title": fm.get("source_title", ""),
            "source_author": fm.get("source_author", ""),
            "body": body,
            "content_html": md(body),
            "reading_time": reading_time(body),
            "excerpt": extract_excerpt(body),
        }
        articles.append(article)
        print(f"  {md_file.name} ({article['reading_time']} min)")

    # Sort by date descending
    articles.sort(key=lambda a: a["date"], reverse=True)

    # Build indexes
    tags_map = defaultdict(list)
    categories_map = defaultdict(list)
    series_map = defaultdict(list)
    authors_map = defaultdict(list)

    for a in articles:
        for tag in a["tags"]:
            tags_map[tag].append(a)
        categories_map[a["category"]].append(a)
        if a["series"]:
            series_map[a["series"]].append(a)
        authors_map[a["author"]].append(a)

    # Sort series articles by order
    for name in series_map:
        series_map[name].sort(key=lambda a: a.get("series_order", 0))

    # Generate pages
    for article in articles:
        generate_article_page(article, articles, series_map)

    generate_tag_pages(tags_map)
    generate_category_pages(categories_map)
    generate_series_pages(series_map)
    generate_author_pages(authors_map, tags_map)
    generate_index(articles, tags_map, categories_map, series_map, authors_map)
    generate_json(articles)

    # Summary
    print(f"\n✓ Built {len(articles)} articles")
    print(f"  Tags: {len(tags_map)} | Categories: {len(categories_map)}"
          f" | Series: {len(series_map)} | Authors: {len(authors_map)}")
    print(f"  Output: {SITE_DIR}/")


if __name__ == "__main__":
    build()
