"""Tests for tools/docx2rtd.py.

Run:  .venv/bin/python -m pytest tests -q
The end-to-end tests convert the real report (about 15 s per conversion plus a
Sphinx build) and skip when the .docx/.pdf or pandoc are not available. All
output goes to pytest's tmp dirs; docs/ is never written.
Tests marked xfail document known defects; drop the marker once fixed.
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
sys.path.insert(0, str(ROOT / "tests"))

import docx2rtd as d  # noqa: E402
from docx_variants import make_variant  # noqa: E402

DOCX = ROOT / "Documentation of IFE-TIMES-Norway v5.docx"
PDF = ROOT / "Documentation of IFE-TIMES-Norway v5.pdf"
SCRIPT = ROOT / "tools" / "docx2rtd.py"
PY = sys.executable
SPHINX = str(Path(sys.executable).with_name("sphinx-build"))

HAVE_INPUTS = DOCX.exists() and PDF.exists() and bool(shutil.which("pandoc"))
needs_inputs = pytest.mark.skipif(not HAVE_INPUTS, reason="real report or pandoc not available")

VALID = set(range(1, 168))


# ---------------------------------------------------------------- helpers
def convert(docx: Path, out: Path, pdf: Path = PDF, extra=(), rtd_root: Path | None = None,
            tidy: bool = False):
    """Run the converter. These tests check the converter's own output, so they use
    --raw-html (the HTML-flavoured Markdown before tools/tidy_myst.py); the tidy step and
    the hand-editable format are tested in test_tidy_roundtrip.py."""
    return subprocess.run(
        [PY, str(SCRIPT), "--docx", str(docx), "--pdf", str(pdf), "--out", str(out),
         "--rtd-root", str(rtd_root or out), *(() if tidy else ("--raw-html",)), *extra],
        capture_output=True, text=True)


def report(out: Path) -> dict:
    return json.loads((out / "conversion_report.json").read_text())


def warnings_of(out: Path) -> list[str]:
    return [w for w in report(out)["warnings"] if w.startswith("WARNING")]


def sphinx(out: Path):
    return subprocess.run([SPHINX, "-W", "-q", "-b", "html", str(out / "source"), str(out / "build")],
                          capture_output=True, text=True)


def variant(tmp_path_factory, name, extra=()):
    d_ = tmp_path_factory.mktemp(name)
    dx = make_variant(DOCX, d_ / "in.docx", name)
    res = convert(dx, d_ / "out", extra=extra)
    return res, d_ / "out"


def allmd(out: Path) -> str:
    return "".join(p.read_text() for p in sorted((out / "source").glob("*.md")))


# ---------------------------------------------------------------- citations
@pytest.mark.parametrize("text,cited", [
    ("[3]", [3]),
    (r"\[3\]", [3]),
    ("[3, 5]", [3, 5]),
    ("[3,4,7]", [3, 4, 7]),
    ("[3–5]", [3, 4, 5]),
    ("[3-5]", [3, 4, 5]),
    ("[3 – 5]", [3, 4, 5]),
    ("[3—5]", [3, 4, 5]),
    ("[3−5]", [3, 4, 5]),
    ("[3]-[5]", [3, 4, 5]),
    ("[3]–[5]", [3, 4, 5]),
    ("([3])", [3]),
    (r"\[100\], \[101\]", [100, 101]),
])
def test_citation_forms_linked(text, cited):
    md, got = d.link_citations(text, VALID)
    assert got == cited
    for n in {cited[0], cited[-1]}:
        assert f'href="#ref-{n}"' in md
    assert re.sub(r"<[^>]+>", "", md) == text  # text itself unchanged


@pytest.mark.parametrize("text,n", [("[53, p. 130]", 53), ("[3, pp. 4–5]", 3)])
def test_citation_with_page_locator(text, n):
    md, got = d.link_citations(text, VALID)
    assert got == [n]
    assert md.count('class="cite"') == 1 and re.sub(r"<[^>]+>", "", md) == text


@pytest.mark.parametrize("text", [
    "[kNOK/MW]", "[2020]", "[0]", "[1–200]", "[168]", "[12](http://example.org)",
    "x[3]", "[^3]", "[ 3 ]", "[60]%", "$x = [3]$", "$$a[3]$$",
    r'<span class="math notranslate nohighlight">\([3]\)</span>',
])
def test_citation_non_matches_left_alone(text):
    md, got = d.link_citations(text, VALID)
    assert got == [] and md == text


def test_citation_after_display_math():
    _, got = d.link_citations("$$a[3]$$ then [4]", VALID)
    assert got == [4]


def test_citation_skips_directive_options_and_fences():
    md = ":::{figure} images/figure-01.png\n:alt: Figure 1 [3]\n:align: center\n<img alt='[3]'>\n```\n[3]\n```"
    out, cited = d.link_citations(md, VALID)
    assert cited == [] and out == md


def test_citation_between_escaped_dollars():
    _, got = d.link_citations(r"cost 5 \$/kW [3] and 10 \$/kW", VALID)
    assert got == [3]


def test_page_reference_list_sorted_and_anchored():
    bib = {1: r"\[1\] A", 2: r"\[2\] B", 10: r"\[10\] C"}
    out = d.page_reference_list([10, 1], bib)
    assert out.index('id="ref-1"') < out.index('id="ref-10"')
    assert 'id="ref-2"' not in out
    assert 'references.html#ref-10' in out


# ---------------------------------------------------------------- small helpers
def test_slugify():
    assert d.slugify("Final remarks") == "final-remarks"
    assert d.slugify("CCS and DACCS") == "ccs-and-daccs"
    assert d.slugify("Green ammonia and e-fuels") == "green-ammonia-and-e-fuels"
    assert len(d.slugify("x" * 80)) <= 50


def test_alt_strips_markup():
    assert d._alt(r"Figure 1 *A* <a href='#'>[3]</a> \_x") == "Figure 1 A [3] x"


def test_requirements_pinned():
    reqs = d.REQUIREMENTS.split()
    assert all("==" in r for r in reqs)
    assert {"sphinx==7.4.7", "sphinx-rtd-theme==3.1.0", "myst-parser==3.0.1"} <= set(reqs)


@needs_inputs
def test_preprocess_renames_styles_and_drops_hidden(tmp_path):
    dst = tmp_path / "p.docx"
    msgs = d.preprocess_docx(DOCX, dst, "IFE Heading")
    z = zipfile.ZipFile(dst)
    styles = z.read("word/styles.xml").decode()
    assert 'w:name w:val="IFE Heading 1"' not in styles
    assert 'w:name w:val="heading 1"' in styles
    assert "Appendix A start" in msgs  # white marker paragraph dropped
    assert "Appendix A start" not in z.read("word/document.xml").decode()
    fields = [m for m in msgs if m.startswith("@field ")]
    assert any("'SEQ Table': '29' -> '28'" in m for m in fields)


def test_update_fields_renumbers_seq_and_ref():
    w = d.NS["w"]
    xml = f"""<w:document xmlns:w="{w}"><w:body>
      <w:p><w:bookmarkStart w:id="1" w:name="_RefA"/><w:r><w:t>Table </w:t></w:r>
        <w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText> SEQ Table \\* ARABIC </w:instrText></w:r>
        <w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>7</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r>
        <w:bookmarkEnd w:id="1"/><w:r><w:t> Costs</w:t></w:r></w:p>
      <w:p><w:r><w:t>See </w:t></w:r><w:r><w:fldChar w:fldCharType="begin"/></w:r>
        <w:r><w:instrText> REF _RefA \\h </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r>
        <w:r><w:t>Table 7</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>
    </w:body></w:document>"""
    from lxml import etree
    root = etree.fromstring(xml)
    msgs = d.update_fields(root)
    text = "|".join("".join(t.text or "" for t in p.iter(d.W + "t")) for p in root.iter(d.W + "p"))
    assert text == "Table 1 Costs|See Table 1"
    assert len(msgs) == 2


# ---------------------------------------------------------------- figure classification
@needs_inputs
def test_scan_docx_figures_classification():
    figs = d.scan_docx_figures(DOCX)
    assert sorted(figs) == list(range(1, 49))
    kinds = {n: f.kind for n, f in figs.items()}
    assert sum(k == "raster" for k in kinds.values()) == 16
    assert kinds[2] == "raster" and figs[2].media.endswith((".png", ".jpg", ".jpeg"))
    assert kinds[6] == "crop" and "chart" in figs[6].reasons       # native Word chart
    assert kinds[3] == "crop" and any(r.endswith(".emf") for r in figs[3].reasons)
    assert kinds[9] == "crop" and "wordprocessingShape" in figs[9].reasons
    assert kinds[11] == "crop"  # chart + png overlay -> must not be taken as raster


# ---------------------------------------------------------------- CLI errors
def _cli(*args):
    return subprocess.run([PY, str(SCRIPT), *args], capture_output=True, text=True)


def test_cli_missing_input_exit2_and_keeps_output(tmp_path):
    out = tmp_path / "out"
    (out / "source").mkdir(parents=True)
    (out / "source" / "keep.md").write_text("x")
    res = _cli("--docx", str(tmp_path / "missing.docx"), "--pdf", str(tmp_path / "x.pdf"),
               "--out", str(out), "--rtd-root", str(tmp_path))
    assert res.returncode == 2
    assert "error:" in res.stderr and "--docx file not found" in res.stderr
    assert "Traceback" not in res.stderr
    assert (out / "source" / "keep.md").exists()


@needs_inputs
def test_cli_out_outside_rtd_root(tmp_path):
    res = _cli("--docx", str(DOCX), "--pdf", str(PDF), "--out", str(tmp_path / "a" / "out"),
               "--rtd-root", str(tmp_path / "b"))
    assert res.returncode == 2 and "must be inside --rtd-root" in res.stderr
    assert not (tmp_path / "a").exists()


# ---------------------------------------------------------------- end-to-end on the real document
@pytest.fixture(scope="module")
def real_run(tmp_path_factory):
    if not HAVE_INPUTS:
        pytest.skip("real report or pandoc not available")
    out = tmp_path_factory.mktemp("real") / "out"
    res = convert(DOCX, out)
    assert res.returncode == 0, res.stderr
    return out


EXPECTED_PAGES = [
    "01-introduction", "02-model-structure", "03-energy-carriers-and-emissions",
    "04-conversion-processes-and-transmission", "04-01-electricity", "04-02-district-heating",
    "04-03-bioenergy", "04-04-hydrogen", "04-05-green-ammonia-and-e-fuels", "04-06-ccs-and-daccs",
    "05-end-use-demand", "05-01-industry", "05-02-buildings", "05-03-transport",
    "06-final-remarks", "references", "appendix-a",
]
TOP_PAGES = [p for p in EXPECTED_PAGES if not re.match(r"\d\d-\d\d-", p)]
FRONT_PAGES = ["summary", "report-information"]


def test_e2e_report_counts(real_run):
    r = report(real_run)
    assert r["references"] == 167
    assert r["pages"] == EXPECTED_PAGES
    figs = r["figures"]
    assert len(figs) == 48 and all(f["file"] for f in figs.values())
    assert sum(f["method"] == "pdf-crop" for f in figs.values()) == 32
    for f in figs.values():
        assert (real_run / "source" / "images" / f["file"]).stat().st_size > 1000
    clip11 = figs["11"]["pdf_page_clip"]
    assert set(clip11) >= {"page", "clip", "extra"} and clip11["extra"] == ["figure-11-part1.png"]
    assert (real_run / "source" / "images" / "figure-11-part1.png").exists()
    assert {"field_updates", "front_matter", "pdf_text_differences"} <= set(r)


def test_e2e_warnings(real_run):
    w = warnings_of(real_run)
    assert any("repeats 79 numbers ([87]..[165])" in x for x in w)
    # the broken REF _Ref89622146 ("Table 28" in 4.1.9) is corrected to Figure 11 from its context
    fixed = [x for x in w if "_Ref89622146" in x]
    assert len(fixed) == 1 and "corrected from its context" in fixed[0] and "Figure 11" in fixed[0]
    # ... which makes that paragraph differ from the PDF (which shows Word's error text)
    assert any("1 paragraph(s) differ between the docx and the PDF" in x for x in w)
    assert len(w) == 3, w
    notes = report(real_run)["warnings"]
    assert any("dropped invisible paragraph" in x and "Appendix A start" in x for x in notes)


def test_e2e_broken_xref_relinked(real_run):
    md = (real_run / "source" / "04-01-electricity.md").read_text()
    assert "Error! Reference source not found." not in allmd(real_run)
    for target in re.findall(r'<a class="internal" href="#([^"]+)">Figure 11</a>', md):
        assert f'id="{target}"' in md
    assert len(report(real_run)["pdf_text_differences"]) == 1  # the intentional correction


def test_e2e_field_updates_tables_renumbered(real_run):
    fu = report(real_run)["field_updates"]
    seq = [x for x in fu if x.startswith("field 'SEQ Table'")]
    assert seq[0] == "field 'SEQ Table': '29' -> '28'"
    assert seq[-1] == "field 'SEQ Table': '84' -> '83'"
    assert "Table 84" not in allmd(real_run)


def test_e2e_files_and_config(real_run):
    src = real_run / "source"
    for p in EXPECTED_PAGES + FRONT_PAGES + ["index"]:
        assert (src / f"{p}.md").exists(), p
    conf = (src / "conf.py").read_text()
    assert "smartquotes = False" in conf and "linkify" not in conf
    assert (src / "_static" / "custom.css").exists()
    y = (real_run / ".readthedocs.yaml").read_text()
    assert "configuration: source/conf.py" in y and "requirements: requirements.txt" in y
    assert "sphinx==7.4.7" in (real_run / "requirements.txt").read_text()


def test_e2e_index(real_run):
    idx = (real_run / "source" / "index.md").read_text()
    assert idx.startswith("# Documentation of IFE-TIMES-Norway v5")
    assert f":numbered: {d.TOC_DEPTH}" in idx and d.TOC_DEPTH == 4
    about = idx.index(":caption: About this report")
    contents = idx.index(":caption: Contents")
    assert about < contents
    assert all(idx.index(p) > about and idx.index(p) < contents for p in FRONT_PAGES)
    assert all(p in idx for p in TOP_PAGES)
    assert "_Toc" not in idx and "<img" not in idx  # Word TOC and cover images dropped


def test_e2e_front_pages(real_run):
    info = (real_run / "source" / "report-information.md").read_text()
    assert "IFE/E-2026/007" in info and "978-82-7017-963-3" in info  # PDF values win
    assert "IFE/E-2024/004xx" not in info
    assert (real_run / "source" / "summary.md").read_text().startswith("# Summary")


def test_e2e_references_page(real_run):
    md = (real_run / "source" / "references.md").read_text()
    ids = re.findall(r'<span id="ref-(\d+)"></span>', md)
    assert [int(i) for i in ids] == list(range(1, 168))
    assert '<a class="reference external" href="http' in md  # URLs linked by link_urls


def test_e2e_citations_and_page_lists(real_run):
    md = (real_run / "source" / "04-01-electricity.md").read_text()
    assert md.count('class="cite"') > 50
    cited = {int(n) for n in re.findall(r'class="cite" href="#ref-(\d+)"', md)}
    listed = {int(n) for n in re.findall(r'<span id="ref-(\d+)"></span>', md)}
    assert cited <= listed
    body = md.split("References cited on this page")[0]
    assert not re.search(r"\\\[\d{1,3}\\\]", body)  # no unlinked numeric citations


def test_e2e_markup(real_run):
    text = allmd(real_run)
    assert len(re.findall(r"^:::\{figure\} images/figure-\d\d\.\w+$", text, re.M)) == 48
    assert "@@FIGURE" not in text and "@@LINK" not in text and "@@IMAGE" not in text
    assert not re.search(r"^\|", text, re.M)  # no pipe tables
    assert not re.search(r"^:alt:.*<", text, re.M)  # no HTML in alt text
    assert "Appendix A start" not in text
    assert 'id="sec-introduction"' in text
    assert not re.search(r'<span id="(?!sec-|ref-|_|fn)', text)  # every id is namespaced or a Word bookmark


def test_e2e_footnotes_numbered_site_wide(real_run):
    src = real_run / "source"
    nums = []
    for p in sorted(src.glob("*.md")):
        t = p.read_text()
        nums += [int(n) for n in re.findall(r"\[\^(\d+)\]:", t)]
        nums += [int(n) for n in re.findall(r'class="footnote-ref"[^>]*><sup>(\d+)</sup>', t)]
    assert nums and len(nums) == len(set(nums))


def test_e2e_sphinx_build_strict(real_run):
    res = sphinx(real_run)
    assert res.returncode == 0, res.stderr[-2000:]
    for p in EXPECTED_PAGES + FRONT_PAGES + ["index"]:
        assert (real_run / "build" / f"{p}.html").exists()


def test_e2e_deterministic(real_run, tmp_path):
    out2 = tmp_path / "out"
    assert convert(DOCX, out2).returncode == 0
    a = sorted(p.relative_to(real_run / "source") for p in (real_run / "source").rglob("*") if p.is_file())
    b = sorted(p.relative_to(out2 / "source") for p in (out2 / "source").rglob("*") if p.is_file())
    assert a == b
    for rel in a:
        assert (real_run / "source" / rel).read_bytes() == (out2 / "source" / rel).read_bytes(), rel


def test_e2e_strict_flag_fails_on_warnings(real_run, tmp_path):
    res = convert(DOCX, tmp_path / "out", extra=["--strict"])
    assert res.returncode == 2 and "--strict" in res.stderr


# ---------------------------------------------------------------- future-version variants
@needs_inputs
def test_variant_new_chapter(tmp_path_factory):
    res, out = variant(tmp_path_factory, "new_chapter")
    assert res.returncode == 0, res.stderr
    pages = report(out)["pages"]
    assert "06-scenarios" in pages and "07-final-remarks" in pages
    md = (out / "source" / "06-scenarios.md").read_text()
    assert 'href="#ref-9"' in md and '<span id="ref-8">' in md  # range 7-9 expanded in page list


@needs_inputs
def test_variant_long_chapter_is_split(tmp_path_factory):
    res, out = variant(tmp_path_factory, "long_chapter")
    assert res.returncode == 0, res.stderr
    pages = report(out)["pages"]
    assert {"06-final-remarks", "06-01-first-new-section", "06-02-second-new-section"} <= set(pages)
    parent = (out / "source" / "06-final-remarks.md").read_text()
    assert "06-01-first-new-section" in parent and "{toctree}" in parent
    assert sphinx(out).returncode == 0


@needs_inputs
def test_variant_reference_168(tmp_path_factory):
    res, out = variant(tmp_path_factory, "reference_168")
    assert res.returncode == 0, res.stderr
    assert report(out)["references"] == 168
    assert 'href="#ref-168"' in (out / "source" / "01-introduction.md").read_text()


@needs_inputs
def test_variant_duplicate_reference_number(tmp_path_factory):
    res, out = variant(tmp_path_factory, "duplicate_reference_number")
    assert res.returncode == 0, res.stderr
    assert report(out)["references"] == 167
    assert "Stale duplicate entry" not in (out / "source" / "references.md").read_text()
    assert any("repeats 80 numbers" in w for w in warnings_of(out))


@needs_inputs
def test_variant_added_figure_with_stale_seq(tmp_path_factory):
    res, out = variant(tmp_path_factory, "add_raster_figure_49")
    assert res.returncode == 0, res.stderr
    f = report(out)["figures"].get("49")
    assert f and f["method"] == "docx-media" and f["file"] == "figure-49.png"


@needs_inputs
def test_variant_stale_seq_number(tmp_path_factory):
    res, out = variant(tmp_path_factory, "stale_seq_figure")
    assert res.returncode == 0, res.stderr
    figs = report(out)["figures"]
    assert sorted(map(int, figs)) == list(range(1, 49))
    assert all(f["file"] for f in figs.values())


@needs_inputs
def test_variant_caption_not_in_pdf_degrades(tmp_path_factory):
    res, out = variant(tmp_path_factory, "caption_not_in_pdf")
    assert res.returncode == 0, res.stderr
    r = report(out)
    assert r["figures"]["1"]["file"] is None
    assert any("Figure 1" in w and "not found in PDF" in w for w in r["warnings"])
    assert any("have no image: [1]" in w for w in r["warnings"])
    assert sphinx(out).returncode == 0


@needs_inputs
def test_variant_references_renamed_bibliography(tmp_path_factory):
    res, out = variant(tmp_path_factory, "references_renamed")
    assert res.returncode == 0, res.stderr
    assert report(out)["references"] == 167
    assert re.search(r"^# Bibliography", (out / "source" / "references.md").read_text(), re.M)


@needs_inputs
def test_variant_references_missing_clear_error(tmp_path_factory):
    res, out = variant(tmp_path_factory, "references_missing")
    assert res.returncode == 2
    assert "error:" in res.stderr and "--references-title" in res.stderr
    assert "Traceback" not in res.stderr and not (out / "source").exists()


@needs_inputs
def test_variant_heading_style_other(tmp_path_factory):
    res, _ = variant(tmp_path_factory, "heading_style_other")
    assert res.returncode == 2 and "--heading-style" in res.stderr and "Traceback" not in res.stderr
    res, out = variant(tmp_path_factory, "heading_style_other", extra=["--heading-style", "IFE Overskrift"])
    assert res.returncode == 0, res.stderr
    assert report(out)["pages"] == EXPECTED_PAGES


@needs_inputs
def test_variant_heading_style_builtin(tmp_path_factory):
    res, out = variant(tmp_path_factory, "heading_style_builtin")
    assert res.returncode == 0, res.stderr
    assert report(out)["pages"] == EXPECTED_PAGES


@needs_inputs
def test_variant_no_appendix(tmp_path_factory):
    res, out = variant(tmp_path_factory, "no_appendix")
    assert res.returncode == 0, res.stderr
    assert report(out)["pages"] == EXPECTED_PAGES[:-1]
    assert ":caption: Appendix" not in (out / "source" / "index.md").read_text()


@needs_inputs
def test_variant_two_appendices(tmp_path_factory):
    res, out = variant(tmp_path_factory, "two_appendices")
    assert res.returncode == 0, res.stderr
    pages = report(out)["pages"]
    assert pages[-2:] == ["appendix-a", "appendix-b"]
    b = (out / "source" / "appendix-b.md").read_text()
    assert re.search(r"^# Appendix B – Additional data", b, re.M) and 'href="#ref-12"' in b
    assert "Appendix B" not in (out / "source" / "appendix-a.md").read_text()
    assert sphinx(out).returncode == 0


@needs_inputs
def test_variant_body_text_starting_with_figure(tmp_path_factory):
    res, out = variant(tmp_path_factory, "body_text_starts_with_figure")
    assert res.returncode == 0, res.stderr
    figs = report(out)["figures"]
    assert figs["5"]["caption"].startswith("Figure 5 Illustration") and figs["5"]["file"]
    assert all(f["file"] for f in figs.values())


@needs_inputs
def test_variant_citation_forms(tmp_path_factory):
    res, out = variant(tmp_path_factory, "citation_forms")
    assert res.returncode == 0, res.stderr
    lines = {re.sub(r"<[^>]+>", "", l).split(" ", 2)[1]: l
             for l in (out / "source" / "01-introduction.md").read_text().splitlines()
             if l.startswith("CITETEST")}
    for k in ("Comma", "Range", "Hyphen", "Separate", "List"):
        assert 'class="cite"' in lines[k], k
    for k in ("Unit", "Percent", "Year", "Zero", "Out"):
        assert 'class="cite"' not in lines[k], k


@needs_inputs
def test_variant_xref_broken_fixed_from_context(tmp_path_factory):
    res, out = variant(tmp_path_factory, "xref_broken_fixable")
    assert res.returncode == 0, res.stderr
    md = (out / "source" / "01-introduction.md").read_text()
    m = re.search(r'presented in <a class="internal" href="#([^"]+)">Figure 1</a>', md)
    assert m and f'id="{m.group(1)}"' in md  # relinked to a target on the same page
    assert "Error! Reference" not in md
    assert any("corrected from its context" in w and "_Ref99999991" in w for w in warnings_of(out))
    assert not any("_Ref99999991" in w and "not found" in w for w in warnings_of(out))


@needs_inputs
def test_variant_xref_broken_without_match(tmp_path_factory):
    res, out = variant(tmp_path_factory, "xref_broken_unfixable")
    assert res.returncode == 0, res.stderr
    md = (out / "source" / "01-introduction.md").read_text()
    assert "Error! Reference source not found." in md
    assert '#_Ref99999992' not in md
    w = [x for x in warnings_of(out) if "_Ref99999992" in x]
    assert w and not any("corrected" in x for x in w)
    assert sphinx(out).returncode == 0
