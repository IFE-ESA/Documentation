#!/usr/bin/env python3
"""Re-draw the data figures of the IFE-TIMES-Norway report in one consistent style.

Usage:
    python tools/restyle_figures.py --docx <report.docx> --pdf <report.pdf> --out mirror/figures

What it does
------------
1. Walks the body paragraphs of the docx and assigns every drawing (native chart,
   raster image, EMF, text box, ...) to the next "Figure N" caption paragraph.
2. Native Word charts: parses ``word/charts/chartN.xml`` (series, categories,
   axis titles, number formats, legend, grouping) and takes the data from
   (a) the embedded workbook referenced by the chart rels when its ``c:f``
   formulas resolve, else (b) the chart's cached values.
3. Raster/EMF figures listed in ``DIGITIZE`` are digitized from the PDF render
   by colour segmentation + axis calibration (approximate, marked ``digitized``).
4. Everything else is marked ``original`` (diagram/map/schematic).
5. Writes figNN.png/.svg, data/figNN.csv, manifest.json and contact_sheet.png.

Per-figure tweaks (chart-type overrides, digitizing settings, figure kinds) are
kept in the CONFIG section below. Figures are matched by caption number.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np

# =============================================================================
# CONFIG  --  all per-figure settings live here
# =============================================================================

# Figures that are diagrams, schematics, maps or tables: never re-drawn.
ORIGINAL_ONLY = {
    1: "schematic (EMF + images + text boxes)",
    2: "schematic",
    3: "map of regions (EMF)",
    4: "time-slice tree diagram",
    9: "map with text-box overlays",
    10: "map of transmission capacities",
    17: "schematic",
    18: "schematic",
    19: "illustration/diagram",
    20: "RES diagram",
    26: "schematic",
    27: "diagram of end-use technologies",
    28: "schematic",
    39: "matrix/table drawing",
}

# Per-chart overrides for native charts (keyed by figure number).
#   chart_type: force a renderer ('bar', 'barh', 'line', 'scatter', 'area', 'pie')
#   note:       extra text for the manifest
#   legend_ncol, figsize, ylim, xlabel, ylabel: plotting tweaks (labels only
#   when the original carries the text outside the chart, never reworded)
#   colors:     {series name: hex} explicit colours (e.g. keep a semantic family)
#   highlight:  {series name: {color, lw, zorder}} -- emphasised series; all
#               other series become thin lines in a sequential ramp (``others``)
#   tint_of:    {series name: [base series name, lighten 0..1]} -- same hue as base
#   marker_max_points: drop markers on line series longer than this
FAMILY_2030 = ["#9fe0cf", "#00b894", "#00735c"]      # aqua ramp light -> dark
FAMILY_2050 = ["#a9cbf3", "#257de0", "#0d4a8f"]      # blue ramp light -> dark
CHART_OVERRIDES: dict[int, dict] = {
    7: {"highlight": {"Average": {"color": "#191919", "lw": 2.6, "zorder": 10}},
        "others": "years", "marker_max_points": 20,
        "note": "Individual weather years drawn as thin lines on a light-to-dark blue ramp (2000 light -> "
                "2015 dark) without markers; the original has no legend either. 'Average' is emphasised "
                "in black as in the original (the chart contains the Average series twice; drawn once)."},
    11: {"colors": {"Low 2030": FAMILY_2030[0], "Medium 2030": FAMILY_2030[1], "High 2030": FAMILY_2030[2],
                    "Low 2050": FAMILY_2050[0], "Medium 2050": FAMILY_2050[1], "High 2050": FAMILY_2050[2]},
         "note": "Colour encodes year (2030 aqua, 2050 blue) and lightness encodes price level, as in the "
                 "original (2030 greens, 2050 blues). This is the native chart part of Figure 11; the second "
                 "part (image12.png, four seasonal panels for 2030/2040/2050) is re-drawn separately as "
                 "fig11b (digitized)."},
    24: {"tint_of": {f"New P{i}": [f"P{i}", 0.55] for i in range(1, 6)},
         "box_series": [f"P{i}" for i in range(1, 6)],
         "note": "Stacked: existing demand P1-P5 (full colour, bottom) and new demand 'New P1'..'P5' "
                 "(same hue, lighter, top). As in the original, the legend lists P1-P5 only (new-demand "
                 "entries are deleted from the legend in the source chart; the original separates them "
                 "by a black outline, kept here as a black box around the existing part of each bar, which the caption refers to). Chart axis uses display unit 'thousands' -> values divided by 1000."},
    22: {"note": "Original x axis is a date axis: years are placed proportionally (2018, 2020, 2025...). "
                 "Statnett Low/Mid/High share one colour and differ by dash style, as in the original."},
    29: {"colors": {"DHW_new": "#f9b48a", "DHW_ex": "#f47230",
                    "PS-H_new": "#a9cbf3", "C-H_new": "#5d9fe8", "PS-H_ex": "#257de0", "C-H_ex": "#0d4a8f",
                    "ElSpec_new": "#cfcfcf", "ElSpec_ex": "#8c8c8c"},
         "note": "Colour families as in the original: DHW oranges, heat (PS-H/C-H) blues, ElSpec greys; "
                 "new = lighter, existing = darker."},
    36: {"colors": {"Total": "#6b6b6b", ">50 ton, short": "#00b894", ">50 ton, long": "#8fdcc9",
                    "<50ton": "#f47230"},
         "note": "The two '>50 ton' series share one hue (long = lighter) as in the original, where they "
                 "differ only by outline style; their values are identical."},
    37: {"note": "Series colours repeat in the original (e.g. car/air); here every series has its own colour."},
    38: {"colors": {"Relative change - 2020-2050": "#191919"}, "secondary_ylim": (0, 1.4),
         "secondary_ymajor": 0.7,
         "note": "Original is a combo chart with a secondary y-axis (bars in GWh/year, triangle markers for "
                 "'Relative change - 2020-2050' on a right-hand axis 0-1.6). Re-drawn as two aligned panels "
                 "sharing the category axis (relative change on top) to avoid a dual-axis chart; values identical."},
    45: {"colors": {"Worst case": "#ec4647", "Best case": "#257de0"}, "xlim_pad": 0.5, "ylim_pad_low": 0.04,
         "note": "Axes padded by 0.5 \u00b0C / 4 % so points on the axis limits (e.g. Borbas at 20 \u00b0C, 0 %) "
                 "are fully visible; points outside the original axis range stay hidden as in the original. "
                 "Scatter: best/worst-case lines plus literature points with marker shapes as in the original."},
}

# Raster / EMF figures that are data plots and get digitized from the PDF
# render.  Filled in below (see DIGITIZE definition further down).
#
# Pixel calibrations below refer to the full-resolution images embedded in the
# docx (word/media/...); vector figures (EMF) are read from the PDF instead.
# If the source images change, re-check these numbers.
_LOAD_SERIES = [
    {"name": "Space heat, point source", "rgb": (29, 41, 130), "tol": 70},
    {"name": "Hot water, point source", "rgb": (224, 74, 27), "tol": 70},
    {"name": "Space heat and hot water, central heat", "rgb": (181, 139, 80), "tol": 30},
    {"name": "El-specific", "rgb": (128, 128, 128), "tol": 30},
]
_SEASONS_WSSF = ["Winter", "Spring", "Summer", "Fall"]


def _load_profile_cfg(x0, x24, y0px, y25px, legend_box, sep_cols):
    return {
        "method": "build_seasonal_profile", "chart_type": "line (digitized, 4 seasons x 24 h)",
        "seasons": _SEASONS_WSSF, "series": _LOAD_SERIES, "ylabel": "Commodity fraction", "edge_jump": 0.001,
        "ylim": (0, 0.0265), "yfmt": "0.000",
        # x: pixel of hour 0 (winter) and hour 24; hours 0..95 sampled
        "panels": [{"x_cal": [(x0, 0), (x24, 24)], "y_cal": [(y0px, 0.0), (y25px, 0.025)],
                    "xs": list(range(96))}],
        "exclude": [legend_box] + [(c - 4, 0, c + 5, 10000) for c in sep_cols],
        "note_base": "Digitized from the raster image by colour segmentation and axis calibration "
                     "(gridlines/ticks); estimated accuracy about +/-0.0003 (1-2 % of full scale) where lines "
                     "are visible; where thick lines overlap (e.g. hot water vs. el-specific) the hidden series "
                     "is interpolated and may deviate more. Seasons are drawn as separate 24-h segments as in "
                     "the original.",
    }


DIGITIZE: dict = {
    5: {"method": "build_pdf_vector_lines", "chart_type": "line (weekly, 16 weather years + black line)",
        "ylabel": "Unregulated hydroinflow NO2, GWh", "xlabel": "Week", "xlim": (0, 52), "xmajor": 2,
        "ylim": (0, 1200), "ylabel_max_dx": 75, "xlabel_max_dy": 40,
        "series_name": "series {k}", "black_name": "black line",
        "note_base": "EMF vector chart: the polylines were read from the PDF vector paths and calibrated "
                     "against the tick labels, so values are near-exact (<0.5 % of full scale). Series names "
                     "are not shown in the original (no legend); the 16 coloured lines are presumably the weather "
                     "years 2000-2015 in order and the black line the average. Drawn like Figure 7: thin lines "
                     "on a blue ramp, black line emphasised."},
    21: {"method": "build_pdf_vector_pies", "chart_type": "pie (two pies)", "split": "x",
         "note_base": "EMF vector pies: category names and values are the data labels printed in the original "
                      "(read from the PDF text layer; values are the rounded integers shown, TWh); pie titles "
                      "'All energy' and 'Electricity' as in the original. Shares therefore carry the rounding "
                      "of the printed labels (+/-0.5 TWh)."},
    31: _load_profile_cfg(145, 362, 476, 23, (505, 10, 1045, 170), [357, 574, 791]),
    32: _load_profile_cfg(145, 362, 476, 23, (505, 10, 1045, 170), [357, 574, 791]),
    33: _load_profile_cfg(147, 367, 483, 30, (520, 10, 1062, 180), [363, 583, 803]),
    34: {"method": "build_panels_lines", "chart_type": "scatter (2 panels, digitized)",
         "series": [{"name": "Air-water", "rgb": (29, 41, 130), "tol": 70, "marker": "x", "noline": True,
                     "ms": 3.5},
                    {"name": "Air-air", "rgb": (224, 74, 27), "tol": 70, "marker": "x", "noline": True,
                     "ms": 3.5}],
         "exclude": [(140, 30, 420, 150)], "interpolate": False, "win": 1, "sharex": True,
         "panels": [{"x_cal": [(133, -10), (1247, 20)], "y_cal": [(424, 1.75), (20, 3.75)],
                     "xs": list(np.round(np.arange(-8.75, 22.01, 0.25), 2)), "crop": (128, 20, 1377, 422),
                     "ylabel": "COP", "ylim": (1.75, 3.75), "xlim": (-10.5, 23.5)},
                    {"x_cal": [(133, -10), (1247, 20)], "y_cal": [(906, 0.4), (504, 1.2)],
                     "xs": list(np.round(np.arange(-8.75, 22.01, 0.25), 2)), "crop": (128, 505, 1377, 906),
                     "ylabel": "Available heat output", "xlabel": "Temperature (\u00b0C)", "ylim": (0.4, 1.2),
                     "xlim": (-10.5, 23.5)}],
         "note_base": "Digitized from the raster image: marker positions sampled every 0.25 \u00b0C where markers "
                      "are present (the original has one marker per temperature observation; here one marker per "
                      "0.25 \u00b0C bin). Estimated accuracy +/-0.02 COP and +/-0.01 heat output."},
    43: {"method": "build_panels_lines", "chart_type": "line (digitized)",
         "fill_leading_zero_below": 3, "extrapolate_end": 2, "cap": 100,
         "series": [
             {"name": "Nye personbiler", "rgb": (46, 117, 182), "tol": 70, "rank": 0, "dash": "dash",
              "color": "#257de0"},
             {"name": "Nye varebiler", "rgb": (236, 44, 117), "tol": 70, "rank": 0, "dash": "dash",
              "color": "#ec4647"},
             {"name": "Nye lastebiler og trekkvogner", "rgb": (112, 173, 71), "tol": 60, "rank": 0,
              "dash": "dash", "color": "#008a17"},
             {"name": "Bestanden av personbiler", "rgb": (46, 117, 182), "tol": 70, "rank": 1,
              "color": "#257de0"},
             {"name": "Bestanden av varebiler", "rgb": (236, 44, 117), "tol": 70, "rank": 1, "color": "#ec4647"},
             {"name": "Bestanden av lastebiler og trekkvogner", "rgb": (112, 173, 71), "tol": 60, "rank": 1,
              "color": "#008a17"}],
         "exclude": [(80, 70, 430, 205), (0, 662, 2000, 2000)],
         "panels": [{"x_cal": [(73.5, 2010), (971, 2050)], "y_cal": [(661, 0), (71, 100)],
                     "xs": list(range(2010, 2051)), "crop": (75, 60, 975, 662),
                     "ylabel": "Prosent", "ylim": (0, 100), "xlim": (2010, 2050), "xmajor": 5, "ymajor": 10}],
         "note_base": "Digitized from a screenshot of an external report. The embedded image also contains a "
                      "title and an external caption ('Figur 3.21 ...'), but both are cropped away in the report "
                      "(Word picture crop), so they are not shown here either; legend and axis labels verbatim. "
                      "Points hidden by the x-axis line (about 0 %) are set to 0, and the 2050 end points are "
                      "extrapolated by one year where the line ends just before the plot edge. Sampled "
                      "yearly 2010-2050; dashed (new vehicles) and solid (fleet) curves of the same colour are "
                      "separated by position (new >= fleet) and continuity. Estimated accuracy +/-1.5 "
                      "percentage points; around crossings and dash gaps values are interpolated."},
    46: {"method": "build_bars_seasonal", "chart_type": "bar (digitized, 96 time slices)",
         "seasons": ["Fall", "Winter", "Spring", "Summer"], "series_name": "Annual share of charging",
         "ylabel": "Annual share of charging", "rgb": (112, 173, 71), "tol": 50, "base_row": 400,
         "y_cal": [(403, 0.0), (23, 0.025)], "ylim": (0, 0.025), "yfmt": "0.000", "expect": 96,
         "note_base": "Digitized from the raster image: bar tops detected per bar (96 = 4 seasons x 24 h); "
                      "estimated accuracy +/-0.0001 (about 1 px)."},
    "11b": {"method": "build_panels_lines", "chart_type": "line (4 panels, digitized)", "image_index": 0,
            "part_of": 11, "ncols": 2, "sharey": True,
            "series": [{"name": "2030", "rgb": (80, 129, 189), "tol": 60},
                       {"name": "2040", "rgb": (192, 80, 77), "tol": 60},
                       {"name": "2050", "rgb": (155, 187, 89), "tol": 60}],
            "panels": [
                {"title": "Fall", "x_cal": [(86, 0), (622, 23)], "y_cal": [(419, 200), (37, 1200)],
                 "xs": list(range(24)), "crop": (87, 33, 622, 448), "ylabel": "NOK/MWh", "xlim": (0, 23), "ylim": (100, 1220),
                 "xmajor": 3},
                {"title": "Spring", "x_cal": [(654, 0), (1190, 23)], "y_cal": [(419, 200), (37, 1200)],
                 "xs": list(range(24)), "crop": (655, 33, 1190, 448), "xlim": (0, 23), "ylim": (100, 1220), "xmajor": 3},
                {"title": "Summer", "x_cal": [(86, 0), (622, 23)], "y_cal": [(918, 200), (536, 1200)],
                 "xs": list(range(24)), "crop": (87, 532, 622, 947), "ylabel": "NOK/MWh", "xlim": (0, 23), "ylim": (100, 1220),
                 "xmajor": 3},
                {"title": "Winter", "x_cal": [(654, 0), (1190, 23)], "y_cal": [(918, 200), (536, 1200)],
                 "xs": list(range(24)), "crop": (655, 532, 1190, 947), "xlim": (0, 23), "ylim": (100, 1220), "xmajor": 3}],
            "note_base": "Second part of Figure 11 (raster image, four seasonal panels, prices 2030/2040/2050). "
                         "Digitized hourly (0-23) by colour segmentation; estimated accuracy +/-10 NOK/MWh "
                         "(about 1 % of full scale); overlapping lines interpolated."},
}

# Original-figure crop tweaks for the contact sheet: extra page regions.
ORIG_CROP_EXTRA = {11: {"page_delta": -1}}

# =============================================================================
# Style
# =============================================================================

PALETTE = ["#257de0", "#f47230", "#00b894", "#f2a600", "#ee7fac", "#008a17",
           "#6a4ce2", "#ec4647", "#7f7f7f", "#8c564b", "#17becf", "#bcbd22",
           "#2f4b7c", "#a05195", "#d45087", "#665191"]
TEXT = "#191919"
TEXT2 = "#666666"
GRID = "#e3e3e3"
FIGSIZE = (8.0, 4.5)          # 16:9
DPI = 200

STYLE = {
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "axes.labelcolor": TEXT,
    "axes.edgecolor": "#9a9a9a",
    "axes.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.grid.axis": "y",
    "axes.axisbelow": True,
    "axes.prop_cycle": None,   # set at runtime
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "xtick.color": TEXT2,
    "ytick.color": TEXT2,
    "xtick.labelcolor": TEXT,
    "ytick.labelcolor": TEXT,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "xtick.major.size": 3,
    "ytick.major.size": 0,
    "legend.frameon": False,
    "legend.fontsize": 9,
    "lines.linewidth": 2.0,
    "lines.markersize": 5,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "svg.fonttype": "none",
}

# =============================================================================
# docx: figure discovery
# =============================================================================

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}
CAPTION_RE = re.compile(r"^\s*Figure\s*(\d+)")


def _q(tag):
    p, t = tag.split(":")
    return "{%s}%s" % (NS[p], t)


def _rels(z, path):
    """Return {rId: (target, mode)} for the part at ``path`` inside zip ``z``."""
    from lxml import etree
    d, f = path.rsplit("/", 1)
    rp = f"{d}/_rels/{f}.rels"
    if rp not in z.namelist():
        return {}
    root = etree.fromstring(z.read(rp))
    return {r.get("Id"): (r.get("Target"), r.get("TargetMode", "Internal")) for r in root}


def _norm(base_dir, target):
    parts = (base_dir + "/" + target).split("/")
    out = []
    for p in parts:
        if p == "..":
            out.pop()
        elif p and p != ".":
            out.append(p)
    return "/".join(out)


def find_figures(docx_path):
    """Return {num: {caption, items:[(kind, part_path)]}} in document order."""
    from lxml import etree
    z = zipfile.ZipFile(docx_path)
    doc = etree.fromstring(z.read("word/document.xml"))
    rels = _rels(z, "word/document.xml")
    body = doc.find(_q("w:body"))
    figs = {}
    pending = []
    for p in body.iter(_q("w:p")):
        text = "".join(t.text or "" for t in p.iter(_q("w:t")))
        for el in p.iter():
            if not isinstance(el.tag, str):
                continue
            tag = el.tag.split("}")[1]
            rid = None
            if tag == "chart" and el.tag == _q("c:chart"):
                rid = el.get(_q("r:id")); kind = "chart"
            elif tag == "blip":
                rid = el.get(_q("r:embed")); kind = "image"
            elif tag == "imagedata":
                rid = el.get(_q("r:id")); kind = "image"
            elif tag == "txbx":
                pending.append(("textbox", None)); continue
            else:
                continue
            if rid in rels:
                pending.append((kind, _norm("word", rels[rid][0])))
        m = CAPTION_RE.match(text)
        if m:
            n = int(m.group(1))
            if n not in figs:
                figs[n] = {"caption": re.sub(r"\s+", " ", text).strip(), "items": pending}
            pending = []
    return z, figs


# =============================================================================
# Chart XML parsing
# =============================================================================

def _rich_text(el):
    if el is None:
        return None
    paras = []
    for p in el.iter(_q("a:p")):
        paras.append("".join(t.text or "" for t in p.iter(_q("a:t"))))
    s = "\n".join(x for x in paras if x is not None).strip()
    if s:
        return s
    # title from a strRef
    for v in el.iter(_q("c:v")):
        return v.text
    return None


def _val(el, path, default=None):
    if el is None:
        return default
    x = el.find(path, NS)
    return x.get("val") if x is not None else default


def _cache_points(cache, apply_fmt=False):
    n = int(_val(cache, "c:ptCount", 0) or 0)
    out = [None] * n
    for pt in cache.findall("c:pt", NS):
        i = int(pt.get("idx"))
        v = pt.find("c:v", NS)
        if i >= len(out):
            out += [None] * (i + 1 - len(out))
        txt = v.text if v is not None else None
        if apply_fmt and pt.get("formatCode") and txt is not None:
            txt = fmt_excel(txt, pt.get("formatCode"))
        out[i] = txt
    return out


def _data_ref(el):
    """Parse a c:cat / c:val / c:tx / c:xVal / c:yVal element.

    Returns dict(f=formula, cache=list or list-of-levels, kind='num'|'str'|'multi'|'lit').
    """
    if el is None:
        return None
    for kind, tag, ctag in (("num", "c:numRef", "c:numCache"), ("str", "c:strRef", "c:strCache"),
                            ("multi", "c:multiLvlStrRef", "c:multiLvlStrCache")):
        ref = el.find(tag, NS)
        if ref is not None:
            f = ref.find("c:f", NS)
            cache = ref.find(ctag, NS)
            if kind == "multi":
                levels = [_cache_points(l) for l in cache.findall("c:lvl", NS)] if cache is not None else []
                n = int(_val(cache, "c:ptCount", 0) or 0)
                levels = [(l + [None] * n)[:n] for l in levels]
                return {"f": f.text if f is not None else None, "cache": levels, "kind": "multi",
                        "fmt": None}
            fmt = cache.find("c:formatCode", NS) if cache is not None else None
            return {"f": f.text if f is not None else None,
                    "cache": _cache_points(cache) if cache is not None else [],
                    "cache_fmt": _cache_points(cache, True) if cache is not None else [],
                    "kind": kind, "fmt": fmt.text if fmt is not None else None}
    for kind, tag in (("num", "c:numLit"), ("str", "c:strLit")):
        lit = el.find(tag, NS)
        if lit is not None:
            return {"f": None, "cache": _cache_points(lit), "kind": kind, "fmt": None}
    v = el.find("c:v", NS)
    if v is not None:
        return {"f": None, "cache": [v.text], "kind": "str", "fmt": None}
    return None


def _color(sppr):
    """First solid fill / line colour of a spPr, as (kind, value)."""
    if sppr is None:
        return None
    for path in ("a:solidFill", "a:ln/a:solidFill"):
        sf = sppr.find(path, NS)
        if sf is not None:
            for c in sf:
                mods = ",".join(f"{m.tag.split('}')[1]}={m.get('val')}" for m in c)
                return (c.tag.split("}")[1], c.get("val") + (f"[{mods}]" if mods else ""))
    if sppr.find("a:noFill", NS) is not None:
        return ("none", None)
    return None


def _line_props(sppr):
    if sppr is None:
        return {}
    ln = sppr.find("a:ln", NS)
    if ln is None:
        return {}
    d = {}
    dash = ln.find("a:prstDash", NS)
    if dash is not None:
        d["dash"] = dash.get("val")
    if ln.find("a:noFill", NS) is not None:
        d["noline"] = True
    if ln.get("w"):
        d["w"] = int(ln.get("w")) / 12700.0
    return d


_BUILTIN_UNITS = {"hundreds": 1e2, "thousands": 1e3, "tenThousands": 1e4, "hundredThousands": 1e5,
                  "millions": 1e6, "tenMillions": 1e7, "hundredMillions": 1e8, "billions": 1e9,
                  "trillions": 1e12}


def _disp_units(ax_el):
    du = ax_el.find("c:dispUnits", NS)
    if du is None:
        return 1.0
    b = _val(du, "c:builtInUnit")
    if b:
        return _BUILTIN_UNITS.get(b, 1.0)
    c = _val(du, "c:custUnit")
    return float(c) if c else 1.0


def _dlbl_range(ser):
    for el in ser.iter("{http://schemas.microsoft.com/office/drawing/2012/chart}dlblRangeCache"):
        return _cache_points(el)
    return None


def parse_chart(xml_bytes):
    from lxml import etree
    root = etree.fromstring(xml_bytes)
    chart = root.find("c:chart", NS)
    spec = {"title": None, "plots": [], "axes": {}, "legend": None}
    t = chart.find("c:title", NS)
    if t is not None and _val(chart, "c:autoTitleDeleted", "0") != "1":
        spec["title"] = _rich_text(t.find("c:tx", NS))
    elif t is not None:
        spec["title"] = _rich_text(t.find("c:tx", NS))
    pa = chart.find("c:plotArea", NS)
    for el in pa:
        tag = el.tag.split("}")[1]
        if tag.endswith("Chart"):
            plot = {"type": tag[:-5], "barDir": _val(el, "c:barDir"),
                    "grouping": _val(el, "c:grouping"), "overlap": _val(el, "c:overlap"),
                    "gapWidth": _val(el, "c:gapWidth"), "varyColors": _val(el, "c:varyColors"),
                    "scatterStyle": _val(el, "c:scatterStyle"),
                    "holeSize": _val(el, "c:holeSize"),
                    "axIds": [a.get("val") for a in el.findall("c:axId", NS)],
                    "dLbls": _val(el, "c:dLbls/c:showVal"), "series": []}
            for s in el.findall("c:ser", NS):
                sppr = s.find("c:spPr", NS)
                mk = s.find("c:marker", NS)
                ser = {"idx": int(_val(s, "c:idx", 0)), "order": int(_val(s, "c:order", 0)),
                       "tx": _data_ref(s.find("c:tx", NS)),
                       "cat": _data_ref(s.find("c:cat", NS)) or _data_ref(s.find("c:xVal", NS)),
                       "val": _data_ref(s.find("c:val", NS)) or _data_ref(s.find("c:yVal", NS)),
                       "color": _color(sppr), "line": _line_props(sppr),
                       "marker": _val(mk, "c:symbol") if mk is not None else None,
                       "smooth": _val(s, "c:smooth"),
                       "showVal": _val(s, "c:dLbls/c:showVal"),
                       "showPercent": _val(s, "c:dLbls/c:showPercent"),
                       "showCatName": _val(s, "c:dLbls/c:showCatName"),
                       "dlblRange": _dlbl_range(s),
                       "trendline": s.find("c:trendline", NS) is not None,
                       "errBars": s.find("c:errBars", NS) is not None,
                       "dPt": [int(_val(d, "c:idx")) for d in s.findall("c:dPt", NS)]}
                plot["series"].append(ser)
            spec["plots"].append(plot)
        elif tag in ("catAx", "valAx", "dateAx", "serAx"):
            title = el.find("c:title", NS)
            nf = el.find("c:numFmt", NS)
            spec["axes"][_val(el, "c:axId")] = {
                "kind": tag, "pos": _val(el, "c:axPos"), "delete": _val(el, "c:delete") == "1",
                "title": _rich_text(title.find("c:tx", NS)) if title is not None else None,
                "numFmt": nf.get("formatCode") if nf is not None else None,
                "srcLinked": nf.get("sourceLinked") if nf is not None else None,
                "min": _val(el, "c:scaling/c:min"), "max": _val(el, "c:scaling/c:max"),
                "orientation": _val(el, "c:scaling/c:orientation"),
                "logBase": _val(el, "c:scaling/c:logBase"),
                "majorUnit": _val(el, "c:majorUnit"),
                "crossAx": _val(el, "c:crossAx"), "crosses": _val(el, "c:crosses"),
                "crossesAt": _val(el, "c:crossesAt"),
                "gridlines": el.find("c:majorGridlines", NS) is not None,
                "tickLblPos": _val(el, "c:tickLblPos"),
                "noMultiLvlLbl": _val(el, "c:noMultiLvlLbl"),
                "tickLblSkip": _val(el, "c:tickLblSkip"),
                "dispUnits": _disp_units(el),
            }
    lg = chart.find("c:legend", NS)
    if lg is not None:
        spec["legend"] = {"pos": _val(lg, "c:legendPos", "r"),
                          "deleted": [int(_val(e, "c:idx")) for e in lg.findall("c:legendEntry", NS)
                                      if _val(e, "c:delete") == "1"]}
    return spec


# =============================================================================
# Workbook formula resolution
# =============================================================================

_REF_RE = re.compile(r"^(?:'?(?:\[[^\]]*\])?(?P<sheet>[^'!]+)'?!)?\$?(?P<c1>[A-Z]+)\$?(?P<r1>\d+)"
                     r"(?::\$?(?P<c2>[A-Z]+)\$?(?P<r2>\d+))?$")


def _split_union(f):
    f = f.strip()
    if f.startswith("(") and f.endswith(")"):
        f = f[1:-1]
    # split on commas not inside quotes
    parts, cur, q = [], "", False
    for ch in f:
        if ch == "'":
            q = not q
        if ch == "," and not q:
            parts.append(cur); cur = ""
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def resolve_formula(wb, f, multi=False):
    """Resolve a chart c:f formula against an openpyxl workbook (data_only).

    Returns a flat list (row-major for 1-D ranges), or for ``multi`` a list of
    levels (outermost first -> reversed to match chart cache order: innermost first).
    Returns None if anything fails.
    """
    from openpyxl.utils import column_index_from_string as ci
    if wb is None or not f:
        return None
    blocks = []
    sheet_last = None
    for part in _split_union(f):
        m = _REF_RE.match(part)
        if not m:
            return None
        sheet = m.group("sheet") or sheet_last
        sheet_last = sheet
        if sheet not in wb.sheetnames:
            return None
        ws = wb[sheet]
        c1, r1 = ci(m.group("c1")), int(m.group("r1"))
        c2 = ci(m.group("c2")) if m.group("c2") else c1
        r2 = int(m.group("r2")) if m.group("r2") else r1
        grid = [[ws.cell(r, c).value for c in range(c1, c2 + 1)] for r in range(r1, r2 + 1)]
        blocks.append(grid)
    if multi:
        # categories run along the longer dimension; levels along the shorter
        grid = blocks[0]
        nr, nc = len(grid), len(grid[0])
        if nr >= nc:   # categories in rows, levels in columns (outer = first col)
            levels = [[grid[r][c] for r in range(nr)] for c in range(nc)]
        else:
            levels = [[grid[r][c] for c in range(nc)] for r in range(nr)]
        return levels[::-1]
    flat = []
    for grid in blocks:
        nr, nc = len(grid), len(grid[0])
        if nr == 1 or nc == 1:
            flat += [v for row in grid for v in row]
        else:  # 2-D for a name/1-D: join cells (e.g. series name in 2 cells)
            if nr >= nc:
                flat += [" ".join(str(v) for v in row if v is not None) for row in grid]
            else:
                flat += [" ".join(str(grid[r][c]) for r in range(nr) if grid[r][c] is not None)
                         for c in range(nc)]
    return flat


def _num(v):
    if v is None or v == "":
        return np.nan
    try:
        return float(v)
    except (TypeError, ValueError):
        return np.nan


def _same(a, b, tol=1e-6):
    """Compare workbook values with cache values."""
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        fx, fy = _num(x), _num(y)
        if np.isnan(fx) and np.isnan(fy):
            if x not in (None, "") and y not in (None, "") and str(x).strip() != str(y).strip():
                return False
            continue
        if np.isnan(fx) != np.isnan(fy):
            return False
        if abs(fx - fy) > tol * max(1, abs(fy)):
            return False
    return True


def load_embedded_workbook(z, chart_part):
    """Return (openpyxl workbook or None, description) for a chart part."""
    import openpyxl
    rels = _rels(z, chart_part)
    for rid, (target, mode) in rels.items():
        if mode == "External":
            continue
        path = _norm(chart_part.rsplit("/", 1)[0], target)
        if not path.startswith("word/embeddings/"):
            continue
        data = z.read(path)
        if path.endswith(".bin"):
            try:
                import olefile
                ole = olefile.OleFileIO(io.BytesIO(data))
                for name in ole.listdir():
                    s = ole.openstream(name).read()
                    if s[:2] == b"PK":
                        data = s
                        break
                else:
                    return None, f"{path} (OLE, no xlsx package inside)"
            except Exception as e:  # noqa
                return None, f"{path} (OLE unreadable: {e})"
        try:
            wb = openpyxl.load_workbook(io.BytesIO(data), data_only=True)
            return wb, path
        except Exception as e:  # noqa
            return None, f"{path} (unreadable: {e})"
    ext = [t for t, m in rels.values() if m == "External" and t != "NULL"]
    return None, ("external link: " + ext[0]) if ext else "no workbook"


def chart_data(spec, wb):
    """Fill every series with resolved data: ser['name'], ser['cats'], ser['vals'].

    Returns source label: 'embedded-xlsx' if all formulas resolved from the
    workbook and matched (or replaced) the cache, else 'chart-cache'.
    Also records mismatches in spec['_mismatch'].
    """
    used_wb = wb is not None
    spec["_mismatch"] = []
    for plot in spec["plots"]:
        for s in plot["series"]:
            for key in ("tx", "cat", "val"):
                ref = s[key]
                if ref is None:
                    s["_" + key] = None
                    continue
                cache = ref.get("cache_fmt") if key == "cat" and ref.get("cache_fmt") else ref["cache"]
                if key == "tx" and cache and any(c not in (None, "") for c in cache):
                    s["_tx"] = cache          # names: what Word displays
                    continue
                res = resolve_formula(wb, ref["f"], multi=ref["kind"] == "multi") if wb else None
                if res is not None and key != "tx" and ref["kind"] != "multi" and cache and \
                        not _same(res, cache):
                    spec["_mismatch"].append(f"{ref['f']}")
                if res is None or (ref["kind"] == "multi" and len(res) != len(cache)):
                    if wb is not None and ref["f"]:
                        used_wb = False
                    res = cache
                elif key == "tx" and cache and str(res[0]).strip() != str(cache[0]).strip():
                    spec["_mismatch"].append(f"name {ref['f']}: wb={res[0]!r} cache={cache[0]!r}")
                s["_" + key] = res
            nm = s["_tx"]
            s["name"] = (" ".join(str(x) for x in nm if x is not None).strip() if nm else
                         f"Series {s['idx'] + 1}")
            vals = s["_val"] or []
            s["vals"] = [_num(v) for v in vals]
            c = s["_cat"]
            if c is None:
                s["cats"] = list(range(1, len(vals) + 1))
            elif s["cat"]["kind"] == "multi":
                s["cats"] = c       # list of levels, innermost first
            else:
                s["cats"] = c
    return "embedded-xlsx" if (wb is not None and used_wb) else "chart-cache"


# =============================================================================
# PDF: caption location and original-figure crops
# =============================================================================

def find_pdf_captions(pdf, captions):
    """Return {num: (page_no, caption_rect)} matching docx caption text."""
    import fitz
    out = {}
    for page in pdf:
        for b in page.get_text("blocks"):
            txt = re.sub(r"\s+", " ", b[4]).strip()
            m = re.search(r"Figure\s*(\d+)", txt)
            if not m:
                continue
            n = int(m.group(1))
            if n in out or n not in captions:
                continue
            ref = re.sub(r"\s+", "", captions[n])[:40]
            # the caption may be preceded by other text in the same block
            if re.sub(r"\s+", "", txt[m.start():])[:40] != ref[:len(re.sub(r"\s+", "", txt[m.start():])[:40])]:
                continue
            # locate the exact line rect
            rect = None
            for inst in page.search_for(f"Figure {n}") + page.search_for(f"Figure{n}"):
                if inst.y0 >= b[1] - 1 and inst.y1 <= b[3] + 1:
                    rect = fitz.Rect(inst.x0, inst.y0, b[2], b[3])
                    break
            out[n] = (page.number, rect or fitz.Rect(b[:4]))
    return out


def pdf_figure_rect(page, cap_rect):
    """Bounding box of the figure graphics directly above a caption."""
    import fitz
    W = page.rect.width
    items = []
    for info in page.get_image_info():
        items.append(fitz.Rect(info["bbox"]))
    for d in page.get_drawings():
        r = d["rect"]
        if r.width < 0.5 and r.height < 0.5:
            continue
        items.append(fitz.Rect(r))
    items = [r & page.rect for r in items]
    items = [r for r in items if r.y1 <= cap_rect.y0 + 2 and r.y1 > cap_rect.y0 - 600
             and not (r.height < 2 and r.width > 0.7 * W)]          # skip header rules
    if not items:
        return None
    # seed: the item whose bottom is closest to the caption
    items.sort(key=lambda r: cap_rect.y0 - r.y1)
    if cap_rect.y0 - items[0].y1 > 40:
        return None
    box = fitz.Rect(items[0])
    changed = True
    while changed:
        changed = False
        for r in items:
            if r in box:
                continue
            if r.y1 >= box.y0 - 14 and r.y0 <= box.y1 + 2 and not box.contains(r):
                nb = box | r
                if nb != box:
                    box = nb
                    changed = True
    # include text that lies inside/at the edge of the graphics (axis labels etc.)
    for b in page.get_text("blocks"):
        tr = fitz.Rect(b[:4])
        if tr.y1 <= cap_rect.y0 + 1 and abs(tr & box) > 0.5 * abs(tr):
            box |= tr
    return box


def render_pdf_crop(pdf_path, page_no, rect, out_png, zoom=2.5):
    import fitz
    doc = fitz.open(pdf_path)
    page = doc[page_no]
    clip = fitz.Rect(rect.x0 - 4, rect.y0 - 4, rect.x1 + 4, rect.y1 + 4) & page.rect
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
    pix.save(out_png)
    return clip


# =============================================================================
# Number formats
# =============================================================================

def _fmt_parts(code):
    """(is_percent, decimals, thousands) from an Excel number format."""
    if not code or code == "General":
        return None
    sec = code.split(";")[0]
    sec = re.sub(r'"[^"]*"|\\.|_.|\*.', "", sec)
    pct = "%" in sec
    m = re.search(r"0\.(0+)", sec)
    dec = len(m.group(1)) if m else 0
    thou = "," in sec
    if not re.search(r"[0#]", sec):
        return None
    return pct, dec, thou


def fmt_excel(v, code):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return v
    parts = _fmt_parts(code)
    if parts is None:
        return v if isinstance(v, str) else f"{x:g}"
    pct, dec, thou = parts
    if pct:
        x *= 100
    s = f"{x:,.{dec}f}" if thou else f"{x:.{dec}f}"
    return s + ("%" if pct else "")


def axis_formatter(code):
    from matplotlib.ticker import FuncFormatter
    parts = _fmt_parts(code)
    if parts is None:
        return None
    pct, dec, thou = parts

    def f(x, _pos):
        if pct:
            x *= 100
        s = f"{x:,.{dec}f}" if thou else f"{x:.{dec}f}"
        if s.startswith("-") and float(s.replace(",", "").rstrip("%") or 0) == 0:
            s = s[1:]
        return s + ("%" if pct else "")
    return FuncFormatter(f)


def _label(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


# =============================================================================
# Chart spec -> plotting model
# =============================================================================
#
# A "model" is a renderer-independent description used both for native charts
# and digitized figures:
#   {kind: 'category'|'xy'|'pie', levels: [inner, outer...] (category kind),
#    series: [{name, type: bar|line|area|scatter, vals | x,y, dash, marker,
#              noline, legend, color, stack}],
#    barh, grouping, xlabel, ylabel, title, yfmt, xfmt, ylim, xlim, ymajor,
#    xmajor, legend, secondary: {series, ylabel, yfmt, ylim}}
#   or {panels: [model, ...], ncols, sharey, legend}

DASH = {"dash": (0, (5, 2.5)), "sysDash": (0, (3, 1.5)), "sysDot": (0, (1, 1.5)),
        "lgDash": (0, (8, 3)), "dashDot": (0, (5, 2, 1, 2)), "sysDashDot": (0, (3, 1, 1, 1)),
        "lgDashDot": (0, (8, 3, 1, 3)), "solid": "-"}
MARKER = {"circle": "o", "square": "s", "diamond": "D", "triangle": "^", "x": "x",
          "star": "*", "plus": "P", "dash": "_", "dot": ".", "none": None, None: None}


def _ax_of(spec, plot):
    val = cat = None
    for a in plot["axIds"]:
        ax = spec["axes"].get(a)
        if ax is None:
            continue
        if ax["kind"] == "valAx" and (val is None or plot["type"] == "scatter"):
            if plot["type"] == "scatter" and ax["pos"] in ("b", "t"):
                cat = ax
            else:
                val = ax
        elif ax["kind"] in ("catAx", "dateAx"):
            cat = ax
    return cat, val


def chart_to_model(spec, fig_no):
    plots = spec["plots"]
    if not plots:
        return None
    p0 = plots[0]
    legend_on = spec["legend"] is not None
    deleted = set(spec["legend"]["deleted"]) if legend_on else set()
    if p0["type"] in ("pie", "doughnut", "pie3D"):
        s = p0["series"][0]
        labels = [_label(c) for c in s["cats"]]
        val_fmt = (s["val"] or {}).get("fmt")
        dl = []
        for i, v in enumerate(s["vals"]):
            parts = []
            if s.get("dlblRange"):
                parts.append(s["dlblRange"][i] or "")
            if s.get("showVal") == "1":
                parts.append(fmt_excel(v, val_fmt) if val_fmt and val_fmt != "General" else _label(v))
            dl.append(", ".join(p for p in parts if p))
        return {"kind": "pie", "labels": labels, "vals": s["vals"], "dlabels": dl,
                "title": spec["title"], "legend": legend_on, "name": s["name"],
                "donut": p0["type"] == "doughnut"}
    model = {"kind": "xy" if p0["type"] == "scatter" else "category", "series": [],
             "title": spec["title"], "legend": legend_on, "grouping": p0["grouping"] or "standard",
             "barh": p0["barDir"] == "bar", "gap": float(p0["gapWidth"] or 150)}
    cat_ax, val_ax = _ax_of(spec, p0)
    secondary = []
    for plot in plots:
        c_ax, v_ax = _ax_of(spec, plot)
        is_sec = v_ax is not None and val_ax is not None and v_ax is not val_ax
        typ = {"bar": "bar", "line": "line", "area": "area", "scatter": "scatter"}.get(plot["type"], "line")
        for s in sorted(plot["series"], key=lambda s: s["order"]):
            unit = (v_ax or {}).get("dispUnits", 1.0) or 1.0
            vals = [v / unit for v in s["vals"]] if unit != 1.0 else s["vals"]
            entry = {"name": s["name"], "type": typ, "vals": vals,
                     "ckey": s["color"][1] if s["color"] else None,
                     "dash": DASH.get(s["line"].get("dash")), "marker": MARKER.get(s["marker"]),
                     "noline": bool(s["line"].get("noline")) and typ in ("line", "scatter"),
                     "legend": s["idx"] not in deleted, "smooth": s["smooth"] == "1",
                     "stack": plot["grouping"] if plot["grouping"] in ("stacked", "percentStacked") else None,
                     "idx": s["idx"]}
            if typ == "line" and s["marker"] is None and plot.get("type") == "line":
                entry["marker"] = None
            if typ == "scatter":
                entry["x"] = [_num(v) for v in s["cats"]]
                entry["y"] = vals
                if model["kind"] != "xy":
                    pass
            (secondary if is_sec else model["series"]).append(entry)
    # categories from the first series of the primary plot
    if model["kind"] == "category":
        s0 = p0["series"][0]
        if s0["cat"] is not None and s0["cat"]["kind"] == "multi":
            model["levels"] = [[_label(v).strip() for v in lvl] for lvl in s0["cats"]]
        else:
            model["levels"] = [[_label(v).strip() for v in s0["cats"]]]
        model["date_axis"] = cat_ax is not None and cat_ax["kind"] == "dateAx"
    if cat_ax:
        model["xlabel"] = cat_ax["title"]
        model["xfmt"] = cat_ax["numFmt"] if model["kind"] == "xy" else None
        if model["kind"] == "xy":
            model["xlim"] = (_num(cat_ax["min"]), _num(cat_ax["max"]))
            model["xmajor"] = _num(cat_ax["majorUnit"])
        model["x_reverse"] = cat_ax["orientation"] == "maxMin"
    if val_ax:
        model["ylabel"] = val_ax["title"]
        model["yfmt"] = val_ax["numFmt"]
        model["ylim"] = (_num(val_ax["min"]), _num(val_ax["max"]))
        model["ymajor"] = _num(val_ax["majorUnit"])
        model["y_reverse"] = val_ax["orientation"] == "maxMin"
    if secondary:
        _, v2 = _ax_of(spec, plots[-1])
        model["secondary"] = {"series": secondary, "ylabel": v2["title"] if v2 else None,
                              "yfmt": v2["numFmt"] if v2 else None,
                              "ylim": (_num(v2["min"]), _num(v2["max"])) if v2 else (np.nan, np.nan)}
    return model


# =============================================================================
# Rendering
# =============================================================================

def setup_style(style_file=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from cycler import cycler
    st = dict(STYLE)
    st["axes.prop_cycle"] = cycler(color=PALETTE)
    plt.rcParams.update(st)
    if style_file and Path(style_file).exists():
        plt.style.use(str(style_file))
    return plt


def _lighten(hex_color, amount):
    import matplotlib.colors as mc
    r, g, b = mc.to_rgb(hex_color)
    return mc.to_hex((r + (1 - r) * amount, g + (1 - g) * amount, b + (1 - b) * amount))


def _darken(hex_color, amount):
    import matplotlib.colors as mc
    r, g, b = mc.to_rgb(hex_color)
    return mc.to_hex((r * (1 - amount), g * (1 - amount), b * (1 - amount)))


def _next_free(k, taken):
    for j in range(len(PALETTE)):
        if PALETTE[(k + j) % len(PALETTE)].lower() not in taken:
            return k + j
    return k


def assign_colors(series, cfg=None):
    cfg = cfg or {}
    explicit = cfg.get("colors", {})
    # Series that share the original colour AND are told apart by dash style in
    # the original keep one shared colour (colour follows the entity family).
    fam = {}
    for s in series:
        if s.get("ckey"):
            fam.setdefault(s["ckey"], []).append(s)
    shared = {k for k, v in fam.items()
              if len(v) > 1 and len({str(x.get("dash")) for x in v}) == len(v)}
    blacks = [s for s in series if s.get("ckey") in ("sysClr:windowText", "schemeClr:tx1", "srgbClr:000000")
              or str(s.get("ckey", "")).split("[")[0] in ("windowText", "tx1", "000000")]
    if len(blacks) == 1 and blacks[0]["type"] in ("line", "scatter") and not blacks[0].get("color"):
        blacks[0]["color"] = TEXT          # a single black series (Total/Average) stays black
    taken = {c.lower() for c in explicit.values()}
    k = 0
    used = {}
    for s in series:
        if s.get("color"):
            continue
        if s["name"] in explicit:
            s["color"] = explicit[s["name"]]
            continue
        if s.get("ckey") in shared:
            if s["ckey"] not in used:
                k = _next_free(k, taken)
                used[s["ckey"]] = PALETTE[k % len(PALETTE)]
                k += 1
            s["color"] = used[s["ckey"]]
            continue
        k = _next_free(k, taken)
        s["color"] = PALETTE[k % len(PALETTE)]
        k += 1


def _ylim(ax, lim, horizontal=False):
    lo, hi = lim if lim else (np.nan, np.nan)
    get, set_ = (ax.get_xlim, ax.set_xlim) if horizontal else (ax.get_ylim, ax.set_ylim)
    cur = get()
    lo = cur[0] if lo is None or np.isnan(lo) else lo
    hi = cur[1] if hi is None or np.isnan(hi) else hi
    set_(lo, hi)


def _major(ax, unit, horizontal=False):
    from matplotlib.ticker import MultipleLocator
    if unit is not None and not np.isnan(unit):
        (ax.xaxis if horizontal else ax.yaxis).set_major_locator(MultipleLocator(unit))


def _group_spans(level, blank=None):
    """Excel multi-level: a label at idx i spans until the next label."""
    idx = [i for i, v in enumerate(level) if v not in ("", None)]
    spans = []
    for j, i in enumerate(idx):
        end = idx[j + 1] - 1 if j + 1 < len(idx) else len(level) - 1
        while blank is not None and end > i and blank[end]:
            end -= 1
        spans.append((i, end, level[i]))
    return spans


def _draw_category_axis(ax, levels, horizontal, max_labels=36, blank=None):
    """Inner labels as ticks, outer levels as grouped labels with separators."""
    import matplotlib.transforms as mt
    inner = levels[0]
    n = len(inner)
    pos = np.arange(n)
    nonempty = [i for i, v in enumerate(inner) if v != ""]
    step = 1
    if len(nonempty) > max_labels:
        step = int(np.ceil(len(nonempty) / max_labels))
    ticks = nonempty[::step] if len(nonempty) < n else list(range(0, n, step))
    labels = [inner[i] for i in ticks]
    axis = ax.yaxis if horizontal else ax.xaxis
    axis.set_ticks(pos[ticks])
    axis.set_ticklabels(labels)
    if not horizontal:
        import textwrap
        width_pt = ax.figure.get_figwidth() * 72 * 0.85
        slot = width_pt / max(1, len(labels))          # points available per label
        chars = int(slot / 5.6)                        # ~5.6 pt per character at 9 pt
        longest = max((len(l) for l in labels), default=0)
        if longest > chars:
            if chars >= 6 and all(len(l) <= 3 * chars for l in labels):
                axis.set_ticklabels([textwrap.fill(l, chars, break_long_words=False) for l in labels])
            else:
                for t in ax.get_xticklabels():
                    t.set_rotation(90)
                    t.set_ha("center")
    ax.tick_params(axis="y" if horizontal else "x", length=0)
    if len(levels) == 1:
        return 0
    m_lines = sum(max((str(v).count("\n") + 1 for v in l if v), default=1) for l in levels[1:])
    # outer levels
    for depth, lvl in enumerate(levels[1:], start=1):
        spans = _group_spans(lvl, blank)
        lvl_lines = max((str(v).count("\n") + 1 for v in lvl if v), default=1)
        for (a, b, text) in spans:
            mid = (a + b) / 2.0
            if horizontal:
                tr = mt.blended_transform_factory(ax.transAxes, ax.transData)
                ax.annotate(text, xy=(0, mid), xycoords=tr, xytext=(-34 - 46 * (depth - 1), 0),
                            textcoords="offset points", ha="right", va="center",
                            fontsize=9, color=TEXT, annotation_clip=False)
                for edge in (a - 0.5, b + 0.5):
                    ax.annotate("", xy=(0, edge), xycoords=tr, xytext=(-30 - 46 * (depth - 1), 0),
                                textcoords="offset points",
                                arrowprops=dict(arrowstyle="-", color=GRID, lw=0.8),
                                annotation_clip=False)
            else:
                tr = mt.blended_transform_factory(ax.transData, ax.transAxes)
                inner_lines = max((str(t.get_text()).count("\n") + 1 for t in ax.get_xticklabels()), default=1)
                prev_lines = sum(max((str(v).count("\n") + 1 for v in l if v), default=1)
                                 for l in levels[1:depth])
                off = -8 - 12 * inner_lines - 12 * prev_lines - 4 * (depth - 1)
                ax.annotate(text, xy=(mid, 0), xycoords=tr, xytext=(0, off),
                            textcoords="offset points", ha="center", va="top",
                            fontsize=9, color=TEXT, annotation_clip=False, linespacing=1.1)
                if a > 0:
                    ax.annotate("", xy=(a - 0.5, 0), xycoords=tr, xytext=(0, off - 12 * (lvl_lines - 1) - 2),
                                textcoords="offset points",
                                arrowprops=dict(arrowstyle="-", color="#bdbdbd", lw=0.8),
                                annotation_clip=False)
    return m_lines


def draw_category(ax, m):
    levels = m["levels"]
    n = len(levels[0])
    x = np.arange(n, dtype=float)
    if m.get("date_axis"):
        try:
            x = np.array([float(v) for v in levels[0]])
        except ValueError:
            pass
    horizontal = m.get("barh", False)
    series = m["series"]
    bars = [s for s in series if s["type"] == "bar"]
    handles = []
    if bars:
        stacked = any(s.get("stack") for s in bars)
        pct = any(s.get("stack") == "percentStacked" for s in bars)
        group_w = 1.0 / (1.0 + m.get("gap", 150) / 100.0)
        group_w = max(group_w, 0.5) if not stacked else min(max(group_w, 0.45), 0.8)
        if m.get("gap", 150) == 0:
            group_w = 1.0
        if stacked:
            vals = np.array([[0 if np.isnan(v) else v for v in s["vals"][:n]] + [0] * (n - len(s["vals"]))
                             for s in bars])
            if pct:
                tot = np.abs(vals).sum(axis=0)
                tot[tot == 0] = 1
                vals = vals / tot
            pos_base = np.zeros(n)
            neg_base = np.zeros(n)
            for s, v in zip(bars, vals):
                base = np.where(v >= 0, pos_base, neg_base)
                kw = dict(color=s["color"], edgecolor="white", linewidth=0.6 if n < 60 else 0,
                          label=s["name"])
                if horizontal:
                    h = ax.barh(x, v, height=group_w, left=base, **kw)
                else:
                    h = ax.bar(x, v, width=group_w, bottom=base, **kw)
                pos_base = pos_base + np.where(v >= 0, v, 0)
                neg_base = neg_base + np.where(v < 0, v, 0)
                if s.get("legend", True):
                    handles.append(h)
            if m.get("box_series"):
                # black box around the stacked total of the listed (bottom) series
                tot = sum(v for s, v in zip(bars, vals) if s["name"] in m["box_series"])
                from matplotlib.patches import Rectangle
                for xi, t in zip(x, tot):
                    if t > 0:
                        r = (Rectangle((0, xi - group_w / 2), t, group_w) if horizontal else
                             Rectangle((xi - group_w / 2, 0), group_w, t))
                        r.set(fill=False, edgecolor=TEXT, linewidth=1.3, zorder=5)
                        ax.add_patch(r)
        else:
            k = len(bars)
            w = group_w / k
            for i, s in enumerate(bars):
                v = np.array(s["vals"][:n], dtype=float)
                off = (i - (k - 1) / 2.0) * w
                kw = dict(color=s["color"], edgecolor="white",
                          linewidth=0.6 if (w * 72 > 6 and m.get("gap", 150) > 0) else 0,
                          label=s["name"])
                if horizontal:
                    h = ax.barh(x + off, v, height=w, **kw)
                else:
                    h = ax.bar(x + off, v, width=w, **kw)
                if s.get("legend", True):
                    handles.append(h)
    areas = [s for s in series if s["type"] == "area"]
    if areas:
        vals = np.array([[0 if np.isnan(v) else v for v in s["vals"][:n]] for s in areas])
        polys = ax.stackplot(x, vals, colors=[s["color"] for s in areas],
                             labels=[s["name"] for s in areas], edgecolor="white", linewidth=0.6)
        handles += [p for p, s in zip(polys, areas) if s.get("legend", True)]
        ax.set_xlim(x[0], x[-1])
    lines = [s for s in series if s["type"] in ("line",)]
    if lines:
        stacked = any(s.get("stack") for s in lines) and len(lines) > 1
        base = np.zeros(n)
        for s in lines:
            v = np.array(s["vals"][:n] + [np.nan] * (n - len(s["vals"])), dtype=float)
            if stacked:
                v = base + np.nan_to_num(v)
                base = v
            kw = dict(color=s["color"], label=s["name"], lw=s.get("lw", 2.0),
                      linestyle=s.get("dash") or "-", zorder=s.get("zorder", 3))
            if s.get("noline"):
                kw["linestyle"] = "none"
            if s.get("marker"):
                kw.update(marker=s["marker"], markersize=s.get("ms", 5 if not s.get("noline") else 7),
                          markeredgecolor="white", markeredgewidth=0.6)
            if horizontal:
                h, = ax.plot(v, x, **kw)
            else:
                h, = ax.plot(x, v, **kw)
            if s.get("legend", True):
                handles.append(h)
    if not m.get("date_axis"):
        pad = 0.5 if (bars or m.get("pad", False)) else 0.0
        if horizontal:
            ax.set_ylim(-0.5, n - 0.5)
        elif not areas:
            if bars:
                ax.set_xlim(-0.5, n - 0.5)
            else:
                ax.set_xlim(-0.25 if n < 40 else 0, n - 0.75 if n < 40 else n - 1)
        blank = [levels[0][i] == "" and all(np.isnan(_num((s["vals"] + [None] * n)[i])) for s in series)
                 for i in range(n)]
        depth = _draw_category_axis(ax, levels, horizontal, blank=blank)
    else:
        depth = 0
        ax.set_xlim(x.min(), x.max())
        ax.set_xticks([v for v in x])
        ax.set_xticklabels([_label(v) for v in levels[0]])
    m["_depth"] = depth
    return handles


def draw_xy(ax, m):
    handles = []
    for s in m["series"]:
        x = np.array(s["x"], dtype=float)
        y = np.array(s["y"], dtype=float)
        kw = dict(color=s["color"], label=s["name"], lw=s.get("lw", 2.0),
                  linestyle=s.get("dash") or "-", zorder=s.get("zorder", 3))
        if s.get("noline"):
            kw["linestyle"] = "none"
        if s.get("marker"):
            kw.update(marker=s["marker"], markersize=s.get("ms", (10 if s["marker"] == "*" else 7)
                                                         if s.get("noline") else 4),
                      markeredgecolor="white", markeredgewidth=0.5)
            if s["marker"] in ("x", "+", "_", "|", "1", "2", "3", "4"):
                kw.update(markeredgecolor=s["color"], markeredgewidth=1.1)
        h, = ax.plot(x, y, **kw)
        if s.get("legend", True):
            handles.append(h)
    ax.grid(True, axis="both" if m.get("grid_x", True) else "y")
    for v in m.get("vlines", []):
        ax.axvline(v, color="#c8c8c8", lw=1.0, zorder=1)
    if m.get("xticks"):
        import matplotlib.transforms as mt
        pos, labs = m["xticks"]
        ax.set_xticks(pos)
        ax.set_xticklabels(labs)
        tr = mt.blended_transform_factory(ax.transData, ax.transAxes)
        for (a, b, text) in m.get("xgroups", []):
            ax.annotate(text, xy=((a + b) / 2, 0), xycoords=tr, xytext=(0, -20), textcoords="offset points",
                        ha="center", va="top", fontsize=9, color=TEXT, annotation_clip=False)
        if m.get("xgroups"):
            m["_depth"] = 1
    return handles


def draw_pie(ax, m):
    vals = np.array(m["vals"], dtype=float)
    cols = m.get("colors") or [PALETTE[i % len(PALETTE)] for i in range(len(vals))]
    wedges, _ = ax.pie(np.nan_to_num(vals), colors=cols, startangle=90, counterclock=False,
                       wedgeprops=dict(edgecolor="white", linewidth=1.5,
                                       width=0.45 if m.get("donut") else None))
    tot = np.nansum(vals)
    for w, lab in zip(wedges, m["dlabels"]):
        if not lab:
            continue
        ang = np.deg2rad((w.theta1 + w.theta2) / 2)
        r = 1.12
        an = ax.annotate(lab, xy=(np.cos(ang), np.sin(ang)), xytext=(r * np.cos(ang) * 1.04, r * np.sin(ang) * 1.04),
                         ha="left" if np.cos(ang) >= 0 else "right", va="center", fontsize=9, color=TEXT,
                         arrowprops=dict(arrowstyle="-", color="#9a9a9a", lw=0.6, shrinkA=0, shrinkB=0))
        an.set_in_layout(False)      # let the pie use the available height
    ax.set_aspect("equal")
    lim = m.get("pie_lim", (2.15, 1.3))
    ax.set_xlim(-lim[0], lim[0])
    ax.set_ylim(-lim[1], lim[1])
    ax.grid(False)
    for w, lab in zip(wedges, m["labels"]):
        w.set_label(lab)
    return list(wedges)


def apply_axes(ax, m):
    horizontal = m.get("barh", False) and m["kind"] == "category"
    if horizontal:
        ax.grid(True, axis="x")
        ax.grid(False, axis="y")
        ax.tick_params(axis="x", length=0)
    if m.get("ylabel"):
        (ax.set_xlabel if horizontal else ax.set_ylabel)(m["ylabel"])
    if m.get("xlabel"):
        if horizontal:
            ax.set_ylabel(m["xlabel"])
        else:
            ax.set_xlabel(m["xlabel"], labelpad=4 + 12 * m.get("_depth", 0) + 4)
    fmt = axis_formatter(m.get("yfmt"))
    if fmt:
        (ax.xaxis if horizontal else ax.yaxis).set_major_formatter(fmt)
        parts = _fmt_parts(m.get("yfmt"))
        if parts and (parts[1] == 0 or (parts[0] and parts[1] == 0)):
            from matplotlib.ticker import MaxNLocator
            (ax.xaxis if horizontal else ax.yaxis).set_major_locator(
                MaxNLocator(nbins="auto", steps=[1, 2, 2.5, 5, 10], integer=not parts[0]))
    if m["kind"] == "xy":
        fx = axis_formatter(m.get("xfmt"))
        if fx:
            ax.xaxis.set_major_formatter(fx)
        _ylim(ax, m.get("xlim"), horizontal=True)
        _major(ax, m.get("xmajor"), horizontal=True)
    lim = list(m.get("ylim") or (np.nan, np.nan))
    if lim[0] is None or np.isnan(lim[0]):
        ys = np.concatenate([np.asarray(s.get("vals") if s.get("vals") is not None else s.get("y", []), float)
                             for s in m.get("series", [])] or [np.array([])])
        ys = ys[~np.isnan(ys)]
        if ys.size and ys.min() >= 0 and ys.max() > 0 and (ys.max() - ys.min()) / ys.max() > 1 / 6:
            lim[0] = 0.0       # Excel's automatic axis minimum
    _ylim(ax, lim, horizontal)
    _major(ax, m.get("ymajor"), horizontal)
    if m.get("y_reverse"):
        (ax.invert_xaxis if horizontal else ax.invert_yaxis)()
    if m.get("x_reverse"):
        (ax.invert_yaxis if horizontal else ax.invert_xaxis)()
    if m.get("panel_title"):
        ax.set_title(m["panel_title"], fontsize=10, color=TEXT, loc="center")


def draw_model(ax, m):
    if m["kind"] == "pie":
        return draw_pie(ax, m)
    if m["kind"] == "xy":
        h = draw_xy(ax, m)
    else:
        h = draw_category(ax, m)
    apply_axes(ax, m)
    return h


def _legend(fig, handles, labels, ncol=None, anchor_ax=None):
    if not handles:
        return
    if ncol is None:
        longest = max(len(l) for l in labels)
        per = max(1, int(120 / (longest + 6)))
        ncol = min(len(labels), per, 6)
        # balance rows
        rows = int(np.ceil(len(labels) / ncol))
        ncol = int(np.ceil(len(labels) / rows))
    fig.legend(handles, labels, loc="outside lower center", ncol=ncol, frameon=False,
               handlelength=1.8, columnspacing=1.4, borderaxespad=0.2)


def render(model, out_base, cfg=None):
    """Draw a model (or multi-panel model) and save png+svg."""
    import matplotlib.pyplot as plt
    cfg = cfg or {}
    figsize = cfg.get("figsize", FIGSIZE)
    fig = plt.figure(figsize=figsize, layout="constrained")
    panels = model.get("panels")
    handles, labels = [], []

    def collect(hs):
        for h in hs:
            lab = h.get_label() if hasattr(h, "get_label") else None
            if isinstance(h, list) or lab is None:
                continue
            if lab.startswith("_") or lab in labels:
                continue
            handles.append(h); labels.append(lab)

    if panels:
        ncols = model.get("ncols", len(panels))
        nrows = int(np.ceil(len(panels) / ncols))
        axs = fig.subplots(nrows, ncols, sharey=model.get("sharey", False),
                           sharex=model.get("sharex", False), squeeze=False,
                           height_ratios=model.get("height_ratios"))
        for ax, pm in zip(axs.flat, panels):
            for s in pm.get("series", []):
                pass
            hs = draw_model(ax, pm)
            if pm["kind"] == "pie":
                if pm.get("panel_title"):
                    ax.set_title(pm["panel_title"], fontsize=10, color=TEXT)
                if model.get("legend", True) and not labels:
                    collect(hs)
            else:
                collect(hs)
        for ax in list(axs.flat)[len(panels):]:
            ax.set_visible(False)
        if model.get("title"):
            fig.suptitle(model["title"], fontsize=11, color=TEXT)
    elif model.get("secondary"):
        sec = model["secondary"]
        ax2, ax = fig.subplots(2, 1, sharex=True, height_ratios=[1, 2.6])
        fig.get_layout_engine().set(hspace=0.12)
        if cfg.get("secondary_ylim"):
            sec["ylim"] = cfg["secondary_ylim"]
        if cfg.get("secondary_ymajor"):
            sec["ymajor"] = cfg["secondary_ymajor"]
        collect(draw_model(ax, model))
        sm = {"kind": "category", "levels": model["levels"], "series": sec["series"],
              "ylabel": sec["ylabel"], "yfmt": sec["yfmt"], "ylim": sec["ylim"], "ymajor": sec.get("ymajor")}
        hs = draw_category(ax2, sm)
        apply_axes(ax2, sm)
        ax2.tick_params(axis="x", labelbottom=False)
        ax2.set_xlabel("")
        collect(hs)
        if model.get("title"):
            ax2.set_title(model["title"])
    else:
        ax = fig.subplots()
        collect(draw_model(ax, model))
        if model.get("title"):
            ax.set_title(model["title"], color=TEXT, pad=8)
    if model.get("legend", True) and len(labels) >= 1 and not (len(labels) == 1 and model.get("kind") != "pie"
                                                                and not model.get("force_legend")):
        _legend(fig, handles, labels, cfg.get("legend_ncol"))
    for ext in ("png", "svg"):
        fig.savefig(f"{out_base}.{ext}", dpi=DPI)
    plt.close(fig)


def model_to_frame(model):
    """Tidy table of exactly what is plotted."""
    import pandas as pd
    if model.get("panels"):
        frames = []
        for i, pm in enumerate(model["panels"]):
            f = model_to_frame(pm)
            f.insert(0, "panel", pm.get("panel_title") or pm.get("ylabel") or f"panel {i + 1}")
            frames.append(f)
        return pd.concat(frames, ignore_index=True)
    if model["kind"] == "pie":
        d = {"category": model["labels"], "value": model["vals"]}
        if any(model["dlabels"]):
            d["data_label"] = model["dlabels"]
        return pd.DataFrame(d)
    if model["kind"] == "xy":
        rows = []
        for s in model["series"]:
            for x, y in zip(s["x"], s["y"]):
                rows.append({"series": s["name"], "x": x, "y": y})
        return pd.DataFrame(rows)
    levels = model["levels"]
    n = len(levels[0])
    d = {}
    for k, lvl in reversed(list(enumerate(levels))):
        # forward-fill outer levels so every row is self-describing
        if k > 0:
            cur, filled = "", []
            for v in lvl:
                cur = v if v else cur
                filled.append(cur)
            lvl = filled
        d["category" if k == 0 else f"group{k}"] = lvl
    cols = {}
    allser = model["series"] + (model.get("secondary") or {}).get("series", [])
    for s in allser:
        name = s["name"]
        while name in cols:
            name += " (dup)"
        cols[name] = list(s["vals"][:n]) + [np.nan] * (n - len(s["vals"]))
    d.update(cols)
    return pd.DataFrame(d)


# =============================================================================
# Driver
# =============================================================================

def build_chart_figure(z, n, chart_part):
    spec = parse_chart(z.read(chart_part))
    wb, wb_desc = load_embedded_workbook(z, chart_part)
    source = chart_data(spec, wb)
    model = chart_to_model(spec, n)
    cfg = CHART_OVERRIDES.get(n, {})
    if cfg.get("box_series"):
        model["box_series"] = cfg["box_series"]
    if cfg.get("xlim_pad") and model.get("xlim"):
        model["xlim"] = (model["xlim"][0] - cfg["xlim_pad"], model["xlim"][1] + cfg["xlim_pad"])
    if cfg.get("ylim_pad_low") is not None:
        lo, hi = model.get("ylim") or (np.nan, np.nan)
        model["ylim"] = ((0 if np.isnan(lo) else lo) - cfg["ylim_pad_low"], hi)
    if "patch" in cfg:
        cfg["patch"](model)
    if model["kind"] != "pie":
        allser = model["series"] + (model.get("secondary") or {}).get("series", [])
        apply_series_overrides(model, cfg)
        assign_colors(allser, cfg)
        for name, (base, amt) in cfg.get("tint_of", {}).items():
            b = next((x for x in allser if x["name"] == base), None)
            for x in allser:
                if x["name"] == name and b is not None:
                    x["color"] = _lighten(b["color"], amt)
    note = []
    if source == "embedded-xlsx":
        note.append(f"data from {wb_desc} via chart series formulas")
        if spec["_mismatch"]:
            note.append("workbook differs from chart cache for: " + "; ".join(spec["_mismatch"][:4]))
    else:
        note.append(f"data from chart cache (workbook: {wb_desc})")
    if cfg.get("note"):
        note.append(cfg["note"])
    ctype = cfg.get("chart_type_label") or describe_type(spec)
    return model, source, ctype, " ".join(note)


def apply_series_overrides(model, cfg):
    """Dedupe identical series, emphasis/ramps, marker thinning (see CHART_OVERRIDES)."""
    seen, keep = set(), []
    for x in model["series"]:
        key = (x["name"], tuple(np.round(np.nan_to_num(np.asarray(x.get("vals") or x.get("y"), float)), 9)))
        if key in seen:
            continue
        seen.add(key)
        keep.append(x)
    model["series"] = keep
    mx = cfg.get("marker_max_points")
    if mx:
        for x in model["series"]:
            if len(x.get("vals") or x.get("y") or []) > mx:
                x["marker"] = None
    hl = cfg.get("highlight", {})
    if hl:
        others = [x for x in model["series"] if x["name"] not in hl]
        import matplotlib
        cmap = matplotlib.colormaps["Blues"]
        for i, x in enumerate(others):
            x["color"] = matplotlib.colors.to_hex(cmap(0.3 + 0.6 * i / max(1, len(others) - 1)))
            x["lw"] = 1.0
            x["legend"] = False
        for x in model["series"]:
            if x["name"] in hl:
                x.update(hl[x["name"]])
        # draw emphasised series last
        model["series"] = others + [x for x in model["series"] if x["name"] in hl]


def describe_type(spec):
    p = spec["plots"][0]
    t = p["type"]
    if t == "bar":
        t = ("horizontal " if p["barDir"] == "bar" else "") + f"bar ({p['grouping']})"
    elif t in ("line", "area"):
        t = f"{t} ({p['grouping']})" if p["grouping"] not in (None, "standard") else t
    if len(spec["plots"]) > 1:
        t += " + " + ", ".join(q["type"] for q in spec["plots"][1:])
    return t


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--docx", required=True)
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--out", default="mirror/figures")
    ap.add_argument("--only", type=int, nargs="*", help="only these figure numbers")
    ap.add_argument("--no-contact-sheet", action="store_true")
    args = ap.parse_args(argv)
    import warnings
    warnings.filterwarnings("ignore")
    import fitz
    out = Path(args.out)
    (out / "data").mkdir(parents=True, exist_ok=True)
    (out / "_orig").mkdir(parents=True, exist_ok=True)
    plt = setup_style(Path(__file__).with_name("restyle_style.mplstyle"))

    z, figs = find_figures(args.docx)
    pdf = fitz.open(args.pdf)
    caps = find_pdf_captions(pdf, {n: f["caption"] for n, f in figs.items()})
    man_path = out / "manifest.json"
    manifest = json.loads(man_path.read_text()) if (args.only and man_path.exists()) else {}

    for n in sorted(figs):
        if args.only and n not in args.only:
            continue
        f = figs[n]
        kinds = [k for k, _ in f["items"]]
        parts = [p for _, p in f["items"] if p]
        charts = [p for k, p in f["items"] if k == "chart"]
        entry = {"caption_start": f["caption"][:80], "docx_parts": parts}
        # original crop from the PDF
        if n in caps:
            pno, crect = caps[n]
            box = pdf_figure_rect(pdf[pno], crect)
            extra = ORIG_CROP_EXTRA.get(n)
            if box is not None and extra:
                pg = pdf[pno + extra["page_delta"]]
                gr = [fitz.Rect(dr["rect"]) for dr in pg.get_drawings()
                      if 60 < dr["rect"].y0 and dr["rect"].y1 < pg.rect.height - 60 and dr["rect"].height > 2]
                if gr:
                    u = gr[0]
                    for r in gr[1:]:
                        u |= r
                    a_ = str(out / "_orig" / f"_a{n:02d}.png")
                    b_ = str(out / "_orig" / f"_b{n:02d}.png")
                    render_pdf_crop(args.pdf, pno + extra["page_delta"], u, a_)
                    render_pdf_crop(args.pdf, pno, box, b_)
                    _stack_images([a_, b_], str(out / "_orig" / f"orig{n:02d}.png"))
                    entry["pdf_page"] = pno + 1
                    entry["pdf_bbox"] = [round(v, 1) for v in box]
                    entry["pdf_extra_regions"] = [{"pdf_page": pno + extra["page_delta"] + 1,
                                                   "pdf_bbox": [round(v, 1) for v in u],
                                                   "content": "native chart part"}]
                    box = None
            if box is not None:
                render_pdf_crop(args.pdf, pno, box, str(out / "_orig" / f"orig{n:02d}.png"))
                entry["pdf_page"] = pno + 1
                entry["pdf_bbox"] = [round(v, 1) for v in box]
        base = out / f"fig{n:02d}"
        try:
            if n in ORIGINAL_ONLY and n not in DIGITIZE:
                entry.update(file=None, source="original", chart_type="diagram",
                             notes=ORIGINAL_ONLY[n] + "; not a data plot, use original image/PDF crop")
            elif n in DIGITIZE:
                d = DIGITIZE[n]
                model = globals()[d["method"]](args, pdf, caps.get(n), z, f, d)
                assign_colors(_all_series(model), d)
                render(model, base, d)
                model_to_frame(model).to_csv(out / "data" / f"fig{n:02d}.csv", index=False)
                entry.update(file=base.name + ".png", source="digitized", chart_type=d["chart_type"],
                             notes=d["note"])
            elif charts:
                model, source, ctype, note = build_chart_figure(z, n, charts[0])
                render(model, base, CHART_OVERRIDES.get(n, {}))
                model_to_frame(model).to_csv(out / "data" / f"fig{n:02d}.csv", index=False)
                entry.update(file=base.name + ".png", source=source, chart_type=ctype, notes=note)
                for key, d in DIGITIZE.items():
                    if isinstance(key, str) and d.get("part_of") == n:
                        model = globals()[d["method"]](args, pdf, caps.get(n), z, f, d)
                        render(model, out / f"fig{key}", d)
                        model_to_frame(model).to_csv(out / "data" / f"fig{key}.csv", index=False)
                        entry.setdefault("extra_files", []).append(
                            {"file": f"fig{key}.png", "source": "digitized", "chart_type": d["chart_type"],
                             "notes": d["note"]})
            else:
                entry.update(file=None, source="original",
                             chart_type="image" if "image" in kinds else "other",
                             notes="no native chart and no digitizing config; kept as original")
        except Exception as e:  # keep going, record failure
            import traceback
            traceback.print_exc()
            entry.update(file=None, source="original", chart_type="?",
                         notes=f"re-draw failed ({type(e).__name__}: {e}); use original")
        manifest[str(n)] = entry
        print(f"Figure {n:2d}: {entry['source']:13s} {entry.get('chart_type','')}")

    manifest = {k: manifest[k] for k in sorted(manifest, key=int)}
    man_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    if not args.no_contact_sheet:
        contact_sheet(out, manifest)
    return 0


def _stack_images(paths, out_path):
    from PIL import Image
    ims = [Image.open(p).convert("RGB") for p in paths]
    w = max(i.width for i in ims)
    h = sum(i.height for i in ims)
    canvas = Image.new("RGB", (w, h), "white")
    y = 0
    for i in ims:
        canvas.paste(i, ((w - i.width) // 2, y))
        y += i.height
    canvas.save(out_path)
    for p in paths:
        Path(p).unlink()


def _all_series(model):
    if model.get("panels"):
        return []          # panel builders assign colours themselves
    return model.get("series", []) + (model.get("secondary") or {}).get("series", [])


def contact_sheet(out, manifest):
    """Grid: original PDF crop | restyled, for every re-drawn figure."""
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    items = [(int(k), v) for k, v in manifest.items() if v.get("file")]
    if not items:
        return
    ncol = 2   # pairs per row
    rows = int(np.ceil(len(items) / ncol))
    fig, axs = plt.subplots(rows, ncol * 2, figsize=(ncol * 2 * 4.2, rows * 2.6), squeeze=False)
    for ax in axs.flat:
        ax.axis("off")
    for i, (n, v) in enumerate(items):
        r, c = divmod(i, ncol)
        o = out / "_orig" / f"orig{n:02d}.png"
        if o.exists():
            axs[r, 2 * c].imshow(mpimg.imread(o))
        axs[r, 2 * c].set_title(f"Fig {n} original (PDF)", fontsize=8)
        axs[r, 2 * c + 1].imshow(mpimg.imread(out / v["file"]))
        axs[r, 2 * c + 1].set_title(f"Fig {n} restyled [{v['source']}]", fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "contact_sheet.png", dpi=110)
    plt.close(fig)



# =============================================================================
# Digitizing (raster images and vector EMF renders in the PDF)
# =============================================================================

def _runs(mask):
    out, s = [], None
    for i, v in enumerate(mask):
        if v and s is None:
            s = i
        elif not v and s is not None:
            out.append((s, i - 1)); s = None
    if s is not None:
        out.append((s, len(mask) - 1))
    return out


def _lin(p0, v0, p1, v1):
    """Linear map pixel -> value and its inverse."""
    a = (v1 - v0) / (p1 - p0)
    return (lambda p: v0 + (p - p0) * a), (lambda v: p0 + (v - v0) / a)


def _load_image(z, fig, index=0):
    from PIL import Image
    imgs = [p for k, p in fig["items"] if k == "image"]
    data = z.read(imgs[index])
    im = Image.open(io.BytesIO(data))
    if im.mode == "P":
        im = im.convert("RGBA")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    if im.mode == "RGBA":
        bg.paste(im, mask=im.split()[3])
    else:
        bg.paste(im.convert("RGB"))
    return np.asarray(bg).astype(int), imgs[index]


def _color_mask(a, rgb, tol, exclude=()):
    d = np.sqrt(((a - np.array(rgb)) ** 2).sum(2))
    m = d < tol
    for (x0, y0, x1, y1) in exclude:
        m[y0:y1, x0:x1] = False
    return m


def _interp_nans(v, limit=None):
    v = np.array(v, float)
    n = np.isnan(v)
    if n.all() or not n.any():
        return v, 0
    idx = np.arange(len(v))
    inside = (idx > idx[~n].min()) & (idx < idx[~n].max())
    fill = n & inside
    v[fill] = np.interp(idx[fill], idx[~n], v[~n])
    return v, int(fill.sum())


def trace_line(mask, xs_px, y_of, win=2, prev_hint=None):
    """Median y (value units) of mask pixels in a column window, continuity-aware."""
    out = []
    prev = prev_hint
    for xp in xs_px:
        x0, x1 = int(round(xp)) - win, int(round(xp)) + win + 1
        col = mask[:, max(0, x0):x1].any(axis=1)
        rs = _runs(col)
        if not rs:
            out.append(np.nan); continue
        cands = [(a + b) / 2.0 for a, b in rs]
        if prev is None or len(cands) == 1:
            y = cands[int(np.argmax([b - a for a, b in rs]))] if prev is None else cands[0]
        else:
            y = min(cands, key=lambda c: abs(c - prev))
        prev = y
        out.append(y_of(y))
    return np.array(out, float)


def digitize_lines(a, d):
    """Generic line digitizer.  d: panels[{x_cal, y_cal, xs, crop}], series[{name, rgb, tol, rank}]."""
    panels = []
    total_interp = 0
    for p in d["panels"]:
        (px0, vx0), (px1, vx1) = p["x_cal"]
        (py0, vy0), (py1, vy1) = p["y_cal"]
        _, x_px = _lin(px0, vx0, px1, vx1)
        y_of, _ = _lin(py0, vy0, py1, vy1)
        xs = np.asarray(p["xs"], float)
        x0, y0, x1, y1 = p.get("crop", (0, 0, a.shape[1], a.shape[0]))
        sub_ex = d.get("exclude", [])
        series = []
        groups = {}
        for s in d["series"]:
            groups.setdefault(tuple(s["rgb"]), []).append(s)
        for rgb, ss in groups.items():
            m = _color_mask(a, rgb, ss[0].get("tol", 60), sub_ex)
            m[:y0, :] = False; m[y1:, :] = False; m[:, :x0] = False; m[:, x1:] = False
            if len(ss) == 1:
                v = trace_line(m, [x_px(x) for x in xs], y_of, d.get("win", 2))
                vals = {ss[0]["name"]: v}
            else:     # several curves of the same colour, ordered top (rank 0) to bottom
                k = len(ss)
                tracks = [[] for _ in range(k)]
                prev = [None] * k
                for xp in [x_px(x) for x in xs]:
                    col = m[:, max(0, int(round(xp)) - 1):int(round(xp)) + 2].any(axis=1)
                    cands = [(r0 + r1) / 2.0 for r0, r1 in _runs(col)]
                    assign = [None] * k
                    if len(cands) >= k:
                        cands = sorted(cands)[:k] if len(cands) == k else sorted(cands)
                        # choose k candidates closest to previous, else top-k
                        if len(cands) > k and all(p_ is not None for p_ in prev):
                            cands = sorted(sorted(cands, key=lambda c: min(abs(c - p_) for p_ in prev))[:k])
                        for i in range(k):
                            assign[i] = cands[i]
                    elif len(cands) >= 1:
                        for c in cands:
                            # nearest previous track
                            opts = [(abs(c - prev[i]) if prev[i] is not None else 1e9, i) for i in range(k)
                                    if assign[i] is None]
                            if opts:
                                assign[min(opts)[1]] = c
                    for i in range(k):
                        tracks[i].append(y_of(assign[i]) if assign[i] is not None else np.nan)
                        if assign[i] is not None:
                            prev[i] = assign[i]
                vals = {s_["name"]: np.array(tracks[s_.get("rank", i)]) for i, s_ in enumerate(ss)}
            for name, v in vals.items():
                if d.get("interpolate", True):
                    v, nfill = _interp_nans(v)
                    total_interp += nfill
                series.append((name, v))
        order = [s["name"] for s in d["series"]]
        series.sort(key=lambda t: order.index(t[0]))
        panels.append((p, xs, series))
    return panels, total_interp


def digitize_bars(a, d):
    (py0, vy0), (py1, vy1) = d["y_cal"]
    y_of, _ = _lin(py0, vy0, py1, vy1)
    m = _color_mask(a, d["rgb"], d.get("tol", 60))
    base_row = d["base_row"]
    rs = [r for r in _runs(m[base_row]) if r[1] - r[0] >= 2]
    vals = []
    for (x0, x1) in rs:
        xc = (x0 + x1) // 2
        col = m[:, xc - 1:xc + 2].any(axis=1)
        ys = np.where(col[:base_row + 1])[0]
        vals.append(y_of(ys.min() - 0.5) if ys.size else np.nan)
    return np.array(vals)


def pdf_vector_polylines(page, box, min_points=10):
    """Stroked polylines inside ``box``: list of (rgb, [(x,y),...])."""
    import fitz
    out = []
    for dr in page.get_drawings():
        if dr.get("type") != "s" or not fitz.Rect(dr["rect"]).intersects(box):
            continue
        items = [it for it in dr["items"] if it[0] == "l"]
        if len(items) < min_points:
            continue
        pts = [(items[0][1].x, items[0][1].y)] + [(it[2].x, it[2].y) for it in items]
        out.append((dr["color"], pts))
    return out


def pdf_axis_calibration(page, box, axis="y", max_x=None, min_y=None, exclude_below=None):
    """Fit value=f(pixel) from numeric tick labels found as words in ``box``.

    y-axis labels are snapped to the horizontal axis/grid line next to them when one
    exists (text bounding boxes are not vertically centred on the tick).
    """
    import fitz
    hlines = []
    if axis == "y":
        for dr in page.get_drawings():
            for it in dr["items"]:
                if it[0] == "l" and abs(it[1].y - it[2].y) < 0.2 and abs(it[1].x - it[2].x) > 0.4 * box.width \
                        and fitz.Rect(dr["rect"]).intersects(box):
                    hlines.append((it[1].y, min(it[1].x, it[2].x)))
    pts = []
    for w in page.get_text("words"):
        r = fitz.Rect(w[:4])
        if not r.intersects(box):
            continue
        try:
            v = float(w[4].replace(",", ""))
        except ValueError:
            continue
        if axis == "y" and max_x is not None and r.x1 <= max_x and \
                (exclude_below is None or r.y0 < exclude_below):
            yc = (r.y0 + r.y1) / 2
            near = [y for y, x0 in hlines if abs(y - yc) < 4 and x0 >= r.x1 - 2]
            pts.append((yc, v, min(near, key=lambda y: abs(y - yc)) if near else None))
        if axis == "x" and min_y is not None and r.y0 >= min_y:
            pts.append(((r.x0 + r.x1) / 2, v))
    if axis == "y" and pts:
        # text boxes sit slightly off their tick: measure the offset on labels that
        # have an axis/grid line and apply it to all labels
        offs = [ln - yc for yc, _, ln in pts if ln is not None]
        bias = float(np.mean(offs)) if offs else 0.0
        pts = [(ln if ln is not None else yc + bias, v) for yc, v, ln in pts]
    p = np.array(pts)
    a, b = np.polyfit(p[:, 0], p[:, 1], 1)
    resid = np.abs(p[:, 1] - (a * p[:, 0] + b)).max()
    return (lambda q: a * q + b), resid, len(pts)


# ---- per-figure builders (settings live in DIGITIZE below) --------------------

def _season_axis(model, seasons, per=24, ticks=(6, 12, 18, 24)):
    model["xticks"] = ([k * per + t for k in range(len(seasons)) for t in ticks],
                       [str(t) for _ in seasons for t in ticks])
    model["xgroups"] = [(k * per, (k + 1) * per, s) for k, s in enumerate(seasons)]
    return model


def build_seasonal_profile(args, pdf, cap, z, fig, d):
    a, part = _load_image(z, fig, d.get("image_index", 0))
    panels, nfill = digitize_lines(a, d)
    p, xs, series = panels[0]
    m = {"kind": "xy", "series": [], "ylabel": d["ylabel"], "xlabel": d.get("xlabel"),
         "ylim": d.get("ylim"), "xlim": (0, 24 * len(d["seasons"])), "yfmt": d.get("yfmt"),
         "legend": True, "grid_x": False}
    for k in range(len(d["seasons"])):
        pass
    thr = d.get("edge_jump")
    nfix = 0
    for name, v in series:
        # reject spikes at season edges (separator bars / anti-aliasing): replace an edge
        # point that jumps more than ``edge_jump`` by linear extrapolation from inside
        if thr:
            for k in range(len(d["seasons"])):
                b0, b1 = 24 * k, 24 * k + 23
                for i, j, jj in ((b0 + 1, b0 + 2, b0 + 3), (b0, b0 + 1, b0 + 2),
                                 (b1 - 1, b1 - 2, b1 - 3), (b1, b1 - 1, b1 - 2)):
                    if abs(v[i] - v[j]) > thr and abs(v[j] - v[jj]) < thr / 2:
                        v[i] = v[j] + (v[j] - v[jj]); nfix += 1
        # break the line at season boundaries like the original
        x = xs.copy().astype(float)
        y = v.copy()
        xx, yy = [], []
        for k in range(len(d["seasons"])):
            sel = (x >= 24 * k) & (x < 24 * (k + 1))
            xx += list(x[sel]) + [np.nan]
            yy += list(y[sel]) + [np.nan]
        m["series"].append({"name": name, "x": xx, "y": yy, "type": "line", "lw": 2.0})
    m["vlines"] = [24 * k for k in range(1, len(d["seasons"]))]
    _season_axis(m, d["seasons"])
    d["_csv_extra"] = None
    d["note"] = d["note_base"] + (f" Source image {part}; {nfill} hidden/overlapped points linearly "
                                  f"interpolated; {nfix} season-edge spikes replaced by extrapolation.")
    return m


def build_bars_seasonal(args, pdf, cap, z, fig, d):
    a, part = _load_image(z, fig, d.get("image_index", 0))
    vals = digitize_bars(a, d)
    n = len(vals)
    per = n // len(d["seasons"])
    inner = ["" for _ in range(n)]
    for k in range(len(d["seasons"])):
        for t in (6, 12, 18, 24):
            inner[k * per + t - 1] = str(t)
    outer = ["" for _ in range(n)]
    for k, s in enumerate(d["seasons"]):
        outer[k * per] = s
    m = {"kind": "category", "levels": [inner, outer], "series": [
        {"name": d["series_name"], "type": "bar", "vals": list(vals), "legend": False}],
        "ylabel": d["ylabel"], "ylim": d.get("ylim"), "gap": 30, "legend": False, "yfmt": d.get("yfmt")}
    d["note"] = d["note_base"] + f" Source image {part}; {n} bars detected (expected {d.get('expect', n)})."
    if d.get("expect") and n != d["expect"]:
        raise RuntimeError(f"bar detection found {n} bars, expected {d['expect']}")
    return m


def build_panels_lines(args, pdf, cap, z, fig, d):
    a, part = _load_image(z, fig, d.get("image_index", 0))
    panels, nfill = digitize_lines(a, d)
    pm = []
    for (p, xs, series) in panels:
        for i, (name, v) in enumerate(series):
            v = np.array(v, float)
            ok = np.where(~np.isnan(v))[0]
            if ok.size and d.get("fill_leading_zero_below") is not None and \
                    v[ok[0]] < d["fill_leading_zero_below"]:
                v[:ok[0]] = 0.0
            ne = d.get("extrapolate_end", 0)
            if ok.size >= 2 and ne and len(v) - 1 - ok[-1] <= ne:
                a_, b_ = v[ok[-2]], v[ok[-1]]
                for j in range(ok[-1] + 1, len(v)):
                    v[j] = min(b_ + (b_ - a_) * (j - ok[-1]), d.get("cap", np.inf))
            series[i] = (name, v)
        sm = {"kind": "xy", "series": [], "panel_title": p.get("title"), "ylabel": p.get("ylabel"),
              "xlabel": p.get("xlabel"), "ylim": p.get("ylim"), "xlim": p.get("xlim"),
              "xmajor": p.get("xmajor"), "ymajor": p.get("ymajor"), "yfmt": p.get("yfmt")}
        for (name, v), s in zip(series, d["series"]):
            e = {"name": name, "x": list(xs), "y": list(v), "type": "line",
                 "color": s.get("color"), "marker": s.get("marker"), "noline": s.get("noline", False),
                 "ms": s.get("ms"), "dash": DASH.get(s.get("dash")) if s.get("dash") else None}
            if e["ms"] is None:
                e.pop("ms")
            sm["series"].append(e)
        assign_colors(sm["series"], d)
        pm.append(sm)
    model = {"panels": pm, "ncols": d.get("ncols", 1), "sharex": d.get("sharex", False),
             "sharey": d.get("sharey", False), "title": d.get("title"), "legend": True}
    if len(pm) == 1:
        model = dict(pm[0], title=d.get("title"), legend=True)
    d["note"] = d["note_base"] + f" Source image {part}; {nfill} hidden/overlapped points linearly interpolated."
    return model


def build_pdf_vector_lines(args, pdf, cap, z, fig, d):
    """EMF line chart rendered as vectors in the PDF: exact polyline coordinates."""
    import fitz
    pno, crect = cap
    page = pdf[pno]
    box = pdf_figure_rect(page, crect)
    lines = pdf_vector_polylines(page, box, d.get("min_points", 10))
    fy, ry, ny = pdf_axis_calibration(page, box, "y", max_x=box.x0 + d["ylabel_max_dx"],
                                      exclude_below=box.y1 - d["xlabel_max_dy"])
    fx, rx, nx = pdf_axis_calibration(page, box, "x", min_y=box.y1 - d["xlabel_max_dy"])
    series = []
    k = 0
    for rgb, pts in lines:
        xs = [round(fx(x), 2) for x, _ in pts]
        xs = [round(x) if abs(x - round(x)) < 0.15 else x for x in xs]
        ys = [fy(y) for _, y in pts]
        black = max(rgb) < 0.05
        if black:
            name = d["black_name"]
        else:
            k += 1
            name = d["series_name"].format(k=k)
        series.append({"name": name, "x": xs, "y": ys, "type": "line", "_black": black})
    others = [s for s in series if not s["_black"]]
    blacks = [s for s in series if s["_black"]]
    import matplotlib
    cmap = matplotlib.colormaps["Blues"]
    for i, s in enumerate(others):
        s.update(color=matplotlib.colors.to_hex(cmap(0.3 + 0.6 * i / max(1, len(others) - 1))),
                 lw=1.0, legend=False)
    for s in blacks:
        s.update(color=TEXT, lw=2.6, zorder=10, legend=False)
    m = {"kind": "xy", "series": others + blacks, "ylabel": d["ylabel"], "xlabel": d["xlabel"],
         "xlim": d.get("xlim"), "xmajor": d.get("xmajor"), "ylim": d.get("ylim"), "legend": False}
    d["note"] = (d["note_base"] + f" Extracted {len(series)} vector polylines from PDF page {pno + 1}; "
                 f"axis calibration from {ny} y-tick and {nx} x-tick labels (max residual "
                 f"{max(ry, rx):.3g} axis units).")
    return m


def build_pdf_vector_pies(args, pdf, cap, z, fig, d):
    """EMF pie charts rendered in the PDF: labels 'NAME, value' read from PDF text."""
    import fitz
    pno, crect = cap
    page = pdf[pno]
    box = pdf_figure_rect(page, crect)
    mid = (box.x0 + box.x1) / 2 if d.get("split") == "x" else None
    words = [w for w in page.get_text("words") if fitz.Rect(w[:4]).intersects(box)]
    wedges = [dr for dr in page.get_drawings()
              if dr.get("fill") is not None and fitz.Rect(dr["rect"]).intersects(box)
              and dr.get("color") is not None and min(dr["color"]) > 0.95
              and fitz.Rect(dr["rect"]).width < box.width / 2]
    pies = []
    for side in (0, 1):
        ws = [w for w in words if ((w[0] + w[2]) / 2 < mid) == (side == 0)]
        wd = [dr for dr in wedges if ((dr["rect"].x0 + dr["rect"].x1) / 2 < mid) == (side == 0)]
        labels, cur, title = [], [], []
        for w in ws:
            t = w[4]
            if re.fullmatch(r"[\d.,]+", t):
                labels.append((" ".join(x[4] for x in cur), float(t.replace(",", "")),
                               fitz.Rect(cur[0][:4]) | fitz.Rect(w[:4])))
                cur = []
            else:
                cur.append(w)
        title = " ".join(x[4] for x in cur)
        # order categories by the wedges (draw order = data order), matching by angle
        u = fitz.Rect(wd[0]["rect"])
        for dr in wd:
            u |= dr["rect"]
        cx, cy = (u.x0 + u.x1) / 2, (u.y0 + u.y1) / 2

        def ang(x, y):
            return np.arctan2(y - cy, x - cx)

        def wedge_angle(dr):
            pts = []
            for it in dr["items"]:
                for q in it[1:]:
                    if hasattr(q, "x"):
                        pts.append((q.x, q.y))
            pts = np.array(pts)
            far = pts[np.hypot(pts[:, 0] - cx, pts[:, 1] - cy) > 0.5 * u.width / 2]
            if len(far) == 0:
                far = pts
            vec = np.mean([[np.cos(ang(*p)), np.sin(ang(*p))] for p in far], axis=0)
            return np.arctan2(vec[1], vec[0])
        wa = [wedge_angle(dr) for dr in wd]
        order = []
        free = list(range(len(labels)))
        for a_ in wa:
            if not free:
                break
            j = min(free, key=lambda j: abs(np.angle(np.exp(1j * (ang((labels[j][2].x0 + labels[j][2].x1) / 2,
                                                                       (labels[j][2].y0 + labels[j][2].y1) / 2) - a_)))))
            order.append(j)
            free.remove(j)
        order += free
        # the PDF text stream lists labels in data order; keep it (angle matching is
        # only a fallback when the text order is unavailable)
        labs = labels if d.get("text_order", True) else [labels[j] for j in order]
        pies.append({"title": title, "labels": labs})
    # consistent colours per category across the pies
    cats = []
    for p in pies:
        for name, _, _ in p["labels"]:
            key = re.sub(r"[,;]\s*$", "", name)
            if key not in cats:
                cats.append(key)
    panels = []
    for p in pies:
        names = [re.sub(r"[,;]\s*$", "", n) for n, _, _ in p["labels"]]
        vals = [v for _, v, _ in p["labels"]]
        dl = [f"{n} {_label(v)}" for n, v, _ in p["labels"]]
        panels.append({"kind": "pie", "labels": names, "vals": vals, "dlabels": dl,
                       "panel_title": p["title"], "colors": [PALETTE[cats.index(n) % len(PALETTE)] for n in names]})
    d["note"] = d["note_base"]
    return {"panels": panels, "ncols": 2, "legend": False}


if __name__ == "__main__":
    sys.exit(main())
