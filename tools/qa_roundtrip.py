#!/usr/bin/env python3
"""Measure how closely a report rebuilt by tools/rtd2docx.py matches the original.

    python tools/qa_roundtrip.py \
        --orig-docx "Documentation of IFE-TIMES-Norway v5.docx" \
        --orig-pdf  "Documentation of IFE-TIMES-Norway v5.pdf" \
        --new-docx build/report.docx [--new-pdf build/report.pdf] --out build/qa

It writes ``qa_report.json`` and ``qa_report.md`` to --out, plus side-by-side page
images (``pages/*.png``) for a visual check. The original PDF is authoritative
where it differs from the original Word file (stale field numbers in the .docx).

Checks
------
text        word-level comparison of the body text (Introduction .. before References),
            from the PDFs when both are given, else from the .docx files
headings    level, number and text of every heading, in order
captions    "Figure N" / "Table N" captions, in order, with their text
tables      number of tables and the text of each, in order
references  number of entries in the reference list
styles      which Word styles the body uses (IFE heading styles, caption, Bibliography...)
objects     images, footnotes, fields (SEQ, TOC, REF), sections, page count
layout      side-by-side images of matching pages (same heading or caption)
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = "{%s}" % W_NS
CAP_RE = re.compile(r"^(Figure|Table)\s+((?:[A-Z]-)?\d+)\b[\s:.]*(.*)")


# --------------------------------------------------------------------------- docx
class Docx:
    def __init__(self, path: Path):
        self.path = path
        with zipfile.ZipFile(path) as z:
            self.names = z.namelist()
            self.doc = etree.fromstring(z.read("word/document.xml"))
            self.styles = etree.fromstring(z.read("word/styles.xml"))
            self.footnotes = etree.fromstring(z.read("word/footnotes.xml")) if "word/footnotes.xml" in self.names else None
        self.style_name = {}
        self.style_num = {}
        for s in self.styles.findall(W + "style"):
            n = s.find(W + "name")
            sid = s.get(W + "styleId")
            self.style_name[sid] = n.get(W + "val") if n is not None else sid
            self.style_num[sid] = s.find(f"{W}pPr/{W}numPr") is not None
        self.body = self.doc.find(W + "body")

    @staticmethod
    def text(el) -> str:
        out = []
        for node in el.iter(W + "t", W + "tab", W + "br", W + "del", W + "delText"):
            if node.tag == W + "t":
                if any(a.tag == W + "del" for a in node.iterancestors()):
                    continue
                out.append(node.text or "")
            elif node.tag in (W + "tab", W + "br"):
                out.append(" ")
        return re.sub(r"\s+", " ", "".join(out)).strip()

    def pstyle(self, p) -> str:
        ps = p.find(f"{W}pPr/{W}pStyle")
        return self.style_name.get(ps.get(W + "val"), ps.get(W + "val")) if ps is not None else "Normal"

    def numbered(self, p) -> bool:
        num = p.find(f"{W}pPr/{W}numPr/{W}numId")
        if num is not None:
            return num.get(W + "val") != "0"
        ps = p.find(f"{W}pPr/{W}pStyle")
        return bool(ps is not None and self.style_num.get(ps.get(W + "val")))

    def blocks(self):
        """Top-level paragraphs and tables in order: ("p", el) / ("tbl", el)."""
        for el in self.body:
            if el.tag == W + "p":
                yield "p", el
            elif el.tag == W + "tbl":
                yield "tbl", el
            elif el.tag == W + "sdt":  # content controls (e.g. TOC, cover)
                for sub in el.iter(W + "p"):
                    if not any(a.tag == W + "tbl" for a in sub.iterancestors()):
                        yield "p", sub

    def headings(self):
        counters = [0] * 9
        out = []
        for kind, p in self.blocks():
            if kind != "p":
                continue
            st = self.pstyle(p)
            m = re.match(r"(?i)(?:IFE )?Heading (\d)$", st)
            if not m:
                continue
            lvl = int(m.group(1))
            txt = self.text(p)
            if not txt:
                continue
            num = ""
            if self.numbered(p):
                counters[lvl - 1] += 1
                for k in range(lvl, 9):
                    counters[k] = 0
                num = ".".join(str(c) for c in counters[:lvl])
            out.append({"level": lvl, "number": num, "text": txt})
        return out

    def body_paragraphs(self, start_heading="Introduction", stop_heading="References"):
        """Body text paragraphs (not in tables) from the first heading `start` to `stop`."""
        on = False
        out = []
        for kind, p in self.blocks():
            if kind != "p":
                continue
            st = self.pstyle(p)
            txt = self.text(p)
            if re.match(r"(?i)(?:IFE )?Heading 1$", st):
                if txt.strip() == start_heading:
                    on = True
                elif txt.strip() == stop_heading and on:
                    break
            if on and txt:
                out.append(txt)
        return out

    def tables(self):
        out = []
        for kind, t in self.blocks():
            if kind != "tbl":
                continue
            rows = t.findall(W + "tr")
            cells = [[self.text(c) for c in r.findall(W + "tc")] for r in rows]
            out.append({"rows": len(rows), "cols": max((len(r) for r in cells), default=0),
                        "text": " | ".join(" ; ".join(r) for r in cells)})
        return out

    def captions(self):
        out = []
        for kind, p in self.blocks():
            if kind != "p":
                continue
            m = CAP_RE.match(self.text(p))
            if m and len(m.group(3)) > 3 and not re.match(r"^(shows|presents|summari|also|lists|gives)", m.group(3)):
                out.append({"kind": m.group(1), "number": m.group(2), "text": m.group(3)[:120]})
        return out

    def style_histogram(self):
        c = Counter()
        for kind, p in self.blocks():
            if kind == "p" and self.text(p):
                c[self.pstyle(p)] += 1
        return dict(c.most_common())

    def objects(self):
        xml = etree.tostring(self.doc).decode("utf8")
        instr = re.findall(r"<w:instrText[^>]*>([^<]*)<", xml) + re.findall(r'w:instr="([^"]*)"', xml)
        kinds = Counter((i.strip().split() or ["?"])[0].upper() for i in instr)
        fn = 0
        if self.footnotes is not None:
            fn = sum(1 for f in self.footnotes.findall(W + "footnote") if f.get(W + "type") is None)
        return {"images": xml.count("<pic:pic"), "footnotes": fn, "fields": dict(kinds),
                "sections": xml.count("<w:sectPr"), "tables": len(self.tables())}

    def bibliography(self):
        return [self.text(p) for k, p in self.blocks() if k == "p" and self.pstyle(p).lower() == "bibliography"
                and self.text(p)]


# --------------------------------------------------------------------------- pdf
def pdf_lines(path: Path):
    import fitz
    doc = fitz.open(path)
    pages = []
    for pg in doc:
        h = pg.rect.height
        lines = []
        for b in pg.get_text("blocks"):
            x0, y0, x1, y1, txt = b[:5]
            if y1 < 80 or y0 > h - 60:  # running header (logo, page number) / footer
                continue
            for l in txt.splitlines():
                l = l.strip()
                if l and not re.fullmatch(r"\d{1,3}", l):
                    lines.append(l)
        pages.append(lines)
    return pages


def pdf_body_words(pages, start="Introduction", stop="References"):
    """Words of the body text: from the first page whose top line is the chapter
    '1 Introduction' to the line 'References' heading (last occurrence near the end)."""
    flat = []
    for i, ls in enumerate(pages):
        for l in ls:
            flat.append((i, l))
    s = next((k for k, (i, l) in enumerate(flat) if re.fullmatch(rf"(1\s+)?{start}", l)
              and i > 2), 0)
    # skip a table of contents hit: the real chapter is followed by body text
    cands = [k for k, (i, l) in enumerate(flat) if re.fullmatch(rf"(1\s+)?{start}", l)]
    for k in cands:
        nxt = " ".join(l for _, l in flat[k + 1:k + 4])
        if not re.search(r"\.{5,}", nxt):
            s = k
            break
    e = len(flat)
    ends = [k for k, (i, l) in enumerate(flat) if re.fullmatch(rf"(\d+\s+)?{stop}", l) and k > s]
    for k in ends:
        nxt = " ".join(l for _, l in flat[k + 1:k + 3])
        if re.match(r"^\[1\]", nxt):
            e = k
            break
    text = " ".join(l for _, l in flat[s:e])
    text = re.sub(r"-\s+(?=[a-z])", "-", text)  # hyphen at line end
    return re.findall(r"\S+", text), (flat[s][0] if flat else 0), (flat[e - 1][0] if flat and e else 0)


def pdf_captions(pages):
    out = []
    seen = set()
    for i, ls in enumerate(pages):
        for l in ls:
            m = CAP_RE.match(l)
            if m and len(m.group(3)) > 3 and not re.search(r"\.{5,}", l) and \
                    not re.match(r"^(shows|presents|summari|also|lists|gives|and|in|to)\b", m.group(3)):
                key = (m.group(1), m.group(2))
                if key in seen:
                    continue
                seen.add(key)
                out.append({"kind": m.group(1), "number": m.group(2), "text": m.group(3)[:120], "page": i + 1})
    return out


# --------------------------------------------------------------------------- compare
def _norm_words(ws):
    out = []
    for w in ws:
        w = w.replace(" ", " ").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
        w = re.sub(r"[​­]", "", w)
        out.extend(re.findall(r"[\w%]+|[^\w\s]", w))
    return out


def word_diff(a, b, max_chunks=40):
    a, b = _norm_words(a), _norm_words(b)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    chunks = []
    changed = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        changed += max(i2 - i1, j2 - j1)
        if len(chunks) < max_chunks:
            chunks.append({"op": tag, "orig": " ".join(a[max(0, i1 - 5):i2 + 5])[:300],
                           "new": " ".join(b[max(0, j1 - 5):j2 + 5])[:300]})
    return {"orig_words": len(a), "new_words": len(b), "ratio": round(sm.ratio(), 5),
            "changed_words": changed, "chunks": chunks}


def seq_compare(a, b, key):
    ka, kb = [key(x) for x in a], [key(x) for x in b]
    sm = difflib.SequenceMatcher(None, ka, kb, autojunk=False)
    diffs = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            diffs.append({"op": tag, "orig": ka[i1:i2][:10], "new": kb[j1:j2][:10]})
    return {"orig": len(a), "new": len(b), "equal": ka == kb, "differences": diffs[:60]}


def side_by_side(orig_pdf: Path, new_pdf: Path, pairs, outdir: Path, dpi=60):
    import fitz
    from PIL import Image, ImageDraw
    outdir.mkdir(parents=True, exist_ok=True)
    a, b = fitz.open(orig_pdf), fitz.open(new_pdf)
    files = []
    for label, pa, pb in pairs:
        ims = []
        for d, p in ((a, pa), (b, pb)):
            pm = d[p - 1].get_pixmap(dpi=dpi)
            ims.append(Image.frombytes("RGB", (pm.width, pm.height), pm.samples))
        w = sum(i.width for i in ims) + 30
        h = max(i.height for i in ims) + 24
        sheet = Image.new("RGB", (w, h), "white")
        x = 0
        for k, im in enumerate(ims):
            sheet.paste(im, (x, 24))
            ImageDraw.Draw(sheet).text((x + 4, 4), f"{'ORIGINAL' if k == 0 else 'REBUILT'} p.{(pa, pb)[k]}", fill="black")
            x += im.width + 30
        f = outdir / f"{re.sub(r'[^A-Za-z0-9]+', '_', label)}.png"
        sheet.save(f)
        files.append(str(f))
    return files


def run(args) -> dict:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    od, nd = Docx(Path(args.orig_docx)), Docx(Path(args.new_docx))
    rep: dict = {"inputs": {k: v for k, v in vars(args).items() if k != "out"}}

    # headings
    rep["headings"] = seq_compare(od.headings(), nd.headings(),
                                  key=lambda h: f"{h['level']}|{h['number']}|{h['text']}")
    # text
    if args.orig_pdf and args.new_pdf:
        op, np_ = pdf_lines(Path(args.orig_pdf)), pdf_lines(Path(args.new_pdf))
        ow, o0, o1 = pdf_body_words(op)
        nw, n0, n1 = pdf_body_words(np_)
        rep["text"] = {"source": "pdf", "orig_pages": [o0 + 1, o1 + 1], "new_pages": [n0 + 1, n1 + 1],
                       **word_diff(ow, nw)}
        oc, nc = pdf_captions(op), pdf_captions(np_)
        rep["page_count"] = {"orig": len(op), "new": len(np_)}
    else:
        rep["text"] = {"source": "docx", **word_diff(" ".join(od.body_paragraphs()).split(),
                                                       " ".join(nd.body_paragraphs()).split())}
        oc, nc = od.captions(), nd.captions()
    rep["text_docx"] = {"source": "docx", **word_diff(" ".join(od.body_paragraphs()).split(),
                                                       " ".join(nd.body_paragraphs()).split(), 25)}
    rep["captions"] = seq_compare(oc, nc, key=lambda c: f"{c['kind']} {c['number']}: {c['text'][:60]}")
    rep["caption_numbers"] = seq_compare(oc, nc, key=lambda c: f"{c['kind']} {c['number']}")
    # tables
    ot, nt = od.tables(), nd.tables()
    rep["tables"] = {"orig": len(ot), "new": len(nt),
                     "text": word_diff(" ".join(t["text"] for t in ot).split(),
                                       " ".join(t["text"] for t in nt).split(), 25)}
    # references
    ob, nb = od.bibliography(), nd.bibliography()
    seen, ob_u = set(), []
    for r in ob:  # the v5 Word file repeats a stale block of the list
        m = re.match(r"\[(\d+)\]", r)
        if m and m.group(1) in seen:
            continue
        if m:
            seen.add(m.group(1))
        ob_u.append(r)
    rep["references"] = {"orig_unique": len(ob_u), "orig_paragraphs": len(ob), "new": len(nb),
                         "text": word_diff(" ".join(ob_u).split(), " ".join(nb).split(), 15)}
    rep["styles"] = {"orig": od.style_histogram(), "new": nd.style_histogram()}
    rep["objects"] = {"orig": od.objects(), "new": nd.objects()}

    # layout: match pages by caption, sample across the report
    if args.orig_pdf and args.new_pdf:
        by = {(c["kind"], c["number"]): c["page"] for c in oc}
        pairs = []
        for c in nc:
            k = (c["kind"], c["number"])
            if k in by:
                pairs.append((f"{c['kind']} {c['number']}", by[k], c["page"]))
        step = max(1, len(pairs) // args.samples)
        chosen = pairs[::step][:args.samples]
        chosen = [("first page", 1, 1), ("contents", min(5, len(op)), min(4, len(np_)))] + chosen
        rep["layout_images"] = side_by_side(Path(args.orig_pdf), Path(args.new_pdf), chosen, out / "pages")

    (out / "qa_report.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False))
    (out / "qa_report.md").write_text(summary_md(rep))
    return rep


def summary_md(rep) -> str:
    L = ["# Round-trip QA: rebuilt report vs original", ""]
    t = rep["text"]
    L.append(f"* **Body text** ({t['source']}): similarity {t['ratio']:.4f}, "
             f"{t['changed_words']} changed tokens of {t['orig_words']} (orig) / {t['new_words']} (new)")
    td = rep["text_docx"]
    L.append(f"* **Body text** (docx): similarity {td['ratio']:.4f}, {td['changed_words']} changed tokens")
    h = rep["headings"]
    L.append(f"* **Headings**: {h['orig']} orig / {h['new']} new, identical: {h['equal']}")
    c, cn = rep["captions"], rep["caption_numbers"]
    L.append(f"* **Captions**: {c['orig']} orig / {c['new']} new; numbers identical: {cn['equal']}; "
             f"numbers+text identical: {c['equal']}")
    tb = rep["tables"]
    L.append(f"* **Tables**: {tb['orig']} orig / {tb['new']} new; cell text similarity {tb['text']['ratio']:.4f}")
    r = rep["references"]
    L.append(f"* **References**: {r['orig_unique']} orig (unique) / {r['new']} new; "
             f"text similarity {r['text']['ratio']:.4f}")
    if "page_count" in rep:
        L.append(f"* **Pages**: {rep['page_count']['orig']} orig / {rep['page_count']['new']} new")
    o = rep["objects"]
    L.append(f"* **Objects**: orig {o['orig']}  \n  new {o['new']}")
    L += ["", "## Heading differences", ""]
    for d in h["differences"][:30]:
        L.append(f"* {d['op']}: orig {d['orig']} → new {d['new']}")
    L += ["", "## Caption differences", ""]
    for d in c["differences"][:30]:
        L.append(f"* {d['op']}: orig {d['orig']} → new {d['new']}")
    L += ["", "## Body text differences (first chunks)", ""]
    for d in t["chunks"][:25]:
        L.append(f"* {d['op']}: `{d['orig']}` → `{d['new']}`")
    L += ["", "## Styles", "", f"* orig: {rep['styles']['orig']}", f"* new: {rep['styles']['new']}"]
    if rep.get("layout_images"):
        L += ["", "## Page images (original left, rebuilt right)", ""] + [f"* {p}" for p in rep["layout_images"]]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--orig-docx", required=True)
    ap.add_argument("--orig-pdf")
    ap.add_argument("--new-docx", required=True)
    ap.add_argument("--new-pdf")
    ap.add_argument("--out", default="build/qa")
    ap.add_argument("--samples", type=int, default=10, help="number of page pairs to render")
    args = ap.parse_args(argv)
    rep = run(args)
    print((Path(args.out) / "qa_report.md").read_text())
    return 0


if __name__ == "__main__":
    sys.exit(main())
