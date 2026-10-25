# -*- coding: utf-8 -*-
"""生成 reviews.html 书评列表与 reviews/*.html 详情页。
正文取自 raw/reviews/*.docx（只读，作为公众号版底本），
标题沿用公众号发表标题，结尾右下角注明来源。
运行：python3 tools/build_reviews.py
"""
import os
import re
from docx import Document

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(os.path.dirname(SITE), "raw", "reviews")
OUT_REVIEW_DIR = os.path.join(SITE, "reviews")
COVERS = os.path.join(SITE, "assets", "covers")
COVERS_REV = os.path.join(COVERS, "reviews")

# --------------------------------------------------------------- 数据
# source: "上海书评" 或 "新京报书评周刊"
REVIEWS = [
    dict(slug="larmore-women", file="当我们善良理性却又针锋相对_副本.docx",
         title="如果我们都没有错，为什么还是无法达成共识？", source="新京报书评周刊",
         date="2026-10-05", byline="赵英男", tags="书评 政治哲学",
         book=dict(title="什么是政治哲学", author="[美] 查尔斯·拉莫尔",
                   translator="钱一栋", publisher="上海人民出版社", year="2026")),
    dict(slug="gongli-zhuyi", file="揭开功利主义的面纱_副本.docx",
         title="一个人的自私自利，为何最终会通向多数人的幸福？", source="新京报书评周刊",
         date="2026-08-28", byline="赵英男", tags="书评 功利主义",
         book=dict(title="幸福哲学家：功利主义巨擘的生平与著作", author="[美] 巴特·舒尔茨",
                   translator="陈江进 等", publisher="商务印书馆", year="2026")),
    dict(slug="gonggongren", file="公共人的长成_副本.docx",
         title="为什么说法律不仅是底线，也是思考正义的起点？", source="新京报书评周刊",
         date="2026-05-04", byline="赵英男", tags="书评 法律与道德",
         book=dict(title="法袍下的自主概念：法学与哲学的对话", author="张晓燕",
                   publisher="商务印书馆", year="2025")),
    dict(slug="yuwanwu", file="与万物一起生长_副本.docx",
         title="赵英男评《荒野中的哲学家》|与万物一起生长", source="上海书评",
         date="2026-04-26", byline="赵英男", tags="书评 自然主义",
         book=dict(title="荒野中的哲学家", author="孙宁", publisher="上海三联书店",
                   year="2026", pages="223", price="68.00")),
    dict(slug="shiteliaosi-ping", file="赵英男评_副本.docx",
         title="赵英男评《施特劳斯论历史的终结》|当密涅瓦的猫头鹰在黄昏起飞", source="上海书评",
         date="2025-12-06", byline="文 | 赵英男", tags="书评 政治哲学",
         book=dict(title="施特劳斯论历史的终结：黑格尔《历史哲学》讲疏",
                   author="[德] 列奥·施特劳斯 讲疏，[美] 保罗·弗朗哥 编",
                   translator="赵英男", publisher="上海文艺出版社", year="2025",
                   pages="598", price="148.00", cover="shiteliaosi-lishi-zhongjie.jpg")),
    dict(slug="sirendingzhi", file="当法律可以私人定制_副本.docx",
         title="当法律可以私人定制", source="新京报书评周刊",
         date="2025-11-06", byline="赵英男", tags="书评 法律与科技",
         book=dict(title="私人定制的法律", author="[美] 欧姆瑞·本-沙哈尔、[以] 阿里尔·普锐理",
                   translator="王俣璇", publisher="商务印书馆", year="2025")),
    dict(slug="xinxi-fenfan", file="信息纷繁的时代_副本.docx",
         title="信息纷繁的时代，我们还能相信什么？", source="新京报书评周刊",
         date="2025-05-06", byline="赵英男", tags="书评 认识论",
         book=dict(title="实锤", author="[美] 弗雷德里克·肖尔", translator="高虹远",
                   publisher="云南人民出版社（理想国）", year="2025")),
    dict(slug="leiter-fangtan", file="布莱恩·莱特谈尼采与自然主义法理学_副本.docx",
         title="布莱恩·莱特谈尼采与自然主义法理学", source="上海书评",
         date="2025-03-30", byline="采访 | 赵英男", tags="书评 自然主义法理学",
         book=dict(title="自然化法学：美国法律现实主义和法哲学中的自然主义文集",
                   author="[美] 布莱恩·莱特", translator="赵英男",
                   publisher="商务印书馆", year="2024", pages="494", price="78.00",
                   cover="ziranhua-falixue.jpg")),
    dict(slug="jubian-mianqian", file="巨变面前_副本.docx",
         title="巨变面前，法律可以做什么？", source="新京报书评周刊",
         date="2024-12-16", byline="赵英男", tags="书评 法律史",
         book=dict(title="秩序四千年：人类如何战胜混乱", author="[英] 费尔南达·皮里",
                   translator="李立丰", publisher="广西师范大学出版社", year="2024")),
    dict(slug="shiluo-niandai", file="“失落年代”社会理论家的迷惘_副本.docx",
         title="“失落年代”社会理论家的迷惘", source="新京报书评周刊",
         date="2024-10-28", byline="赵英男", tags="书评 社会理论",
         book=dict(title="晚期现代社会的危机：社会理论能做什么？",
                   author="[德] 安德雷亚斯·莱克维茨、[德] 哈特穆特·罗萨",
                   translator="郑作彧", publisher="上海人民出版社", year="2024")),
    dict(slug="scott-huozhe", file="詹姆斯·斯科特：“活着为了讲述”_副本.docx",
         title="赵英男读詹姆斯·斯科特：“活着为了讲述”", source="上海书评",
         date="2024-08-23", byline="赵英男", tags="书评 詹姆斯·斯科特",
         book=dict(title="詹姆斯·斯科特著作群",
                   extra="本书评围绕詹姆斯·斯科特的多部作品展开，包括《作茧自缚》《国家的视角》《六论自发性》《弱者的武器》《农民的道义经济学》等。")),
    dict(slug="weber-zhuan", file="举起时代的重负，掷入心灵的深谷_副本.docx",
         title="赵英男读《韦伯传》|举起时代的重负，掷入心灵的深谷", source="上海书评",
         date="2023-08-30", byline="赵英男", tags="书评 社会学",
         book=dict(title="韦伯传：思与意志", author="[德] 迪尔克·克斯勒",
                   translator="高星璐、黄自勤", reviewer="阎克文 审校",
                   publisher="广西师范大学出版社", year="2023")),
    dict(slug="tamanaha-fangtan", file="塔玛纳哈文字访谈提纲_副本.docx",
         title="布莱恩·塔玛纳哈谈法律多元主义与法理学", source="上海书评",
         date="2023-05-14", byline="采访 | 赵英男", tags="书评 法律多元主义",
         book=dict(title="法律多元主义阐释：历史、理论与影响",
                   author="[美] 布莱恩·Z. 塔玛纳哈", translator="赵英男",
                   publisher="商务印书馆", year="2023", pages="368", price="85.00",
                   cover="falv-duoyuan-zhuyi.jpg")),
    dict(slug="guojia-xingqi", file="国家的兴起与政治哲学的要义_副本.docx",
         title="国家的兴起与政治哲学的要义", source="上海书评",
         date="2022-07-08", byline="赵英男", tags="书评 国家理论",
         book=dict(title="作茧自缚：人类早期国家的深层历史",
                   author="[美] 詹姆斯·C. 斯科特", translator="田雷",
                   publisher="中国政法大学出版社", year="2022")),
    dict(slug="yuese-fu-laz", file="约瑟夫·拉兹与法哲学的战国时代_副本.docx",
         title="约瑟夫·拉兹与法哲学的战国时代", source="上海书评",
         date="2022-05-03", byline="赵英男", tags="书评 法哲学",
         book=dict(title="约瑟夫·拉兹（1939–2022）",
                   extra="本文为纪念国际著名法哲学家约瑟夫·拉兹而作，回顾其学说与影响，并非针对单一著作。")),
    dict(slug="chengren-yide", file="成人以德_副本.docx",
         title="《成人以德》：法律会让我们更道德吗？", source="上海书评",
         date="2021-01-20", byline="赵英男", tags="书评 自然法",
         book=dict(title="成人以德：公民自由和公共道德", author="[美] 罗伯特·P. 乔治",
                   translator="孙海波、彭宁", publisher="商务印书馆", year="2020")),
    dict(slug="jiaoguan-xinling", file="娇惯的心灵_副本.docx",
         title="赵英男评《娇惯的心灵》|我们的教育为何不奏效？", source="上海书评",
         date="2020-08-22", byline="赵英男", tags="书评 教育",
         book=dict(title="娇惯的心灵：“钢铁”是怎么没有炼成的？",
                   author="[美] 格雷格·卢金诺夫、[美] 乔纳森·海特",
                   translator="田雷、苏心", publisher="生活·读书·新知三联书店",
                   year="2020", pages="527", price="69.00")),
    dict(slug="chongdu-fushan", file="重读福山_副本.docx",
         title="重读福山：政治秩序衰败中的制度与人心", source="上海书评",
         date="2020-02-10", byline="赵英男", tags="书评 政治秩序",
         book=dict(title="政治秩序的起源与衰败（福山著作）",
                   extra="本书评聚焦福山的政治秩序研究，涉及《政治秩序的起源》《政治秩序的衰败》《历史的终结与最后的人》等。")),
]

# 按日期从新到旧排序
REVIEWS.sort(key=lambda r: r["date"], reverse=True)

# --------------------------------------------------------------- 正文提取
def clean_para(p):
    return p.replace("\u3000", " ").strip()

def is_boilerplate(p):
    if not p:
        return True
    if len(p) > 120:
        return False
    pats = [
        r"本文为独家原创", r"未经.{0,20}授权", r"未经.*转载", r"欢迎转发",
        r"(撰文|文|采访)\s*[|｜]", r"责任编辑|值班编辑", r"本文来自", r"本文内容出自",
        r"阅读原文", r"更多原创资讯", r"作者[：/]\s*赵英男", r"^\s*作者[:：]",
        r"^\s*《.*》\s*作者[:：]", r"专题更多内容详见", r"点击原文",
    ]
    return any(re.search(pat, p) for pat in pats)

def extract_docx(path):
    doc = Document(path)
    paras = [clean_para(p.text) for p in doc.paragraphs]
    paras = [p for p in paras if p]
    title = paras[0]
    body = paras[1:]
    # 跳过紧邻标题的署名行
    if body and ("赵英男" in body[0]) and len(body[0]) < 60:
        body = body[1:]
    # 副题（破折号开头的“读《…》”提示语）
    dek = ""
    if body and re.match(r"^——.*《", body[0]):
        dek = body.pop(0)
    body = [p for p in body if not is_boilerplate(p)]
    return title, body, dek

def body_to_html(body):
    out = []
    for p in body:
        # 将纯中文短行识别为小节标题
        if re.match(r"^[\u4e00-\u9fff]{2,16}$", p):
            out.append(f'<h2 class="review-h2">{p}</h2>')
        else:
            out.append(f"<p>{p}</p>")
    return "\n".join(out)

def excerpt(body, n=92):
    for p in body:
        if len(p) > 12:
            return (p[:n] + "…") if len(p) > n else p
    return ""

def fmt_date(d):
    y, m, day = d.split("-")
    return f"{int(y)}年{int(m)}月{int(day)}日"

# --------------------------------------------------------------- 模板
def header(title, rel=""):
    return f"""<!doctype html>
<html lang="zh-CN" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} · 一般法理学</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{rel}assets/css/style.css" />
  <link rel="alternate" type="application/rss+xml" title="一般法理学" href="{rel}feed.xml" />
</head>
<body>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="{rel}index.html">一般法理学</a>
      <button class="menu-toggle" data-menu-toggle aria-label="菜单">菜单</button>
      <nav id="nav-links" class="nav-links">
        <a href="{rel}works.html">著作</a>
        <a href="{rel}reviews.html">书评</a>
        <a href="{rel}teaching.html">教学</a>
        <a href="{rel}updates.html">动态</a>
        <a href="{rel}notes.html">札记</a>
        <a href="{rel}tags.html">标签</a>
        <a href="{rel}about.html">关于</a>
        <button class="icon-btn" data-search-open>搜索</button>
        <button class="icon-btn" data-theme-toggle>主题</button>
      </nav>
    </div>
  </header>
"""

FOOTER = """
  <footer class="site-footer">
    <div class="wrap">
      <span>一般法理学</span>
      <span><a href="{rel}about.html">关于</a> · <a href="{rel}tags.html">标签</a> · <a href="{rel}feed.xml">RSS</a></span>
    </div>
  </footer>

  <div class="search-overlay" id="search-overlay">
    <div class="search-box">
      <input id="search-input" type="text" placeholder="搜索本站内容…" autocomplete="off" />
      <div class="hint"><span>按 Esc 关闭</span><span>Cmd/Ctrl + K</span></div>
      <button class="icon-btn" data-search-close style="margin-top:.8rem">关闭</button>
    </div>
  </div>

  <script src="{rel}assets/js/site-config.js"></script>
  <script src="{rel}assets/js/giscus.js"></script>
  <script src="{rel}assets/js/main.js"></script>
</body>
</html>
"""

def book_card(book, slug, rel):
    if not book:
        return ""
    title = book.get("title", "")
    rows = []
    if book.get("author"):
        rows.append(f'<div><dt>作者</dt><dd>{book["author"]}</dd></div>')
    if book.get("translator"):
        rows.append(f'<div><dt>译者</dt><dd>{book["translator"]}</dd></div>')
    if book.get("reviewer"):
        rows.append(f'<div><dt>审校</dt><dd>{book["reviewer"]}</dd></div>')
    pub = book.get("publisher", "")
    yr = book.get("year", "")
    pubstr = " · ".join(x for x in [pub, yr] if x)
    if pubstr:
        rows.append(f'<div><dt>出版</dt><dd>{pubstr}</dd></div>')
    pages = book.get("pages"); price = book.get("price")
    if pages or price:
        bits = []
        if pages: bits.append(f"{pages} 页")
        if price: bits.append(f"{price} 元")
        rows.append(f'<div><dt>篇幅</dt><dd>{" / ".join(bits)}</dd></div>')
    dl = "".join(rows)
    cover_html = ""
    cov = os.path.join(COVERS_REV, slug + ".jpg")
    if os.path.exists(cov):
        alt = title.replace("《", "").replace("》", "")
        cover_html = f'<div class="book-cover"><img src="{rel}assets/covers/reviews/{slug}.jpg" alt="{alt}封面" /></div>'
    else:
        cover_html = f'<div class="book-cover book-cover-ph"><span>《{title}》</span><em>封面待补</em></div>'
    extra = f'<p class="book-extra">{book["extra"]}</p>' if book.get("extra") else ""
    return f"""      <aside class="book-card">
        {cover_html}
        <div class="book-info">
          <div class="book-k">所评著作</div>
          <h2 class="book-title">《{title}》</h2>
          <dl>{dl}</dl>
          {extra}
        </div>
      </aside>"""

def build_list():
    items = []
    for r in REVIEWS:
        _, body, _ = extract_docx(os.path.join(RAW, r["file"]))
        book = r.get("book") or {}
        btitle = book.get("title", "")
        if os.path.exists(os.path.join(COVERS_REV, r["slug"] + ".jpg")):
            thumb = f'<a class="rv-thumb" href="reviews/{r["slug"]}.html"><img src="assets/covers/reviews/{r["slug"]}.jpg" alt="《{btitle}》封面" loading="lazy" /></a>'
        else:
            thumb = f'<a class="rv-thumb rv-thumb-ph" href="reviews/{r["slug"]}.html"><span>《{btitle}》</span></a>'
        items.append(f"""        <li class="post-item review-item" data-searchable data-tags="{r['tags']}">
          {thumb}
          <div class="review-main">
            <div class="post-meta">{r['source']} · {r['date']}</div>
            <h3><a href="reviews/{r['slug']}.html">{r['title']}</a></h3>
            <p class="post-excerpt">{excerpt(body)}</p>
            <div class="tag-row"><span class="tag">书评</span></div>
          </div>
        </li>""")
    body_html = f"""{header("书评")}
  <main>
    <section class="wrap">
      <h1 class="page-title">书评</h1>

      <ul class="post-list">
{chr(10).join(items)}
      </ul>
    </section>

    <section class="wrap comments">
      <h2>评论</h2>
      <div id="giscus-mount"></div>
    </section>
  </main>
"""
    with open(os.path.join(SITE, "reviews.html"), "w", encoding="utf-8") as f:
        f.write(body_html + FOOTER.format(rel=""))
    print("built reviews.html (%d reviews)" % len(REVIEWS))

def build_detail(r):
    title, body, dek = extract_docx(os.path.join(RAW, r["file"]))
    body_html = body_to_html(body)
    src_note = f'本文发表于《{r["source"]}》{fmt_date(r["date"])}'
    card = book_card(r.get("book"), r["slug"], rel="../")
    dek_html = f'<div class="review-dek">{dek}</div>' if dek else ""
    article = f"""{header(r["title"], rel="../")}
  <main>
    <section class="wrap prose review-detail">
      <p class="breadcrumb"><a href="../reviews.html">书评</a> / {r['source']}</p>
      <h1 class="page-title review-title">{r['title']}</h1>
      <div class="byline">{r['byline']}</div>
      {dek_html}
      {card}
      <div class="review-body">
{body_html}
      </div>
      <div class="source-note">{src_note}</div>

      <div class="comments">
        <h2>评论</h2>
        <div id="giscus-mount"></div>
      </div>
    </section>
  </main>
"""
    path = os.path.join(OUT_REVIEW_DIR, r["slug"] + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(article + FOOTER.format(rel="../"))
    print("built reviews/%s.html" % r["slug"])

def main():
    os.makedirs(OUT_REVIEW_DIR, exist_ok=True)
    os.makedirs(COVERS_REV, exist_ok=True)
    build_list()
    for r in REVIEWS:
        build_detail(r)

if __name__ == "__main__":
    main()
