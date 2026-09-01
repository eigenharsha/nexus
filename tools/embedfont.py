#!/usr/bin/env python3
"""Embed a per-file subset of the handwriting font into a sketch SVG.

An SVG loaded through <img src="..."> renders in secure static mode: external
resources, including an @import'ed webfont, are blocked. The handwriting font
therefore never loads on a page and every diagram falls back to a serif.

Outlining the text fixes that but costs 8x file size (25 MB -> 197 MB) and makes
the text unselectable. Embedding a subset containing only the glyphs THIS file
uses is far cheaper and keeps <text> real - selectable, searchable, accessible.

Caveat lacks 13 symbols the diagrams use (arrows, radical, partial, circled
digits); DejaVu Sans covers all of them and is freely redistributable, so it is
embedded alongside as the fallback family.
"""
from __future__ import annotations

import base64
import io
import re
from pathlib import Path
from xml.sax.saxutils import unescape

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

FONTS = Path(__file__).resolve().parent / "fonts"
FACES = [
    ("NexusHand", "400", FONTS / "Caveat-Regular.ttf"),
    ("NexusHand", "700", FONTS / "Caveat-Bold.ttf"),
    ("NexusSym", "400", FONTS / "DejaVuSans.ttf"),
    ("NexusSym", "700", FONTS / "DejaVuSans-Bold.ttf"),
]
_ENTS = {"&quot;": '"', "&apos;": "'", "&#39;": "'", "&nbsp;": " "}


def text_of(svg: str) -> str:
    return "".join(unescape(m, _ENTS)
                   for m in re.findall(r"<text[^>]*>([^<]*)</text>", svg))


def subset_b64(path: Path, chars: str) -> str | None:
    font = TTFont(path)
    cmap = font.getBestCmap()
    keep = {c for c in chars if ord(c) in cmap}
    if not keep:
        return None
    opts = Options()
    opts.layout_features = []
    opts.hinting = False
    opts.desubroutinize = True
    opts.drop_tables += ["GSUB", "GPOS", "GDEF", "DSIG", "kern", "morx"]
    ss = Subsetter(options=opts)
    ss.populate(text="".join(sorted(keep)))
    ss.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff"          # zlib, no brotli dependency
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def embed(svg: str) -> str:
    chars = text_of(svg)
    if not chars.strip():
        return svg
    faces = []
    for family, weight, path in FACES:
        b64 = subset_b64(path, chars)
        if b64:
            faces.append(
                f"@font-face{{font-family:'{family}';font-weight:{weight};"
                f"src:url(data:font/woff;base64,{b64}) format('woff');}}")
    if not faces:
        return svg
    style = "<style>" + "".join(faces) + "</style>"
    svg = re.sub(r"<style>.*?</style>", "", svg, flags=re.S)       # drop @import
    svg = re.sub(r"(<svg[^>]*>)", r"\1" + style, svg, count=1)
    # point every font-family at the embedded faces
    svg = re.sub(r"font-family=\"[^\"]*\"",
                 "font-family=\"NexusHand, NexusSym, cursive\"", svg)
    return svg


if __name__ == "__main__":
    import sys
    src = Path(sys.argv[1]); dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src
    out = embed(src.read_text()); dst.write_text(out)
    print(f"{dst.name}  {src.stat().st_size:,} -> {len(out):,} bytes")
