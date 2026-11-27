"""Build synthetic variations of the IFE-TIMES-Norway report for robustness tests.

Each variant is a function that edits the parsed word/document.xml body (and
optionally styles.xml text) in place. `make_variant(src, dst, name)` writes a
copied .docx with that edit applied.
"""
from __future__ import annotations

import copy
import re
import zipfile
from pathlib import Path

from lxml import etree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def txt(p) -> str:
    return "".join(t.text or "" for t in p.iter(W + "t"))


def style(p) -> str:
    s = p.find(f"{W}pPr/{W}pStyle")
    return s.get(W + "val") if s is not None else ""


def mkpara(text: str, pstyle: str | None = None):
    p = etree.Element(W + "p")
    if pstyle:
        ppr = etree.SubElement(p, W + "pPr")
        etree.SubElement(ppr, W + "pStyle").set(W + "val", pstyle)
    r = etree.SubElement(p, W + "r")
    t = etree.SubElement(r, W + "t")
    t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return p


def set_text(p, text: str):
    ts = list(p.iter(W + "t"))
    ts[0].text = text
    for t in ts[1:]:
        t.text = ""


def find(body, pred):
    return [k for k in body if k.tag == W + "p" and pred(k)]


def h1(body, title):
    return find(body, lambda k: style(k) == "IFEHeading1" and txt(k).strip() == title)[0]


def caption(body, n):
    return find(body, lambda k: re.match(rf"\s*Figure\s+{n}\b", txt(k)))[0]


def _insert_before(anchor, elems):
    for e in elems:
        anchor.addprevious(e)


# ---------------------------------------------------------------- variants
def remove_figure_2(body, styles):
    """Delete Figure 2 (picture + caption) and renumber later captions (stale PDF)."""
    cap = caption(body, 2)
    prev = cap.getprevious()
    body.remove(prev)
    body.remove(cap)
    for k in body:
        m = re.match(r"\s*Figure\s+(\d+)", txt(k)) if k.tag == W + "p" else None
        if m and int(m.group(1)) > 2:
            # only caption paragraphs: they start with "Figure N" and contain a SEQ field
            if any("SEQ Figure" in (it.text or "") for it in k.iter(W + "instrText")):
                for t in k.iter(W + "t"):
                    if re.fullmatch(r"\d+", (t.text or "").strip()) and int(t.text) > 2:
                        t.text = str(int(t.text) - 1)
                        break
    return styles


def add_raster_figure_49(body, styles):
    """Append a copy of Figure 2 (raster + SEQ caption) at the end of Final remarks.

    The cached SEQ number is left at 2: Word-style field updating must make it 49.
    """
    cap = caption(body, 2)
    pic = copy.deepcopy(cap.getprevious())
    newcap = copy.deepcopy(cap)
    for bm in list(newcap.iter(W + "bookmarkStart", W + "bookmarkEnd")):
        bm.getparent().remove(bm)
    ts = list(newcap.iter(W + "t"))
    for t in ts[2:]:
        t.text = ""
    ts[-1].text = " A new raster figure added in a later version."
    ref = h1(body, "References")
    _insert_before(ref, [pic, newcap])
    return styles


def new_chapter(body, styles):
    """Insert a new chapter 'Scenarios' before 'Final remarks'."""
    fr = h1(body, "Final remarks")
    _insert_before(fr, [mkpara("Scenarios", "IFEHeading1"),
                        mkpara("A new chapter citing [5] and [7–9].")])
    return styles


def long_chapter(body, styles):
    """Make 'Final remarks' long (two H2 sections, >120 blocks) so it is split."""
    ref = h1(body, "References")
    els = []
    for s in ("First new section", "Second new section"):
        els.append(mkpara(s, "IFEHeading2"))
        els += [mkpara(f"Filler paragraph {i} in {s} [3].") for i in range(70)]
    _insert_before(ref, els)
    return styles


def reference_168(body, styles):
    """Add bibliography entry [168] and cite it in the introduction."""
    last = find(body, lambda k: txt(k).startswith("[167]"))[0]
    last.addnext(mkpara("[168]\tA. Author, ‘A new reference’, 2026.", "Bibliografi"))
    intro = h1(body, "Introduction")
    intro.addnext(mkpara("This sentence cites the new reference [168]."))
    return styles


def references_renamed(body, styles):
    set_text(h1(body, "References"), "Bibliography")
    return styles


def references_missing(body, styles):
    body.remove(h1(body, "References"))
    return styles


def no_appendix(body, styles):
    last = find(body, lambda k: txt(k).startswith("[167]"))[0]
    for k in list(last.itersiblings()):
        if k.tag != W + "sectPr":
            body.remove(k)
    return styles


def two_appendices(body, styles):
    sect = body[-1]
    _insert_before(sect, [
        mkpara("Appendix B – Additional data"),
        mkpara("Appendix B text citing [12]."),
    ])
    return styles


def caption_not_in_pdf(body, styles):
    """Change the caption text of Figure 1 (a PDF-cropped figure)."""
    set_text(caption(body, 1), "Figure 1 Completely rewritten caption text")
    return styles


def heading_style_builtin(body, styles):
    """Rename 'IFE Heading N' styles to Word's built-in style names 'Heading N'."""
    return re.sub(r'w:name w:val="IFE Heading (\d)"', r'w:name w:val="Heading \1"', styles)


def heading_style_other(body, styles):
    """Rename 'IFE Heading N' to a different custom name (e.g. a new template)."""
    return re.sub(r'w:name w:val="IFE Heading (\d)"', r'w:name w:val="IFE Overskrift \1"', styles)


CITATION_SAMPLES = [
    "Comma [3, 5].",
    "Range [3–5].",
    "Hyphen range [3-5].",
    "Separate [3]-[5].",
    "List [3,4,7].",
    "Unit [kNOK/MW].",
    "Percent [60]%.",
    "Year [2020].",
    "Zero [0].",
    "Out of range [1–200].",
]


def citation_forms(body, styles):
    intro = h1(body, "Introduction")
    for s in reversed(CITATION_SAMPLES):
        intro.addnext(mkpara("CITETEST " + s))
    return styles


def body_text_starts_with_figure(body, styles):
    """A body paragraph beginning 'Figure 5 shows ...' placed before Figure 4."""
    cap = caption(body, 4)
    cap.getprevious().addprevious(mkpara("Figure 5 shows the hydro inflow profile used in NO2."))
    return styles


def _ref_instr(body, bookmark):
    return [it for it in body.iter(W + "instrText") if bookmark in (it.text or "")]


def xref_broken_fixable(body, styles):
    """Break the REF to Figure 1's bookmark; the citing sentence clearly describes Figure 1."""
    it = _ref_instr(body, "_Ref52281664")[0]
    it.text = it.text.replace("_Ref52281664", "_Ref99999991")
    return styles


def xref_broken_unfixable(body, styles):
    """Break the REF to Figure 1 and make its paragraph unrelated to any caption."""
    it = _ref_instr(body, "_Ref52281664")[0]
    it.text = it.text.replace("_Ref52281664", "_Ref99999992")
    p = next(it.iterancestors(W + "p"))
    for t in p.iter(W + "t"):
        if not re.match(r"\s*Figure|\s*\d+\s*$", t.text or ""):
            t.text = "Zzz qqq. "
    return styles


def stale_seq_figure(body, styles):
    """Stale cached SEQ result: Figure 5's caption says 7 (Word F9 / the PDF show 5)."""
    cap = caption(body, 5)
    ts = list(cap.iter(W + "t"))
    assert ts[1].text == "5"
    ts[1].text = "7"
    return styles


def duplicate_reference_number(body, styles):
    """Bibliography repeats [5] with different text after [167]."""
    last = find(body, lambda k: txt(k).startswith("[167]"))[0]
    last.addnext(mkpara("[5]\tStale duplicate entry.", "Bibliografi"))
    return styles


def unicode_dollar_text(body, styles):
    """Body text with literal dollar signs around a citation."""
    intro = h1(body, "Introduction")
    intro.addnext(mkpara("DOLLARTEST costs of 5 $/kW [3] and 10 $/kW."))
    return styles


VARIANTS = {f.__name__: f for f in [
    remove_figure_2, add_raster_figure_49, new_chapter, long_chapter, reference_168,
    references_renamed, references_missing, no_appendix, two_appendices,
    caption_not_in_pdf, heading_style_builtin, heading_style_other, citation_forms,
    body_text_starts_with_figure, xref_broken_fixable, xref_broken_unfixable,
    stale_seq_figure, duplicate_reference_number, unicode_dollar_text,
]}


def make_variant(src: Path, dst: Path, name: str) -> Path:
    fn = VARIANTS[name]
    with zipfile.ZipFile(src) as zi:
        doc = etree.fromstring(zi.read("word/document.xml"))
        styles = zi.read("word/styles.xml").decode("utf8")
        styles = fn(doc.find(W + "body"), styles)
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zo:
            for it in zi.infolist():
                if it.filename == "word/document.xml":
                    zo.writestr(it, etree.tostring(doc, xml_declaration=True,
                                                   encoding="UTF-8", standalone=True))
                elif it.filename == "word/styles.xml":
                    zo.writestr(it, styles.encode("utf8"))
                else:
                    zo.writestr(it, zi.read(it.filename))
    return dst
