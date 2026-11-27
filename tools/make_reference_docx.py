#!/usr/bin/env python3
"""Make the Word template used by tools/rtd2docx.py from an IFE report .docx.

The template keeps the report's styles, heading numbering, theme, page setup and
headers/footers (with their logo images) but none of its content, so it is small
enough to keep in git:

    python tools/make_reference_docx.py --docx "Documentation of IFE-TIMES-Norway v5.docx" \
        --out tools/templates/ife-reference.docx

The section whose page setup and headers/footers the template uses is the one that holds
most of the body text (the largest section), i.e. the chapters, not the cover.
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

KEEP_TYPES = ("styles", "numbering", "settings", "theme", "fontTable", "webSettings",
              "footnotes", "endnotes", "header", "footer", "stylesWithEffects", "customXml")
APP_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
           '<Application>Microsoft Office Word</Application></Properties>')


def make(docx: Path, out: Path) -> dict:
    zin = zipfile.ZipFile(docx)
    doc = zin.read("word/document.xml").decode("utf8")
    rels = zin.read("word/_rels/document.xml.rels").decode("utf8")
    # the section with the most text is the body
    sects = [(m.start(), m.end(), m.group(0)) for m in re.finditer(r"<w:sectPr\b.*?</w:sectPr>", doc, re.S)]
    if not sects:
        raise SystemExit("no sections found in the document")
    best, prev = None, doc.index("<w:body>")
    for start, end, xml in sects:
        size = len(re.sub(r"<[^>]+>", "", doc[prev:start]))
        if best is None or size > best[0]:
            best = (size, xml)
        prev = end
    sect = best[1]
    # headers/footers inherited from earlier sections are not visible to pandoc: copy the
    # most recent ones into this section
    if "<w:headerReference" not in sect or "<w:footerReference" not in sect:
        inherited = {}
        for _, _, xml in sects:
            for kind, typ, rid in re.findall(r'<w:(header|footer)Reference w:type="(\w+)" r:id="(rId\d+)"/>', xml):
                inherited[(kind, typ)] = rid
            if xml == sect:
                break
        own = set(re.findall(r'<w:(header|footer)Reference w:type="(\w+)"', sect))
        add = "".join(f'<w:{k}Reference w:type="{t}" r:id="{r}"/>' for (k, t), r in inherited.items()
                      if (k, t) not in own)
        sect = re.sub(r"(<w:sectPr\b[^>]*>)", lambda m: m.group(1) + add, sect, count=1)
    head = doc[:doc.index("<w:body>")]
    new_doc = head + "<w:body><w:p/>" + sect + "</w:body></w:document>"

    keep_rels = []
    for m in re.finditer(r"<Relationship\b[^>]*/>", rels):
        r = m.group(0)
        typ = re.search(r'Type="[^"]*/([^"/]+)"', r).group(1)
        if typ in KEEP_TYPES:
            keep_rels.append(r)
    new_rels = re.sub(r"<Relationship\b[^>]*/>", "", rels).replace(
        "</Relationships>", "".join(keep_rels) + "</Relationships>")
    kept_targets = {"word/" + re.search(r'Target="([^"]+)"', r).group(1) for r in keep_rels}

    # parts to copy: everything except the body's own media/charts/embeddings/comments
    names = set(zin.namelist())
    needed = set()
    for t in kept_targets:
        needed.add(t)
        relp = t.replace("word/", "word/_rels/", 1) + ".rels"
        if relp in names:
            needed.add(relp)
            for tgt in re.findall(r'Target="([^"]+)"', zin.read(relp).decode("utf8")):
                if not tgt.startswith("http"):
                    needed.add("word/" + tgt.lstrip("./").replace("../", ""))
    out.parent.mkdir(parents=True, exist_ok=True)
    stats = {"parts": 0, "bytes_in": docx.stat().st_size}
    ct = zin.read("[Content_Types].xml").decode("utf8")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in zin.namelist():
            if n == "word/document.xml":
                zout.writestr(n, new_doc)
            elif n == "word/_rels/document.xml.rels":
                zout.writestr(n, new_rels)
            elif n == "[Content_Types].xml":
                # drop overrides for parts that are not copied
                def keep_override(m):
                    part = m.group(1).lstrip("/")
                    return m.group(0) if (part in needed or part in (
                        "word/document.xml", "docProps/core.xml", "docProps/app.xml")) else ""
                zout.writestr(n, re.sub(r'<Override PartName="([^"]+)"[^>]*/>', keep_override, ct))
            elif n.startswith("word/") and n not in needed and not n.startswith("word/_rels/document"):
                continue  # body media, charts, comments, glossary...
            elif n == "docProps/core.xml":
                zout.writestr(n, zin.read(n))
            elif n == "docProps/app.xml":  # the source lists every heading here
                zout.writestr(n, APP_XML)
            elif n == "_rels/.rels":
                r = zin.read(n).decode("utf8")
                r = re.sub(r'<Relationship\b[^>]*Target="(?!word/document\.xml|docProps/core\.xml|docProps/app\.xml)[^"]*"[^>]*/>', "", r)
                zout.writestr(n, r)
            elif n.startswith(("docProps/", "customXml/")):
                continue  # SharePoint/DOCUS metadata of the source document
            elif n in needed:
                zout.writestr(n, zin.read(n))
            else:
                continue
            stats["parts"] += 1
    stats["bytes_out"] = out.stat().st_size
    return stats


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--docx", required=True, help="an IFE report in Word format")
    ap.add_argument("--out", default="tools/templates/ife-reference.docx")
    args = ap.parse_args(argv)
    st = make(Path(args.docx), Path(args.out))
    print(f"Wrote {args.out}: {st['parts']} parts, {st['bytes_out'] // 1024} KB "
          f"(from {st['bytes_in'] // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
