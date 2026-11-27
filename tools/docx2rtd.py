#!/usr/bin/env python3
"""Convert the IFE-TIMES-Norway Word report into a Sphinx / Read the Docs site.

Usage
-----
    python tools/docx2rtd.py --docx "Documentation of IFE-TIMES-Norway v5.docx" \
                             --pdf  "Documentation of IFE-TIMES-Norway v5.pdf"  \
                             --out  docs --rtd-root .

    # mirror site with restyled figures (see tools/restyle_figures.py)
    python tools/docx2rtd.py --docx ... --pdf ... --out mirror --rtd-root mirror \
                             --figure-manifest mirror/figures/manifest.json

    # fail (exit 2) on any missing figure / unresolved reference, e.g. in CI
    python tools/docx2rtd.py ... --strict

Pipeline
--------
1. Copy the .docx and rename the custom "IFE Heading N" styles to "heading N"
   so pandoc recognises them as headings (text is untouched).
2. pandoc docx -> JSON AST (media extracted).
3. Scan the .docx XML to classify every "Figure N": a single raster picture is
   taken from the .docx; native Word charts, EMF drawings, shape groups and
   text-box overlays are cropped from the PDF (200 dpi) because pandoc cannot
   render them.
4. Transform the AST (front matter, figures, captions, anchors, links, math in
   tables), split it into pages (one per chapter; long chapters one per
   section), and write MyST Markdown with pandoc.
5. Numbered citations "[n]" become links; every page gets a list of the
   references it cites, and references.md holds the full numbered list.
6. Write conf.py, index.md, .readthedocs.yaml, requirements.txt and CSS.
7. Tidy the Markdown for people to edit by hand (tools/tidy_myst.py): tables as
   list-table, named labels and {numref} cross-references, {cite} citations; the
   numbering and per-page reference lists then come from the Sphinx extension
   tools/ifereport.py, copied to source/_ext/. --raw-html skips this step.

Requirements: pandoc >= 3.0 on PATH; python packages pymupdf and lxml.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import zlib
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import fitz  # pymupdf
from lxml import etree

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "v": "urn:schemas-microsoft-com:vml",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}
WP = "{%s}" % NS["wp"]
EMU_PER_PT = 12700
W = "{%s}" % NS["w"]

CAPTION_RE = re.compile(r"^\s*Figure\s+(\d+)\b")
TABLE_CAPTION_RE = re.compile(r"^\s*Table\s+(A-)?\d+\b")
BIB_RE = re.compile(r"^\[(\d+)\]")
RASTER_EXT = {".png", ".jpg", ".jpeg", ".gif"}

# Chapters with more top-level blocks than this are split into one page per
# second-level section.
SPLIT_THRESHOLD = 120
TOC_DEPTH = 4  # the report numbers headings to four levels (e.g. 5.1.4.1)

log_lines: list[str] = []
field_log: list[str] = []


def log(msg: str) -> None:
    log_lines.append(msg)
    print(msg, file=sys.stderr)


# --------------------------------------------------------------------------
# pandoc AST helpers
# --------------------------------------------------------------------------
def stringify(x) -> str:
    if isinstance(x, dict):
        t, c = x.get("t"), x.get("c")
        if t == "Str":
            return c
        if t in ("Space", "SoftBreak", "LineBreak"):
            return " "
        if t == "Math":
            return c[1]
        if t in ("Code", "RawInline"):
            return c[1]
        if t == "Image":
            return stringify(c[1])
        return stringify(c)
    if isinstance(x, list):
        return "".join(stringify(i) for i in x)
    return ""


def has_image(x) -> bool:
    return '"t": "Image"' in json.dumps(x)


def raw(html: str) -> dict:
    return {"t": "RawInline", "c": ["html", html]}


def raw_block(html: str) -> dict:
    return {"t": "RawBlock", "c": ["html", html]}


def para(inlines) -> dict:
    return {"t": "Para", "c": inlines}


def str_inlines(text: str) -> list:
    out = []
    for i, w in enumerate(text.split(" ")):
        if i:
            out.append({"t": "Space"})
        if w:
            out.append({"t": "Str", "c": w})
    return out


def walk_inlines(obj, fn):
    """Apply fn to every inline list in obj (post-order). fn returns new list."""
    if isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_inlines(v, fn)
        if obj and all(isinstance(v, dict) and "t" in v for v in obj) and any(
            v["t"] in INLINE_TYPES for v in obj
        ):
            obj[:] = fn(obj)
    elif isinstance(obj, dict):
        walk_inlines(obj.get("c"), fn)


INLINE_TYPES = {
    "Str", "Emph", "Underline", "Strong", "Strikeout", "Superscript", "Subscript",
    "SmallCaps", "Quoted", "Cite", "Code", "Space", "SoftBreak", "LineBreak",
    "Math", "RawInline", "Link", "Image", "Note", "Span",
}


def collect_ids(obj, out: set):
    if isinstance(obj, dict):
        t, c = obj.get("t"), obj.get("c")
        if t == "Header" and c[1][0]:
            out.add(c[1][0])
        if t in ("Span", "Div", "Table", "Figure", "Image", "Link", "CodeBlock") and isinstance(c, list):
            attr = c[0]
            if isinstance(attr, list) and attr and isinstance(attr[0], str) and attr[0]:
                out.add(attr[0])
        if t == "RawInline" or t == "RawBlock":
            for m in re.finditer(r'id="([^"]+)"', c[1]):
                out.add(m.group(1))
        collect_ids(c, out)
    elif isinstance(obj, list):
        for v in obj:
            collect_ids(v, out)


# --------------------------------------------------------------------------
# 1. docx preprocessing and scanning
# --------------------------------------------------------------------------
def _is_hidden_paragraph(p) -> bool:
    """True if every text run is hidden (w:vanish) or white (FFFFFF): invisible in the report."""
    runs = [r for r in p.iter(W + "r") if "".join(t.text or "" for t in r.iter(W + "t")).strip()]
    if not runs:
        return False
    for r in runs:
        rpr = r.find(W + "rPr")
        hidden = rpr is not None and (
            rpr.find(W + "vanish") is not None
            or (rpr.find(W + "color") is not None
                and (rpr.find(W + "color").get(W + "val") or "").upper() == "FFFFFF")
        )
        if not hidden:
            return False
    return True


ERROR_REF = "Error! Reference source not found."


def update_fields(root) -> list[str]:
    """Recompute SEQ numbers and REF texts like Word's "Update fields" (F9).

    The published PDF is made after Word updates its fields, while the .docx
    keeps whatever results were last saved, e.g. stale table numbers after a
    table was deleted. Emulating the update makes the site match the PDF.
    Returns log messages for every changed field result.
    """
    msgs = []
    fields = []  # dicts: instr, result_t (list of w:t), in document order of 'end'
    stack = []
    for el in root.iter(W + "fldChar", W + "instrText", W + "t", W + "fldSimple"):
        tag = el.tag[len(W):]
        if tag == "fldChar":
            typ = el.get(W + "fldCharType")
            if typ == "begin":
                stack.append({"instr": "", "res": [], "sep": False, "instr_el": []})
            elif typ == "separate" and stack:
                stack[-1]["sep"] = True
            elif typ == "end" and stack:
                f = stack.pop()
                fields.append(f)
                if stack and stack[-1]["sep"]:
                    stack[-1]["res"] += f["res"]
        elif tag == "instrText" and stack:
            stack[-1]["instr"] += el.text or ""
            stack[-1]["instr_el"].append(el)
        elif tag == "t" and stack and stack[-1]["sep"]:
            stack[-1]["res"].append(el)
        elif tag == "fldSimple":
            fields.append({"instr": el.get(W + "instr") or "", "res": list(el.iter(W + "t"))})

    def set_result(f, text):
        old = "".join(t.text or "" for t in f["res"])
        if old == text or not f["res"]:
            return False
        f["res"][0].text = text
        for t in f["res"][1:]:
            t.text = ""
        msgs.append(f"field '{' '.join(f['instr'].split()[:2])}': {old!r} -> {text!r}")
        return True

    # SEQ fields, in document order (fields are recorded at their end; SEQ has no nesting)
    order = {id(t): i for i, t in enumerate(root.iter(W + "t"))}
    seq_fields = sorted((f for f in fields if f["instr"].split()[:1] == ["SEQ"] and f["res"]),
                        key=lambda f: order[id(f["res"][0])])
    counters: dict = {}
    for f in seq_fields:
        parts = f["instr"].split()
        name = parts[1] if len(parts) > 1 else ""
        sw = " ".join(parts[2:])
        if re.search(r"\\[cC]\b", sw):
            n = counters.get(name, 0)
        elif m := re.search(r"\\r\s*(\d+)", sw):
            n = int(m.group(1))
        else:
            n = counters.get(name, 0) + 1
        counters[name] = n
        if not re.search(r"\\h\b", sw) and re.fullmatch(r"\d+", "".join(t.text or "" for t in f["res"]).strip()):
            set_result(f, str(n))

    # bookmark texts (after SEQ update)
    texts: dict = {}
    open_bm: dict = {}
    for el in root.iter(W + "bookmarkStart", W + "bookmarkEnd", W + "t"):
        tag = el.tag[len(W):]
        if tag == "bookmarkStart":
            open_bm[el.get(W + "id")] = el.get(W + "name")
            texts.setdefault(el.get(W + "name"), "")
        elif tag == "bookmarkEnd":
            open_bm.pop(el.get(W + "id"), None)
        else:
            for name in open_bm.values():
                texts[name] += el.text or ""
    for f in fields:
        parts = f["instr"].split()
        if parts[:1] != ["REF"] or len(parts) < 2 or not f["res"]:
            continue
        sw = " ".join(parts[2:])
        if re.search(r"\\[nrwpf]\b", sw):
            continue  # paragraph-number / position variants: keep Word's result
        name = parts[1]
        new = texts.get(name)
        if new is None:
            fixed = _infer_xref(root, f, texts)
            if fixed:
                new_name, new_text, why = fixed
                _set_instr(f, f["instr"].replace(name, new_name, 1))
                msgs.append(f"xref-fixed {name}: {''.join(t.text or '' for t in f['res'])!r} -> "
                            f"{new_text!r} ({why})")
                set_result(f, new_text)
                continue
        set_result(f, ERROR_REF if new is None else new.strip() if new.strip() else new)
    return msgs


_STOP = set("the and for with from that this are was were which into each have has been "
            "presented shown given some used based model figure table see also more than".split())


def _words(t: str) -> set:
    return {w for w in re.findall(r"[a-zæøå0-9]+", t.lower()) if len(w) > 3 and w not in _STOP}


def _set_instr(f, instr):
    f["instr"] = instr
    if f.get("instr_el"):
        f["instr_el"][0].text = " " + instr + " "
        for e in f["instr_el"][1:]:
            e.text = ""


def _infer_xref(root, f, texts):
    """Find the caption a broken cross-reference most likely meant, from its context.

    Candidates are captions with the same label ("Table"/"Figure") in the same
    section as the reference. The caption whose words best overlap the citing
    sentence wins; a weak match is rejected rather than guessed.
    Returns (bookmark name, text to show, reason) or None.
    """
    old = "".join(t.text or "" for t in f["res"]).strip()
    m = re.match(r"(Table|Figure|Equation)\b", old)
    if not m or not f["res"]:
        return None
    label = m.group(1)
    paras = list(root.iter(W + "p"))
    cite_p = next((a for a in f["res"][0].iterancestors(W + "p")), None)
    if cite_p is None:
        return None

    def is_heading(p):
        st = p.find(f"{W}pPr/{W}pStyle")
        return st is not None and "heading" in (st.get(W + "val") or "").lower()

    idx = paras.index(cite_p)
    lo = next((i for i in range(idx, -1, -1) if is_heading(paras[i])), 0)
    hi = next((i for i in range(idx + 1, len(paras)) if is_heading(paras[i])), len(paras))
    ctext = "".join(t.text or "" for t in cite_p.iter(W + "t"))
    # sentence around the reference
    pos = ctext.find(old)
    start = max(ctext.rfind(".", 0, max(pos, 0)) + 1, 0)
    end = ctext.find(".", pos + len(old)) if pos >= 0 else -1
    sentence = ctext[start:end if end > 0 else None]
    sw = _words(sentence)

    def best_caption(labels, sw):
        best = None
        for p in paras[lo:hi]:
            instrs = "".join(i.text or "" for i in p.iter(W + "instrText"))
            lab = next((l for l in labels if f"SEQ {l}" in instrs), None)
            if lab is None:
                continue
            cap = "".join(t.text or "" for t in p.iter(W + "t")).strip()
            cw = _words(cap)
            score = len(sw & cw) / max(len(cw), 1)
            if best is None or score > best[0]:
                best = (score, p, cap, lab)
        return best

    # 1) same kind (Table -> Table) with a clear word match;
    # 2) otherwise (the referenced item was deleted) the best-matching captioned item of
    #    any kind in the same section, e.g. the figure that now presents the same data
    best = best_caption([label], sw)
    why = "same-section caption"
    if not best or best[0] < 0.25:
        # wider context: the whole citing paragraph
        best = best_caption(["Table", "Figure"], _words(ctext))
        why = f"no {label.lower()} in the section matches; best-matching captioned item"
        if not best or best[0] < 0.3:
            return None
    score, p, cap, label = best
    num = re.match(rf"{label}\s*[A-Z]?-?\d+", cap)
    shown = num.group(0) if num else cap
    bm = next((b.get(W + "name") for b in p.iter(W + "bookmarkStart")
               if (texts.get(b.get(W + "name")) or "").strip() == shown), None)
    if bm is None:  # add a bookmark around the caption paragraph's content
        bm = f"_XrefAuto{zlib.crc32(cap.encode('utf8')) % 10**8}"
        bid = str(900000 + len(texts))
        start_el = etree.SubElement(p, W + "bookmarkStart", {W + "id": bid, W + "name": bm})
        p.remove(start_el)
        ppr = p.find(W + "pPr")
        p.insert(list(p).index(ppr) + 1 if ppr is not None else 0, start_el)
        etree.SubElement(p, W + "bookmarkEnd", {W + "id": bid})
        texts[bm] = shown
    return bm, shown, f"{why}, word match {score:.0%} with {cap[:70]!r}"


def preprocess_docx(src: Path, dst: Path, heading_prefix: str) -> list[str]:
    """Rename heading styles for pandoc and drop invisible paragraphs. Returns dropped texts."""
    dropped = []
    with zipfile.ZipFile(src) as zi, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zo:
        for it in zi.infolist():
            data = zi.read(it.filename)
            if it.filename == "word/styles.xml" and heading_prefix:
                s = data.decode("utf8")
                for n in range(1, 10):
                    s = s.replace(f'w:name w:val="{heading_prefix} {n}"', f'w:name w:val="heading {n}"')
                data = s.encode("utf8")
            elif it.filename == "word/document.xml":
                root = etree.fromstring(data)
                for m in update_fields(root):
                    dropped.append("@field " + m)
                body = root.find(W + "body")
                # only plain body paragraphs: white text in table cells / text boxes / shaded
                # paragraphs sits on a coloured background and is visible
                for p in list(body.findall(W + "p")):
                    shaded = p.find(f"{W}pPr/{W}shd") is not None
                    if (_is_hidden_paragraph(p) and not shaded
                            and not list(p.iter("{%s}graphicData" % NS["a"]))
                            and not list(p.iter(W + "txbxContent"))):
                        dropped.append("".join(t.text or "" for t in p.iter(W + "t")))
                        p.getparent().remove(p)
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            zo.writestr(it, data)
    return dropped


@dataclass
class FigureInfo:
    number: int
    caption: str
    kind: str = "crop"  # "raster" or "crop"
    media: str | None = None  # word/media file name for raster figures
    reasons: list = field(default_factory=list)
    textbox_text: set = field(default_factory=set)
    height_pt: float = 0.0  # summed height of the figure's drawings (Word extents)
    n_drawings: int = 0
    src_rect: dict | None = None  # Word picture crop (a:srcRect, 1/1000 %)


def scan_docx_figures(docx: Path) -> dict[int, FigureInfo]:
    with zipfile.ZipFile(docx) as z:
        doc = etree.fromstring(z.read("word/document.xml"))
        rels = etree.fromstring(z.read("word/_rels/document.xml.rels"))
    rid2target = {r.get("Id"): r.get("Target") for r in rels}

    def ptext(p):
        return "".join(t.text or "" for t in p.iter(W + "t") if not _in_textbox(t))

    figs: dict[int, FigureInfo] = {}
    pending: list = []  # drawing descriptors since last caption / body paragraph
    pending_tb: set = set()
    body = doc.find("w:body", NS)
    for p in body.iter(W + "p"):
        if _in_textbox(p):
            continue
        txt = ptext(p).strip()
        descs = []  # (kind, media name, height pt, srcRect)
        drawings = list(p.iter(WP + "inline", WP + "anchor"))
        for dr in drawings:
            if any(a in drawings for a in dr.iterancestors()):
                continue  # nested inside another drawing
            ext = dr.find(WP + "extent")
            h = int(ext.get("cy", 0)) / EMU_PER_PT if ext is not None else 0.0
            g = dr.find(".//{%s}graphicData" % NS["a"])
            uri = (g.get("uri", "") if g is not None else "").rsplit("/", 1)[-1]
            blips = list(dr.iter("{%s}blip" % NS["a"]))
            if uri == "picture" and len(blips) == 1:
                tgt = rid2target.get(blips[0].get("{%s}embed" % NS["r"]), "")
                sr = dr.find(".//{%s}srcRect" % NS["a"])
                rect = {k: int(sr.get(k, 0)) for k in "ltrb"} if sr is not None and sr.attrib else None
                descs.append(("media", Path(tgt).name, h, rect))
            else:
                descs.append((uri or "drawing", None, h, None))
        for _ in p.iter("{%s}imagedata" % NS["v"]):
            descs.append(("vml", None, 0.0, None))
        tb = {
            "".join(t.text or "" for t in tx.iter(W + "t")).strip()
            for tx in p.iter(W + "txbxContent")
        }
        tb |= {
            "".join(t.text or "" for t in q.iter(W + "t")).strip()
            for tx in p.iter(W + "txbxContent")
            for q in tx.iter(W + "p")
        }
        is_caption = any("SEQ Figure" in (i.text or "") for i in p.iter(W + "instrText")) or \
            any("SEQ Figure" in (f.get(W + "instr") or "") for f in p.iter(W + "fldSimple"))
        m = CAPTION_RE.match(txt) if is_caption else None
        if m:
            pending += descs
            pending_tb |= tb
            n = int(m.group(1))
            fi = FigureInfo(n, txt)
            fi.textbox_text = {t for t in pending_tb if t}
            rasters = [d for d in pending if d[0] == "media"]
            others = [d for d in pending if d[0] != "media"]
            fi.height_pt = sum(d[2] for d in pending)
            fi.n_drawings = len(pending)
            if len(rasters) == 1 and not others and Path(rasters[0][1]).suffix.lower() in RASTER_EXT:
                fi.kind, fi.media, fi.src_rect = "raster", rasters[0][1], rasters[0][3]
            else:
                fi.kind = "crop"
                fi.reasons = [d[1] or d[0] for d in pending] or ["no drawing found in docx"]
            if n not in figs:
                figs[n] = fi
            pending, pending_tb = [], set()
        elif descs:
            pending += descs
            pending_tb |= tb
        elif txt:
            pending, pending_tb = [], set()
    return figs


def _in_textbox(el) -> bool:
    e = el.getparent()
    while e is not None:
        if e.tag == W + "txbxContent":
            return True
        e = e.getparent()
    return False


# --------------------------------------------------------------------------
# 2. PDF cropping
# --------------------------------------------------------------------------
def _norm(s: str) -> str:
    return re.sub(r"\W+", "", s).lower()


def crop_figures_from_pdf(pdf: Path, figs: dict[int, FigureInfo], numbers, outdir: Path, dpi=200):
    doc = fitz.open(pdf)
    pages = [(pg, pg.get_text("blocks")) for pg in doc]
    results = {}
    for n in numbers:
        fi = figs[n]
        key = _norm(fi.caption)[:30]
        hit = None
        for pg, blocks in pages:
            for b in blocks:
                if CAPTION_RE.match(b[4].strip()) and _norm(b[4])[:30] == key:
                    hit = (pg, blocks, fitz.Rect(b[:4]))
                    break
            if hit:
                break
        if not hit:
            log(f"WARNING: caption of Figure {n} not found in PDF (is the PDF the same version "
                f"as the docx?); figure omitted")
            continue
        pg, blocks, cap = hit
        top = _body_bottom(blocks, cap.y0, HEADER_BOTTOM)
        if fi.height_pt:  # never reach higher than the drawings' own height (+ slack)
            top = max(top, cap.y0 - fi.height_pt - 18)
        region = fitz.Rect(MARGIN_LEFT, top + 1, pg.rect.width - MARGIN_RIGHT, cap.y0 - 1)
        content = _content_box(pg, blocks, region)
        if content.is_empty or content.height < 20:
            log(f"WARNING: Figure {n}: no graphic content found above caption on page {pg.number + 1}")
            content = region
        clip = (content + (-4, -4, 4, 3)) & pg.rect
        out = outdir / f"figure-{n:02d}.png"
        pg.get_pixmap(clip=clip, dpi=dpi).save(out)
        results[n] = {"page": pg.number + 1, "clip": [round(v, 1) for v in clip], "extra": []}
        # figure that starts on the previous page (e.g. a chart followed by a picture)
        if fi.n_drawings > 1 and clip.height < 0.85 * fi.height_pt and pg.number > 0:
            prev, pblocks = pages[pg.number - 1]
            ptop = _body_bottom(pblocks, prev.rect.height - FOOTER_HEIGHT, HEADER_BOTTOM)
            preg = fitz.Rect(MARGIN_LEFT, ptop + 1, prev.rect.width - MARGIN_RIGHT,
                             prev.rect.height - FOOTER_HEIGHT)
            pcont = _content_box(prev, pblocks, preg)
            if not pcont.is_empty and pcont.height > 40:
                pclip = (pcont + (-4, -4, 4, 3)) & prev.rect
                pname = f"figure-{n:02d}-part1.png"
                prev.get_pixmap(clip=pclip, dpi=dpi).save(outdir / pname)
                results[n]["extra"].append(pname)
                log(f"NOTE: Figure {n} continues from page {prev.number + 1}; added {pname}")
    return results


# page geometry of the report template (A4, points)
MARGIN_LEFT, MARGIN_RIGHT = 80, 45
HEADER_BOTTOM = 85.0  # running header (logo + page number) ends here
FOOTER_HEIGHT = 70.0  # "Document ID ... Signed ..." footer
BODY_X0 = 87.5  # body text and headings start at the left margin (x0 ~ 85)


def _body_bottom(blocks, limit_y, start):
    """Lowest bottom edge of body text / captions above limit_y."""
    top = start
    for b in blocks:
        r = fitz.Rect(b[:4])
        t = b[4].strip()
        is_body = r.x0 <= BODY_X0 or CAPTION_RE.match(t) or TABLE_CAPTION_RE.match(t)
        if is_body and r.y1 <= limit_y - 1 and r.y1 > top:
            top = r.y1
    return top


def _content_box(pg, blocks, region):
    content = fitz.Rect()
    for d in pg.get_drawings():
        rr = fitz.Rect(d["rect"]) & region
        if not rr.is_empty or (rr.width > 0 or rr.height > 0):
            content |= rr
    for im in pg.get_image_info():
        rr = fitz.Rect(im["bbox"]) & region
        if not rr.is_empty:
            content |= rr
    for b in blocks:
        rr = fitz.Rect(b[:4])
        if rr.intersects(region) and b[4].strip():
            content |= rr & region
    return content


# --------------------------------------------------------------------------
# 3. AST transformation
# --------------------------------------------------------------------------
@dataclass
class Page:
    slug: str
    title: str
    blocks: list
    children: list = field(default_factory=list)  # slugs of sub pages
    numbered: bool = True


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_]+", "-", s)[:50].strip("-")


HEADER_IDS: set = set()  # pandoc heading ids; emitted as "sec-<id>" (docutils uses the bare slug)


def anchor_id(i: str) -> str:
    return "sec-" + i if i in HEADER_IDS else i


def _clean_tex(tex: str) -> str:
    tex = tex.strip()
    while tex.endswith("\\") and not tex.endswith("\\\\"):
        tex = tex[:-1].rstrip()
    return tex


def transform_inlines(inlines: list, in_table: bool, img_map: dict, in_header: bool = False) -> list:
    out = []
    for x in inlines:
        t = x.get("t")
        if t in ("Strong", "Emph") and not in_header:
            content = x["c"]
            if not stringify(content).strip():
                out.extend(content)  # empty emphasis: keep the spaces, drop the markers
                continue
            tag = "strong" if t == "Strong" else "em"
            # html tags avoid CommonMark flanking rules (e.g. "**IFE/E-2026/**0xx")
            out.append(raw(f"<{tag}>"))
            out.extend(content)
            out.append(raw(f"</{tag}>"))
        elif t == "Span":
            attr, content = x["c"]
            if attr[0]:
                out.append(raw(f'<span id="{attr[0]}"></span>'))
            out.extend(content)
        elif t == "Link":
            attr, content, (url, title) = x["c"]
            if url.startswith("#"):
                out.append(raw(f'<a class="internal" href="@@LINK:{anchor_id(url[1:])}@@">'))
                out.extend(content)
                out.append(raw("</a>"))
            else:
                out.append(x)
        elif t == "Math":
            kind, tex = x["c"]
            tex = _clean_tex(tex)
            display = kind["t"] == "DisplayMath"
            if in_table:  # tables are raw HTML: MathJax picks up class="math"
                d = ("\\[", "\\]") if display else ("\\(", "\\)")
                out.append(raw(f'<span class="math notranslate nohighlight">{d[0]}{_html_escape(tex)}{d[1]}</span>'))
            else:  # MyST dollarmath
                out.append({"t": "RawInline", "c": ["markdown", f"$${tex}$$" if display else f"${tex}$"]})
        elif t == "Image":
            attr, alt, (src, title) = x["c"]
            name = Path(src).name
            if Path(name).suffix.lower() not in RASTER_EXT:
                log(f"WARNING: dropped non-raster inline image {name}")
                continue
            img_map.setdefault(name, None)
            x = {"t": "Image", "c": [["", [], []], alt, ("images/" + name, title)]}
            out.append(x)
        else:
            out.append(x)
    return out


def _html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def transform_blocks(blocks: list, img_map: dict) -> list:
    """Anchors, links, math-in-tables and images; returns new block list."""
    out = []
    for b in blocks:
        t = b["t"]
        if t == "Header":
            level, attr, inl = b["c"]
            ids = []
            if attr[0]:
                ids.append(anchor_id(attr[0]))
            ids += _pop_span_ids(inl)
            for i in ids:
                out.append(raw_block(f'<span id="{i}"></span>'))
            walk_inlines(inl, lambda l: transform_inlines(l, False, img_map, in_header=True))
            out.append({"t": "Header", "c": [level, ["", [], []], _strip_header(inl)]})
            continue
        if t in ("Para", "Plain") and not stringify(b["c"]).strip() and not has_image(b["c"]):
            if not any(i.get("t") == "Span" and i["c"][0][0] for i in b["c"]):
                continue  # empty paragraph
        if t == "Figure":  # pandoc figure (image + caption) -> image paragraph + caption
            attr, (short, cap_blocks), content = b["c"]
            imgs = []
            walk_inlines(content, lambda l: (imgs.extend(i for i in l if i.get("t") == "Image"), l)[1])
            sub = [para([im]) for im in imgs] + [
                {"t": "Div", "c": [["", ["fig-caption"], []], cap_blocks]}] if cap_blocks else []
            out.extend(transform_blocks(sub or [para(imgs)], img_map))
            continue
        in_table = t == "Table"
        if in_table and b["c"][1][1]:  # pandoc attached the caption to the table
            cap = b["c"][1][1]
            b["c"][1] = [None, []]
            out.extend(transform_blocks([{"t": "Div", "c": [["", ["table-caption"], []], cap]}], img_map))
        walk_inlines(b, lambda l, it=in_table: transform_inlines(l, it, img_map))
        out.append(b)
    return out


def _pop_span_ids(inl):
    ids = []
    for x in inl:
        if x.get("t") == "Span" and x["c"][0][0]:
            ids.append(x["c"][0][0])
            ids += _pop_span_ids(x["c"][1])
    return ids


def _strip_header(inl):
    out = []
    for x in inl:
        if x.get("t") == "Span":
            out.extend(_strip_header(x["c"][1]))
        else:
            out.append(x)
    # trim leading/trailing spaces and line breaks
    while out and out[0].get("t") in ("Space", "LineBreak", "SoftBreak"):
        out.pop(0)
    while out and out[-1].get("t") in ("Space", "LineBreak", "SoftBreak"):
        out.pop()
    return out


def replace_figures(blocks: list, figs: dict[int, FigureInfo], fig_files: dict[int, str],
                    fig_extra: dict | None = None) -> list:
    fig_extra = fig_extra or {}
    out: list = []
    for b in blocks:
        text = stringify(b["c"]).strip() if b["t"] in ("Para", "Plain") else ""
        m = CAPTION_RE.match(text)
        if m and int(m.group(1)) in figs and _norm(text)[:40] == _norm(figs[int(m.group(1))].caption)[:40]:
            n = int(m.group(1))
            if has_image(b["c"]):  # image and caption share one Word paragraph
                inl = [x for x in b["c"] if x.get("t") != "Image"]
                while inl and inl[0].get("t") in ("Space", "LineBreak", "SoftBreak"):
                    inl.pop(0)
                b = {"t": b["t"], "c": inl}
            fi = figs[n]
            # remove the figure content pandoc emitted just before the caption
            while out:
                prev = out[-1]
                ptxt = stringify(prev.get("c")).strip()
                if prev["t"] in ("Para", "Plain", "BlockQuote", "Figure") and (
                    has_image(prev.get("c")) or not ptxt or ptxt in fi.textbox_text
                ):
                    out.pop()
                    continue
                break
            fname = fig_files.get(n)
            if not fname:
                log(f"WARNING: no image for Figure {n}")
                out.append({"t": "Div", "c": [["", ["fig-caption"], []], [b]]})
                continue
            for extra in fig_extra.get(n, []):
                out.append(raw_block(f"@@IMAGE:{extra}@@"))
            out.append(raw_block(f"@@FIGURE:{fname}@@"))
            out.append({"t": "Div", "c": [["", ["figure-caption-src"], []], [b]]})
            continue
        if b["t"] in ("Para", "Plain") and TABLE_CAPTION_RE.match(text):
            out.append({"t": "Div", "c": [["", ["table-caption"], []], [b]]})
            continue
        out.append(b)
    return out


# --------------------------------------------------------------------------
# 4. writing
# --------------------------------------------------------------------------
def pandoc_to_md(blocks: list, meta_version) -> str:
    doc = {"pandoc-api-version": meta_version, "meta": {}, "blocks": blocks}
    res = subprocess.run(
        ["pandoc", "-f", "json", "-t", "gfm+tex_math_dollars+footnotes+raw_html-smart-pipe_tables",
         "--wrap=none"],
        input=json.dumps(doc), capture_output=True, text=True, check=True,
    )
    return res.stdout


DASHES = "–—−-"
CITE_RE = re.compile(
    r"(?<![\w\\$])(\\?\[)(\d{1,3}(?:\s*[,%s]\s*\d{1,3})*)(\\?\])(?![(%%])" % DASHES)
# "[3]–[5]": a range written as two citations
# "[53, p. 130]": citation with a page locator (only the number is linked)
CITE_PAGE_RE = re.compile(r"(?<![\w\\$])(\\?\[)(\d{1,3})(,\s*pp?\.\s*[\d%s]+)(\\?\])" % DASHES)
CITE_RANGE_RE = re.compile(r"\\?\[(\d{1,3})\\?\]\s*[%s]\s*\\?\[(\d{1,3})\\?\]" % DASHES)
MATH_RE = re.compile(r'(\$\$.*?\$\$|(?<!\\)\$[^$\n]+?(?<!\\)\$|<span class="math[^"]*">.*?</span>)')


def link_citations(md: str, valid: set) -> tuple[str, list[int]]:
    """Link numbered citations to #ref-N; return (markdown, cited numbers in order).

    Text is never changed: only the digits are wrapped in <a> tags. Brackets
    whose numbers are not all valid reference numbers are left alone, as are
    math, code fences, figure directive options and image tags.
    """
    cited: list[int] = []

    def add(n):
        if n not in cited:
            cited.append(n)

    def repl(m):
        body = m.group(2)
        nums = [int(x) for x in re.findall(r"\d+", body)]
        if not nums or any(n not in valid for n in nums):
            return m.group(0)
        parts = re.split(r"(\s*[,%s]\s*)" % DASHES, body)
        for i in range(0, len(parts), 2):
            a = int(parts[i])
            add(a)
            if i + 2 < len(parts) and parts[i + 1].strip() in DASHES:
                for k in range(a + 1, int(parts[i + 2])):
                    add(k)
        linked = re.sub(
            r"\d+", lambda d: f'<a class="cite" href="#ref-{d.group(0)}">{d.group(0)}</a>', body
        )
        return f"{m.group(1)}{linked}{m.group(3)}"

    def link_text(text):
        for m in CITE_RANGE_RE.finditer(text):
            a, b = int(m.group(1)), int(m.group(2))
            if a in valid and b in valid and a < b:
                for k in range(a, b + 1):
                    add(k)
        def page_repl(m):
            n = int(m.group(2))
            if n not in valid:
                return m.group(0)
            add(n)
            return f'{m.group(1)}<a class="cite" href="#ref-{n}">{n}</a>{m.group(3)}{m.group(4)}'

        return CITE_RE.sub(repl, CITE_PAGE_RE.sub(page_repl, text))

    out_lines = []
    in_fence = False
    for line in md.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence or stripped.startswith(("<img", ":::{figure}", ":alt:", ":align:")):
            out_lines.append(line)
            continue
        pieces = MATH_RE.split(line)  # odd indices are math
        out_lines.append("".join(pc if i % 2 else link_text(pc) for i, pc in enumerate(pieces)))
    return "\n".join(out_lines), cited


def postprocess(md: str, page: Page, anchor_page: dict, bib_md: dict) -> str:
    # figures: placeholder + caption div -> MyST figure directive
    def fig_repl(m):
        fname, caption = m.group(1), m.group(2).strip()
        return f":::{{figure}} images/{fname}\n:alt: {_alt(caption)}\n:align: center\n\n{caption}\n:::\n"

    md = re.sub(
        r'@@FIGURE:([^@]+)@@\s*<div class="figure-caption-src">\s*(.*?)\s*</div>',
        fig_repl, md, flags=re.S,
    )
    md = re.sub(r"@@IMAGE:([^@]+)@@", lambda m: f"```{{image}} images/{m.group(1)}\n:align: center\n```", md)
    # internal links
    def link_repl(m):
        target = m.group(1)
        pg = anchor_page.get(target)
        if pg is None:
            log(f"WARNING: {page.slug}: link target #{target} not found")
            return "#" + target
        return f"#{target}" if pg == page.slug else f"{pg}.html#{target}"

    def drop_dead(m):
        if m.group(1) in anchor_page:
            return m.group(0)
        log(f"NOTE: {page.slug}: cross-reference target #{m.group(1)} not found in the "
            f"document (broken Word bookmark); link removed, text kept: {m.group(2)!r}")
        return m.group(2)

    md = re.sub(r'<a class="internal" href="@@LINK:([^@]+)@@">(.*?)</a>', drop_dead, md, flags=re.S)
    md = re.sub(r"@@LINK:([^@]+)@@", link_repl, md)
    # raw html tables: RTD styling + horizontal scroll
    md = re.sub(r"<table(\s[^>]*)?>",
                lambda m: f'<div class="wy-table-responsive"><table class="docutils align-default"{m.group(1) or ""}>', md)
    md = md.replace("</table>", "</table></div>")
    # footnotes: number them through the whole site, as in the report
    fn_map: dict = {}

    def fn_repl(m):
        if m.group(1) not in fn_map:
            FOOTNOTE_COUNTER[0] += 1
            fn_map[m.group(1)] = str(FOOTNOTE_COUNTER[0])
        return f"[^{fn_map[m.group(1)]}]"

    md = re.sub(r"\[\^([^\]\s]+)\]", fn_repl, md)
    # footnotes pandoc had to write as HTML (inside HTML tables)
    html_first = []

    def html_fn(m):
        FOOTNOTE_COUNTER[0] += 1
        html_first.append(FOOTNOTE_COUNTER[0])
        return f"{m.group(1)}<sup>{FOOTNOTE_COUNTER[0]}</sup>"

    md = re.sub(r'(<a href="#fn\d+" class="footnote-ref"[^>]*>)<sup>\d+</sup>', html_fn, md)
    if html_first:
        md = re.sub(r'(<section id="footnotes"[^>]*>\s*(?:<hr />)?\s*)<ol>',
                    lambda m: f'{m.group(1)}<ol start="{html_first[0]}">', md, count=1)
    md, cited = link_citations(md, set(bib_md))
    if cited and page.slug != "references":
        md = md.rstrip() + "\n\n" + page_reference_list(cited, bib_md)
    return md


FOOTNOTE_COUNTER = [0]


def _alt(caption: str) -> str:
    s = re.sub(r"<[^>]+>", "", caption)
    s = re.sub(r"[*_\\]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def page_reference_list(cited: list[int], bib_md: dict) -> str:
    lines = ["```{rubric} References cited on this page", "```", "", '<div class="page-refs">', ""]
    for n in sorted(cited):
        lines.append(
            f'<span id="ref-{n}"></span>{bib_md[n]} '
            f'<a class="ref-full" href="references.html#ref-{n}" title="Full reference list">↗</a>'
        )
        lines.append("")
    lines.append("</div>")
    return "\n".join(lines) + "\n"


CONF_PY = '''# Generated by tools/docx2rtd.py
project = {project!r}
author = {author!r}
copyright = {copyright!r}

extensions = ["myst_parser", "sphinx.ext.mathjax"]
myst_enable_extensions = ["dollarmath", "colon_fence"]
smartquotes = False  # keep the report's quotes and dashes exactly
myst_heading_anchors = 0
source_suffix = {{".md": "markdown"}}
exclude_patterns = ["_build"]

html_theme = "sphinx_rtd_theme"
html_title = {project!r}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_theme_options = {{"navigation_depth": 4, "collapse_navigation": False}}
'''

CONF_PY_TIDY = '''
# Report numbering and citations: see _ext/ifereport.py
import os
import sys
sys.path.insert(0, os.path.abspath("_ext"))
extensions += ["ifereport"]
numfig = True
numfig_secnum_depth = 0  # Figure 1..N and Table 1..N through the whole report
numfig_format = {{"figure": "Figure %s", "table": "Table %s", "code-block": "Listing %s", "section": "%s"}}
ifereport_references_doc = "references"
ifereport_appendix_prefixes = {appendix!r}
'''

CUSTOM_CSS = """/* Generated by tools/docx2rtd.py */
.rst-content .fig-caption p { text-align: center; }
.rst-content .table-caption p { font-style: italic; text-align: center; margin-bottom: 6px; }
.rst-content figure figcaption p, .rst-content .figure .caption { font-style: italic; }
.rst-content table.docutils td, .rst-content table.docutils th { white-space: normal; vertical-align: top; }
.rst-content table.docutils td p, .rst-content table.docutils th p { margin: 0; font-size: 90%; line-height: 1.35; }
.rst-content table.docutils thead th { background: #e6eef5; }
.rst-content .wy-table-responsive table td, .rst-content .wy-table-responsive table th { white-space: normal; }
.rst-content figure img { border: 1px solid #e1e4e5; }
.page-refs { font-size: 90%; border-top: 1px solid #e1e4e5; padding-top: 8px; }
.page-refs p { margin-bottom: 6px; }
.references-list p { margin-bottom: 8px; padding-left: 3.2em; text-indent: -3.2em; }
.rst-content table.report-info th { text-align: left; width: 30%; background: #f3f6f6; }
a.cite { text-decoration: none; }
a.ref-full { text-decoration: none; font-size: 85%; }
.rst-content .math { overflow-x: auto; }
.rst-content table.docutils caption { font-style: italic; text-align: center; padding-bottom: 6px; }
.rst-content table.docutils td.text-center, .rst-content table.docutils th.text-center { text-align: center; }
.rst-content table.docutils td.text-right, .rst-content table.docutils th.text-right { text-align: right; }
.rst-content figure.align-default { margin-left: auto; margin-right: auto; text-align: center; }
.rst-content p.ref-entry { padding-left: 3.2em; text-indent: -3.2em; margin-bottom: 8px; }
.rst-content .page-refs p.ref-entry { padding-left: 0; text-indent: 0; margin-bottom: 6px; }
.underline { text-decoration: underline; }
"""

RTD_YAML = """# Read the Docs configuration (generated by tools/docx2rtd.py)
version: 2
build:
  os: ubuntu-24.04
  tools:
    python: "3.12"
sphinx:
  configuration: {conf}
python:
  install:
    - requirements: {req}
"""

# versions the generated site was tested with
REQUIREMENTS = "sphinx==7.4.7\nsphinx-rtd-theme==3.1.0\nmyst-parser==3.0.1\n"


def write_page(path: Path, md: str):
    path.write_text(md.rstrip() + "\n", encoding="utf8")


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
class ConversionError(Exception):
    pass


def check_inputs(args) -> None:
    for label, p in (("--docx", args.docx), ("--pdf", args.pdf)):
        if not Path(p).is_file():
            raise ConversionError(f"{label} file not found: {p}")
    if args.figure_manifest and not Path(args.figure_manifest).is_file():
        raise ConversionError(f"--figure-manifest file not found: {args.figure_manifest}")
    if not shutil.which("pandoc"):
        raise ConversionError("pandoc not found on PATH (install it, e.g. 'brew install pandoc')")
    try:
        Path(args.out).resolve().relative_to(Path(args.rtd_root).resolve())
    except ValueError:
        raise ConversionError(f"--out {args.out} must be inside --rtd-root {args.rtd_root}")


def build(args):
    check_inputs(args)
    log_lines.clear()
    field_log.clear()
    docx, pdf, out = Path(args.docx), Path(args.pdf), Path(args.out)
    tmp = Path(tempfile.mkdtemp(prefix="docx2rtd-"))
    try:
        _build(args, docx, pdf, out, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _build(args, docx, pdf, out, tmp):
    final_src = out / "source"
    src = tmp / "source"  # built here, swapped in at the end (a failed run keeps the old site)
    (src / "images").mkdir(parents=True)
    (src / "_static").mkdir()

    # 1-2. preprocess + pandoc
    pre = tmp / "doc.docx"
    n_fields = 0
    for t in preprocess_docx(docx, pre, args.heading_style):
        if t.startswith("@field "):
            n_fields += 1
            field_log.append(t[7:])
            if ERROR_REF in t:
                log(f"WARNING: cross-reference to a missing bookmark and no matching table/figure "
                    f"found from its context; Word (and the PDF) show {ERROR_REF!r}: {t[7:]}")
            elif t.startswith("@field xref-fixed"):
                log(f"WARNING: broken cross-reference corrected from its context (please check): {t[17:].strip()}")
        else:
            log(f"NOTE: dropped invisible paragraph (white or hidden text in Word): {t!r}")
    if n_fields:
        log(f"NOTE: updated {n_fields} stale Word field results (SEQ numbers / REF texts) to "
            f"match what Word shows after updating fields; see 'field_updates' in the report")
    ast = json.loads(subprocess.run(
        ["pandoc", str(pre), "-t", "json", f"--extract-media={tmp}"],
        capture_output=True, text=True, check=True).stdout)
    media_dir = tmp / "media"
    blocks = ast["blocks"]

    # 3. figures
    figs = scan_docx_figures(pre)  # field-updated copy: same caption numbers as the pandoc text
    print(f"Found {len(figs)} figure captions in docx", file=sys.stderr)
    manifest = {}
    if args.figure_manifest:
        manifest = json.loads(Path(args.figure_manifest).read_text())
    fig_files: dict[int, str] = {}
    fig_extra: dict[int, list] = {}
    to_crop = []
    for n, fi in sorted(figs.items()):
        m = manifest.get(str(n))
        if m and m.get("source") != "original" and m.get("file"):
            # restyled figure (mirror build); extra parts are shown after the main file,
            # the last one carries the caption
            mdir = Path(args.figure_manifest).parent
            parts = [m["file"]] + [e["file"] if isinstance(e, dict) else e for e in m.get("extra_files", [])]
            names = []
            for k, part in enumerate(parts):
                f = mdir / part
                dst = f"figure-{n:02d}{'' if k == len(parts) - 1 else f'-part{k + 1}'}{f.suffix}"
                shutil.copy(f, src / "images" / dst)
                names.append(dst)
            fig_files[n] = names[-1]
            fig_extra[n] = names[:-1]
        elif fi.kind == "raster" and (media_dir / fi.media).exists():
            dst = f"figure-{n:02d}{Path(fi.media).suffix.lower()}"
            copy_cropped(media_dir / fi.media, src / "images" / dst, fi.src_rect)
            fig_files[n] = dst
        else:
            to_crop.append(n)
    crops = crop_figures_from_pdf(pdf, figs, to_crop, src / "images")
    for n, c in crops.items():
        fig_files[n] = f"figure-{n:02d}.png"
        fig_extra[n] = c["extra"]
    fig_report = {
        n: {"caption": figs[n].caption, "file": fig_files.get(n),
            "method": ("manifest" if manifest.get(str(n), {}).get("source", "original") != "original"
                       else "docx-media" if figs[n].kind == "raster" else "pdf-crop"),
            "reasons": figs[n].reasons, "pdf_page_clip": crops.get(n)}
        for n in sorted(figs)
    }

    # front matter: everything before first H1
    first_h1 = next((i for i, b in enumerate(blocks) if b["t"] == "Header" and b["c"][0] == 1), None)
    if first_h1 is None:
        raise ConversionError(
            f"no level-1 headings found. Chapter headings must use Word's built-in 'Heading 1-4' "
            f"styles or '{args.heading_style} 1-4' (change with --heading-style)")
    front, rest = blocks[:first_h1], blocks[first_h1:]
    title = None
    front_keep = []
    info_table = None
    for b in front:
        txt = stringify(b["c"]).strip()
        if not txt and not has_image(b["c"]):
            continue
        if txt == "Contents" or _is_toc_entry(b):
            continue  # Word table of contents (the site has its own navigation)
        if has_image(b["c"]) or b["t"] == "Figure":
            continue  # cover photo, logos and decorations are not shown on the site
        if b["t"] == "Table" and info_table is None:
            info_table = b  # report information table -> Summary + report information pages
            continue
        if title is None and b["t"] in ("BlockQuote", "Para") and not has_image(b["c"]):
            title = txt
            continue
        front_keep.append(b)
    title = title or docx.stem
    pdf_front = pdf_front_matter(pdf)
    front_keep = [reconcile_with_pdf(b, pdf_front["lines"]) for b in front_keep]
    info = parse_info_table(info_table, pdf) if info_table else []

    # split references / appendix
    ref_titles = [t.strip().lower() for t in args.references_title.split(",")]
    ref_idx = next((i for i, b in enumerate(rest)
                    if b["t"] == "Header" and b["c"][0] == 1
                    and stringify(b["c"][2]).strip().lower() in ref_titles), None)
    if ref_idx is None:
        raise ConversionError(
            f"no level-1 heading titled {args.references_title!r} found; the reference list "
            f"must follow such a heading (use --references-title to change it)")
    ref_title = stringify(rest[ref_idx]["c"][2]).strip()
    bib_blocks, appendix = [], []
    i = ref_idx + 1
    while i < len(rest):
        b = rest[i]
        if b["t"] in ("Para", "Plain") and BIB_RE.match(stringify(b["c"]).strip()):
            bib_blocks.append(b)
            i += 1
        elif b["t"] in ("Para", "Plain") and not stringify(b["c"]).strip():
            i += 1
        else:
            break
    appendix = rest[i:]
    body = rest[:ref_idx]
    ref_header = rest[ref_idx]

    # figures/captions
    body = replace_figures(body, figs, fig_files, fig_extra)
    appendix = replace_figures(appendix, figs, fig_files, fig_extra)
    pdf_diff = compare_body_with_pdf(body + appendix, pdf)

    # pages
    img_map: dict = {}
    pages: list[Page] = []
    chapters: list[list] = []
    for b in body:
        if b["t"] == "Header" and b["c"][0] == 1:
            chapters.append([b])
        else:
            chapters[-1].append(b)
    for ci, ch in enumerate(chapters, 1):
        ctitle = stringify(ch[0]["c"][2]).strip()
        slug = f"{ci:02d}-{slugify(ctitle)}"
        n_h2 = sum(1 for b in ch if b["t"] == "Header" and b["c"][0] == 2)
        if len(ch) > SPLIT_THRESHOLD and n_h2 > 1:
            head = []
            subs: list[list] = []
            for b in ch:
                if b["t"] == "Header" and b["c"][0] == 2:
                    subs.append([b])
                elif subs:
                    subs[-1].append(b)
                else:
                    head.append(b)
            parent = Page(slug, ctitle, head)
            pages.append(parent)
            for si, sb in enumerate(subs, 1):
                stitle = stringify(sb[0]["c"][2]).strip()
                sslug = f"{ci:02d}-{si:02d}-{slugify(stitle)}"
                for b in sb:
                    if b["t"] == "Header":
                        b["c"][0] -= 1
                pages.append(Page(sslug, stitle, sb))
                parent.children.append(sslug)
        else:
            pages.append(Page(slug, ctitle, ch))
    pages.append(Page("references", ref_title, [ref_header]))
    # appendices: each "Appendix X – ..." paragraph (or level-1 heading) starts a
    # page and is promoted to its title (text unchanged)
    current = None
    for b in appendix:
        t = stringify(b["c"]).strip() if b["t"] in ("Para", "Plain", "Header") else ""
        m = re.match(r"^Appendix\s+([A-Z])\b", t)
        if m and (b["t"] == "Header" or re.match(r"^Appendix\s+[A-Z]\s*[:.–—-]", t)):
            inl = b["c"][2] if b["t"] == "Header" else b["c"]
            current = Page(f"appendix-{m.group(1).lower()}", t,
                           [{"t": "Header", "c": [1, ["", [], []], inl]}], numbered=False)
            pages.append(current)
        elif current is None:
            if stringify(b.get("c")).strip():
                log(f"WARNING: content after the reference list before any 'Appendix X' title "
                    f"was put on page 'appendix': {stringify(b.get('c')).strip()[:60]!r}")
                current = Page("appendix", "Appendix",
                               [{"t": "Header", "c": [1, ["", [], []], str_inlines("Appendix")]}],
                               numbered=False)
                pages.append(current)
                current.blocks.append(b)
        else:
            current.blocks.append(b)

    HEADER_IDS.clear()
    for p in pages:
        for b in p.blocks:
            if b["t"] == "Header" and b["c"][1][0]:
                HEADER_IDS.add(b["c"][1][0])
    FOOTNOTE_COUNTER[0] = 0
    for p in pages:
        p.blocks = transform_blocks(p.blocks, img_map)
    front_keep = transform_blocks(front_keep, img_map)
    bib_t = transform_blocks(bib_blocks, img_map)

    # anchors -> page
    anchor_page = {}
    for p in pages:
        ids: set = set()
        collect_ids(p.blocks, ids)
        for i in ids:
            anchor_page.setdefault(i, p.slug)

    # inline images (non-figure) e.g. the cover
    for name in img_map:
        if (media_dir / name).exists():
            shutil.copy(media_dir / name, src / "images" / name)
        else:
            log(f"WARNING: missing media {name}")

    # bibliography markdown
    ver = ast["pandoc-api-version"]
    bib_md = {}
    dupes = []
    for b in bib_t:
        n = int(BIB_RE.match(stringify(b["c"]).strip()).group(1))
        if n in bib_md:  # keep the first entry: Word's bibliography field repeats a stale block
            dupes.append(n)
            continue
        md = pandoc_to_md([b], ver).strip()
        md = re.sub(r"@@LINK:([^@]+)@@", lambda m: "references.html#" + m.group(1), md)
        bib_md[n] = link_urls(md)
    if dupes:
        log(f"WARNING: the reference list repeats {len(dupes)} numbers ([{dupes[0]}]..[{dupes[-1]}]), "
            f"a stale copy left in the Word bibliography; the first occurrence of each was used")
    expected = set(range(1, max(bib_md) + 1)) if bib_md else set()
    if expected - set(bib_md):
        log(f"WARNING: reference numbers missing from the list: {sorted(expected - set(bib_md))}")

    # write pages
    for p in pages:
        md = pandoc_to_md(p.blocks, ver)
        if p.slug == "references":
            md = md.rstrip() + "\n\n" + '<div class="references-list">\n\n' + "\n\n".join(
                f'<span id="ref-{n}"></span>{bib_md[n]}' for n in sorted(bib_md)) + "\n\n</div>\n"
        if p.children:
            md = md.rstrip() + "\n\n```{toctree}\n:maxdepth: 2\n\n" + "\n".join(p.children) + "\n```\n"
        md = postprocess(md, p, anchor_page, bib_md)
        write_page(src / f"{p.slug}.md", md)

    # front pages from the report information table (unnumbered, before chapter 1)
    front_pages = []
    summary = next((it for it in info if it["label"].lower().startswith("summary")), None)
    if summary:
        sblocks = summary["blocks"] if summary["source"] == "docx" else [para(str_inlines(summary["text"]))]
        md = "# Summary\n\n" + pandoc_to_md(transform_blocks(sblocks, img_map), ver)
        md = postprocess(md, Page("summary", "Summary", []), anchor_page, bib_md)
        write_page(src / "summary.md", md)
        front_pages.append("summary")
    rows = [it for it in info if it is not summary and it["text"].strip()]
    if rows:
        people = [it for it in rows if re.match(r"(prepared|written|reviewed|approved|author)", it["label"], re.I)]
        other = [it for it in rows if it not in people]
        md = "# Authors and report information\n\n"
        for heading, items in (("Authors and approval", people), ("Report information", other)):
            if not items:
                continue
            md += f"## {heading}\n\n" + '<div class="wy-table-responsive"><table class="docutils align-default report-info"><tbody>\n'
            for it in items:
                md += (f"<tr><th>{_html_escape(it['label'].rstrip(':'))}</th>"
                       f"<td>{_html_escape(it['text'])}</td></tr>\n")
            md += "</tbody></table></div>\n\n"
        write_page(src / "report-information.md", md)
        front_pages.append("report-information")

    # index
    front_md = postprocess(pandoc_to_md(front_keep, ver), Page("index", title, []), anchor_page, {})
    top = [p for p in pages if not any(p.slug in q.children for q in pages)]
    numbered = [p.slug for p in top if p.numbered]
    unnumbered = [p.slug for p in top if not p.numbered]
    index = f"# {title}\n\n{front_md.strip()}\n\n"
    if front_pages:
        index += "```{toctree}\n:maxdepth: 1\n:caption: About this report\n\n" + "\n".join(front_pages) + "\n```\n\n"
    index += f"```{{toctree}}\n:maxdepth: 2\n:numbered: {TOC_DEPTH}\n:caption: Contents\n\n" + "\n".join(numbered) + "\n```\n"
    if unnumbered:
        index += "\n```{toctree}\n:maxdepth: 2\n:caption: Appendix\n\n" + "\n".join(unnumbered) + "\n```\n"
    write_page(src / "index.md", index)

    missing = [n for n in figs if n not in fig_files]
    if missing:
        log(f"WARNING: {len(missing)} figure(s) have no image: {missing}")

    # tidy the Markdown for hand editing (tools/tidy_myst.py)
    tidy_report = None
    conf = CONF_PY.format(project=title, author="Institute for Energy Technology (IFE)",
                          copyright="Institute for Energy Technology (IFE)")
    if not args.raw_html:
        import tidy_myst
        ctx = tidy_myst.tidy_dir(src, log=lambda m: log(m))
        (src / "_ext").mkdir(exist_ok=True)
        shutil.copy(Path(__file__).with_name("ifereport.py"), src / "_ext" / "ifereport.py")
        appendix = {p.slug: p.slug.split("-", 1)[1].upper() for p in pages
                    if re.fullmatch(r"appendix-[a-z]", p.slug)}
        conf += CONF_PY_TIDY.format(appendix=appendix)
        tidy_report = {"stats": dict(ctx.stats), "notes": ctx.notes}

    # config files
    (src / "conf.py").write_text(conf)
    (src / "_static" / "custom.css").write_text(CUSTOM_CSS)
    out.mkdir(parents=True, exist_ok=True)
    (out / "requirements.txt").write_text(REQUIREMENTS)
    root = Path(args.rtd_root)
    rel = lambda p: Path(p).resolve().relative_to(root.resolve()).as_posix()
    (root / ".readthedocs.yaml").write_text(RTD_YAML.format(
        conf=rel(final_src / "conf.py"), req=rel(out / "requirements.txt")))
    (out / "conversion_report.json").write_text(json.dumps({
        "docx": str(docx), "pdf": str(pdf), "pages": [p.slug for p in pages],
        "site_pages": ["index"] + front_pages + [p.slug for p in pages],
        "references": len(bib_md), "figures": fig_report, "warnings": log_lines, "field_updates": field_log,
        "front_matter": [{k: v for k, v in it.items() if k != "blocks"} for it in info],
        "pdf_text_differences": pdf_diff,
        "tidy": tidy_report,
    }, indent=2, ensure_ascii=False))
    if final_src.exists():
        shutil.rmtree(final_src)
    shutil.move(str(src), str(final_src))
    print(f"Wrote {len(pages) + len(front_pages) + 1} pages, {len(bib_md)} references, {len(fig_files)} figures to {final_src}")
    problems = [l for l in log_lines if l.startswith("WARNING")]
    if args.strict and problems:
        raise ConversionError(f"--strict: {len(problems)} warning(s); see {out / 'conversion_report.json'}")


# --------------------------------------------------------------------------
# front matter and PDF reconciliation (the PDF is authoritative)
# --------------------------------------------------------------------------
def _is_toc_entry(b) -> bool:
    """A Word TOC line: a paragraph that is one internal link ending in a page number."""
    if b["t"] not in ("Para", "Plain"):
        return False
    inl = [x for x in b["c"] if x.get("t") not in ("Space", "SoftBreak")]
    return (len(inl) == 1 and inl[0].get("t") == "Link" and inl[0]["c"][2][0].startswith("#")
            and re.search(r"\d+$", stringify(inl[0]["c"][1]).strip()) is not None)


def _ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def pdf_front_matter(pdf: Path, max_pages: int = 4) -> dict:
    """Text lines and labelled cells of the PDF's first pages (cover, report information)."""
    doc = fitz.open(pdf)
    lines, blocks = [], []
    for pg in list(doc)[:max_pages]:
        for b in pg.get_text("blocks"):
            t = b[4]
            if not t.strip() or "Document ID" in t:
                continue
            blocks.append((pg.number, fitz.Rect(b[:4]), t))
            lines += [_ws(l) for l in t.split("\n") if l.strip()]
    return {"lines": lines, "blocks": blocks}


def pdf_label_values(labels: list[str], pdf: Path, max_pages: int = 4) -> dict:
    """Values of labelled cells ("Report number:", ...) on the PDF's report information page.

    The page's text lines are read top to bottom (blocks sorted by position);
    a value is every line after its label up to the next known label.
    """
    keys = {_norm(l): l for l in labels}
    doc = fitz.open(pdf)
    for pg in list(doc)[:max_pages]:
        blocks = sorted((b for b in pg.get_text("blocks")
                         if b[4].strip() and b[1] < pg.rect.height - 100),
                        key=lambda b: (round(b[1]), b[0]))
        lines = [l.strip() for b in blocks for l in b[4].split("\n") if l.strip()]
        if sum(1 for l in lines if _norm(l) in keys) < max(2, len(keys) // 2):
            continue
        values, cur = {}, None
        for l in lines:
            k = _norm(l)
            if k in keys:
                cur = keys[k]
                values[cur] = []
            elif cur is not None:
                values[cur].append(l)
        return {k: _ws(" ".join(v)) for k, v in values.items()}
    return {}


def parse_info_table(table, pdf: Path) -> list[dict]:
    """Label/value pairs of the report information table; the PDF value wins when it differs."""
    def cells(t):
        c = t["c"]
        rows = c[3][1] + [r for body in c[4] for r in body[2] + body[3]] + c[5][1]
        for row in rows:
            yield [cell[4] for cell in row[1]]

    items = []
    for row in cells(table):
        k = 0
        while k < len(row):
            blocks = []
            _flatten_blocks(row[k], blocks)
            texts = [stringify(b["c"]).strip() for b in blocks]
            if texts and texts[0].endswith(":"):
                label, vblocks = texts[0], blocks[1:]
                if not vblocks and k + 1 < len(row):
                    nxt = []
                    _flatten_blocks(row[k + 1], nxt)
                    if nxt and not stringify(nxt[0]["c"]).strip().endswith(":"):
                        vblocks = nxt
                        k += 1
                dtext = _ws(" ".join(stringify(b["c"]) for b in vblocks))
                items.append({"label": label.rstrip(":").strip(), "raw_label": label, "text": dtext,
                              "source": "docx", "docx_text": dtext, "blocks": vblocks})
            k += 1
    pvals = pdf_label_values([it["raw_label"] for it in items], pdf)
    if not pvals:
        log("WARNING: report information table not found in the PDF; docx values used")
    for it in items:
        ptext = pvals.get(it["raw_label"])
        if ptext is not None and _norm(ptext) != _norm(it["docx_text"]):
            it.update(text=ptext, source="pdf")
            log(f"NOTE: report information '{it['label']}': PDF value used "
                f"(docx {it['docx_text'][:60]!r} -> PDF {ptext[:60]!r})")
    return items


def _flatten_blocks(blocks, out):
    for b in blocks:
        if b["t"] in ("BlockQuote", "Div"):
            _flatten_blocks(b["c"] if b["t"] == "BlockQuote" else b["c"][1], out)
        elif b["t"] in ("Para", "Plain"):
            out.append(b)


def reconcile_with_pdf(b, pdf_lines):
    """Front-page paragraph: use the PDF's text when the PDF has a close but different line."""
    if b["t"] not in ("Para", "Plain") or has_image(b["c"]):
        return b
    txt = _ws(stringify(b["c"]))
    if not txt or any(_norm(l) == _norm(txt) for l in pdf_lines):
        return b
    import difflib
    best = max(pdf_lines, key=lambda l: difflib.SequenceMatcher(None, l, txt).ratio(), default=None)
    if best and difflib.SequenceMatcher(None, best, txt).ratio() >= 0.75:
        log(f"NOTE: front page: PDF text used ({txt!r} -> {best!r})")
        return {"t": b["t"], "c": str_inlines(best)}
    return b


def _pdf_body_words(pdf: Path) -> list[str]:
    words = []
    for pg in fitz.open(pdf):
        for b in pg.get_text("blocks"):
            if b[1] >= HEADER_BOTTOM - 10 and b[3] <= pg.rect.height - FOOTER_HEIGHT + 10:
                words += _norm_words(b[4].replace("-\n", ""))
    return words


def _norm_words(t: str) -> list[str]:
    return [w for w in (re.sub(r"\W+", "", x).lower() for x in t.split()) if w]


def compare_body_with_pdf(blocks, pdf: Path) -> list[dict]:
    """List body paragraphs whose words are missing or changed in the PDF (after field updates).

    Word-level alignment against the PDF text (running header/footer removed).
    Extra words on the PDF side (page breaks, figure labels) are ignored; docx
    words missing or replaced in the PDF are reported. Report only: the
    differences go to conversion_report.json so a version mismatch is noticed.
    """
    import bisect
    import difflib
    pw = _pdf_body_words(pdf)
    joined = " ".join(pw)
    starts = [0]
    for w in pw[:-1]:
        starts.append(starts[-1] + len(w) + 1)
    diffs = []
    for b in blocks:
        if b["t"] not in ("Para", "Plain") or '"Math"' in json.dumps(b):
            continue
        dw = _norm_words(stringify(b["c"]))
        if len(dw) < 8:
            continue
        cands = set()
        for anchor, back in ((dw[:6], 0), (dw[-6:], len(dw)), (dw[len(dw) // 2: len(dw) // 2 + 6], len(dw) // 2)):
            k = joined.find(" ".join(anchor))
            while k >= 0 and len(cands) < 40:
                cands.add(max(0, bisect.bisect_left(starts, k) - back))
                k = joined.find(" ".join(anchor), k + 1)
        if not cands:
            diffs.append({"docx_text": _ws(stringify(b["c"]))[:300], "issue": "paragraph not found in PDF"})
            continue
        best = None
        for pos in sorted(cands):
            window = pw[pos: pos + int(len(dw) * 1.5) + 80]
            sm = difflib.SequenceMatcher(None, window, dw, autojunk=False)
            changes = []
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op in ("replace", "insert") and j2 > j1:
                    d, q = " ".join(dw[j1:j2]), " ".join(window[i1:i2])
                    if d.replace(" ", "") != q.replace(" ", ""):  # ignore spacing/hyphenation
                        changes.append({"docx": d, "pdf": q[:200]})
            cost = sum(len(c["docx"].split()) for c in changes)
            if best is None or cost < best[0]:
                best = (cost, changes)
        changes = best[1]
        if changes:
            diffs.append({"docx_text": _ws(stringify(b["c"]))[:300], "changes": changes[:10]})
    if diffs:
        log(f"WARNING: {len(diffs)} paragraph(s) differ between the docx and the PDF; see "
            f"'pdf_text_differences' in conversion_report.json (the PDF is authoritative)")
    return diffs


def copy_cropped(src: Path, dst: Path, rect: dict | None) -> None:
    """Copy a picture, applying Word's crop (a:srcRect l/t/r/b in 1/1000 of a percent)."""
    if not rect or not any(rect.values()):
        shutil.copy(src, dst)
        return
    from PIL import Image
    with Image.open(src) as im:
        w, h = im.size
        box = (max(0, round(w * rect["l"] / 100000)), max(0, round(h * rect["t"] / 100000)),
               min(w, round(w * (1 - rect["r"] / 100000))), min(h, round(h * (1 - rect["b"] / 100000))))
        im.crop(box).save(dst)
    log(f"NOTE: applied Word picture crop to {dst.name}: {rect}")


URL_RE = re.compile(r"(?<![(\"=])(https?://[^\s<>\"]+?)(?=[.,;)]*(?:\s|$))")


def link_urls(md: str) -> str:
    """Make bare URLs clickable without changing how they are displayed."""
    def repl(m):
        shown = m.group(1)
        href = shown.replace("\\", "").replace("&", "&amp;").replace('"', "%22")
        return f'<a class="reference external" href="{href}">{shown}</a>'
    return URL_RE.sub(repl, md)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--docx", required=True)
    ap.add_argument("--pdf", required=True, help="same report as PDF (used to render charts/EMF)")
    ap.add_argument("--out", default="docs", help="output folder (source/ is regenerated)")
    ap.add_argument("--figure-manifest", help="manifest.json from tools/restyle_figures.py (mirror build)")
    ap.add_argument("--rtd-root", default=".",
                    help="repository root where .readthedocs.yaml is written (default: current folder)")
    ap.add_argument("--heading-style", default="IFE Heading",
                    help='name of the custom heading styles, without the level number '
                         '(default: "IFE Heading"; Word\'s built-in "Heading N" always works)')
    ap.add_argument("--references-title", default="References,Bibliography",
                    help="comma-separated titles of the level-1 heading above the reference list")
    ap.add_argument("--raw-html", action="store_true",
                    help="skip the tidy step and keep the HTML-heavy Markdown of the first versions")
    ap.add_argument("--strict", action="store_true",
                    help="exit with status 2 if there are any warnings (missing figures, broken links...)")
    args = ap.parse_args(argv)
    try:
        build(args)
    except ConversionError as e:
        ap.exit(2, f"error: {e}\n")


if __name__ == "__main__":
    main()
