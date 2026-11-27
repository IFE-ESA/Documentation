#!/usr/bin/env python3
"""Rewrite the converter's HTML-heavy Markdown into MyST that people can edit by hand.

docx2rtd.py writes its pages through pandoc, which leaves raw HTML for tables, links,
citations and bookmarks. This pass (run by docx2rtd.py at the end, or on its own on a
site's source folder) turns that into plain MyST:

* tables        -> ``:::{list-table}`` with ``{rowspan}``/``{colspan}`` for merged cells
* captions      -> figure/table captions without the number; Sphinx numbers them
* bookmarks     -> named labels (``fig-…``, ``tab-…``, ``sec-…``)
* cross-refs    -> ``{numref}`label``` ("Figure 18", "Table 37", "4.1.2")
* citations     -> ``{cite}`79, 80```; the per-page reference lists are generated
* references    -> one paragraph per reference starting with ``[N]``
* inline HTML   -> ``*em*``, ``**strong**``, ``{sub}``, ``{sup}``, ``{u}``, ``$math$``

The text itself is unchanged. Usage: ``python tools/tidy_myst.py docs/source``.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

from lxml import etree
from lxml import html as lhtml

DASHES = "–—−-"
STOP = {"the", "of", "and", "in", "for", "a", "an", "to", "by", "per", "with", "on", "from", "at", "as",
        "is", "are", "its", "or", "excl", "incl", "based", "different"}


class Ctx:
    def __init__(self, log=print):
        self.log = log
        self.id_label: dict[str, str] = {}      # old html id -> label
        self.label_kind: dict[str, tuple] = {}  # label -> ("figure"|"table"|"section", number str|None)
        self.used: set = set()
        self.by_number: dict[tuple, list] = {}  # ("table", "57") -> labels made in pass 1
        self.stats: Counter = Counter()
        self.notes: list[str] = []

    def new_label(self, prefix: str, text: str) -> str:
        words = [w for w in re.findall(r"[a-z0-9]+", _ascii(text).lower()) if w not in STOP]
        base = f"{prefix}-" + "-".join(words[:5]) if words else prefix
        label, k = base, 2
        while label in self.used:
            label, k = f"{base}-{k}", k + 1
        self.used.add(label)
        return label

    def note(self, msg):
        self.notes.append(msg)
        self.log("NOTE: " + msg)


def _ascii(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def _plain(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("\\[", "[").replace("\\]", "]")
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


SPAN_ID = re.compile(r'<span id="([^"]+)"></span>')
FIG_BLOCK = re.compile(r":::\{figure\} (\S+)\n(?::alt: [^\n]*\n)?(?::align: [^\n]*\n)?\n(.*?)\n:::\n", re.S)
_DIV_BODY = r"((?:(?!</?div).)*?)"
TABLE_BLOCK = re.compile(
    r'(?:<div class="table-caption">\s*' + _DIV_BODY + r'\s*</div>\s*)?'
    r'<div class="wy-table-responsive">(<table(?:(?!</table>).)*</table>)</div>', re.S)
CAPTION_DIV = re.compile(r'<div class="table-caption">\s*' + _DIV_BODY + r'\s*</div>', re.S)
# body text that the converter boxed as a caption because it starts with "Table N"
# (the number is a cross-reference link there, never in a real caption)
XREF_START = re.compile(r'^\s*<a class="internal"')
FIG_NUM = re.compile(r"^\s*Figure\s+(\d+)\s*([:.])?\s*")
TAB_NUM = re.compile(r"^\s*Table\s+((?:[A-Z]-)?\d+)\s*([:.])?\s*")
PAGE_REFS = re.compile(r"```\{rubric\} References cited on this page\n```\s*<div class=\"page-refs\">.*?</div>\s*$", re.S)


# --------------------------------------------------------------------------- pass 1
def collect(pages: dict[str, str], ctx: Ctx):
    for slug, md in pages.items():
        for m in FIG_BLOCK.finditer(md):
            cap = m.group(2)
            ids = SPAN_ID.findall(cap)
            text = _plain(cap)
            n = FIG_NUM.match(text)
            if not n:
                continue
            label = ctx.new_label("fig", text[n.end():])
            ctx.label_kind[label] = ("figure", n.group(1))
            ctx.by_number.setdefault(("figure", n.group(1)), []).append(label)
            for i in ids:
                ctx.id_label[i] = label
        for m in re.finditer(r'((?:<span id="[^"]+"></span>\s*)*)' + CAPTION_DIV.pattern, md, re.S):
            cap = m.group(2)
            if XREF_START.match(cap):
                continue
            ids = SPAN_ID.findall(m.group(1)) + SPAN_ID.findall(cap)
            text = _plain(cap)
            n = TAB_NUM.match(text)
            if not n:
                continue
            label = ctx.new_label("tab", text[n.end():])
            ctx.label_kind[label] = ("table", n.group(1))
            ctx.by_number.setdefault(("table", n.group(1)), []).append(label)
            for i in ids:
                ctx.id_label[i] = label
        # bookmarks in front of headings
        for m in re.finditer(r"((?:<span id=\"[^\"]+\"></span>\s*)+)(#+ .*)", md):
            ids = SPAN_ID.findall(m.group(1))
            sec = [i for i in ids if i.startswith("sec-")]
            label = sec[0] if sec else ctx.new_label("sec", m.group(2).lstrip("# "))
            ctx.used.add(label)
            ctx.label_kind[label] = ("section", None)
            for i in ids:
                ctx.id_label[i] = label


# --------------------------------------------------------------------------- inline
MATH_SPAN = re.compile(r'<span class="math notranslate nohighlight">\\([(\[])(.*?)\\([)\]])</span>', re.S)
MATH_MD = re.compile(r"(\$\$.*?\$\$|(?<!\\)\$[^$\n]+?(?<!\\)\$)", re.S)
CITE_HTML = re.compile(r'\\?\[((?:<a class="cite" href="#ref-\d+">\d+</a>|[^\[\]<\\\n])+?)\\?\]')
INTERNAL = re.compile(r'<a class="internal" href="(?:([\w.-]+)\.html)?#([^"]+)">(.*?)</a>', re.S)
EXTERNAL = re.compile(r'<a class="reference external" href="([^"]+)">(.*?)</a>', re.S)
FN_REF = re.compile(r'<a href="#fn\d+" class="footnote-ref"[^>]*><sup>(\d+)</sup></a>')
PUNCT = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~") | set("‘’“”–—…")


def _safe_wrap(marker, inner, before, after):
    if not inner.strip() or inner != inner.strip() or re.search(r"(?<!\\)\*", inner) or "\n" in inner:
        return None
    if before in ("*", "\\", ">", "`") or after in ("*", "<", "`"):
        return None
    if inner[0] in PUNCT and before and (before.isalnum()):
        return None
    if inner[-1] in PUNCT and after and (after.isalnum()):
        return None
    return f"{marker}{inner}{marker}"


def _sub_tags(s, tag, marker, ctx):
    pat = re.compile(rf"<{tag}>((?:(?!<{tag}>).)*?)</{tag}>", re.S)
    while True:
        out, last, changed = [], 0, False
        for m in pat.finditer(s):
            inner = m.group(1)
            before = s[m.start() - 1] if m.start() else ""
            after = s[m.end()] if m.end() < len(s) else ""
            w = _safe_wrap(marker, inner, before, after) if "<" not in inner else None
            out.append(s[last:m.start()])
            if w is None:
                out.append(m.group(0).replace(f"<{tag}>", f"\x00{tag}\x01").replace(f"</{tag}>", f"\x00/{tag}\x01"))
                ctx.stats[f"html_{tag}_kept"] += 1
            else:
                out.append(w)
                changed = True
            last = m.end()
        out.append(s[last:])
        s = "".join(out)
        if not changed:
            break
    return s.replace("\x00", "<").replace("\x01", ">")


def _role(name, text):
    text = text.replace("`", "")
    return f"{{{name}}}`{text}`"


def inline_md(s: str, ctx: Ctx, page: str, br="\\\n") -> str:
    protected: list[str] = []

    def protect(x):
        protected.append(x)
        return f"\x02{len(protected) - 1}\x03"

    s = FN_REF.sub(lambda m: f"[^{m.group(1)}]", s)

    def math_span(m):
        tex = html.unescape(m.group(2)).strip()
        return protect(f"$${tex}$$" if m.group(1) == "[" else f"${tex}$")

    s = MATH_SPAN.sub(math_span, s)
    s = MATH_MD.sub(lambda m: protect(m.group(0)), s)

    def cite(m):
        if 'class="cite"' not in m.group(1):
            return m.group(0)
        body = re.sub(r'<a class="cite" href="#ref-\d+">(\d+)</a>', r"\1", m.group(1))
        ctx.stats["citations"] += 1
        return protect(_role("cite", html.unescape(body)))

    s = CITE_HTML.sub(cite, s)

    def internal(m):
        target, text = m.group(2), m.group(3)
        plain = _plain(text)
        if "<em>" in text:
            ctx.stats["italic_xref_text_dropped"] += 1
        label = ctx.id_label.get(target)
        if label is None:
            m2 = re.fullmatch(r"(Figure|Table) ((?:[A-Z]-)?\d+)", plain)
            same = [l for l, (k, n) in ctx.label_kind.items()
                    if m2 and k == m2.group(1).lower() and n == m2.group(2)]
            if len(same) == 1:
                ctx.note(f"{page}: link to missing bookmark #{target} ({plain!r}) pointed at the "
                         f"caption with that number ({same[0]})")
                ctx.stats["xref_fixed_by_number"] += 1
                return protect(f"{{numref}}`{same[0]}`")
            ctx.note(f"{page}: link to unknown target #{target} kept as text {plain!r}")
            return text
        kind, num = ctx.label_kind[label]
        expect = {"figure": f"Figure {num}", "table": f"Table {num}"}.get(kind)
        if (expect and plain == expect) or (kind == "section" and re.fullmatch(r"\d+(\.\d+)*", plain)):
            ctx.stats["numref"] += 1
            return protect(f"{{numref}}`{label}`")
        ctx.stats["ref_explicit"] += 1
        return protect(f"{{ref}}`{plain} <{label}>`")

    s = INTERNAL.sub(internal, s)

    def external(m):
        url, text = html.unescape(m.group(1)), m.group(2)
        if _plain(text) == url:
            # <url> would show percent-escapes decoded (%C3%B8 as ø); keep the text as written
            return protect(f"[{url}]({url})" if "%" in url else f"<{url}>")
        return protect(f"[{inline_md(text, ctx, page)}]({url})")

    s = EXTERNAL.sub(external, s)

    def span_id(m):
        i = m.group(1)
        if i.startswith("ref-"):
            return ""
        ctx.stats["inline_bookmark_dropped"] += 1
        return ""

    s = SPAN_ID.sub(span_id, s)
    for tag in ("sub", "sup"):
        s = re.sub(rf"<{tag}>([^<`]*)</{tag}>", lambda m, t=tag: protect(_role(t, html.unescape(m.group(1)))), s)
    # underlined links are just links (they are underlined on the page anyway)
    s = re.sub(r"<u>([^<`]*)</u>", lambda m: m.group(1) if ("\x02" in m.group(1) or "](" in m.group(1))
               else protect(_role("u", html.unescape(m.group(1)))), s)
    s = re.sub(r"(?:<br\s*/?>\s*)+$", "", s)  # a line break at the very end shows nothing
    s = re.sub(r"<br\s*/?>\n?", lambda m: protect(br), s)
    s = re.sub(r"<em><strong>([^<*]+)</strong></em>|<strong><em>([^<*]+)</em></strong>",
               lambda m: f"\x04{m.group(1) or m.group(2)}\x05", s)
    s = _sub_tags(s, "em", "*", ctx)
    s = _sub_tags(s, "strong", "**", ctx)
    s = re.sub(r"\x04(.*?)\x05", lambda m: _safe_wrap("***", m.group(1), "", "") or
               f"<em><strong>{m.group(1)}</strong></em>", s)
    # pandoc's escaping of brackets is not needed unless the bracket could start a link
    s = re.sub(r"\\\[", "[", s)
    s = re.sub(r"\\\](?![(\[:])", "]", s)
    s = s.replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", "\u00a0")
    s = re.sub(r"&lt;(?![A-Za-z/!?])", "<", s)
    s = re.sub(r"&gt;", ">", s)
    while "\x02" in s:
        s = re.sub(r"\x02(\d+)\x03", lambda m: protected[int(m.group(1))], s)
    return s


# --------------------------------------------------------------------------- tables
def _inner_html(el) -> str:
    return (html.escape(el.text or "", quote=False)
            + "".join(etree.tostring(c, encoding="unicode", method="html") for c in el))


def _cell_md(cell, ctx, page) -> list[str]:
    """Cell content as a list of Markdown paragraphs."""
    for bq in cell.findall(".//blockquote"):
        bq.drop_tag()
    paras = []
    ps = [c for c in cell if c.tag == "p"]
    if ps and all(c.tag == "p" for c in cell) and not (cell.text or "").strip():
        for p in ps:
            paras.append(_inner_html(p))
    else:
        paras.append(_inner_html(cell))
    out = []
    for p in paras:
        md = inline_md(p.strip(), ctx, page, br="\\\n")
        md = re.sub(r"[ \t]*\n[ \t]*", "\n", md).strip()
        # text that Markdown would read as a list, heading or quote ("-", "+ 5", "1. x")
        md = "\n".join(_escape_block_start(l) for l in md.split("\n"))
        if md:
            out.append(md)
    return out


def _escape_block_start(line: str) -> str:
    if re.match(r"^([-+*])(\s|$)", line) or re.match(r"^[#>]", line):
        return "\\" + line
    m = re.match(r"^(\d{1,9})([.)])(\s|$)", line)
    if m:
        return m.group(1) + "\\" + line[len(m.group(1)):]
    return line


def _align(cell):
    m = re.search(r"text-align:\s*(left|center|right)", cell.get("style", ""))
    return m.group(1) if m else "left"


def table_md(table_html: str, caption: str | None, ctx: Ctx, page: str) -> str:
    t = lhtml.fragment_fromstring(table_html)
    widths = [int(round(float(re.search(r"([\d.]+)%", c.get("style", "")).group(1))))
              for c in t.findall(".//col") if re.search(r"([\d.]+)%", c.get("style", ""))]
    head = [tr for sec in t.findall("thead") for tr in sec.findall("tr")]
    body = [tr for sec in t.findall("tbody") for tr in sec.findall("tr")] + t.findall("tr")
    if head and not body:  # layout tables (equation + number): no header row
        body, head = head, []
    rows = head + body
    header_rows = len(head)
    # grid positions, for per-column alignment
    occupied: set = set()
    cells = []
    for r, tr in enumerate(rows):
        c = 0
        rc = []
        for cell in tr:
            if cell.tag not in ("td", "th"):
                continue
            while (r, c) in occupied:
                c += 1
            rs, cs = int(cell.get("rowspan", 1)), int(cell.get("colspan", 1))
            for i in range(rs):
                for j in range(cs):
                    occupied.add((r + i, c + j))
            rc.append((c, rs, cs, cell))
            c += cs
        cells.append(rc)
    ncols = max((c for _, c in occupied), default=-1) + 1
    stub = 1 if body and all(rc and rc[0][3].tag == "th" and all(x[3].tag == "td" for x in rc[1:])
                             for rc in cells[header_rows:]) else 0
    col_votes = [Counter() for _ in range(ncols)]
    head_votes = Counter()
    for r, rc in enumerate(cells):
        for c, rs, cs, cell in rc:
            (head_votes if r < header_rows else col_votes[c]).update([_align(cell)])
    col_align = [v.most_common(1)[0][0] if v else "left" for v in col_votes]
    head_align = head_votes.most_common(1)[0][0] if head_votes else "left"
    deviating = 0
    for r, rc in enumerate(cells):
        for c, rs, cs, cell in rc:
            want = head_align if r < header_rows else col_align[c]
            if _align(cell) != want and _plain(_inner_html(cell)):
                deviating += 1
    if deviating:
        ctx.stats["cell_alignment_normalised"] += deviating

    lines = [":::{list-table}" + (f" {caption}" if caption else "")]
    if caption:
        lines.append(f":name: {ctx._pending_label}")
    if header_rows:
        lines.append(f":header-rows: {header_rows}")
    if stub:
        lines.append(":stub-columns: 1")
    if widths and len(widths) == ncols and all(w > 0 for w in widths):
        lines.append(":widths: " + " ".join(map(str, widths)))
    if any(a != "left" for a in col_align):
        lines.append(":column-align: " + " ".join(col_align))
    if header_rows and head_align != "left":
        lines.append(f":header-align: {head_align}")
    cls = [c for c in (t.get("class") or "").split() if c not in ("docutils", "align-default")]
    if cls:
        lines.append(":class: " + " ".join(cls))
    lines.append("")
    for rc in cells:
        for k, (c, rs, cs, cell) in enumerate(rc):
            paras = _cell_md(cell, ctx, page)
            prefix = ""
            if rs > 1:
                prefix += f"{{rowspan}}`{rs}` "
            if cs > 1:
                prefix += f"{{colspan}}`{cs}` "
            first = (prefix + paras[0]) if paras else prefix.rstrip()
            bullet = "* - " if k == 0 else "  - "
            cell_lines = [first] + sum(([""] + p.split("\n") for p in paras[1:]), [])
            cell_lines = sum((l.split("\n") for l in cell_lines), [])
            lines.append((bullet + cell_lines[0]).rstrip())
            for l in cell_lines[1:]:
                lines.append(("    " + l).rstrip())
        if not rc:
            ctx.note(f"{page}: empty table row dropped")
    lines.append(":::")
    ctx.stats["tables"] += 1
    if any(rs > 1 or cs > 1 for rc in cells for _, rs, cs, _ in rc):
        ctx.stats["tables_with_merged_cells"] += 1
    return "\n".join(lines)


def caption_md(cap_html: str, kind: str, ctx: Ctx, page: str):
    """Return (label, caption markdown without the number)."""
    ids = SPAN_ID.findall(cap_html)
    cap = SPAN_ID.sub("", cap_html)
    cap = re.sub(r"</?em>", "", cap).strip()  # the caption style is italic anyway
    cap = re.sub(r"\\\n|<br\s*/?>", " ", cap)  # captions are one line
    num_re = FIG_NUM if kind == "figure" else TAB_NUM
    m = num_re.match(cap)
    if not m:
        return None, inline_md(cap, ctx, page)
    if m.group(2):
        ctx.stats[f"{kind}_caption_separator_normalised"] += 1
        ctx.note(f"{page}: {kind.title()} {m.group(1)} caption separator '{m.group(2)}' dropped "
                 f"(Sphinx writes '{kind.title()} N ' for every caption)")
    label = next((ctx.id_label[i] for i in ids if i in ctx.id_label), None)
    same = ctx.by_number.get((kind, m.group(1)), [])
    if label is None and len(same) == 1:
        label = same[0]
    if label is None:
        label = ctx.new_label("fig" if kind == "figure" else "tab", _plain(cap[m.end():]))
        ctx.label_kind[label] = (kind, m.group(1))
    text = inline_md(cap[m.end():].strip(), ctx, page, br=" ")  # captions are one line
    return label, re.sub(r"\s*\n\s*", " ", text)


# --------------------------------------------------------------------------- page
def tidy_page(md: str, slug: str, ctx: Ctx, refs_slug="references") -> str:
    md = PAGE_REFS.sub("", md).rstrip() + "\n"
    if slug == refs_slug:
        md = md.replace('<div class="references-list">\n\n', "").replace("\n</div>\n", "\n")
        md = re.sub(r'<span id="ref-(\d+)"></span>\\\[<a class="cite" href="#ref-\d+">\d+</a>\\\]',
                    r"[\1]", md)
    # footnotes that pandoc had to write as HTML (inside tables)
    fn_defs = []

    def fn_section(m):
        start = int(re.search(r'<ol start="(\d+)"', m.group(0)).group(1)) if "start=" in m.group(0) else 1
        for k, li in enumerate(re.findall(r"<li id=\"fn\d+\">(.*?)</li>", m.group(0), re.S)):
            li = re.sub(r'<a href="#fnref\d+" class="footnote-back"[^>]*>.*?</a>', "", li)
            li = re.sub(r"^\s*<p>|</p>\s*$", "", li.strip())
            fn_defs.append((start + k, li))
        return ""

    md = re.sub(r'<section id="footnotes".*?</section>', fn_section, md, flags=re.S)

    # tables (with their captions)
    def table(m):
        cap_html, tbl = m.group(1), m.group(2)
        caption = None
        ctx._pending_label = None
        if cap_html and XREF_START.match(cap_html):
            ctx.stats["body_text_unboxed"] += 1
            return cap_html + "\n\n" + table_md(tbl, None, ctx, slug)
        if cap_html:
            label, caption = caption_md(cap_html, "table", ctx, slug)
            if label is None:
                ctx.note(f"{slug}: table caption without 'Table N' kept as a paragraph: {caption[:50]!r}")
                return caption + "\n\n" + table_md(tbl, None, ctx, slug)
            ctx._pending_label = label
        return table_md(tbl, caption, ctx, slug)

    md = re.sub(r'((?:<span id="[^"]+"></span>\s*)+)<div class="table-caption">\s*',
                lambda m: '\n\n<div class="table-caption">\n\n' + "".join(SPAN_ID.findall(m.group(1)) and
                          [f'<span id="{i}"></span>' for i in SPAN_ID.findall(m.group(1))]), md)
    md = TABLE_BLOCK.sub(table, md)

    def lone_caption(m):
        if XREF_START.match(m.group(1)):
            ctx.stats["body_text_unboxed"] += 1
            return m.group(1)
        label, caption = caption_md(m.group(1), "table", ctx, slug)
        ctx.note(f"{slug}: table caption not followed by a table kept as a paragraph")
        return (f"Table {ctx.label_kind[label][1]} " if label else "") + caption

    md = CAPTION_DIV.sub(lone_caption, md)

    # figures
    def figure(m):
        src, cap_html = m.group(1), m.group(2)
        label, caption = caption_md(cap_html, "figure", ctx, slug)
        name = f":name: {label}\n" if label else ""
        ctx.stats["figures"] += 1
        return f":::{{figure}} {src}\n{name}\n{caption}\n:::\n"

    md = FIG_BLOCK.sub(figure, md)
    md = re.sub(r"```\{image\} (\S+)\n:align: center\n```", r"```{image} \1\n```", md)

    # heading labels
    def heading(m):
        ids = SPAN_ID.findall(m.group(1))
        label = next((ctx.id_label[i] for i in ids if i in ctx.id_label), None)
        return (f"({label})=\n" if label else "") + m.group(2)

    md = re.sub(r"((?:<span id=\"[^\"]+\"></span>\s*)+)(#+ .*)", heading, md)

    # everything else (directive options, fences and labels are left alone)
    md = _inline_outside(md, ctx, slug)

    if fn_defs:
        md = md.rstrip() + "\n\n" + "\n\n".join(
            f"[^{n}]: " + inline_md(t, ctx, slug).strip() for n, t in fn_defs) + "\n"
    leftover = sorted(set(re.findall(r"</?([a-z]+)[\s>/]", _strip_code(md))) - {"https", "http"})
    if leftover:
        ctx.note(f"{slug}: HTML left in the page: {', '.join('<' + t + '>' for t in leftover)}")
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.rstrip() + "\n"


def _strip_code(md):
    return re.sub(r"```.*?```", "", md, flags=re.S)


def _inline_outside(md: str, ctx: Ctx, slug: str) -> str:
    """Run inline_md on paragraphs, leaving fences, directive options and labels alone.

    Table directives were already converted (their cells went through inline_md).
    """
    out = []
    in_fence = False
    in_table = False
    para: list[str] = []

    def flush():
        if para:
            out.append(inline_md("\n".join(para), ctx, slug, br="\\\n"))
            para.clear()

    for line in md.split("\n"):
        st = line.strip()
        if in_fence:
            out.append(line)
            if st.startswith("```"):
                in_fence = False
            continue
        if in_table:
            out.append(line)
            if st == ":::":
                in_table = False
            continue
        if st.startswith("```"):
            flush()
            out.append(line)
            in_fence = not (st.count("```") > 1)
            continue
        if st.startswith(":::{list-table}"):
            flush()
            out.append(line)
            in_table = True
            continue
        if (st.startswith(":::") or re.match(r"^:[\w-]+:\s", st) or re.match(r"^\([\w-]+\)=$", st)):
            flush()
            out.append(line)
            continue
        if not st:
            flush()
            out.append(line)
            continue
        para.append(line)
    flush()
    return "\n".join(out)


# --------------------------------------------------------------------------- driver
def tidy_dir(source: Path, log=print, refs_slug="references") -> Ctx:
    source = Path(source)
    pages = {p.stem: p.read_text(encoding="utf8") for p in sorted(source.glob("*.md"))}
    ctx = Ctx(log)
    collect(pages, ctx)
    for slug, md in pages.items():
        (source / f"{slug}.md").write_text(tidy_page(md, slug, ctx, refs_slug), encoding="utf8")
    return ctx


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("source", help="site source folder, e.g. docs/source")
    args = ap.parse_args(argv)
    ctx = tidy_dir(Path(args.source))
    print(dict(ctx.stats))
    return 0


if __name__ == "__main__":
    sys.exit(main())
