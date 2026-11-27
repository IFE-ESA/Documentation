"""Sphinx extension for the IFE report sites (copied into <site>/source/_ext/ by docx2rtd.py).

It keeps the Markdown easy to write by hand:

``{cite}`79```, ``{cite}`79, 80```, ``{cite}`3–5```, ``{cite}`53, p. 130```
    A numbered citation. It renders as "[79]" and so on, with each number linked.
    Every page that cites something gets a "References cited on this page" list at its
    end; the entries are copied from the references page.

``{cite}`seljomShorttermUncertaintyLongterm2015``` (Zotero mode)
    With ``ifereport_bibliography = "_bib/formatted.json"`` citations use Zotero /
    Better BibTeX citation keys. References are numbered in order of first citation
    through the report (as Zotero's IEEE style does in Word), and the references page
    holds a ``{bibliography}`` directive that lists them. ``{nocite}`key``` gives a
    reference its number at that point without showing anything (for entries that are
    listed but not cited in the text). tools/zotero_refs.py keeps the data in sync.

References page without Zotero (``ifereport_references_doc``, default ``references``)
    Each paragraph that starts with ``[N]`` is reference *N*, cited as ``{cite}`N```.

``{list-table}`` with merged cells
    The standard directive, plus ``{rowspan}`N``` / ``{colspan}`N``` at the start of a
    cell (HTML semantics: the cell covers N rows / columns; later rows simply leave the
    covered cells out), and the options ``:column-align: left center ...`` (body rows)
    and ``:header-align: center``.

``{u}`text```
    Underlined text.

Appendix numbering (``ifereport_appendix_prefixes = {"appendix-a": "A"}``)
    Tables, figures and equations in those pages are numbered A-1, A-2, ...

Building with ``-t docx`` (used by tools/rtd2docx.py) leaves out the per-page lists, so
citations link to the references page (the build is one page).
"""
from __future__ import annotations

import html as htmllib
import json
import os
import re
from html.parser import HTMLParser

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives.tables import ListTable
from sphinx.util import logging
from sphinx.util.docutils import SphinxRole

logger = logging.getLogger(__name__)

DASHES = "–—−-"
PAGE_LIST_TITLE = "References cited on this page"


# --------------------------------------------------------------------------- nodes
class cite_group(nodes.inline):
    """[79, 80]: holds the cited numbers in ``nums``."""


class nocite_marker(nodes.Inline, nodes.Element):
    """{nocite}`key`: numbers a reference here without showing anything."""


class bibliography_list(nodes.General, nodes.Element):
    """{bibliography}: replaced by the numbered reference list."""


class span_marker(nodes.Inline, nodes.Element):
    """Placeholder left by {rowspan}/{colspan}; removed by the table directive."""


def _skip(self, node):
    raise nodes.SkipNode


# --------------------------------------------------------------------------- roles
CITE_TOKEN = re.compile(r"(\d{1,4})|([^\d]+)")
LOCATOR = re.compile(r",\s*pp?\.\s")


KEY_RE = re.compile(r"^[\w][\w:.\-]*$")


class CiteRole(SphinxRole):
    def run(self):
        body = self.text.strip()
        m = LOCATOR.search(body)
        numbered, locator = (body[:m.start()], body[m.start():]) if m else (body, "")
        # with a Zotero bibliography every citation is a key (keys may be all digits, e.g. "2026")
        if self.config.ifereport_bibliography or not re.fullmatch(r"[\d\s,%s]+" % DASHES, numbered):
            # Zotero citation keys; numbers are filled in once every page is read
            keys = [k.strip() for k in numbered.split(",") if k.strip()]
            bad = [k for k in keys if not KEY_RE.match(k)]
            node = cite_group(classes=["cite-group"], keys=keys, nums=[], locator=locator)
            node += nodes.Text("[" + ", ".join(keys) + locator + "]")
            if bad or not keys:
                msg = self.inliner.reporter.warning(f"{{cite}}: not a citation key: {self.text!r}",
                                                    line=self.lineno)
                return [node], [msg]
            return [node], []
        node = cite_group(classes=["cite-group"])
        nums: list[int] = []
        node += nodes.Text("[")
        prev = None
        sep = ""
        for num, other in CITE_TOKEN.findall(numbered):
            if other:
                node += nodes.Text(other)
                sep = other.strip()
                continue
            n = int(num)
            if prev is not None and sep and sep in DASHES:
                nums.extend(range(prev + 1, n))  # 3–5 cites 4 as well
            nums.append(n)
            prev, sep = n, ""
            ref = nodes.reference("", num, internal=True, refid=f"ref-{n}", classes=["cite"])
            node += ref
        if locator:
            node += nodes.Text(locator)
        node += nodes.Text("]")
        node["nums"] = nums
        if not nums:
            msg = self.inliner.reporter.warning(f"{{cite}} without a reference number: {self.text!r}",
                                                line=self.lineno)
            return [node], [msg]
        return [node], []


def nocite_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    keys = [k.strip() for k in text.split(",") if k.strip()]
    return [nocite_marker(keys=keys)], []


class BibliographyDirective(Directive):
    """Where the numbered reference list goes (Zotero mode)."""
    has_content = False

    def run(self):
        return [bibliography_list()]


def _span_role(kind):
    def role(name, rawtext, text, lineno, inliner, options=None, content=None):
        try:
            n = int(text)
            assert n >= 1
        except (ValueError, AssertionError):
            msg = inliner.reporter.error(f"{{{kind}}} needs a whole number >= 1, got {text!r}", line=lineno)
            return [], [msg]
        return [span_marker(kind=kind, n=n)], []
    return role


def underline_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    return [nodes.inline(rawtext, text, classes=["underline"])], []


# --------------------------------------------------------------------------- tables
def _align(arg):
    vals = arg.split()
    for v in vals:
        if v not in ("left", "center", "right", "-"):
            raise ValueError(f"column alignment must be left, center, right or -, not {v!r}")
    return vals


class SpanListTable(ListTable):
    """list-table that also understands {rowspan}`n` / {colspan}`n` cell markers."""

    option_spec = dict(ListTable.option_spec)
    option_spec.update({
        "column-align": _align,
        "header-align": lambda a: directives.choice(a, ("left", "center", "right")),
    })

    def run(self):
        if not self.content:
            return [self.reporter.error(f'The "{self.name}" directive is empty; content required.',
                                        line=self.lineno)]
        title, messages = self.make_title()
        holder = nodes.Element()
        self.state.nested_parse(self.content, self.content_offset, holder)
        if len(holder) != 1 or not isinstance(holder[0], nodes.bullet_list):
            return [self._err("must contain a single bulleted list of rows")] + messages
        rows = []
        for item in holder[0]:
            if len(item) != 1 or not isinstance(item[0], nodes.bullet_list):
                return [self._err("each row must be a bulleted list of cells")] + messages
            cells = []
            for cell in item[0]:
                rs, cs = self._pop_spans(cell)
                cells.append((list(cell.children), rs, cs))
            rows.append(cells)

        # place cells on a grid
        occupied: set = set()
        placed = []
        for r, row in enumerate(rows):
            c = 0
            pr = []
            for content, rs, cs in row:
                while (r, c) in occupied:
                    c += 1
                pr.append((c, rs, cs, content))
                for i in range(rs):
                    for j in range(cs):
                        occupied.add((r + i, c + j))
                c += cs
            placed.append(pr)
        ncols = max((c for _, c in occupied), default=-1) + 1
        nrows = len(rows)
        for r in range(nrows):
            missing = [c for c in range(ncols) if (r, c) not in occupied]
            if missing:
                return [self._err(f"row {r + 1} has no cell in column(s) {[m + 1 for m in missing]}; "
                                  f"every row needs {ncols} cells after spans")] + messages
        if any(rr >= nrows for rr, _ in occupied):
            return [self._err("a {rowspan} reaches past the last row")] + messages

        widths = self.options.get("widths")
        if isinstance(widths, list):
            if len(widths) != ncols:
                return [self._err(f":widths: has {len(widths)} values but the table has {ncols} columns")] + messages
            col_widths = widths
        else:
            col_widths = [100 // max(ncols, 1)] * ncols
        header_rows = self.options.get("header-rows", 0)
        stub_columns = self.options.get("stub-columns", 0)
        col_align = self.options.get("column-align", [])
        if col_align and len(col_align) != ncols:
            return [self._err(f":column-align: has {len(col_align)} values but the table has {ncols} columns")] + messages
        head_align = self.options.get("header-align")

        table = nodes.table()
        if widths == "auto":
            table["classes"] += ["colwidths-auto"]
        elif widths:
            table["classes"] += ["colwidths-given"]
        tgroup = nodes.tgroup(cols=ncols)
        table += tgroup
        for i, w in enumerate(col_widths):
            colspec = nodes.colspec(colwidth=w)
            if i < stub_columns:
                colspec.attributes["stub"] = 1
            tgroup += colspec
        thead = nodes.thead()
        tbody = nodes.tbody()
        for r, pr in enumerate(placed):
            row_node = nodes.row()
            for c, rs, cs, content in pr:
                entry = nodes.entry()
                if rs > 1:
                    entry["morerows"] = rs - 1
                if cs > 1:
                    entry["morecols"] = cs - 1
                a = head_align if r < header_rows else (col_align[c] if col_align else None)
                if a and a != "-":
                    entry["classes"].append(f"text-{a}")
                entry += content
                row_node += entry
            (thead if r < header_rows else tbody).append(row_node)
        if header_rows:
            tgroup += thead
        tgroup += tbody
        if "align" in self.options:
            table["align"] = self.options["align"]
        table["classes"] += self.options.get("class", [])
        self.set_table_width(table)
        self.add_name(table)
        if title:
            table.insert(0, title)
        return [table] + messages

    def _err(self, text):
        return self.reporter.error(f'Error parsing "{self.name}": {text}.', line=self.lineno)

    @staticmethod
    def _pop_spans(cell):
        rs = cs = 1
        for m in list(cell.findall(span_marker)):
            if m["kind"] == "rowspan":
                rs = m["n"]
            else:
                cs = m["n"]
            parent = m.parent
            parent.remove(m)
            # drop the space that followed the marker
            if parent.children and isinstance(parent[0], nodes.Text):
                parent[0] = nodes.Text(parent[0].lstrip())
            if isinstance(parent, nodes.paragraph) and not parent.astext().strip() and not len(parent.children):
                parent.parent.remove(parent)
        return rs, cs


# --------------------------------------------------------------------------- references
REF_START = re.compile(r"^\[(\d{1,4})\]\s")


def _refs_doc(app):
    return app.config.ifereport_references_doc


def on_doctree_read(app, doctree):
    env = app.env
    docname = env.docname
    if not hasattr(env, "ifereport_refs"):
        env.ifereport_refs = {}
    if not hasattr(env, "ifereport_cites"):
        env.ifereport_cites = {}
    if docname == _refs_doc(app):
        for k in [k for k, v in env.ifereport_refs.items() if v[0] == docname]:
            del env.ifereport_refs[k]
        for p in doctree.findall(nodes.paragraph):
            m = REF_START.match(p.astext())
            if not m or isinstance(p.parent, nodes.entry):
                continue
            n = int(m.group(1))
            if n in env.ifereport_refs:
                logger.warning(f"reference [{n}] is listed twice", location=p)
                continue
            p["ids"].append(f"ref-{n}")
            p["classes"].append("ref-entry")
            env.ifereport_refs[n] = (docname, p.deepcopy())
    # citations in reading order; "[3]–[5]" written as two citations cites 4 too
    nums: list = []
    for g in doctree.findall(lambda n: isinstance(n, (cite_group, nocite_marker))):
        if isinstance(g, nocite_marker) or g.get("keys"):
            nums.extend(g["keys"])
            continue
        nums.extend(g["nums"])
        nxt = g.next_node(descend=False, siblings=True)
        if isinstance(nxt, nodes.Text) and nxt.astext().strip() in tuple(DASHES):
            after = nxt.next_node(descend=False, siblings=True)
            if isinstance(after, cite_group) and g["nums"] and after["nums"]:
                nums.extend(range(g["nums"][-1] + 1, after["nums"][0]))
    env.ifereport_cites[docname] = nums
    if not hasattr(env, "ifereport_nocite"):
        env.ifereport_nocite = {}
    env.ifereport_nocite[docname] = [k for m in doctree.findall(nocite_marker) for k in m["keys"]]


def on_env_purge_doc(app, env, docname):
    if hasattr(env, "ifereport_cites"):
        env.ifereport_cites.pop(docname, None)
    if hasattr(env, "ifereport_nocite"):
        env.ifereport_nocite.pop(docname, None)
    if hasattr(env, "ifereport_refs"):
        for k in [k for k, v in env.ifereport_refs.items() if v[0] == docname]:
            del env.ifereport_refs[k]


def on_env_merge_info(app, env, docnames, other):
    for attr in ("ifereport_refs", "ifereport_cites"):
        if not hasattr(env, attr):
            setattr(env, attr, {})
        getattr(env, attr).update(getattr(other, attr, {}))


def _docx_mode(app):
    return app.tags.has("docx")


def on_doctree_resolved(app, doctree, docname):
    if _bib(app) is not None:
        return _resolve_zotero(app, doctree, docname)
    env = app.env
    refs = getattr(env, "ifereport_refs", {})
    refdoc = _refs_doc(app)
    cited = sorted(set(getattr(env, "ifereport_cites", {}).get(docname, [])))
    for g in doctree.findall(cite_group):
        for n in g["nums"]:
            if n not in refs:
                logger.warning(f"{{cite}}: reference [{n}] is not on the '{refdoc}' page", location=g)
    if docname == refdoc or not cited:
        return
    if _docx_mode(app):  # one document: citations link to the full list
        return
    section = next(iter(doctree.findall(nodes.section)), None)
    target = section if section is not None else doctree
    rubric = nodes.rubric("", PAGE_LIST_TITLE)
    box = nodes.container(classes=["page-refs"])
    try:
        uri = app.builder.get_relative_uri(docname, refdoc)
    except Exception:  # builders without URIs
        uri = None
    for n in cited:
        if n not in refs:
            continue
        p = refs[n][1].deepcopy()
        p["ids"] = [f"ref-{n}"]
        p["classes"] = ["ref-entry"]
        if uri is not None:
            p += nodes.Text(" ")
            p += nodes.reference("", "↗", refuri=f"{uri}#ref-{n}", classes=["ref-full"],
                                 reftitle="Full reference list")
        box += p
    target += rubric
    target += box


# --------------------------------------------------------------------------- Zotero mode
_BIB_CACHE: dict = {}


def _bib(app):
    """{key: html} from ifereport_bibliography, or None when not configured."""
    rel = app.config.ifereport_bibliography
    if not rel:
        return None
    path = os.path.join(app.srcdir, rel)
    mtime = os.path.getmtime(path) if os.path.exists(path) else None
    if _BIB_CACHE.get("key") != (path, mtime):
        if mtime is None:
            logger.warning(f"ifereport_bibliography: {rel} not found")
            data = {}
        else:
            with open(path, encoding="utf8") as f:
                data = json.load(f)
            data = data.get("entries", data)
        _BIB_CACHE.update(key=(path, mtime), data=data)
    return _BIB_CACHE["data"]


def _reading_order(env, root):
    order, seen = [], set()

    def visit(doc):
        if doc in seen:
            return
        seen.add(doc)
        order.append(doc)
        for child in env.toctree_includes.get(doc, []):
            visit(child)

    visit(root)
    order += sorted(d for d in env.found_docs if d not in seen)
    return order


def on_env_updated(app, env):
    """Number the references in order of first citation through the report."""
    if _bib(app) is None:
        return []
    numbers: dict = {}
    for doc in _reading_order(env, app.config.root_doc):
        for k in getattr(env, "ifereport_cites", {}).get(doc, []):
            if isinstance(k, str) and k not in numbers:
                numbers[k] = len(numbers) + 1
    old = getattr(env, "ifereport_numbers", None)
    env.ifereport_numbers = numbers
    if old is not None and old != numbers:  # numbers changed: rewrite every citing page
        return [d for d, ks in env.ifereport_cites.items() if ks] + [_refs_doc(app)]
    return []


class _HTMLToNodes(HTMLParser):
    TAGS = {"i": nodes.emphasis, "em": nodes.emphasis, "b": nodes.strong, "strong": nodes.strong,
            "sup": nodes.superscript, "sub": nodes.subscript}
    URL = re.compile(r"(https?://[^\s<>\]]+?)(?=[.,;)]?(?:\s|$))")

    def __init__(self, root):
        super().__init__(convert_charrefs=True)
        self.stack = [root]

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.TAGS:
            el = self.TAGS[tag]()
        elif tag == "a" and a.get("href"):
            el = nodes.reference("", "", refuri=a["href"])
        elif tag == "span" and "small-caps" in (a.get("style") or ""):
            el = nodes.inline(classes=["small-caps"])
        else:
            el = nodes.inline()
        self.stack[-1] += el
        self.stack.append(el)

    def handle_endtag(self, tag):
        if len(self.stack) > 1:
            self.stack.pop()

    def handle_data(self, data):
        parent = self.stack[-1]
        if isinstance(parent, nodes.reference):
            parent += nodes.Text(data)
            return
        pos = 0
        for m in self.URL.finditer(data):  # link the URLs, as the report does
            parent += nodes.Text(data[pos:m.start()])
            parent += nodes.reference("", m.group(1), refuri=m.group(1))
            pos = m.end()
        parent += nodes.Text(data[pos:])


def _entry(n, html_text, extra_ids=()):
    p = nodes.paragraph(classes=["ref-entry"], ids=[f"ref-{n}", *extra_ids])
    p += nodes.Text(f"[{n}] ")
    parser = _HTMLToNodes(p)
    parser.feed(html_text or "")
    parser.close()
    return p


def _resolve_zotero(app, doctree, docname):
    env = app.env
    bib = _bib(app)
    numbers = getattr(env, "ifereport_numbers", {})
    refdoc = _refs_doc(app)
    for g in list(doctree.findall(cite_group)):
        keys = g.get("keys")
        if not keys:
            logger.warning("numbered {cite} in a Zotero bibliography: use the citation key", location=g)
            continue
        g.children = []
        g += nodes.Text("[")
        for i, k in enumerate(keys):
            if i:
                g += nodes.Text(", ")
            n = numbers.get(k)
            if n is None or k not in bib:
                logger.warning(f"{{cite}}: citation key {k!r} is not in the bibliography "
                               f"(run tools/zotero_refs.py sync)", location=g)
                g += nodes.Text(f"?{k}")
                continue
            g["nums"].append(n)
            g += nodes.reference("", str(n), internal=True, refid=f"ref-{n}", classes=["cite"])
        if g.get("locator"):
            g += nodes.Text(g["locator"])
        g += nodes.Text("]")
    for m in list(doctree.findall(nocite_marker)):
        for k in m["keys"]:
            if k not in bib:
                logger.warning(f"{{nocite}}: citation key {k!r} is not in the bibliography", location=m)
        m.parent.remove(m)
    by_number = sorted((n, k) for k, n in numbers.items() if k in bib)
    for ph in list(doctree.findall(bibliography_list)):
        box = nodes.container(classes=["references-list"])
        for n, k in by_number:
            box += _entry(n, bib[k])
        ph.replace_self(box)
    if docname == refdoc or _docx_mode(app):
        return
    shown = {k for g in doctree.findall(cite_group) for k in g.get("keys", [])}  # not {nocite}
    cited = sorted({numbers[k] for k in shown if k in numbers and k in bib})
    if not cited:
        return
    keys_by_n = {n: k for k, n in numbers.items()}
    section = next(iter(doctree.findall(nodes.section)), None)
    target = section if section is not None else doctree
    box = nodes.container(classes=["page-refs"])
    try:
        uri = app.builder.get_relative_uri(docname, refdoc)
    except Exception:
        uri = None
    for n in cited:
        p = _entry(n, bib[keys_by_n[n]])
        if uri is not None:
            p += nodes.Text(" ")
            p += nodes.reference("", "↗", refuri=f"{uri}#ref-{n}", classes=["ref-full"],
                                 reftitle="Full reference list")
        box += p
    target += nodes.rubric("", PAGE_LIST_TITLE)
    target += box


def on_doctree_read_figures(app, doctree):
    """Figures get their caption as alt text unless :alt: is given."""
    for fig in doctree.findall(nodes.figure):
        cap = next(iter(fig.findall(nodes.caption)), None)
        if cap is None:
            continue
        for img in fig.findall(nodes.image):
            if not img.get("alt"):
                img["alt"] = cap.astext()


# --------------------------------------------------------------------------- appendix numbering
def on_env_get_updated(app, env):
    prefixes = app.config.ifereport_appendix_prefixes
    for docname, prefix in prefixes.items():
        figs = env.toc_fignumbers.get(docname)
        if not figs:
            continue
        for figtype, ids in figs.items():
            for i, key in enumerate(ids, 1):  # dict order is document order
                ids[key] = (f"{prefix}-{i}",)
    return []


# --------------------------------------------------------------------------- setup
def setup(app):
    app.add_config_value("ifereport_references_doc", "references", "env")
    app.add_config_value("ifereport_appendix_prefixes", {}, "env")
    app.add_config_value("ifereport_bibliography", "", "env")
    app.add_node(nocite_marker, html=(_skip, None), latex=(_skip, None), text=(_skip, None),
                 man=(_skip, None), texinfo=(_skip, None))
    app.add_node(bibliography_list, html=(_skip, None), latex=(_skip, None), text=(_skip, None),
                 man=(_skip, None), texinfo=(_skip, None))
    app.add_role("nocite", nocite_role)
    app.add_directive("bibliography", BibliographyDirective)
    app.connect("env-updated", on_env_updated)
    app.add_node(cite_group)
    app.add_node(span_marker, html=(_skip, None), latex=(_skip, None), text=(_skip, None),
                 man=(_skip, None), texinfo=(_skip, None))
    app.add_role("cite", CiteRole(), override=True)
    app.add_role("rowspan", _span_role("rowspan"))
    app.add_role("colspan", _span_role("colspan"))
    app.add_role("u", underline_role)
    app.add_directive("list-table", SpanListTable, override=True)
    app.connect("doctree-read", on_doctree_read)
    app.connect("env-purge-doc", on_env_purge_doc)
    app.connect("env-merge-info", on_env_merge_info)
    app.connect("doctree-resolved", on_doctree_resolved)
    app.connect("doctree-read", on_doctree_read_figures)
    app.connect("env-get-updated", on_env_get_updated, priority=900)
    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True,
            "env_version": 2}
