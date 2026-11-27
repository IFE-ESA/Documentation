# QA findings: rebuilt IFE-TIMES-Norway v5 report (phase A)

Build: `tools/rtd2docx.py --source docs/source --out build/qa/report.docx --pdf` (Word PDF step succeeded, ~70 s).
Compared with `Documentation of IFE-TIMES-Norway v5.pdf` (authoritative) and `.docx` via `tools/qa_roundtrip.py`.
I also ran the full word diff (all chunks, not only the first 25/40) and wrote it to the scratchpad. Side-by-side page images are in `build/qa/pages/` (`x_*.png` are the extra pages I picked).

## Verdict

**The rebuilt Word file is fit for content review, with two caveats.** The body text, headings, captions, references, citations, footnotes and equations all match the original. The only content differences are the documented accepted ones. Two layout defects should be fixed before the file goes to reviewers:
1. In the Word-generated PDF, every page number in the table of contents is "1".
2. About 10 dense tables have columns so narrow that words and numbers break mid-token ("Hydroge|n", "20|%", "17.|0").

Everything else is cosmetic: the table look (first-column shading, widths), the equation layout (numbers inline, not right-aligned) and the spacing after tables.

## Key metrics (qa_report.md)

| Metric | Original | Rebuilt | Note |
|---|---|---|---|
| Body text similarity (PDF, p.5–116 vs 6–110) | 45 639 tokens | 44 741 | 0.9818; 1 582 changed tokens, all explained (see below) |
| Body text similarity (docx) | 36 039 words | 36 030 | 0.9965; 129 changed tokens, all accepted or stale original fields |
| Headings | 75 | 80 | the 75 original headings are identical (level, number, text); +5 unnumbered front/appendix headings |
| Captions (number + text) | 137 | 137 | identical |
| Tables | 92 | 93 | +1 = report-information block split into 2 tables; cell text similarity 0.981, all diffs are in that block |
| References | 167 | 167 | text similarity 1.0000, same order |
| Citations → reference | – | 383 links | all 383 point to the matching `[n]` entry |
| Figure/Table cross-refs | – | 143 links | all resolve to the right caption; 0 missing bookmarks (544 internal links) |
| Footnotes | 2 | 2 | OK |
| Equations (OMML) | 15 | 15 | Word equations, no LaTeX left |
| Sub/superscript runs | – | 86 / 74 | the same text as the original (only empty runs differ) |
| SEQ fields | 132 | 131 | 48 Figure + 83 Table; the 6 appendix captions "Table A-n" are plain text |
| Pages | 134 | 123 | −2 cover/report-info pages (phase B); chapter 5 is ~6 pages shorter (denser tables, no empty paragraphs after tables) |

## Findings (most severe first)

### F1 – major – TOC page numbers are all "1" in the PDF
- **Evidence:** `build/qa/report.pdf` p.4–5 (`build/qa/pages/contents.png`, `x_toc_end.png`). Every entry from "Summary" to "Appendix A" shows page 1. The original PDF p.5 has the correct numbers.
- **Cause (likely):** `tools/rtd2docx.py` APPLESCRIPT (~l.625–640) updates all fields, and then the TOC, right after `open` + `delay 1`. Word has not repaginated the 120-page document yet, so the PAGEREF results are 1.
- **Fix:**
  - Add `repaginate d` (or a longer wait) before `update table of contents`.
  - Or run the TOC update twice, the second time page numbers only (`update table of contents … ` with the page-numbers-only option).
  - Check: p.4 should show "1 Introduction … 6".
- **Note:** in the `.docx` itself the TOC is the placeholder "Right-click and choose Update Field…" until Word updates it. Word prompts for this because `updateFields` is set, which is fine for reviewers.

### F2 – major – narrow table columns break words and numbers mid-token
- **Evidence:** affected tables, with rebuilt PDF pages:
  - Table 14/15 "Capacit|y 2030" (p.25–26)
  - Table 28 "BIOGA|S", "BIOMAS|S", "ELECTRI|C" (p.38)
  - Table 34 "Efficienc|y", "Lifetim|e" (p.44)
  - **Table 49** (p.64, `build/qa/pages/x_ind_table.png`):
    - every "20%", "21%", "100%" in the narrow Bio-fuel/Bio-gas/Bio-mass columns wraps to "20 / %";
    - the headers wrap as "Bio-mas|s", "Hydroge|n", "Distric|t Heat";
    - this is the worst case and is hard to read.
  - Table 53/54 "Efficien|cy", "INVCOS|T", "year|s", "NOK/k|W" (p.75–76)
  - Table 56 "(TWh/yea|r)" and the Sum rows "17.|0 14.|2 / 16.|3 13.|5 / 36.|0 30.|0" (p.79–80, `x_table56b.png`)
  - Tables 66–68 "kWh/k|m" (p.89–91)
  - Table 79 "Residenti|al Commerci|al" (p.103)

  The original renders all of these on one line. These breaks cause the "replace" chunks (e.g. "ALUminium 20% → ALUminium %") in the PDF text diff. The cell text in the docx is correct (tables word diff: 0 changes outside the report-information block).
- **Cause:**
  - all 93 tables are forced to 100% width (`tblW pct 5000/4990…5010`), with grid widths from the `:widths:` of the list-table;
  - the IFE table style's cell margins and font size leave about 0.5 cm of text in a 6% column (e.g. Table 49 `:widths: 15 6 7 11 6 9 7 7 11 7 9`, `docs/source/05-01-industry.md:163`; gridCol 498 twips).
  - The original uses a smaller table font (8 pt / Arial in Table 56) and tighter margins.
- **Fix (any of):**
  - set the table cell margins and font size (8–9 pt) in the template table style;
  - let Word autofit to contents (`tblLayout autofit`) when the `:widths:` columns are below about 8%;
  - widen the narrow columns in the affected `:widths:` lines (e.g. Table 49: give the first column less width).

### F3 – minor – equations: number is inline instead of right-aligned; display layout lost
- **Evidence:**
  - Original p.33 / p.105: equations (1)–(6) are centred, with "(n)" at the right margin.
  - Rebuilt p.31 / p.100 (`x_eq1.png`, `x_eq6.png`): the equation is left-aligned with "(1)" right after it, and (1) and (2) are stacked with no spacing.
  - Eq. (3) "INVCOST…" wraps at p.31 because it is inline math.
- **Cause:** the Markdown has them as inline math followed by text, e.g. `docs/source/05-03-transport.md:1273` `$y_{WC} = …$ (5)`.
- **Fix:** in rtd2docx, turn a paragraph that is just `$…$ (n)` into a centred equation paragraph with a right tab stop and "(n)". This keeps the Markdown unchanged. Alternatively use `$$…$$` with a label in the Markdown.
- **Note (cosmetic):** Word maths shows `~` in `NCAP_AFC~DAYNITE` as `∼` (U+223C).

### F4 – minor – table styling differs from the original
- **Evidence:**
  - Every table uses `Bluegridadjusted2`. The original uses 9 styles; for example 19 tables use "Grid Table 5 Dark Accent 1", which has a dark-blue bold first column.
  - Examples: Tables 6, 11, 19, 31, 39, 44, 49, 70 (`Table_6.png`, `Table_11.png`, `Table_19.png`, `Table_32.png`, `Table_37.png`, `Table_70.png`). Their first-column labels are normal weight on light blue; in the original they are white bold on dark blue.
  - Narrow tables (e.g. Table 48 `:widths: 50`, Table 16, Table 19) are full width; the original has them at about 50–60% width, centred.
  - The original's bold header text in some cells and the indented sub-rows of Table 70 are approximated with empty cells.
- **Fix:**
  - apply first-column emphasis (`tblLook firstColumn=1`, plus a style with that conditional format) where the original had it, e.g. via a list-table `:class:`;
  - honour a total width when `:widths:` sums to less than 100.

### F5 – cosmetic – no spacing after tables
- **Evidence:**
  - Rebuilt p.49: the Table 37 caption follows directly after Table 36, and heading 4.4.2 directly after Table 38.
  - Rebuilt p.27: heading 4.1.4 sits directly under Table 16.
  - The original has an empty paragraph or space after every table.
- **Effect:** this is part of why the rebuilt report is 11 pages shorter.
- **Fix:** give the paragraph after a table `spacing before ≈ 12 pt`, or the table style a bottom spacing.

### F6 – cosmetic – front matter, TOC scope and page numbering
- **Page numbering:**
  - The rebuilt report numbers pages 1…123 continuously from the title page.
  - The original has roman numerals for the front matter ("i" on the Contents page), restarts at 1 at "1 Introduction", and restarts again in the appendix.
  - So the TOC numbers will not match the original even after F1 is fixed.
- **TOC scope:** the rebuilt TOC also lists Summary, Authors and report information (+2 sub-entries) and Appendix A; the original TOC starts at "1 Introduction" and does not list the appendix.
- **Title page:** the title is justified, which gives wide gaps ("Documentation   of   IFE-TIMES-Norway v5", p.1). Use left/centre alignment.
- **Authors table (p.3):** the labels wrap ("Prepared / by") because the first column is narrow.
- Most of this belongs to phase B.

### F7 – cosmetic – figure sizes and link styling
- **Figure sizes:** some figures are noticeably larger than in the original, e.g. Fig. 1 (p.7), Fig. 10 map (p.34) and Fig. 23 (p.61); Fig. 25 is slightly smaller.
- **Link styling:** the URLs in the reference list are blue and underlined hyperlinks; in the original they are plain text.
- **Cross-reference formatting:** in the original some figure/table references are italic, e.g. "(*Table 17*)" on p.28; the rebuilt cross-references are upright.

### Not a defect (checked)
- **Paragraph break before "Table 57" in 5.3.1** (`docs/source/05-03-transport.md:7–9`): the original PDF p.83 has the same break ("…briefly described in ¶ Table 57."). The rebuilt report reproduces it faithfully; it could be joined in the source if desired.
- **"Eva Rosenberg"** appears in the original .docx author list but not in the original PDF. The rebuilt report follows the PDF (correct).

## Accepted differences (confirmed)

1. **Caption separator dropped**
   - The 8 body captions are confirmed in the diffs: Figure 3, 9, 18, 24, 45 and Table 24 ("."), 48 and 77 (":").
   - The ninth is Table A-3 in the appendix, which is listed in `conversion_report.json`. The body diff ends at References, so it is not in these diffs.
2. **Charts are images**
   - About 25 PDF-diff chunks are only chart axis labels and legends in the original, and appear as "delete" in the diff.
   - Affected figures: Figs. 1, 3, 6–8, 9 (labels), 11, 13, 15/16, 17, 22, 23, 24, 25, 30, 31, 34, 38–40, 42, 43, 45, 46, 48, plus the Table 60/62/74/76 charts.
3. **Cover page, report-information block and signature footer** are not reproduced. The front pages are title, Summary, Authors and report information, and Contents (+4 headings, +1 table, −2 pages).
4. **"Table 28" → "Figure 11"** in 4.1.9:
   - in the docx diff, the original reads "Table 28";
   - in the PDF diff, the original reads "Error! Reference source not found.".
5. **Cross-references and citations are hyperlinks**, not REF fields. All 544 resolve; 383 citations and 143 caption references were checked against their targets.

The stale numbering in the original .docx is not a defect: the docx diff has about 100 chunks "Table 29…84 → 28…83", and the rebuilt numbers match the PDF.

## Measurement notes

- **Repeated header rows:** the rebuilt tables repeat their header rows on every page (101 `tblHeader` rows; the original has 0). Where a table breaks across pages, the PDF diff shows inserted header text, e.g. "Energy fee (øre/kWh)…", "Offshore area CF Capacity…", "Region Installed capacity…", "NO1…NO5", "2020 2025 2050", "Values", "Type Name in TIMES Description", "Type of locomotive…". This is an artefact of the comparison, and arguably an improvement.
- **Extraction order:**
  - Some chunks are only a different order from the PDF text extraction around merged cells or page breaks: Table 15 rows "Sørvest E/F, Sønnavind A", Table 3 footnote 1 position, and the Table 80 "2018" row.
  - "NOK/M Wh" is an extraction artefact in the original.
- **Body text diff range:** the PDF body diff stops at "References", so the appendix text was compared only by eye. Table A-1/A-2 match (`x_appendix1.png`), and the table word diff covers the appendix tables (no differences).
- **Images:** 49 in the docx (48 figures + the header logo).
- **Not checked:**
  - the docx opened directly in Word with updateFields (only the AppleScript path was exercised);
  - all 123 pages by eye: I reviewed 16 sampled pages plus 12 more;
  - the 18 section cross-references in detail (all targets exist).

## Notes for phase B

- **Cover page (p.1 of the original):**
  - IFE logo, boxed title, report number line, the full-page blue "Research for a better future" graphic;
  - put these in the template as a first section, with a different first page and fields/content controls for the title and report number.
- **Report-information block (original p.2):**
  - a single bordered table: Report number | ISSN | Availability | Publication date; Revision | ISBN | DOCUS-ID | Number of pages; Client; Title; Summary (the full Summary text sits inside the table); Prepared/Reviewed/Approved by, with signature images; Report distribution; and the IFE address block below it;
  - the metadata already lives in `docs/source/report-information.md`, and "Revision" and "Client" (empty in v5) need fields;
  - Number of pages should be a NUMPAGES/section-pages field;
  - this replaces the rebuilt "Summary" and "Authors and report information" pages.
- **Signature footer:** "Document ID … / Signed TASS, NON, MLA" with a seal on every page. It is added by the signing system, so it probably should not be generated at all; at most leave room in the footer.
- **Sections and numbering:**
  - front matter in roman numerals (the Contents page is "i");
  - the body restarts at 1 at "1 Introduction";
  - the appendix restarts at 1 in its own section (the original has 5 sections; the rebuilt report has 1);
  - the TOC should exclude the front-matter headings and the appendix, as the original does;
  - fix F1 first.
- **Template (tied to the per-table styles in F4):** carry the original's table style variants (dark first column, "Grid Table 5 Dark Accent 1/2") into the template.
