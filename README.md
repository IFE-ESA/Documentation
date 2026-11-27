# IFE-TIMES-Norway documentation: Read the Docs ⇄ Word

The report *Documentation of IFE-TIMES-Norway* is kept as MyST Markdown in `docs/source/`
and published with Sphinx and the Read the Docs theme. That Markdown is the master copy:
edit it, review the change in git, and export the IFE-formatted Word report (and PDF) from
it for review and publishing. References live in Zotero.

```
docs/source/*.md ──sphinx──► website (Read the Docs)
        │
        └──tools/rtd2docx.py──► report.docx (IFE template) ──Word──► report.pdf
Zotero group ──tools/zotero_refs.py sync──► docs/source/_bib/*.json
```

v5 was converted once from Word (`tools/docx2rtd.py`); that converter is kept for the record
and for comparisons, but it overwrites `docs/source/`, so it is no longer part of the normal
workflow.

## Layout

| Path | What it is |
|---|---|
| `docs/source/*.md` | the report, one page per chapter (chapters 4 and 5 one per section) |
| `docs/source/_bib/` | Zotero data: `library.json` (CSL-JSON), `formatted.json` (Zotero's IEEE formatting), `zotero.json` (settings), `ieee.csl` (fallback) |
| `docs/source/_ext/ifereport.py` | Sphinx extension: citations, reference lists, merged table cells, appendix numbering (copy of `tools/ifereport.py`) |
| `docs/source/conf.py` | Sphinx settings (numbering of figures/tables, Zotero bibliography) |
| `tools/rtd2docx.py` | Markdown → Word (+ PDF with Microsoft Word on macOS) |
| `tools/templates/ife-reference.docx` | Word template: the report's styles, numbering, headers/footers, no content |
| `tools/zotero_refs.py` | sync references from Zotero; check citation keys |
| `tools/qa_roundtrip.py`, `tools/compare_sites.py` | QA: rebuilt report vs original; two site builds vs each other |
| `.claude/agents/report-roundtrip-qa.md` | QA agent for Claude Code: rebuilds, compares, looks at the pages, writes findings |
| `mirror/` | second site with the charts redrawn in one style (not published) |
| `tools/docx2rtd.py`, `tools/tidy_myst.py`, `tools/make_reference_docx.py` | one-off Word → Markdown conversion and template extraction |
| `tests/` | pytest suite |

## Writing in the Markdown

```markdown
(sec-hydrogen)=
# Hydrogen

Hydrogen is produced as shown in {numref}`fig-schematic-hydrogen-system-ife-times`
and {numref}`tab-investment-costs-opex-electrolysers` {cite}`danebergsTechnoeconomicStudyHydrogen2020`.

:::{figure} images/figure-18.png
:name: fig-schematic-hydrogen-system-ife-times

Schematic of the hydrogen system in IFE-TIMES-Norway.
:::

:::{list-table} Investment costs and OPEX for the different electrolysers
:name: tab-investment-costs-opex-electrolysers
:header-rows: 1
:column-align: left center center

* - {rowspan}`2` 20 MW{sub}`el`
  - PEM
  - 17 366
* - Alkaline
  - 11658
:::
```

- **Numbers are automatic.** Captions have no number; Sphinx numbers figures and tables
  through the whole report (Appendix A: "Table A-1"…), and `{numref}` writes "Figure 18",
  "Table 37" or a section number such as "4.1.2".
- **Citations** use the Zotero (Better BibTeX) citation key: `{cite}`key``, or
  `{cite}`key, p. 130`` with a page. References are numbered in order of first citation,
  as in Word. `{nocite}`key`` numbers a reference at that point without showing it.
  Each page gets its "References cited on this page" list automatically, and the
  References page holds `:::{bibliography}` — do not type reference lists by hand.
- **Tables**: one bullet per row, one sub-bullet per cell. `{rowspan}`N`` / `{colspan}`N``
  at the start of a cell merges cells (later rows leave the covered cells out).
  A cell that starts with `-`, `+` or `1.` needs a backslash (`\-`).
- Also: `*italic*`, `**bold**`, `{sub}`2``, `{sup}`3``, `{u}`underlined``, `$math$`,
  footnotes `[^1]` … `[^1]: text`.

Preview: `.venv/bin/sphinx-build -W -b html docs/source docs/build/html` and open
`docs/build/html/index.html`.

## References (Zotero)

Zotero must be running with Better BibTeX. After adding or editing items in the group:

```sh
.venv/bin/python tools/zotero_refs.py sync    # refresh docs/source/_bib/
.venv/bin/python tools/zotero_refs.py check   # cited keys that are not in Zotero
```

Commit the changed `_bib/*.json` files: Read the Docs builds from them, not from Zotero.
The formatting is Zotero's own IEEE style (locale en-GB), the same engine as the Zotero
Word plugin. Without Better BibTeX's formatter, `sync --formatter pandoc` uses pandoc and
`_bib/ieee.csl` (small differences).

## Word / PDF for review and publishing

```sh
.venv/bin/python tools/rtd2docx.py --source docs/source --out build/report.docx --pdf
```

Needs pandoc ≥ 3 (`brew install pandoc`); `--pdf` needs Microsoft Word on macOS (the first
run asks to allow Terminal to control Word). The Word file uses the IFE styles from
`tools/templates/ife-reference.docx` (headings with numbering, captions with SEQ fields,
Bibliography style, IFE table style, logo header and page numbers) and has a table of
contents that Word updates on opening. Cover page, report-information block and signature
footer are not generated yet.

Check a rebuild against the original (numbers, text, tables, references, side-by-side pages):

```sh
.venv/bin/python tools/qa_roundtrip.py --orig-docx "<original>.docx" --orig-pdf "<original>.pdf" \
    --new-docx build/report.docx --new-pdf build/report.pdf --out build/qa
```

or, in Claude Code, ask the `report-roundtrip-qa` agent to review the export.

## Setup

```sh
python3 -m venv .venv
.venv/bin/pip install -r docs/requirements.txt pymupdf lxml pillow pytest beautifulsoup4
.venv/bin/python -m pytest tests -q      # end-to-end tests skip without the v5 .docx/.pdf
```

The v5 `.docx`/`.pdf` are not in git; put them in the project root to run the conversion,
the QA comparison and the full tests.
