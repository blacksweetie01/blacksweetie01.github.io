# -*- coding: utf-8 -*-
"""生成「教学」栏目：teaching.html（资料列表）+ teaching/<slug>.html（课程大纲详情）。

数据来源：content/teaching/法学经典著作导读（大纲）.docx
  - 直接解析 docx，按层级（必读书目 / 参考书目 / 各讲 授课内容·必读文献·参考文献）结构化后渲染。
  - 后续若更新大纲，替换该 docx 并重跑本脚本即可。

用法：
  python3 tools/build_teaching.py
"""
import os
import re
from docx import Document

from build_works import header, FOOTER, SITE

SRC_DOCX = os.path.join(SITE, "content", "teaching", "法学经典著作导读（大纲）.docx")
SLUG = "faxue-jingdian-zhuzuo-daodu"
TITLE = "法学经典著作导读课程大纲"

LECTURE_RE = re.compile(r"^([一二三四五六七八九十]+)、\s*(.+)$")
SUB_RE = re.compile(r"^（([一二三四五])）(.+)$")
NUM_RE = re.compile(r"^\d+\.\s*(.+)$")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def strip_num(s):
    return NUM_RE.sub("", s).strip()


def parse_docx(path):
    doc = Document(path)
    paras = [p.text.strip() for p in doc.paragraphs]
    paras = [p for p in paras if p]

    doc_title = ""
    doc_subtitle = ""
    sections = []
    cur = None
    reading_group = None
    lecture = None
    sub = None
    ref_group = None

    def append_item(item):
        nonlocal cur, reading_group, sub, ref_group
        if cur is not None and cur.get("type") == "reading" and reading_group is not None:
            reading_group["items"].append(item)
        elif cur is not None and cur.get("type") == "reference":
            cur["items"].append(item)
        elif lecture is not None and cur is lecture and sub is not None:
            if sub["kind"] == "参考文献":
                if ref_group is not None:
                    ref_group["items"].append(item)
                else:
                    sub["items"].append(item)
            else:
                sub["items"].append(item)

    for text in paras:
        if not doc_title:
            doc_title = text
            continue
        if not doc_subtitle:
            doc_subtitle = text
            continue

        if text == "课程必读书目：":
            cur = {"type": "reading", "heading": "课程必读书目", "groups": []}
            sections.append(cur)
            reading_group = None
            lecture = None
            sub = None
            ref_group = None
            continue
        if text in ("中文版本：", "英文版本："):
            reading_group = {"name": text[:-1], "items": []}
            cur["groups"].append(reading_group)
            continue
        if text == "课程参考书目：":
            cur = {"type": "reference", "heading": "课程参考书目", "items": []}
            sections.append(cur)
            reading_group = None
            lecture = None
            sub = None
            ref_group = None
            continue
        m = LECTURE_RE.match(text)
        if m:
            lecture = {"type": "lecture", "no": m.group(1), "title": m.group(2).strip(), "blocks": []}
            sections.append(lecture)
            cur = lecture
            sub = None
            ref_group = None
            reading_group = None
            continue
        m = SUB_RE.match(text)
        if m and lecture is not None and cur is lecture:
            sub = {"kind": m.group(2).strip(), "groups": None, "items": []}
            if sub["kind"] == "参考文献":
                sub["groups"] = []
            lecture["blocks"].append(sub)
            ref_group = None
            continue
        if text.startswith("·") and sub is not None and sub["kind"] == "参考文献":
            ref_group = {"name": text[1:].strip(), "items": []}
            sub["groups"].append(ref_group)
            continue
        m = NUM_RE.match(text)
        if m:
            append_item(m.group(1).strip())
            continue
        append_item(text.strip())

    return doc_title, doc_subtitle, sections


def render_lists(items, ordered):
    tag = "ol" if ordered else "ul"
    inner = "".join(f"<li>{esc(strip_num(it) if ordered else it)}</li>" for it in items)
    return f'<{tag} class="syl-list">{inner}</{tag}>'


def render_top(sec):
    out = ['<section class="syl-block">', f"<h2>{esc(sec['heading'])}</h2>"]
    if sec["type"] == "reading":
        out.append('<div class="syl-reading">')
        for g in sec["groups"]:
            out.append(f'<h3>{esc(g["name"])}</h3>')
            out.append(render_lists(g["items"], ordered=False))
        out.append("</div>")
    elif sec["type"] == "reference":
        out.append(render_lists(sec["items"], ordered=True))
    out.append("</section>")
    return "\n".join(out)


def render_lectures(lectures):
    out = ['<section class="syl-lectures">']
    for lec in lectures:
        out.append('<article class="syl-lecture">')
        out.append(f'<h2 class="syl-lecture-h"><span class="syl-no">{esc(lec["no"])}</span>{esc(lec["title"])}</h2>')
        for blk in lec["blocks"]:
            out.append('<div class="syl-sub">')
            out.append(f"<h3>{esc(blk['kind'])}</h3>")
            if blk["kind"] == "参考文献" and blk.get("groups"):
                for g in blk["groups"]:
                    out.append('<div class="syl-refgroup">')
                    out.append(f"<h4>{esc(g['name'])}</h4>")
                    out.append(render_lists(g["items"], ordered=True))
                    out.append("</div>")
            else:
                ordered = blk["kind"] == "授课内容"
                out.append(render_lists(blk["items"], ordered=ordered))
            out.append("</div>")
        out.append("</article>")
    out.append("</section>")
    return "\n".join(out)


def build_detail(doc_title, doc_subtitle, sections):
    lectures = [s for s in sections if s["type"] == "lecture"]
    top = "\n".join(render_top(s) for s in sections if s["type"] in ("reading", "reference"))
    lec_html = render_lectures(lectures)
    lead = f'<p class="syl-lead">{esc(doc_subtitle)}</p>' if doc_subtitle else ""

    body = f"""{header(TITLE, rel="../")}
  <main>
    <section class="wrap prose">
      <p class="breadcrumb"><a href="../teaching.html">教学</a> / {esc(TITLE)}</p>
      <h1 class="page-title">{esc(TITLE)}</h1>
      {lead}
{top}
{lec_html}
    </section>

    <section class="wrap comments">
      <h2>评论</h2>
      <div id="giscus-mount"></div>
    </section>
  </main>
"""
    out_dir = os.path.join(SITE, "teaching")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, SLUG + ".html"), "w", encoding="utf-8") as f:
        f.write(body + FOOTER.format(rel="../"))
    print("built teaching/%s.html (%d lectures)" % (SLUG, len(lectures)))


def build_index(doc_subtitle, lecture_count):
    desc = f"课程大纲，共 {lecture_count} 讲，附课程必读书目、参考书目与每讲研究性文献指引。"
    meta = f"课程大纲 · 共 {lecture_count} 讲"
    card = f"""      <a class="teach-card" href="teaching/{SLUG}.html">
        <h3>{esc(TITLE)}</h3>
        <p class="teach-meta">{esc(meta)}</p>
        <p class="teach-desc">{esc(desc)}</p>
      </a>"""
    body = f"""{header("教学")}
  <main>
    <section class="wrap-wide">
      <h1 class="page-title">教学</h1>

      <div class="teaching-grid">
{card}
      </div>
    </section>

    <section class="wrap comments">
      <h2>评论</h2>
      <div id="giscus-mount"></div>
    </section>
  </main>
"""
    with open(os.path.join(SITE, "teaching.html"), "w", encoding="utf-8") as f:
        f.write(body + FOOTER.format(rel=""))
    print("built teaching.html (1 item)")


def main():
    doc_title, doc_subtitle, sections = parse_docx(SRC_DOCX)
    lectures = [s for s in sections if s["type"] == "lecture"]
    build_detail(doc_title, doc_subtitle, sections)
    build_index(doc_subtitle, len(lectures))


if __name__ == "__main__":
    main()
