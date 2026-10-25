# -*- coding: utf-8 -*-
"""生成「城市」栏目：city.html（三大城市入口）+ city/<slug>.html（摄影作品集）。

用法：
  python3 tools/build_city.py

照片来源：content/city/<slug>/ 下的 jpg / jpeg / png / webp 文件。
  - 上传照片后重跑本脚本即可，无需改代码。
  - 可选说明文字：在同目录放 captions.json，格式 {"文件名": "说明文字"}。
  - 分类标识图（城市特色横幅）位于 assets/city/<slug>.jpg。
"""
import os
import json
from urllib.parse import quote

from build_works import header, FOOTER, SITE

CITIES = [
    dict(
        slug="beijing", name="北京", en="BEIJING",
        tagline="红墙金瓦 · 皇城气韵",
    ),
    dict(
        slug="shanghai", name="上海", en="SHANGHAI",
        tagline="外滩云影 · 浦江两岸",
    ),
    dict(
        slug="wuhan", name="武汉", en="WUHAN",
        tagline="黄鹤楼头 · 江城烟火",
    ),
]

EXTS = (".jpg", ".jpeg", ".png", ".webp")


def city_photos(slug):
    """读取某城市的照片列表，返回 [(文件名, 说明), ...]，按文件名排序。"""
    d = os.path.join(SITE, "content", "city", slug)
    if not os.path.isdir(d):
        return []
    files = sorted(f for f in os.listdir(d) if f.lower().endswith(EXTS))
    cap_path = os.path.join(d, "captions.json")
    caps = {}
    if os.path.exists(cap_path):
        with open(cap_path, encoding="utf-8") as f:
            caps = json.load(f)
    return [(f, caps.get(f, "")) for f in files]


def build_index():
    tiles = []
    for c in CITIES:
        n = len(city_photos(c["slug"]))
        count = f'{n} 幅作品' if n else '即将上线'
        tiles.append(f"""      <a class="city-tile" href="city/{c['slug']}.html">
        <div class="city-tile-img"><img src="assets/city/{c['slug']}.jpg" alt="{c['name']}——{c['tagline']}" /></div>
        <div class="city-tile-body">
          <span class="city-en">{c['en']}</span>
          <h2>{c['name']}</h2>
          <p class="city-tag">{c['tagline']}</p>
          <span class="city-count">{count}</span>
        </div>
      </a>""")
    body = f"""{header("城市")}
  <main>
    <section class="wrap-wide">
      <h1 class="page-title">城市</h1>

      <div class="city-grid">
{chr(10).join(tiles)}
      </div>
    </section>

    <section class="wrap comments">
      <h2>评论</h2>
      <div id="giscus-mount"></div>
    </section>
  </main>
"""
    with open(os.path.join(SITE, "city.html"), "w", encoding="utf-8") as f:
        f.write(body + FOOTER.format(rel=""))
    print("built city.html (%d cities)" % len(CITIES))


def build_gallery(c):
    photos = city_photos(c["slug"])
    rel = "../"
    if photos:
        items = []
        for fname, cap in photos:
            src = f"{rel}content/city/{c['slug']}/{quote(fname)}"
            figcap = f"<figcaption>{cap}</figcaption>" if cap else ""
            items.append(f"""      <figure class="photo-item">
        <img src="{src}" alt="{cap or c['name']}" loading="lazy" />
        {figcap}
      </figure>""")
        grid = '<div class="photo-grid">\n' + "\n".join(items) + "\n    </div>"
    else:
        grid = '<p class="placeholder-note">作品整理中，即将上传。</p>'

    body = f"""{header(c["name"], rel=rel)}
  <main>
    <section class="wrap-wide">
      <p class="breadcrumb"><a href="../city.html">城市</a> / {c['name']}</p>
      <h1 class="page-title">{c['name']}<span class="title-en">{c['en']}</span></h1>

    {grid}
    </section>

    <section class="wrap comments">
      <h2>评论</h2>
      <div id="giscus-mount"></div>
    </section>
  </main>
"""
    out_dir = os.path.join(SITE, "city")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, c["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(body + FOOTER.format(rel=rel))
    print("built city/%s.html (%d photos)" % (c["slug"], len(photos)))


def main():
    build_index()
    for c in CITIES:
        build_gallery(c)


if __name__ == "__main__":
    main()
