#!/usr/bin/env python3
"""Compare two Sphinx HTML builds of the report page by page.

Used to check that a change to the Markdown sources (e.g. tools/tidy_myst.py) leaves
what readers see unchanged: the words of every page, the figure and table numbers and
captions, the shape of every table (rows, columns, merged cells) and the amount of
italic, bold, sub/superscript and link markup.

    python tools/compare_sites.py OLD_HTML_DIR NEW_HTML_DIR [--json report.json]

Exit status 1 if the words or the numbering differ.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

SKIP = {"genindex.html", "search.html", "py-modindex.html"}


def body(path: Path):
    soup = BeautifulSoup(path.read_text(encoding="utf8"), "lxml")
    main = soup.select_one('div[itemprop="articleBody"]') or soup.select_one("div.body")
    for el in main.select("a.headerlink"):
        el.decompose()
    return main


def words(main) -> list[str]:
    txt = main.get_text(" ")
    txt = txt.replace(" ", " ")
    return re.findall(r"[^\s]+", re.sub(r"([\[\](),;:.])", r" \1 ", txt))


def captions(main) -> list[str]:
    out = []
    for el in main.select("figcaption, caption, .table-caption, .fig-caption"):
        t = re.sub(r"\s+", " ", el.get_text(" ")).strip()
        m = re.match(r"(Figure|Table)\s+((?:[A-Z]-)?\d+)", t)
        if m:
            out.append(f"{m.group(1)} {m.group(2)}")
    for el in main.select("p"):  # old site: captions were italic paragraphs
        t = re.sub(r"\s+", " ", el.get_text(" ")).strip()
        if el.find_parent(class_=["table-caption", "fig-caption"]) or el.find_parent("figcaption"):
            continue
        if el.find("em") and re.match(r"(Figure|Table)\s+(?:[A-Z]-)?\d+\s", t) and \
                re.sub(r"\s+", " ", el.find("em").get_text(" ")).strip().startswith(("Figure", "Table")):
            m = re.match(r"(Figure|Table)\s+((?:[A-Z]-)?\d+)", t)
            out.append(f"{m.group(1)} {m.group(2)}")
    return sorted(set(out), key=out.index)


def table_shapes(main) -> list[tuple]:
    shapes = []
    for t in main.select("table"):
        rows = t.select("tr")
        spans = sum(1 for c in t.select("td, th") if c.get("rowspan", "1") != "1" or c.get("colspan", "1") != "1")
        cells = len(t.select("td, th"))
        shapes.append((len(rows), cells, spans))
    return shapes


def markup(main) -> Counter:
    c = Counter()
    for tag in ("em", "strong", "sub", "sup", "u"):
        c[tag] = len(main.find_all(tag))
    c["underline"] = len(main.select(".underline")) + c.pop("u")
    c["external_links"] = len(main.select("a.reference.external, a.external"))
    c["math"] = len(main.select(".math, span.math, div.math"))
    c["images"] = len(main.select("img"))
    return c


def compare(old: Path, new: Path):
    report = {"pages": {}, "word_differences": 0, "numbering_differences": 0}
    pages = sorted(p.name for p in old.glob("*.html") if p.name not in SKIP)
    for name in pages:
        if not (new / name).exists():
            report["pages"][name] = {"missing": True}
            report["word_differences"] += 1
            continue
        a, b = body(old / name), body(new / name)
        wa, wb = words(a), words(b)
        diff = [d for d in difflib.unified_diff(wa, wb, lineterm="", n=4) if not d.startswith(("---", "+++"))]
        ca, cb = captions(a), captions(b)
        pr = {
            "words_old": len(wa), "words_new": len(wb),
            "word_diff": diff[:200],
            "captions_equal": ca == cb,
            "captions_old_only": [x for x in ca if x not in cb],
            "captions_new_only": [x for x in cb if x not in ca],
            "tables_old": table_shapes(a), "tables_new": table_shapes(b),
            "markup_old": dict(markup(a)), "markup_new": dict(markup(b)),
        }
        pr["tables_equal"] = pr["tables_old"] == pr["tables_new"]
        report["pages"][name] = pr
        if diff:
            report["word_differences"] += 1
        if ca != cb:
            report["numbering_differences"] += 1
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--json")
    args = ap.parse_args(argv)
    rep = compare(Path(args.old), Path(args.new))
    for name, pr in rep["pages"].items():
        if pr.get("missing"):
            print(f"{name}: MISSING in new build")
            continue
        flags = []
        if pr["word_diff"]:
            flags.append(f"WORDS differ ({len(pr['word_diff'])} diff lines)")
        if not pr["captions_equal"]:
            flags.append(f"CAPTIONS old-only={pr['captions_old_only']} new-only={pr['captions_new_only']}")
        if not pr["tables_equal"]:
            flags.append("TABLE SHAPES differ")
        mk = {k: (pr["markup_old"].get(k, 0), pr["markup_new"].get(k, 0)) for k in
              set(pr["markup_old"]) | set(pr["markup_new"]) if pr["markup_old"].get(k, 0) != pr["markup_new"].get(k, 0)}
        if mk:
            flags.append(f"markup {mk}")
        print(f"{name}: {'; '.join(flags) if flags else 'same'}")
    if args.json:
        Path(args.json).write_text(json.dumps(rep, indent=1, ensure_ascii=False))
    return 1 if rep["word_differences"] or rep["numbering_differences"] else 0


if __name__ == "__main__":
    sys.exit(main())
