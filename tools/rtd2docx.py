#!/usr/bin/env python3
"""Build the IFE Word report (and optionally a PDF) from the Read the Docs sources.

This is the reverse of tools/docx2rtd.py: the MyST Markdown in docs/source is the
master copy, and this script turns it into a .docx in the IFE report format for review
and publishing.

    python tools/rtd2docx.py --source docs/source --out build/IFE-TIMES-Norway.docx [--pdf]

Pipeline
--------
1. Sphinx builds the site as one HTML page (``singlehtml``) with the tag ``docx``.
   Sphinx resolves the numbering of sections, figures and tables, the cross-references
   and the citations, exactly as on the website. The per-page reference lists are left
   out in this mode.
2. The HTML is reshaped for Word: section numbers are dropped (the IFE heading styles
   number themselves), captions become caption paragraphs with SEQ fields, footnotes
   become Word footnotes, the references get the Bibliography style.
3. pandoc writes the .docx with tools/templates/ife-reference.docx as the template, so
   styles, heading numbering, page setup and headers/footers are the report's own.
4. The .docx is post-processed: IFE heading styles, unnumbered front/appendix headings,
   SEQ/TOC fields, the IFE table style, images scaled to the text width.
5. ``--pdf``: Microsoft Word (macOS, via AppleScript) opens the file, updates all fields
   and the table of contents, and saves a PDF next to the .docx.

Requirements: pandoc >= 3 on PATH; python packages sphinx (with the site's requirements),
beautifulsoup4, lxml.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from lxml import etree

HERE = Path(__file__).resolve().parent
DEFAULT_TEMPLATE = HERE / "templates" / "ife-reference.docx"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = "{%s}" % W_NS
NS = {"w": W_NS,
      "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
SEQ_MARK = "⟦SEQ:{kind}:{num}⟧"  # ⟦SEQ:Figure:18⟧, replaced by a SEQ field
SEQ_RE = re.compile("⟦SEQ:(\\w+):([\\w-]+)⟧")
TOC_MARK = "⟦TOC⟧"
MATH_MARK = "\u27e6MATH:{}\u27e7"  # replaced by a pandoc Math element (pandoc's HTML reader
MATH_RE = re.compile("\u27e6MATH:(\\d+)\u27e7")  # does not read Sphinx's MathJax spans)
UNNUM_MARK = "\u27e6UNNUM\u27e7"  # heading without a number (front pages, appendices)
HEADING_LEVELS = 4
TABLE_STYLE_NAME = "Blue grid adjusted2"  # the table style used most in the v5 report
CAPTION_STYLE_NAME = "caption"
BIB_STYLE_NAME = "Bibliography"
TITLE_STYLE_NAME = "Title"
FRONT_DOCS = ("summary", "report-information")


class BuildError(Exception):
    pass


def log(msg):
    print(msg, file=sys.stderr)


# --------------------------------------------------------------------------- 1. sphinx
def build_singlehtml(source: Path, out: Path) -> Path:
    cmd = [sys.executable, "-m", "sphinx", "-q", "-b", "singlehtml", "-t", "docx", "-E",
           str(source), str(out)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    warnings = [l for l in res.stderr.splitlines() if "WARNING" in l or "ERROR" in l]
    if res.returncode != 0:
        raise BuildError("sphinx-build failed:\n" + res.stderr[-3000:])
    for w in warnings:
        log(w)
    return out / "index.html"


# --------------------------------------------------------------------------- 2. html
def _doc_of(section) -> str | None:
    """singlehtml wraps each page in <span id="document-NAME"></span> + section."""
    prev = section.find_previous_sibling()
    if prev is not None and prev.name == "span" and str(prev.get("id", "")).startswith("document-"):
        return prev["id"][len("document-"):]
    return None


def prepare_html(index_html: Path, report: dict) -> str:
    soup = BeautifulSoup(index_html.read_text(encoding="utf8"), "lxml")
    main = soup.select_one('div[itemprop="articleBody"]') or soup.select_one("div.body")
    if main is None:
        raise BuildError("could not find the page body in the Sphinx output")
    for el in main.select("a.headerlink"):
        el.decompose()
    # singlehtml puts every included page inside its toctree block: keep the pages,
    # drop the toctree captions ("Contents", "Appendix", ...)
    for tw in main.select("div.toctree-wrapper"):
        for cap in tw.find_all("p", class_="caption", recursive=False):
            cap.decompose()
        tw.unwrap()

    # pages whose headings are not numbered: everything outside the numbered toctree
    unnumbered_ids = []
    for sec in main.find_all("section"):
        h = sec.find(re.compile("^h[1-6]$"), recursive=False)
        if h is None:
            continue
        numbered = h.find("span", class_="section-number") is not None
        if not numbered and sec.get("id"):
            unnumbered_ids.append(sec["id"])
    report["unnumbered_headings"] = unnumbered_ids

    # root title -> Title paragraph; every other heading moves up one level
    root = main.find("section")
    root_h = root.find("h1", recursive=False)
    title = root_h.get_text(" ", strip=True)
    report["title"] = title
    root_h.decompose()  # pandoc writes the <title> as the Title paragraph
    for el in main.select("span.section-number"):
        el.decompose()
    for h in main.find_all(re.compile("^h[2-7]$")):
        lvl = int(h.name[1]) - 1
        sec = h.find_parent("section")
        h.name = f"h{lvl}"
        if sec is not None and sec.get("id"):
            sid = sec["id"]
            labels = [sp["id"] for sp in sec.find_all("span", recursive=False)
                      if sp.get("id") and not sp.contents]
            h["id"] = next((l for l in labels if l.startswith("sec-")), labels[0] if labels else sec["id"])
            for sp in sec.find_all("span", recursive=False):
                if sp.get("id") and not sp.contents:
                    sp.decompose()
            # links to the section's own id go to the heading
            if h["id"] != sec["id"]:
                for a in main.select(f'a[href="#{sec["id"]}"]'):
                    a["href"] = "#" + h["id"]
            del sec["id"]  # pandoc puts the bookmark on the heading
            if sid in unnumbered_ids:
                h["class"] = h.get("class", []) + ["unnumbered"]
        if lvl > HEADING_LEVELS:
            report.setdefault("notes", []).append(f"heading deeper than level {HEADING_LEVELS}: {h.get_text()[:40]}")
    # labels that Sphinx emits as empty spans before sections stay as bookmarks (pandoc keeps ids)

    # table of contents goes after the front pages (before chapter 1)
    first_numbered = next((h for h in main.find_all(re.compile("^h1$")) if "unnumbered" not in h.get("class", [])), None)
    if first_numbered is not None:
        toc = soup.new_tag("p")
        toc.string = TOC_MARK
        first_numbered.insert_before(toc)

    # figures: image paragraph + caption paragraph (SEQ field, bookmark)
    for fig in main.find_all("figure"):
        cap = fig.find("figcaption")
        fid = fig.get("id")
        new = []
        for img in fig.find_all("img"):
            p = soup.new_tag("p")
            img.extract()
            img.attrs = {"src": img["src"], "alt": img.get("alt", "")}
            p.append(img)
            new.append(p)
        if cap is not None:
            new.append(_caption(soup, cap, fid, "Figure"))
        for el in reversed(new):
            fig.insert_after(el)
        fig.decompose()
        report["figures"] = report.get("figures", 0) + 1

    # tables: caption before the table, alignment as inline style, report-info tables plain
    for t in main.find_all("table"):
        cap = t.find("caption")
        tid = t.get("id")
        if cap is not None:
            t.insert_before(_caption(soup, cap, tid, "Table"))
            cap.decompose()
            report["tables_captioned"] = report.get("tables_captioned", 0) + 1
        report["tables"] = report.get("tables", 0) + 1
        for c in t.find_all(["td", "th"]):
            for cls in c.get("class", []):
                m = re.fullmatch(r"text-(left|center|right)", cls)
                if m:
                    c["style"] = f"text-align: {m.group(1)};"
                    c["align"] = m.group(1)
        t.attrs = {k: v for k, v in t.attrs.items() if k in ("class",)}

    # math -> placeholders, turned into pandoc Math elements in the AST
    maths = report.setdefault("_math", [])

    def math_mark(tex):
        tex = tex.strip()
        display = tex.startswith("\\[") or tex.startswith("$$")
        tex = re.sub(r"^(\\\(|\\\[|\$\$)|(\\\)|\\\]|\$\$)$", "", tex).strip()
        maths.append(("DisplayMath" if display else "InlineMath", tex))
        return MATH_MARK.format(len(maths) - 1)

    for m in main.select("span.math"):
        m.replace_with(NavigableString(math_mark(m.get_text())))
    for d in main.select("div.math"):
        p = soup.new_tag("p")
        p.string = math_mark("\\[" + d.get_text().strip().strip("\\[]").strip() + "\\]")
        d.replace_with(p)
    report["equations"] = len(maths)

    # references: Bibliography style, bookmark ref-N on each entry
    refs = main.select("p.ref-entry")
    for p in refs:
        rid = p.get("id")
        if rid:
            p.insert(0, soup.new_tag("span", attrs={"id": rid}))
            del p["id"]
        wrap = soup.new_tag("div", attrs={"data-custom-style": BIB_STYLE_NAME})
        p.wrap(wrap)
    report["references"] = len(refs)

    # footnotes -> placeholders resolved in the pandoc AST
    defs = soup.new_tag("div", attrs={"id": "fn-defs"})
    n = 0
    for ref in main.select("a.footnote-reference"):
        target = ref.get("href", "").lstrip("#")
        aside = ref.find_next("aside", id=target)
        if aside is None:
            report.setdefault("notes", []).append(f"footnote {target} has no text")
            continue
        n += 1
        key = f"fn{n}"
        body = copy.copy(aside)
        for lab in body.select("span.label"):
            lab.decompose()
        d = soup.new_tag("div", attrs={"id": "fndef-" + key})
        for ch in list(body.children):
            d.append(ch.extract() if not isinstance(ch, NavigableString) else NavigableString(str(ch)))
        defs.append(d)
        ref.replace_with(soup.new_tag("span", attrs={"class": "fnref", "data-fn": key}))
    for a in main.select("aside.footnote-list, aside.footnote"):
        a.decompose()
    main.append(defs)
    report["footnotes"] = n

    # links between parts of the one page: keep only #fragment
    for a in main.find_all("a", href=True):
        if a["href"].startswith("index.html#"):
            a["href"] = a["href"][len("index.html"):]
        if a["href"].startswith("#document-"):
            a.unwrap()
    # docutils rubric (e.g. headings inside tables of contents) -> bold paragraph
    for r in main.select("p.rubric"):
        r.name = "p"
    for s in main.select("span[id^=document-]"):
        s.decompose()
    for img in main.find_all("img"):
        img["src"] = img["src"].split("?")[0]
    return "<!doctype html><html><head><meta charset='utf-8'><title>" + title + "</title></head><body>" + \
        str(main) + "</body></html>"


def _caption(soup, cap, target_id, kind):
    num = cap.find("span", class_="caption-number")
    text = cap.find("span", class_="caption-text")
    numtxt = num.get_text(strip=True) if num else ""
    m = re.fullmatch(rf"{kind}\s+((?:[A-Z]-)?\d+)", numtxt)
    div = soup.new_tag("div", attrs={"data-custom-style": CAPTION_STYLE_NAME})
    p = soup.new_tag("p")
    if target_id:
        p.append(soup.new_tag("span", attrs={"id": target_id}))
    if m and re.fullmatch(r"\d+", m.group(1)):
        p.append(NavigableString(f"{kind} " + SEQ_MARK.format(kind=kind, num=m.group(1)) + " "))
    elif numtxt:
        p.append(NavigableString(numtxt + " "))  # appendix numbers (A-1) stay as text
    if text is not None:
        for ch in list(text.children):
            p.append(ch.extract())
    div.append(p)
    return div


# --------------------------------------------------------------------------- 3. pandoc
def pandoc(args, inp: str | None = None) -> str:
    res = subprocess.run(["pandoc"] + args, input=inp, capture_output=True, text=True)
    if res.returncode != 0:
        raise BuildError("pandoc failed: " + res.stderr[-2000:])
    for l in res.stderr.splitlines():
        if l.strip() and "Could not fetch resource" not in l:
            log("pandoc: " + l)
        elif "Could not fetch resource" in l:
            raise BuildError("pandoc: " + l)
    return res.stdout


def _walk(x, fn):
    if isinstance(x, list):
        out = []
        for i in x:
            r = fn(i) if isinstance(i, dict) and "t" in i else None
            if r is None:
                out.append(_walk(i, fn))
            else:
                out.extend(r)
        return out
    if isinstance(x, dict):
        return {k: _walk(v, fn) for k, v in x.items()}
    return x


def ast_filter(doc: dict, report: dict) -> dict:
    # collect footnote bodies
    defs = {}

    def grab(el):
        if el["t"] == "Div":
            ident = el["c"][0][0]
            if ident == "fn-defs":
                for d in el["c"][1]:
                    if d["t"] == "Div" and d["c"][0][0].startswith("fndef-"):
                        defs[d["c"][0][0][len("fndef-"):]] = d["c"][1]
                return []
        return None

    doc["blocks"] = _walk(doc["blocks"], grab)

    def notes(el):
        if el["t"] == "Span":
            attr = el["c"][0]
            kv = dict(attr[2])
            if "fnref" in attr[1] and kv.get("fn") in defs:
                return [{"t": "Note", "c": defs[kv["fn"]]}]
        if el["t"] == "Header":
            # pandoc's docx writer only keeps the id of a heading; mark unnumbered ones
            attr = el["c"][1]
            if "unnumbered" in attr[1]:  # bookmark names get hashed, so mark the text
                el["c"][2] = [{"t": "Str", "c": UNNUM_MARK}] + el["c"][2]
        return None

    doc["blocks"] = _walk(doc["blocks"], notes)
    maths = report.pop("_math", [])

    def math(el):
        if el["t"] == "Str" and "\u27e6MATH" in el["c"]:
            out = []
            for k, piece in enumerate(MATH_RE.split(el["c"])):
                if k % 2:
                    kind, tex = maths[int(piece)]
                    out.append({"t": "Math", "c": [{"t": kind}, tex]})
                elif piece:
                    out.append({"t": "Str", "c": piece})
            return out
        return None

    doc["blocks"] = _walk(doc["blocks"], math)
    return doc


# --------------------------------------------------------------------------- 4. docx post-processing
def _style_ids(styles_xml: bytes) -> dict:
    root = etree.fromstring(styles_xml)
    out = {}
    for s in root.findall(W + "style"):
        name = s.find(W + "name")
        if name is not None:
            out.setdefault(name.get(W + "val").lower(), s.get(W + "styleId"))
    return out


def _run_with_text(rpr, text):
    r = etree.Element(W + "r")
    if rpr is not None:
        r.append(copy.deepcopy(rpr))
    t = etree.SubElement(r, W + "t")
    t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return r


def _field_runs(rpr, instr, result):
    runs = []
    for kind, extra in (("begin", None), ("instr", instr), ("separate", None), ("result", result), ("end", None)):
        r = etree.Element(W + "r")
        if rpr is not None:
            r.append(copy.deepcopy(rpr))
        if kind in ("begin", "separate", "end"):
            fc = etree.SubElement(r, W + "fldChar")
            fc.set(W + "fldCharType", kind)
        elif kind == "instr":
            it = etree.SubElement(r, W + "instrText")
            it.text = f" {extra} "
            it.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        else:
            t = etree.SubElement(r, W + "t")
            t.text = extra
        runs.append(r)
    return runs


def postprocess_docx(path: Path, report: dict, template: Path):
    with zipfile.ZipFile(path) as z:
        parts = {n: z.read(n) for n in z.namelist()}
    ids = _style_ids(parts["word/styles.xml"])
    doc = etree.fromstring(parts["word/document.xml"])
    body = doc.find(W + "body")

    # heading styles -> IFE Heading N
    heading_map = {}
    for lvl in range(1, 10):
        src = ids.get(f"heading {lvl}")
        dst = ids.get(f"ife heading {lvl}")
        if src and dst:
            heading_map[src] = (dst, lvl)
    plain = {ids.get(n) for n in ("first paragraph", "body text", "compact") if ids.get(n)}
    plain |= {"FirstParagraph", "BodyText", "Compact"}
    caption_id = ids.get(CAPTION_STYLE_NAME)
    counts = {"headings": 0, "unnumbered": 0, "seq_fields": 0, "tables": 0, "images_scaled": 0}
    for p in body.iter(W + "p"):
        ppr = p.find(W + "pPr")
        ps = ppr.find(W + "pStyle") if ppr is not None else None
        if ps is None:
            continue
        sid = ps.get(W + "val")
        if sid in heading_map:
            ps.set(W + "val", heading_map[sid][0])
            counts["headings"] += 1
            marks = [t for t in p.iter(W + "t") if t.text and UNNUM_MARK in t.text]
            for t in marks:
                t.text = t.text.replace(UNNUM_MARK, "")
            if marks:
                numpr = etree.SubElement(ppr, W + "numPr")
                etree.SubElement(numpr, W + "ilvl").set(W + "val", "0")
                etree.SubElement(numpr, W + "numId").set(W + "val", "0")
                # numPr must come right after pStyle/keepNext...: move it after pStyle
                ppr.remove(numpr)
                ps.addnext(numpr)
                counts["unnumbered"] += 1
        elif sid in plain:
            ppr.remove(ps)

    # ⟦SEQ:Figure:18⟧ -> SEQ field;  ⟦TOC⟧ -> table of contents field
    for t in list(body.iter(W + "t")):
        if not t.text:
            continue
        if TOC_MARK in t.text:
            p = t.getparent().getparent()
            toc_heading = etree.Element(W + "p")
            pp = etree.SubElement(toc_heading, W + "pPr")
            tid = ids.get("toc heading") or ids.get("ife heading list")
            if tid:
                etree.SubElement(pp, W + "pStyle").set(W + "val", tid)
            numpr = etree.SubElement(pp, W + "numPr")  # the heading style may be numbered
            etree.SubElement(numpr, W + "ilvl").set(W + "val", "0")
            etree.SubElement(numpr, W + "numId").set(W + "val", "0")
            etree.SubElement(pp, W + "pageBreakBefore")
            toc_heading.append(_run_with_text(None, "Contents"))
            p.addprevious(toc_heading)
            for r in list(p):
                if r.tag != W + "pPr":
                    p.remove(r)
            for r in _field_runs(None, 'TOC \\o "1-3" \\h \\z \\u', "Right-click and choose Update Field to build the table of contents."):
                p.append(r)
            counts["toc"] = 1
            continue
        if "⟦SEQ" not in t.text:
            continue
        r = t.getparent()
        rpr = r.find(W + "rPr")
        pieces = SEQ_RE.split(t.text)
        new = []
        for i in range(0, len(pieces), 3):
            if pieces[i]:
                new.append(_run_with_text(rpr, pieces[i]))
            if i + 2 < len(pieces):
                kind, num = pieces[i + 1], pieces[i + 2]
                new.extend(_field_runs(rpr, f"SEQ {kind} \\* ARABIC", num))
                counts["seq_fields"] += 1
        for nr in new:
            r.addprevious(nr)
        r.getparent().remove(r)

    # tables: IFE table style, full width, header rows repeat
    tstyle = ids.get(TABLE_STYLE_NAME.lower())
    for tbl in body.iter(W + "tbl"):
        tpr = tbl.find(W + "tblPr")
        st = tpr.find(W + "tblStyle")
        if tstyle and st is not None:
            st.set(W + "val", tstyle)
        # as in the report: automatic width, 10 pt text, slim cell margins (dense tables
        # otherwise break words and numbers across lines)
        tw = tpr.find(W + "tblW")
        if tw is not None:
            tw.set(W + "w", "0")
            tw.set(W + "type", "auto")
        lay = tpr.find(W + "tblLayout")
        if lay is not None:
            tpr.remove(lay)
        mar = tpr.find(W + "tblCellMar")
        if mar is None:
            mar = etree.Element(W + "tblCellMar")
            look = tpr.find(W + "tblLook")
            (look.addprevious(mar) if look is not None else tpr.append(mar))
        for side in ("left", "right"):
            e = mar.find(W + side)
            if e is None:
                e = etree.SubElement(mar, W + side)
            e.set(W + "w", "57")
            e.set(W + "type", "dxa")
        for r in tbl.iter(W + "r"):
            rpr = r.find(W + "rPr")
            if rpr is None:
                rpr = etree.Element(W + "rPr")
                r.insert(0, rpr)
            if rpr.find(W + "sz") is None:
                for tag in ("sz", "szCs"):
                    e = etree.SubElement(rpr, W + tag)
                    e.set(W + "val", "20")
        counts["tables"] += 1

    # paragraph formatting of the report (direct formatting in the v5 file)
    bib = ids.get(BIB_STYLE_NAME.lower())
    counts["captions"] = 0
    for p in body.iter(W + "p"):
        in_table = any(a.tag == W + "tbl" for a in p.iterancestors())
        ppr = p.find(W + "pPr")
        if ppr is None:
            ppr = etree.Element(W + "pPr")
            p.insert(0, ppr)
        ps = ppr.find(W + "pStyle")
        sid = ps.get(W + "val") if ps is not None else None
        has_img = p.find(".//" + "{%s}inline" % NS["wp"]) is not None
        if sid == caption_id:
            _set_ppr(ppr, keep_next=_next_is_table(p), spacing=("120", "120"), jc="center")
            for r in p.iter(W + "r"):
                rpr = r.find(W + "rPr")
                if rpr is None:
                    rpr = etree.Element(W + "rPr")
                    r.insert(0, rpr)
                if rpr.find(W + "i") is None:
                    _insert_rpr(rpr, etree.Element(W + "i"))
            counts["captions"] += 1
        elif has_img and not in_table:
            _set_ppr(ppr, keep_next=True, spacing=("120", "0"), jc="center")
        elif sid is None and not in_table and p.find(W + "r") is not None and ppr.find(W + "numPr") is None:
            _set_ppr(ppr, spacing=("120", "200"))
    # cross-references and citations look like text (as REF fields do in the report)
    for h in body.iter(W + "hyperlink"):
        if h.get(W + "anchor"):
            for rs in h.iter(W + "rStyle"):
                rs.getparent().remove(rs)

    # page break before chapters (Heading 1), as in the report
    h1 = ids.get("ife heading 1")
    for p in body.iter(W + "p"):
        ppr = p.find(W + "pPr")
        ps = ppr.find(W + "pStyle") if ppr is not None else None
        if ps is not None and ps.get(W + "val") == h1 and ppr.find(W + "pageBreakBefore") is None:
            _put(ppr, etree.Element(W + "pageBreakBefore"))

    # images no wider than the text
    sect = body.find(W + "sectPr")
    pgw = int(sect.find(W + "pgSz").get(W + "w"))
    mar = sect.find(W + "pgMar")
    text_twips = pgw - int(mar.get(W + "left")) - int(mar.get(W + "right"))
    max_emu = text_twips * 635
    for inline in body.iter("{%s}inline" % NS["wp"]):
        ext = inline.find("wp:extent", NS)
        cx, cy = int(ext.get("cx")), int(ext.get("cy"))
        if cx > max_emu:
            f = max_emu / cx
            ext.set("cx", str(int(cx * f)))
            ext.set("cy", str(int(cy * f)))
            for a in inline.iter("{%s}ext" % NS["a"]):
                if a.get("cx"):
                    a.set("cx", str(int(int(a.get("cx")) * f)))
                    a.set("cy", str(int(int(a.get("cy")) * f)))
            counts["images_scaled"] += 1
    parts["word/document.xml"] = etree.tostring(doc, xml_declaration=True, encoding="UTF-8", standalone=True)

    # Word updates fields (TOC, SEQ) when the file is opened
    settings = etree.fromstring(parts["word/settings.xml"])
    if settings.find(W + "updateFields") is None:
        uf = etree.Element(W + "updateFields")
        uf.set(W + "val", "true")
        settings.insert(0, uf)
    parts["word/settings.xml"] = etree.tostring(settings, xml_declaration=True, encoding="UTF-8", standalone=True)

    tmp = path.with_suffix(".tmp.docx")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in parts.items():
            z.writestr(n, data)
    tmp.replace(path)
    report["docx"] = counts


PPR_ORDER = ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl", "numPr",
             "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens", "kinsoku", "wordWrap",
             "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN", "bidi", "adjustRightInd",
             "snapToGrid", "spacing", "ind", "contextualSpacing", "mirrorIndents", "suppressOverlap", "jc",
             "textDirection", "textAlignment", "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr",
             "sectPr", "pPrChange"]


def _put(ppr, el):
    """Insert el into pPr in schema order (Word is strict about it)."""
    name = el.tag[len(W):]
    old = ppr.find(el.tag)
    if old is not None:
        ppr.replace(old, el)
        return
    rank = PPR_ORDER.index(name)
    for i, child in enumerate(ppr):
        cname = child.tag[len(W):] if child.tag.startswith(W) else ""
        if cname in PPR_ORDER and PPR_ORDER.index(cname) > rank:
            ppr.insert(i, el)
            return
    ppr.append(el)


def _set_ppr(ppr, keep_next=False, spacing=None, jc=None):
    if keep_next:
        _put(ppr, etree.Element(W + "keepNext"))
    if spacing:
        sp = etree.Element(W + "spacing")
        sp.set(W + "before", spacing[0])
        sp.set(W + "after", spacing[1])
        _put(ppr, sp)
    if jc:
        j = etree.Element(W + "jc")
        j.set(W + "val", jc)
        _put(ppr, j)


def _insert_rpr(rpr, el):
    # b, i come early in rPr; after rStyle/rFonts
    pos = 0
    for i, child in enumerate(rpr):
        if child.tag in (W + "rStyle", W + "rFonts", W + "b", W + "bCs"):
            pos = i + 1
    rpr.insert(pos, el)


def _next_is_table(p):
    nxt = p.getnext()
    return nxt is not None and nxt.tag == W + "tbl"


# --------------------------------------------------------------------------- 5. pdf
APPLESCRIPT = '''
on run argv
    set inFile to item 1 of argv
    set outFile to item 2 of argv
    with timeout of 1800 seconds
    tell application "Microsoft Word"
        open POSIX file inFile
        delay 1
        set d to active document
        repaginate d
        repeat with i from 1 to (count of fields of d)
            update field (field i of d)
        end repeat
        repaginate d
        repeat with i from 1 to (count of tables of contents of d)
            update table of contents (table of contents i of d)
            -- the page numbers in the contents are PAGEREF fields: refresh them after layout
            repaginate d
            set r to text object of table of contents i of d
            repeat with k from 1 to (count of fields of r)
                update field (field k of r)
            end repeat
        end repeat
        save as d file name outFile file format format PDF
        close d saving no
    end tell
    end timeout
end run
'''
# Word is sandboxed: it can always read and write inside its own container
WORD_DIR = Path.home() / "Library/Containers/com.microsoft.Word/Data/Documents/rtd2docx"


def word_pdf(docx: Path, pdf: Path):
    """Update fields and the table of contents in Word and save a PDF."""
    if sys.platform != "darwin" or not Path("/Applications/Microsoft Word.app").exists():
        raise BuildError("--pdf needs Microsoft Word on macOS")
    WORD_DIR.mkdir(parents=True, exist_ok=True)
    work = WORD_DIR / docx.name
    out = WORD_DIR / (docx.stem + ".pdf")
    # no "update fields?" prompt in the copy Word opens: the script updates them itself
    with zipfile.ZipFile(docx) as z:
        parts = {n: z.read(n) for n in z.namelist()}
    parts["word/settings.xml"] = re.sub(rb"<w:updateFields[^>]*/>", b"", parts["word/settings.xml"])
    with zipfile.ZipFile(work, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in parts.items():
            z.writestr(n, data)
    if out.exists():
        out.unlink()
    try:
        res = subprocess.run(["osascript", "-e", APPLESCRIPT, str(work), str(out)],
                             capture_output=True, text=True, timeout=1800)
        if res.returncode != 0 or not out.exists():
            raise BuildError("Word could not make the PDF: " + (res.stderr or res.stdout)[-1500:])
        shutil.copy(out, pdf)
    finally:
        for f in (work, out):
            if f.exists():
                f.unlink()


# --------------------------------------------------------------------------- main
def build(source: Path, out: Path, template: Path, pdf: bool, keep_html: Path | None = None) -> dict:
    if not (source / "conf.py").exists():
        raise BuildError(f"{source} is not a Sphinx source folder (no conf.py)")
    if not template.exists():
        raise BuildError(f"template not found: {template} (make it with tools/make_reference_docx.py)")
    if shutil.which("pandoc") is None:
        raise BuildError("pandoc is not on PATH")
    report: dict = {"source": str(source), "template": str(template)}
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpd:
        tmp = Path(tmpd)
        index = build_singlehtml(source, tmp / "html")
        html = prepare_html(index, report)
        hpath = tmp / "html" / "word.html"
        hpath.write_text(html, encoding="utf8")
        if keep_html:
            keep_html.write_text(html, encoding="utf8")
        ast = json.loads(pandoc(["-f", "html+native_divs+native_spans", "-t", "json", str(hpath)]))
        ast = ast_filter(ast, report)
        pandoc(["-f", "json", "-t", "docx", "--reference-doc", str(template),
                "--resource-path", str(tmp / "html"), "-o", str(out)], json.dumps(ast))
    postprocess_docx(out, report, template)
    if pdf:
        word_pdf(out, out.with_suffix(".pdf"))
        report["pdf"] = str(out.with_suffix(".pdf"))
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default="docs/source", help="Sphinx source folder (default docs/source)")
    ap.add_argument("--out", default="build/report.docx", help="output .docx")
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE), help="reference .docx with the IFE styles")
    ap.add_argument("--pdf", action="store_true", help="also make a PDF with Microsoft Word (macOS)")
    ap.add_argument("--keep-html", help="save the intermediate HTML given to pandoc (for debugging)")
    ap.add_argument("--report", help="write a JSON summary of the build here")
    args = ap.parse_args(argv)
    try:
        rep = build(Path(args.source), Path(args.out), Path(args.template), args.pdf,
                    Path(args.keep_html) if args.keep_html else None)
    except BuildError as e:
        ap.exit(2, f"error: {e}\n")
    if args.report:
        Path(args.report).write_text(json.dumps(rep, indent=2, ensure_ascii=False))
    print(f"Wrote {args.out}" + (f" and {rep['pdf']}" if rep.get("pdf") else "") +
          f": {rep.get('figures', 0)} figures, {rep.get('tables', 0)} tables, "
          f"{rep.get('references', 0)} references, {rep.get('footnotes', 0)} footnotes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
