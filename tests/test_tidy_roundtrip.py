"""Tests for the hand-editable Markdown and the reverse workflow.

* tools/tidy_myst.py   – HTML-flavoured Markdown -> clean MyST
* tools/ifereport.py   – Sphinx extension: {cite}, page reference lists, merged table
                         cells, appendix numbering
* tools/make_reference_docx.py, tools/rtd2docx.py – Markdown -> IFE Word report
* tools/compare_sites.py, tools/qa_roundtrip.py   – the checks used to prove the above

Run:  .venv/bin/python -m pytest tests -q
End-to-end tests skip without the real report, pandoc, or (for the PDF) Microsoft Word.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import tidy_myst as t  # noqa: E402

DOCX = ROOT / "Documentation of IFE-TIMES-Norway v5.docx"
PDF = ROOT / "Documentation of IFE-TIMES-Norway v5.pdf"
PY = sys.executable
TEMPLATE = ROOT / "tools" / "templates" / "ife-reference.docx"
HAVE_PANDOC = bool(shutil.which("pandoc"))
HAVE_INPUTS = DOCX.exists() and PDF.exists() and HAVE_PANDOC
needs_inputs = pytest.mark.skipif(not HAVE_INPUTS, reason="real report or pandoc not available")
needs_pandoc = pytest.mark.skipif(not HAVE_PANDOC, reason="pandoc not available")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def ctx_with(labels=None):
    c = t.Ctx(log=lambda m: None)
    for old, (label, kind, num) in (labels or {}).items():
        c.id_label[old] = label
        c.label_kind[label] = (kind, num)
        c.by_number.setdefault((kind, num), []).append(label)
    return c


# ---------------------------------------------------------------- tidy: inline
@pytest.mark.parametrize("html,md", [
    (r'\[<a class="cite" href="#ref-79">79</a>\]', "{cite}`79`"),
    (r'\[<a class="cite" href="#ref-3">3</a>, <a class="cite" href="#ref-5">5</a>\]', "{cite}`3, 5`"),
    (r'\[<a class="cite" href="#ref-3">3</a>–<a class="cite" href="#ref-5">5</a>\]', "{cite}`3–5`"),
    (r'\[<a class="cite" href="#ref-53">53</a>, p. 130\]', "{cite}`53, p. 130`"),
    (r"\[Online\]", "[Online]"),
])
def test_tidy_citations_and_brackets(html, md):
    assert t.inline_md(html, ctx_with(), "p") == md


def test_tidy_crossrefs_numref_and_fallbacks():
    c = ctx_with({"_Ref1": ("fig-hydrogen", "figure", "18"), "_Ref2": ("tab-costs", "table", "37"),
                  "sec-x": ("sec-x", "section", None)})
    s = ('<a class="internal" href="#_Ref1">Figure 18</a>, '
         '<a class="internal" href="04-04-hydrogen.html#_Ref2"><em>Table 37</em></a>, '
         '<a class="internal" href="#sec-x">4.1.2</a>, '
         '<a class="internal" href="#_Ref2">the table</a>, '
         '<a class="internal" href="#_RefGone">Table 37</a>')
    out = t.inline_md(s, c, "p")
    assert out == ("{numref}`fig-hydrogen`, {numref}`tab-costs`, {numref}`sec-x`, "
                   "{ref}`the table <tab-costs>`, {numref}`tab-costs`")
    assert c.stats["xref_fixed_by_number"] == 1 and c.stats["italic_xref_text_dropped"] == 1


@pytest.mark.parametrize("html,md", [
    ("an <em>italic</em> word", "an *italic* word"),
    ("<strong>2018</strong>", "**2018**"),
    ("<em><strong>Bio-coal</strong></em>", "***Bio-coal***"),
    (r"<em>\*Adjusted afterward</em>", r"*\*Adjusted afterward*"),
    ("x<em>.</em>y", "x<em>.</em>y"),  # punctuation inside a word: * would not work
    ("H<sub>2</sub>O and m<sup>3</sup>", "H{sub}`2`O and m{sup}`3`"),
    ("<u>The ITEM project</u>", "{u}`The ITEM project`"),
    ("<u>[site](http://x.org)</u>", "[site](http://x.org)"),  # underlined links are just links
    ('<a class="reference external" href="https://a.org/x">https://a.org/x</a>', "<https://a.org/x>"),
    ('<a class="reference external" href="https://a.org/%C3%B8">https://a.org/%C3%B8</a>',
     "[https://a.org/%C3%B8](https://a.org/%C3%B8)"),
    ('<span class="math notranslate nohighlight">\\(x_{1}\\)</span>', "$x_{1}$"),
    ("a &amp; b &lt; 5", "a & b < 5"),
])
def test_tidy_inline_markup(html, md):
    assert t.inline_md(html, ctx_with(), "p") == md


@pytest.mark.parametrize("line,expected", [
    ("-", "\\-"), ("+ increased", "\\+ increased"), ("1. first", "1\\. first"), ("-2.1", "-2.1"),
    ("# x", "\\# x"), ("text", "text"),
])
def test_tidy_cells_do_not_turn_into_lists(line, expected):
    assert t._escape_block_start(line) == expected


def test_tidy_table_with_merged_cells_and_caption():
    html = ('<table><colgroup><col style="width: 30%" /><col style="width: 70%" /></colgroup>'
            '<thead><tr><th style="text-align: center;">A</th><th style="text-align: center;">B</th></tr></thead>'
            '<tbody><tr><td rowspan="2" style="text-align: center;">NO1</td><td>x<br />y</td></tr>'
            '<tr><td>-</td></tr><tr><td colspan="2">all</td></tr></tbody></table>')
    c = ctx_with()
    c._pending_label = "tab-demo"
    md = t.table_md(html, "Demo caption", c, "p")
    assert md.splitlines()[:6] == [
        ":::{list-table} Demo caption", ":name: tab-demo", ":header-rows: 1", ":widths: 30 70",
        ":column-align: center left", ":header-align: center"]
    assert "* - {rowspan}`2` NO1\n  - x\\\n    y\n* - \\-\n* - {colspan}`2` all\n:::" in md


def test_tidy_page_figure_caption_and_labels():
    md = ('<span id="sec-h"></span>\n\n# Hydrogen\n\nSee <a class="internal" href="#_Ref9">Figure 18</a>.\n\n'
          ':::{figure} images/figure-18.png\n:alt: Figure 18: Schematic\n:align: center\n\n'
          '<span id="_Ref9"></span><em>Figure 18: Schematic of the system.</em>\n:::\n')
    c = t.Ctx(log=lambda m: None)
    t.collect({"p": md}, c)
    out = t.tidy_page(md, "p", c)
    assert out.startswith("(sec-h)=\n# Hydrogen\n\nSee {numref}`fig-schematic-system`.")
    assert ":::{figure} images/figure-18.png\n:name: fig-schematic-system\n\nSchematic of the system.\n:::" in out
    assert c.stats["figure_caption_separator_normalised"] == 1
    assert "<" not in out


# ---------------------------------------------------------------- the Sphinx extension
EXT_INDEX = """# Test report

```{toctree}
:numbered: 2

one
references
```

```{toctree}
:caption: Appendix

appendix-a
```
"""
EXT_ONE = """(sec-one)=
# One

Text {cite}`2` and {cite}`1`–{cite}`3`, see {numref}`tab-a` and {numref}`sec-one`.[^1]

:::{list-table} Merged cells
:name: tab-a
:header-rows: 1
:column-align: center left

* - {colspan}`2` Head
* - {rowspan}`2` NO1
  - a
* - b
:::

[^1]: A note.
"""
EXT_REFS = """# References

[1] First reference.

[2] Second reference.

[3] Third reference.
"""
EXT_APP = """# Appendix A – Data

:::{list-table} Appendix table
:name: tab-app

* - x
:::

See {numref}`tab-app`.
"""


@pytest.fixture(scope="module")
def ext_site(tmp_path_factory):
    src = tmp_path_factory.mktemp("ext") / "source"
    (src / "_ext").mkdir(parents=True)
    shutil.copy(ROOT / "tools" / "ifereport.py", src / "_ext" / "ifereport.py")
    conf = ('import os, sys\nsys.path.insert(0, os.path.abspath("_ext"))\n'
            'extensions = ["myst_parser", "ifereport"]\nmyst_enable_extensions = ["colon_fence"]\n'
            'numfig = True\nnumfig_secnum_depth = 0\n'
            'numfig_format = {"figure": "Figure %s", "table": "Table %s", "code-block": "Listing %s", "section": "%s"}\n'
            'ifereport_appendix_prefixes = {"appendix-a": "A"}\n')
    (src / "conf.py").write_text(conf)
    for name, text in (("index", EXT_INDEX), ("one", EXT_ONE), ("references", EXT_REFS), ("appendix-a", EXT_APP)):
        (src / f"{name}.md").write_text(text)
    return src


def _build(src, out, *extra, builder="html"):
    res = subprocess.run([PY, "-m", "sphinx", "-W", "-q", "-b", builder, *extra, str(src), str(out)],
                         capture_output=True, text=True)
    assert res.returncode == 0, res.stderr[-2000:]
    return out


def test_ext_html(ext_site, tmp_path):
    out = _build(ext_site, tmp_path / "html")
    one = (out / "one.html").read_text()
    assert re.search(r'<td class="text-center" colspan="2"><p>Head</p></td>|'
                     r'<th class="head" colspan="2"><p>Head</p></th>', one)
    assert re.search(r'<td class="text-center" rowspan="2"><p>NO1</p></td>', one)
    assert '<span class="caption-number">Table 1 </span>' in one
    assert re.search(r'see <a class="reference internal" href="#tab-a"><span class="std std-numref">Table 1</span></a>', one)
    assert '<span class="std std-numref">1</span>' in one  # section number
    # citations and the generated page list, with 2 (range 1–3) included
    assert re.search(r'\[<a class="cite reference internal" href="#ref-2">2</a>\]', one)
    assert "References cited on this page" in one
    for n in (1, 2, 3):
        assert f'id="ref-{n}"' in one
    refs = (out / "references.html").read_text()
    assert 'class="ref-entry" id="ref-1"' in refs and "References cited on this page" not in refs
    app = (out / "appendix-a.html").read_text()
    assert '<span class="caption-number">Table A-1 </span>' in app
    assert '<span class="std std-numref">Table A-1</span>' in app


def test_ext_docx_tag_leaves_out_page_lists(ext_site, tmp_path):
    out = _build(ext_site, tmp_path / "single", "-t", "docx", builder="singlehtml")
    html = (out / "index.html").read_text()
    assert "References cited on this page" not in html
    assert html.count('id="ref-1"') == 1 and 'href="#ref-2"' in html


def test_ext_bad_spans_are_errors(tmp_path, ext_site):
    src = tmp_path / "src"
    shutil.copytree(ext_site, src)
    (src / "one.md").write_text(EXT_ONE.replace("* - b\n", ""))  # row 3 missing: rowspan reaches past the end
    res = subprocess.run([PY, "-m", "sphinx", "-W", "-q", "-b", "html", str(src), str(tmp_path / "o")],
                         capture_output=True, text=True)
    assert res.returncode != 0 and "rowspan" in res.stderr


# ---------------------------------------------------------------- end to end on the real report
@pytest.fixture(scope="module")
def tidy_and_raw(tmp_path_factory):
    if not HAVE_INPUTS:
        pytest.skip("real report or pandoc not available")
    base = tmp_path_factory.mktemp("tidy")
    outs = {}
    for name, extra in (("tidy", []), ("raw", ["--raw-html"])):
        out = base / name
        res = subprocess.run([PY, str(ROOT / "tools" / "docx2rtd.py"), "--docx", str(DOCX), "--pdf", str(PDF),
                              "--out", str(out), "--rtd-root", str(out), *extra],
                             capture_output=True, text=True)
        assert res.returncode == 0, res.stderr[-2000:]
        _build(out / "source", out / "html")
        outs[name] = out
    return outs


@needs_inputs
def test_e2e_tidy_markdown_has_no_html(tidy_and_raw):
    src = tidy_and_raw["tidy"] / "source"
    for p in src.glob("*.md"):
        text = re.sub(r"<https?://[^>\s]+>", "", p.read_text())
        assert not re.search(r"</?(span|div|table|td|tr|a|em|strong|sub|sup|br|section|p)\b", text), p.name
    rep = json.loads((tidy_and_raw["tidy"] / "conversion_report.json").read_text())["tidy"]["stats"]
    assert rep["tables"] == 93 and rep["figures"] == 48 and rep["tables_with_merged_cells"] == 42
    assert rep.get("html_em_kept", 0) == 0 and rep.get("html_strong_kept", 0) == 0
    assert (src / "_ext" / "ifereport.py").exists()
    assert "numfig = True" in (src / "conf.py").read_text()


@needs_inputs
def test_e2e_tidy_renders_the_same_text(tidy_and_raw):
    sys.path.insert(0, str(ROOT / "tools"))
    import compare_sites
    rep = compare_sites.compare(tidy_and_raw["raw"] / "html", tidy_and_raw["tidy"] / "html")
    assert rep["numbering_differences"] == 0
    for name, pr in rep["pages"].items():
        assert pr["tables_equal"], name
        # only the caption separators ("Figure 9: " -> "Figure 9 ") and footnote placement change
        removed = [d for d in pr["word_diff"] if d.startswith("-") and d not in ("-:", "-.")]
        added = [d for d in pr["word_diff"] if d.startswith("+")]
        if "district-heating" in name or "energy-carriers" in name:  # footnotes move to the page end
            assert sorted(x[1:] for x in removed if x != "-↩︎") == sorted(x[1:] for x in added if x[1:] not in ("[", "]")) or \
                len(removed) <= len(added) + 3, name
        else:
            assert not removed and not added, (name, pr["word_diff"][:20])


@needs_pandoc
@pytest.mark.skipif(not DOCX.exists(), reason="real report not available")
def test_reference_template_is_small_and_has_ife_styles(tmp_path):
    import make_reference_docx as m
    out = tmp_path / "ref.docx"
    m.make(DOCX, out)
    assert out.stat().st_size < 300_000
    with zipfile.ZipFile(out) as z:
        names = z.namelist()
        doc = z.read("word/document.xml").decode()
        styles = z.read("word/styles.xml").decode()
    assert not any(n.startswith("word/media/") and n.endswith(".emf") for n in names)
    assert not any(n.startswith("customXml/") for n in names)
    assert len(re.findall(r"<w:p[ >/]", doc)) <= 2 and "<w:sectPr" in doc and 'w:type="default"' in doc
    assert 'w:val="IFE Heading 1"' in styles


@pytest.fixture(scope="module")
def rebuilt(tidy_and_raw, tmp_path_factory):
    out = tmp_path_factory.mktemp("word") / "report.docx"
    res = subprocess.run([PY, str(ROOT / "tools" / "rtd2docx.py"), "--source",
                          str(tidy_and_raw["tidy"] / "source"), "--out", str(out),
                          "--report", str(out.with_suffix(".json"))], capture_output=True, text=True)
    assert res.returncode == 0, res.stderr[-2000:]
    return out


@needs_inputs
def test_e2e_rtd2docx_contents(rebuilt):
    rep = json.loads(rebuilt.with_suffix(".json").read_text())
    assert rep["figures"] == 48 and rep["tables"] == 93 and rep["references"] == 167
    assert rep["footnotes"] == 2 and rep["equations"] == 15
    assert rep["docx"]["seq_fields"] == 131 and rep["docx"]["unnumbered"] == 5 and rep["docx"]["toc"] == 1
    with zipfile.ZipFile(rebuilt) as z:
        doc = z.read("word/document.xml").decode()
        fn = z.read("word/footnotes.xml").decode()
    assert "\u27e6" not in doc  # no placeholder left
    assert doc.count("<m:oMath>") >= 12
    assert len(re.findall(r'<w:footnoteReference w:id="\d+"', doc)) == 2 and "EMPIRE" in fn
    assert 'w:val="IFEHeading1"' in doc and 'w:val="Bibliografi"' in doc


@needs_inputs
def test_e2e_roundtrip_matches_original_structure(rebuilt, tmp_path):
    import qa_roundtrip as q
    args = type("A", (), {"orig_docx": str(DOCX), "orig_pdf": None, "new_docx": str(rebuilt),
                          "new_pdf": None, "out": str(tmp_path / "qa"), "samples": 0})()
    rep = q.run(args)
    # headings: identical apart from the unnumbered front pages and the appendix title
    for d in rep["headings"]["differences"]:
        assert d["op"] == "insert" and all(x.startswith("1||") or x.startswith("2||") for x in d["new"]), d
    assert rep["references"]["new"] == rep["references"]["orig_unique"] == 167
    assert rep["references"]["text"]["ratio"] > 0.999
    assert rep["text_docx"]["ratio"] > 0.99
    assert rep["objects"]["new"]["footnotes"] == 2


# ---------------------------------------------------------------- Zotero mode (citation keys)
ZOT_ONE = """# One

First {cite}`smith2020`, then {cite}`2026`{nocite}`jones2019` and {cite}`smith2020, p. 4`.
"""
ZOT_TWO = """# Two

Again {cite}`jones2019` and {cite}`brown2021`.
"""
ZOT_ENTRIES = {"smith2020": "A. Smith, ‘Title one’, <i>Journal</i>, 2020. Available: https://a.org/x",
               "2026": "Statnett, ‘All-digit key’, 2026.",
               "jones2019": "B. Jones, ‘Listed, not cited’, 2019.",
               "brown2021": "C. Brown, ‘Title three’, 2021."}


@pytest.fixture(scope="module")
def zot_site(tmp_path_factory):
    src = tmp_path_factory.mktemp("zot") / "source"
    (src / "_ext").mkdir(parents=True)
    (src / "_bib").mkdir()
    shutil.copy(ROOT / "tools" / "ifereport.py", src / "_ext" / "ifereport.py")
    (src / "_bib" / "formatted.json").write_text(json.dumps({"entries": ZOT_ENTRIES}, ensure_ascii=False))
    (src / "conf.py").write_text('import os, sys\nsys.path.insert(0, os.path.abspath("_ext"))\n'
                                 'extensions = ["myst_parser", "ifereport"]\nmyst_enable_extensions = ["colon_fence"]\n'
                                 'ifereport_bibliography = "_bib/formatted.json"\n')
    (src / "index.md").write_text("# T\n\n```{toctree}\none\ntwo\nreferences\n```\n")
    (src / "one.md").write_text(ZOT_ONE)
    (src / "two.md").write_text(ZOT_TWO)
    (src / "references.md").write_text("# References\n\n:::{bibliography}\n:::\n")
    return src


def test_zotero_numbering_follows_first_citation(zot_site, tmp_path):
    out = _build(zot_site, tmp_path / "h")
    one, two, refs = ((out / f"{n}.html").read_text() for n in ("one", "two", "references"))
    assert re.search(r'First <span class="cite-group">\[<a class="cite reference internal" href="#ref-1">1</a>\]', one)
    assert 'href="#ref-2">2</a>]' in one  # the all-digit key "2026" is a key, not number 2026
    assert re.search(r'href="#ref-1">1</a>, p\. 4\]', one)
    # {nocite} numbers jones2019 as 3 but shows nothing and is not in the page list
    assert "jones2019" not in one and 'id="ref-3"' not in one
    assert 'href="#ref-3">3</a>]' in two and 'href="#ref-4">4</a>]' in two
    for n, title in ((1, "Title one"), (2, "All-digit key"), (3, "Listed, not cited"), (4, "Title three")):
        assert re.search(rf'id="ref-{n}">\[{n}\] [^<]*‘{title}’', refs), n
    assert "<em>Journal</em>" in refs and '<a class="reference external" href="https://a.org/x">' in refs


def test_zotero_unknown_key_warns(zot_site, tmp_path):
    src = tmp_path / "s"
    shutil.copytree(zot_site, src)
    (src / "two.md").write_text("# Two\n\n{cite}`nosuchKey2020`\n")
    res = subprocess.run([PY, "-m", "sphinx", "-W", "-q", "-b", "html", str(src), str(tmp_path / "o")],
                         capture_output=True, text=True)
    assert res.returncode != 0 and "nosuchKey2020" in res.stderr


def test_zotero_migrate_matching():
    import zotero_refs as z
    numbered = {1: "A. Smith, ‘Title one’, *Journal*, 2020. Available: <https://a.org/x>",
                2: "B. Jones, ‘Listed, not cited’, 2019."}
    m = z.match_references(numbered, ZOT_ENTRIES, {})
    assert m[1][0] == "smith2020" and m[1][1] == 1.0 and m[2][0] == "jones2019"
    m = z.match_references(numbered, ZOT_ENTRIES, {2: "brown2021"})
    assert m[2] == ("brown2021", 1.0, "assigned")
