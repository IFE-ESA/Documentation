#!/usr/bin/env python3
"""Keep the report's references in Zotero.

The Markdown cites Zotero items by their Better BibTeX citation key,
``{cite}`seljomShorttermUncertaintyLongterm2015```. Sphinx (tools/ifereport.py) numbers
them in order of first citation and lists them on the references page, using two files
that this script writes and that are committed with the sources (Read the Docs cannot
reach your Zotero):

    docs/source/_bib/library.json     the Zotero group as CSL-JSON (Better BibTeX export)
    docs/source/_bib/formatted.json   each item formatted by Zotero itself (IEEE, en-GB),
                                      the same engine the Zotero Word plugin uses

Commands (Zotero must be running with Better BibTeX):

    python tools/zotero_refs.py sync     # refresh both files from Zotero
    python tools/zotero_refs.py check    # citation keys in the Markdown that Zotero lacks
    python tools/zotero_refs.py migrate  # one-off: numbered {cite}`N` -> citation keys

Settings live in docs/source/_bib/zotero.json (group id, export URL, style, locale).
If Better BibTeX's formatter cannot be reached, ``sync --formatter pandoc`` formats the
items with pandoc and docs/source/_bib/ieee.csl instead (small differences to Zotero).
"""
from __future__ import annotations

import argparse
import difflib
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

DEFAULTS = {
    "group_id": 6656322,
    "export_url": "http://127.0.0.1:23119/better-bibtex/export?/group;id:6656322/IFE-TIMES-NORWAY.json",
    "rpc_url": "http://127.0.0.1:23119/better-bibtex/json-rpc",
    "style": "http://www.zotero.org/styles/ieee",
    "locale": "en-GB",
}
DROP_FIELDS = {"file", "abstract", "note"}  # local file paths / long text not needed to cite


def load_config(source: Path) -> dict:
    p = source / "_bib" / "zotero.json"
    cfg = dict(DEFAULTS)
    if p.exists():
        cfg.update(json.loads(p.read_text()))
    return cfg


def _get(url, timeout=30):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()


def _rpc(cfg, method, params, timeout=60):
    req = urllib.request.Request(cfg["rpc_url"], headers={"Content-Type": "application/json"},
                                 data=json.dumps({"jsonrpc": "2.0", "method": method, "params": params,
                                                  "id": 1}).encode())
    with urllib.request.urlopen(req, timeout=timeout) as r:
        res = json.load(r)
    if "error" in res:
        raise RuntimeError(f"Better BibTeX: {res['error']}")
    return res["result"]


def format_zotero(cfg, keys):
    out = {}
    for k in keys:
        html_ = _rpc(cfg, "item.bibliography",
                     [[k], {"id": cfg["style"], "contentType": "html", "locale": cfg["locale"]}, cfg["group_id"]])
        m = re.search(r'<div class="csl-right-inline"[^>]*>(.*?)</div>', html_ or "", re.S)
        if not m:  # styles without a number column
            m = re.search(r'<div class="csl-entry"[^>]*>(.*?)</div>', html_ or "", re.S)
        out[k] = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
    return out


def format_pandoc(cfg, library: Path, keys, csl: Path):
    if not shutil.which("pandoc"):
        raise SystemExit("pandoc is not on PATH")
    with tempfile.TemporaryDirectory() as d:
        md = Path(d) / "x.md"
        md.write_text("---\nnocite: |\n  " + ", ".join("@" + k for k in keys) + "\n---\n")
        res = subprocess.run(["pandoc", str(md), "--citeproc", "-M", f"lang={cfg['locale']}",
                              "--bibliography", str(library), "--csl", str(csl), "-t", "html"],
                             capture_output=True, text=True, check=True)
    out = {}
    for m in re.finditer(r'<div id="ref-([^"]+)" class="csl-entry"[^>]*>\s*(.*?)\s*</div>', res.stdout, re.S):
        body = re.sub(r'<div class="csl-left-margin">.*?</div>', "", m.group(2), flags=re.S)
        body = re.sub(r'</?div[^>]*>', "", body)
        out[m.group(1)] = re.sub(r"\s+", " ", body).strip()
    return out


def cmd_sync(args):
    source = Path(args.source)
    cfg = load_config(source)
    bibdir = source / "_bib"
    bibdir.mkdir(exist_ok=True)
    items = json.loads(_get(cfg["export_url"]))
    items = sorted(({k: v for k, v in it.items() if k not in DROP_FIELDS} for it in items), key=lambda i: i["id"])
    lib = bibdir / "library.json"
    lib.write_text(json.dumps(items, indent=1, ensure_ascii=False) + "\n")
    keys = [i["id"] for i in items]
    if args.formatter == "zotero":
        try:
            entries = format_zotero(cfg, keys)
        except Exception as e:  # noqa: BLE001
            raise SystemExit(f"Better BibTeX formatting failed ({e}); try --formatter pandoc")
    else:
        entries = format_pandoc(cfg, lib, keys, bibdir / "ieee.csl")
    missing = [k for k, v in entries.items() if not v]
    out = {"formatter": args.formatter, "style": cfg["style"], "locale": cfg["locale"],
           "entries": {k: entries[k] for k in sorted(entries) if entries[k]}}
    (bibdir / "formatted.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(items)} items -> {lib}; {len(out['entries'])} formatted by {args.formatter}"
          + (f"; could not format: {missing}" if missing else ""))
    return cmd_check(args, quiet=True)


def cited_keys(source: Path):
    found = {}
    for p in sorted(source.glob("*.md")):
        for m in re.finditer(r"\{(?:cite|nocite)\}`([^`]*)`", p.read_text(encoding="utf8")):
            body = re.split(r",\s*pp?\.\s", m.group(1))[0]
            for k in body.split(","):
                k = k.strip()
                if k and not k.isdigit():
                    found.setdefault(k, p.name)
    return found


def cmd_check(args, quiet=False):
    source = Path(args.source)
    fmt = source / "_bib" / "formatted.json"
    have = set(json.loads(fmt.read_text())["entries"]) if fmt.exists() else set()
    keys = cited_keys(source)
    missing = {k: f for k, f in keys.items() if k not in have}
    for k, f in missing.items():
        print(f"not in Zotero: {k} (cited in {f})")
    if not quiet:
        print(f"{len(keys)} cited keys, {len(missing)} missing")
    return 1 if missing else 0


# --------------------------------------------------------------------------- migrate
def _plain(s):
    s = re.sub(r"<(https?://[^>]+)>", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1", s)
    s = re.sub(r"\{su[bp]\}`([^`]*)`", r"\1", s)
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    return re.sub(r"\s+", " ", s.replace("*", "").replace("\\", "")).strip()


def match_references(numbered: dict, entries: dict, assign: dict):
    """Pair reference numbers with Zotero keys by their formatted text (best first)."""
    plain = {k: _plain(v) for k, v in entries.items()}
    out = {n: (k, 1.0, "assigned") for n, k in assign.items()}
    used = set(assign.values())
    pairs = []
    for n, text in numbered.items():
        if n in out:
            continue
        t = _plain(text)
        for k, z in plain.items():
            if k in used:
                continue
            q = difflib.SequenceMatcher(None, t, z, autojunk=False)
            if q.real_quick_ratio() < 0.6 or q.quick_ratio() < 0.6:
                continue
            pairs.append((q.ratio(), n, k))
    pairs.sort(reverse=True)
    for score, n, k in pairs:
        if n in out or k in used:
            continue
        out[n] = (k, score, "matched")
        used.add(k)
    return out


def cmd_migrate(args):
    source = Path(args.source)
    refs_md = source / "references.md"
    text = refs_md.read_text(encoding="utf8")
    numbered = {int(m.group(1)): m.group(2) for m in re.finditer(r"^\[(\d+)\] (.*)$", text, re.M)}
    if not numbered:
        raise SystemExit("references.md has no numbered entries: already migrated?")
    entries = json.loads((source / "_bib" / "formatted.json").read_text())["entries"]
    assign = {int(a.split("=")[0]): a.split("=")[1] for a in args.assign}
    m = match_references(numbered, entries, assign)
    weak = {n: v for n, v in m.items() if v[1] < args.min_score}
    unmatched = sorted(set(numbered) - set(m))
    report = {"matches": {n: {"key": k, "score": round(s, 4), "how": h} for n, (k, s, h) in sorted(m.items())},
              "weak": sorted(weak), "unmatched": unmatched}
    Path(args.report).write_text(json.dumps(report, indent=1, ensure_ascii=False))
    for n in sorted(weak):
        k, s, _ = m[n]
        print(f"[{n}] weak match {s:.3f} -> {k}\n    report: {_plain(numbered[n])[:150]}\n"
              f"    zotero: {_plain(entries[k])[:150]}")
    if weak or unmatched:
        print(f"{len(weak)} weak, {len(unmatched)} unmatched; fix in Zotero or pass --assign N=key "
              f"(see {args.report}). Nothing was changed.")
        return 1
    key_of = {n: v[0] for n, v in m.items()}

    pages = sorted(p for p in source.glob("*.md") if p.name != "references.md")
    cited: set = set()
    texts = {}
    for p in pages:
        t = p.read_text(encoding="utf8")

        def repl(mm):
            body = mm.group(1)
            loc = re.search(r",\s*pp?\.\s", body)
            nums, tail = (body[:loc.start()], body[loc.start():]) if loc else (body, "")
            ns = [int(x) for x in re.findall(r"\d+", nums)]
            if re.search("[%s]" % "–—−-", nums):
                raise SystemExit(f"{p.name}: range citation {mm.group(0)} – split it first")
            cited.update(ns)
            return "{cite}`" + ", ".join(key_of[n] for n in ns) + tail + "`"

        texts[p] = re.sub(r"\{cite\}`([\d\s,]+(?:,\s*pp?\.\s[^`]*)?)`", repl, t)
    # listed but never cited: number them right after the reference before them
    for n in sorted(set(numbered) - cited):
        prev = key_of.get(n - 1)
        placed = False
        for p, t in texts.items():
            i = t.find("{cite}`" + prev + "`") if prev else -1
            if i >= 0:
                j = i + len("{cite}`" + prev + "`")
                texts[p] = t[:j] + "{nocite}`" + key_of[n] + "`" + t[j:]
                print(f"[{n}] is not cited in the text: {{nocite}} placed after [{n - 1}] in {p.name}")
                placed = True
                break
        if not placed:
            print(f"WARNING: [{n}] is not cited and could not be placed")
    for p, t in texts.items():
        p.write_text(t, encoding="utf8")
    head = text[:text.index("[1] ")].rstrip()
    refs_md.write_text(head + "\n\n:::{bibliography}\n:::\n", encoding="utf8")
    conf = source / "conf.py"
    c = conf.read_text()
    if "ifereport_bibliography" not in c:
        conf.write_text(c.rstrip() + '\nifereport_bibliography = "_bib/formatted.json"  # Zotero: tools/zotero_refs.py\n')
    print(f"Migrated {len(cited)} cited references in {len(pages)} pages to citation keys.")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default="docs/source")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sync", help="refresh _bib/library.json and _bib/formatted.json from Zotero")
    s.add_argument("--formatter", choices=["zotero", "pandoc"], default="zotero")
    sub.add_parser("check", help="list citation keys used in the Markdown that Zotero lacks")
    mg = sub.add_parser("migrate", help="one-off: numbered citations -> Zotero citation keys")
    mg.add_argument("--assign", action="append", default=[], metavar="N=KEY",
                    help="pair reference N with a citation key by hand")
    mg.add_argument("--min-score", type=float, default=0.97,
                    help="text similarity below which a match is not trusted (default 0.97)")
    mg.add_argument("--report", default="build/zotero_migration.json")
    args = ap.parse_args(argv)
    if getattr(args, "report", None):
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    return {"sync": cmd_sync, "check": cmd_check, "migrate": cmd_migrate}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
