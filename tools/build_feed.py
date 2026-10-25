#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 RSS 2.0 feed.xml（一般法理学 静态站）

用法：
  1) 在 content/posts.json 中维护文章列表（见下方示例结构）
  2) 运行：python tools/build_feed.py
  3) 将生成的 feed.xml 提交到仓库根目录（与 index.html 同级）

posts.json 结构（数组，按时间倒序）：
[
  {
    "title": "文章标题",
    "url": "works/shenjing-quanli-daolun.html",   # 相对站点根的路径或绝对 URL
    "date": "2026-10-24",                         # YYYY-MM-DD
    "description": "一句话摘要（支持纯文本）",
    "tags": ["神经权利", "法理学方法论"]
  }
]
"""
import json
import os
from datetime import datetime, timezone
from xml.sax.saxutils import escape

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://blacksweetie01.github.io/"  # 部署地址（GitHub Pages）
POSTS_JSON = os.path.join(SITE_ROOT, "content", "posts.json")
OUT = os.path.join(SITE_ROOT, "feed.xml")

CHANNEL_TITLE = "一般法理学"
CHANNEL_DESC = "赵英男的个人学术思想阵地：汇集法理学领域的译作、书评、教学资料、论文与新书动态，以及研究札记。"


def rfc822(dt_str):
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        dt = datetime.now(timezone.utc)
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


def build():
    with open(POSTS_JSON, encoding="utf-8") as f:
        posts = json.load(f)

    items = []
    for p in posts:
        link = p["url"]
        if not link.startswith("http"):
            link = SITE_URL.rstrip("/") + "/" + link.lstrip("/")
        desc = escape(p.get("description", ""))
        tags = "".join(
            "<category>%s</category>" % escape(t) for t in p.get("tags", [])
        )
        items.append(
            "    <item>\n"
            "      <title>%s</title>\n"
            "      <link>%s</link>\n"
            "      <guid isPermaLink=\"false\">%s</guid>\n"
            "      <pubDate>%s</pubDate>\n"
            "      <description>%s</description>\n"
            "%s"
            "    </item>"
            % (escape(p["title"]), escape(link), escape(link), rfc822(p["date"]), desc, tags)
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        "    <title>%s</title>\n"
        "    <link>%s</link>\n"
        "    <atom:link href=\"%sfeed.xml\" rel=\"self\" type=\"application/rss+xml\"/>\n"
        "    <description>%s</description>\n"
        "    <language>zh-CN</language>\n"
        "    <lastBuildDate>%s</lastBuildDate>\n"
        "    <generator>build_feed.py</generator>\n"
        "%s\n"
        "  </channel>\n"
        "</rss>\n"
        % (
            escape(CHANNEL_TITLE),
            escape(SITE_URL),
            SITE_URL,
            escape(CHANNEL_DESC),
            rfc822(datetime.now(timezone.utc).strftime("%Y-%m-%d")),
            "\n".join(items),
        )
    )

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(xml)
    print("wrote", os.path.relpath(OUT, SITE_ROOT), "with", len(posts), "item(s)")


if __name__ == "__main__":
    build()
