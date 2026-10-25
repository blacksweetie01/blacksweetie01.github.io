#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 content/posts.json —— RSS 数据源。

内容 = 站点公告 + 全部书评（书评数据直接复用 build_reviews.REVIEWS，
不重复维护、不碰 raw）。书评条目包含：
  title   公众号发表标题
  url     reviews/<slug>.html
  date    发表日期
  description  所评著作 + 作者/译者/出版 + 原载来源
  tags    书评标签（如 ["书评","政治哲学"]）

运行：python3 tools/build_posts.py && python3 tools/build_feed.py
"""
import json
import os
import re
import sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SITE, "tools"))

import build_reviews as BR  # noqa: E402  (复用 REVIEWS 数据)

OUT = os.path.join(SITE, "content", "posts.json")

# 站点公告（手工维护的静态条目）
SITE_NOTICE = {
    "title": "一般法理学 · 站点上线",
    "url": "about.html",
    "date": "2026-10-24",
    "description": "赵英男的个人学术思想阵地：汇集法理学领域的译作、书评、教学资料、论文与新书动态，以及研究札记。内容随缘更新，由本人筛选发布。",
    "tags": ["站点"],
}


def review_description(r):
    """书评 RSS 描述：所评著作 + 作者/译者/出版 + 原载来源。"""
    b = r.get("book") or {}
    bits = []
    if b.get("author"):
        bits.append(b["author"])
    if b.get("translator"):
        bits.append("译/" + b["translator"])
    if b.get("publisher"):
        bits.append(b["publisher"])
    if b.get("year"):
        bits.append(b["year"] + "年")
    who = "（" + "，".join(bits) + "）" if bits else ""
    title = b.get("title", "")
    return "书评：评《%s》%s，原载《%s》。" % (title, who, r["source"])


def main():
    posts = [SITE_NOTICE]
    for r in BR.REVIEWS:
        tags = [t for t in re.split(r"\s+", r.get("tags", "")) if t]
        if not tags:
            tags = ["书评"]
        posts.append(
            {
                "title": r["title"],
                "url": "reviews/%s.html" % r["slug"],
                "date": r["date"],
                "description": review_description(r),
                "tags": tags,
            }
        )

    posts.sort(key=lambda p: p["date"], reverse=True)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("wrote content/posts.json with %d post(s) (%d review)" %
          (len(posts), len(posts) - 1))


if __name__ == "__main__":
    main()
