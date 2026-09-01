#!/usr/bin/env python3
"""Convert <text> in a sketch SVG into vector <path> outlines.

Why: an SVG loaded through <img src="..."> renders in secure static mode, where
external resources - including an @import'ed webfont - are blocked. The
handwriting font therefore never loads on a page, and every diagram silently
falls back to a serif. Embedding the font as base64 costs ~120 KB per file
(x1002 files). Outlining the text costs only the glyphs each file actually uses,
deduplicated through <defs>/<use>, and cannot fall back to anything.
"""
from __future__ import annotations

import re
from pathlib import Path
from xml.sax.saxutils import unescape

_ENTS = {"&quot;": '"', "&apos;": "'", "&#39;": "'", "&nbsp;": " "}

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

_HERE = Path(__file__).resolve().parent / "fonts"
FONTS = {"400": _HERE / "Caveat-Regular.ttf", "700": _HERE / "Caveat-Bold.ttf"}
# Caveat has no glyph for 13 symbols the diagrams use (arrows, radical, partial,
# circled digits, alpha, cross). DejaVu covers all 13 and is freely
# redistributable, so missing glyphs are outlined from it rather than dropped.
FALLBACK = {"400": _HERE / "DejaVuSans.ttf", "700": _HERE / "DejaVuSans-Bold.ttf"}
_cache: dict[str, tuple] = {}


def _font(weight: str):
    if weight not in _cache:
        f = TTFont(FONTS[weight])
        _cache[weight] = (f, f.getGlyphSet(), f["head"].unitsPerEm,
                          f.getBestCmap(), f["hmtx"].metrics)
    return _cache[weight]


def _round(d: str, places: int = 0) -> str:
    """Round path coordinates. Glyph outlines are in em units (~2048/em), so
    whole numbers are far below one rendered pixel and halve the file size."""
    return re.sub(r"-?\d+\.\d+", lambda m: f"{float(m.group()):.{places}f}", d)


def _fallback(weight: str):
    key = "fb" + weight
    if key not in _cache:
        f = TTFont(FALLBACK[weight])
        _cache[key] = (f, f.getGlyphSet(), f["head"].unitsPerEm,
                       f.getBestCmap(), f["hmtx"].metrics)
    return _cache[key]


def glyph_path(ch: str, weight: str) -> tuple[str, float, str]:
    """Return (path data, advance in em, source tag). Falls back to DejaVu."""
    for src, load in (("c", _font), ("d", _fallback)):
        font, gs, upem, cmap, hmtx = load(weight)
        name = cmap.get(ord(ch))
        if name is None:
            continue
        pen = SVGPathPen(gs)
        gs[name].draw(pen)
        return _round(pen.getCommands()), hmtx[name][0] / upem, src
    return "", 0.0, "c"


def text_width(s: str, weight: str, size: float) -> float:
    return sum(glyph_path(c, weight)[1] for c in s) * size


def _upem(src: str, weight: str) -> int:
    return (_font(weight) if src == "c" else _fallback(weight))[2]


def convert(svg: str) -> str:
    """Replace every <text> element with outlined glyphs."""
    defs: dict[str, str] = {}
    upem = _font("400")[2]

    def repl(m: re.Match) -> str:
        attrs, body = m.group(1), m.group(2)
        if "<" in body:                       # nested markup: leave alone
            return m.group(0)
        content = unescape(body, _ENTS).strip()
        if not content:
            return ""

        def a(name, default=None):
            g = re.search(rf'{name}="([^"]*)"', attrs)
            return g.group(1) if g else default

        size = float(a("font-size", "16") or 16)
        x, y = float(a("x", "0") or 0), float(a("y", "0") or 0)
        weight = "700" if (a("font-weight", "") or "").strip() in ("700", "bold") else "400"
        anchor = a("text-anchor", "start")
        fill = a("fill", "#1e1e1e")
        opacity = a("opacity")
        transform = a("transform")

        w = text_width(content, weight, size)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w

        out, pen_x = [], x
        for ch in content:
            d, adv, src = glyph_path(ch, weight)
            if d:
                scale = size / _upem(src, weight)
                key = f"{src}{weight}-{ord(ch)}"
                defs.setdefault(key, d)
                out.append(f'<use href="#g{key}" x="{pen_x:.2f}" y="{y:.2f}" '
                           f'transform="translate({pen_x:.2f},{y:.2f}) scale({scale:.5f},{-scale:.5f}) '
                           f'translate({-pen_x:.2f},{-y:.2f})"/>')
            pen_x += adv * size
        if not out:
            return ""
        g = f'<g fill="{fill}"'
        if opacity:
            g += f' opacity="{opacity}"'
        if transform:
            g += f' transform="{transform}"'
        return g + ">" + "".join(out) + "</g>"

    body = re.sub(r"<text([^>]*)>(.*?)</text>", repl, svg, flags=re.S)
    if defs:
        block = "<defs>" + "".join(
            f'<path id="g{k}" d="{v}"/>' for k, v in sorted(defs.items())) + "</defs>"
        body = re.sub(r"(<svg[^>]*>)", r"\1" + block, body, count=1)
    # the webfont @import is now dead weight
    body = re.sub(r"<style>.*?</style>", "", body, flags=re.S)
    return body


if __name__ == "__main__":
    import sys
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src
    out = convert(src.read_text())
    dst.write_text(out)
    print(f"{dst}  {len(out):,} bytes")
