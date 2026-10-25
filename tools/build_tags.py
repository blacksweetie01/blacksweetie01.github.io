#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 tags.html —— 全站标签索引。

做法：扫描各列表页（works.html / reviews.html / updates.html / notes.html /
teaching.html）里带 data-tags 的条目，提取「标签 → 篇目」倒排索引。
书评（reviews/*.html）与著作（works/*.html）因此自动并入同一索引，
无需重复维护；标签分隔符同时支持空格、· 、 、 ， / 。

运行：python3 tools/build_tags.py
（依赖：先跑过 build_works.py 与 build_reviews.py，列表页已生成）
"""
import os
import re
import sys
from html import escape

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SITE, "tools"))

import build_reviews as BR  # noqa: E402  复用站点 header/footer 模板

OUT = os.path.join(SITE, "tags.html")

SRC_PAGES = ["works.html", "reviews.html", "updates.html", "notes.html", "teaching.html"]
TYPE_LABEL = {
    "works": "著作",
    "reviews": "书评",
    "updates": "动态",
    "notes": "札记",
    "teaching": "教学",
}

# 顶层带 data-tags 的条目块（works: <article>, reviews: <li>）
ITEM_RE = re.compile(
    r'<(?P<tag>[a-zA-Z0-9]+)\b[^>]*\bdata-tags="(?P<tags>[^"]*)"[^>]*>'
    r"(?P<body>.*?)</(?P=tag)>",
    re.S,
)
# 条目标题：<h3><a href="...">标题</a></h3>
H3_RE = re.compile(r'<h3>\s*<a href="(?P<url>[^"]+)"[^>]*>(?P<title>.*?)</a>', re.S)

TAG_SPLIT = re.compile(r"[\s·、,，/]+")


def item_type(url):
    for k, label in TYPE_LABEL.items():
        if url.startswith(k + "/"):
            return label
    return "文章"


def parse_page(html):
    items = []
    for m in ITEM_RE.finditer(html):
        hm = H3_RE.search(m.group("body"))
        if not hm:
            continue
        url = hm.group("url")
        title = re.sub(r"<[^>]+>", "", hm.group("title")).strip()
        if not title or not url:
            continue
        # 跳过占位条目（href="#" 等尚无真实页面的链接，避免索引出现死链）
        if url.lstrip().startswith("#"):
            continue
        tags = [t for t in TAG_SPLIT.split(m.group("tags")) if t]
        if not tags:
            continue
        items.append({"url": url, "title": title, "tags": tags, "type": item_type(url)})
    return items


def build():
    agg = {}
    for page in SRC_PAGES:
        path = os.path.join(SITE, page)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            html = f.read()
        found = parse_page(html)
        if found:
            print("  %-14s %d 条目" % (page, len(found)))
        for it in found:
            for t in it["tags"]:
                agg.setdefault(t, []).append(it)

    if not agg:
        print("警告：未解析到任何带 data-tags 的条目，tags.html 未生成。")
        return

    tags_sorted = sorted(agg.keys(), key=lambda t: (-len(agg[t]), t))

    cloud = "\n".join(
        '        <a class="tag" href="#tag-%s">%s<span class="tag-n">%d</span></a>'
        % (escape(t), escape(t), len(agg[t]))
        for t in tags_sorted
    )

    sections = []
    for t in tags_sorted:
        lis = "\n".join(
            '          <li><a href="%s">%s</a><span class="tagtype">%s</span></li>'
            % (escape(it["url"]), escape(it["title"]), escape(it["type"]))
            for it in agg[t]
        )
        sections.append(
            '      <section class="tag-section" id="tag-%s">\n'
            '        <h2>%s<span class="tag-count">%d</span></h2>\n'
            '        <ul class="tag-items">\n%s\n        </ul>\n'
            "      </section>" % (escape(t), escape(t), len(agg[t]), lis)
        )

    body = """  <main>
    <section class="wrap">
    <h1 class="page-title">标签</h1>

    <div class="tag-cloud">
%s
      </div>

%s
    </section>
  </main>
""" % (cloud, "\n".join(sections))

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(BR.header("标签", rel="") + body + BR.FOOTER.format(rel=""))

    print("wrote tags.html with %d tag(s)" % len(agg))


if __name__ == "__main__":
    build()
