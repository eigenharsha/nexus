#!/usr/bin/env python3
"""
excalidraw.py - export a sketch spec as an editable .excalidraw scene.

The lesson pages link an "Editable source" next to every sketch, and
PLAN/03-visual-spec.md makes committing that source a rule: "a diagram nobody
can edit is technical debt". This turns the same declarative spec that
sketch.py renders into a scene excalidraw.com can open, with the house style
already applied - hand-drawn font, hachure fills, bold strokes, roughness 1.

  from excalidraw import to_scene
  json.dump(to_scene(spec), fh)
"""
from __future__ import annotations

import json
import math
import zlib

import sketch

FONT_HAND = 1          # Excalifont / Virgil
ROUGHNESS = 1          # "artist" - matches the visual spec's 1-2
STROKE_BOLD = 2


def _seed(*parts) -> int:
    return zlib.crc32("|".join(str(p) for p in parts).encode()) % 2_000_000_000


def _base(eid, kind, x, y, w, h, stroke, **kw):
    el = {
        "id": str(eid), "type": kind,
        "x": round(float(x), 2), "y": round(float(y), 2),
        "width": round(float(w), 2), "height": round(float(h), 2),
        "angle": kw.pop("angle", 0),
        "strokeColor": stroke,
        "backgroundColor": kw.pop("background", "transparent"),
        "fillStyle": kw.pop("fillStyle", "hachure"),
        "strokeWidth": kw.pop("strokeWidth", STROKE_BOLD),
        "strokeStyle": kw.pop("strokeStyle", "solid"),
        "roughness": ROUGHNESS,
        "opacity": kw.pop("opacity", 100),
        "groupIds": kw.pop("groupIds", []),
        "frameId": None,
        "roundness": kw.pop("roundness", None),
        "seed": _seed(eid, kind),
        "version": 1, "versionNonce": _seed(eid, kind, "n"),
        "isDeleted": False, "boundElements": None,
        "updated": 1, "link": None, "locked": False,
    }
    el.update(kw)
    return el


def _text(eid, x, y, text, size, stroke, align="center", angle=0.0):
    text = str(text)
    lines = text.split("\n")
    w = max(sketch.text_width(l, size) for l in lines) if lines else 10
    h = size * 1.25 * len(lines)
    # excalidraw anchors text by its top-left corner
    if align == "center":
        x -= w / 2
    elif align == "end":
        x -= w
    return _base(eid, "text", x, y - size, max(w, 8), h, stroke,
                 angle=angle, strokeWidth=1,
                 text=text, originalText=text, fontSize=size,
                 fontFamily=FONT_HAND, textAlign=align if align != "end"
                 else "right", verticalAlign="top", containerId=None,
                 lineHeight=1.25, autoResize=True)


def _linear(eid, kind, pts, stroke, **kw):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, y0 = xs[0], ys[0]
    rel = [[round(p[0] - x0, 2), round(p[1] - y0, 2)] for p in pts]
    el = _base(eid, kind, x0, y0, max(xs) - min(xs), max(ys) - min(ys), stroke,
               **kw)
    el.update({"points": rel, "lastCommittedPoint": None,
               "startBinding": None, "endBinding": None,
               "startArrowhead": None,
               "endArrowhead": "arrow" if kind == "arrow" else None})
    return el


def to_scene(spec: dict) -> dict:
    """Convert a sketch spec into an Excalidraw scene dict."""
    theme = "light"
    C = lambda name, default="ink": sketch.color(name or default, theme)
    out = []
    sid = spec.get("id", "sketch")

    title = spec.get("title")
    if title:
        out.append(_text(f"{sid}-title", 28, 42, title, 28, C("ink"),
                         align="left"))

    for i, el in enumerate(spec.get("elements") or []):
        if not isinstance(el, dict):
            continue
        kind = str(el.get("type", "box")).lower()
        eid = f"{sid}-{el.get('id', i)}"
        try:
            stroke = C(el.get("color"), "structure" if kind in
                       ("box", "rect", "card", "ellipse", "circle", "node")
                       else "ink")
            dashed = "dashed" if (el.get("dashed") or el.get("dash")) else "solid"

            if kind in ("box", "rect", "card", "bar", "highlight"):
                x, y = float(el.get("x", 0)), float(el.get("y", 0))
                w, h = float(el.get("w", 120)), float(el.get("h", 60))
                if kind == "highlight":
                    out.append(_base(eid, "rectangle", x, y, w, h,
                                     "transparent",
                                     background=C("highlight"),
                                     fillStyle="solid", opacity=45))
                    continue
                bg = "transparent"
                if el.get("fill"):
                    bg = C(el.get("fill_color") or el.get("fillColor")
                           or el.get("color"))
                if kind == "bar":
                    stroke = C(el.get("color"), "structure")
                    bg = stroke
                out.append(_base(eid, "rectangle", x, y, w, h, stroke,
                                 background=bg, strokeStyle=dashed,
                                 roundness={"type": 3}))
                label = el.get("label") or el.get("text")
                if label:
                    out.append(_text(eid + "-t", x + w / 2, y + h / 2 + 6,
                                     label, float(el.get("size", 18)),
                                     C(el.get("label_color", "ink"))))
                if el.get("sub"):
                    out.append(_text(eid + "-s", x + w / 2, y + h + 18,
                                     el["sub"], 14, C("muted")))
                if el.get("value"):
                    out.append(_text(eid + "-v", x + w + 10, y + h * 0.8,
                                     el["value"], 15, stroke, align="left"))

            elif kind in ("ellipse", "circle", "node"):
                cx = float(el.get("cx", el.get("x", 0)))
                cy = float(el.get("cy", el.get("y", 0)))
                rx = float(el.get("rx", 60))
                ry = float(el.get("ry", el.get("rx", 40)))
                bg = C(el.get("fill_color") or el.get("color")) \
                    if el.get("fill") else "transparent"
                out.append(_base(eid, "ellipse", cx - rx, cy - ry, rx * 2,
                                 ry * 2, stroke, background=bg,
                                 strokeStyle=dashed))
                if el.get("label") or el.get("text"):
                    out.append(_text(eid + "-t", cx, cy + 6,
                                     el.get("label") or el.get("text"),
                                     float(el.get("size", 17)), C("ink")))

            elif kind in ("line", "arrow"):
                x1, y1 = float(el.get("x1", 0)), float(el.get("y1", 0))
                x2, y2 = float(el.get("x2", 0)), float(el.get("y2", 0))
                pts = [[x1, y1], [x2, y2]]
                curve = float(el.get("curve", 0) or 0)
                if curve:
                    dx, dy = x2 - x1, y2 - y1
                    L = math.hypot(dx, dy) or 1
                    pts = [[x1, y1],
                           [(x1 + x2) / 2 - dy / L * curve * L,
                            (y1 + y2) / 2 + dx / L * curve * L],
                           [x2, y2]]
                out.append(_linear(eid, "arrow" if kind == "arrow" else "line",
                                   pts, stroke, strokeStyle=dashed))
                if el.get("label"):
                    out.append(_text(eid + "-t",
                                     float(el.get("label_x", (x1 + x2) / 2)),
                                     float(el.get("label_y", (y1 + y2) / 2 - 8)),
                                     el["label"], float(el.get("label_size", 15)),
                                     C(el.get("label_color", el.get("color")))))

            elif kind in ("path", "polyline", "curve"):
                pts = [[float(a), float(b)] for a, b in el.get("points", [])]
                if len(pts) >= 2:
                    out.append(_linear(eid,
                                       "arrow" if el.get("arrow") else "line",
                                       pts, stroke, strokeStyle=dashed))

            elif kind in ("text", "label"):
                out.append(_text(eid, float(el.get("x", 0)),
                                 float(el.get("y", 0)), el.get("text", ""),
                                 float(el.get("size", 18)), stroke,
                                 align={"start": "left", "end": "end"}.get(
                                     el.get("anchor", "middle"), "center")))

            elif kind in ("note", "margin-note", "margin_note"):
                out.append(_text(eid, float(el.get("x", 0)),
                                 float(el.get("y", 0)), el.get("text", ""),
                                 float(el.get("size", 15)), C("note"),
                                 align="left", angle=math.radians(-2.5)))

            elif kind in ("circled", "circled-term", "circled_term"):
                x, y = float(el.get("x", 0)), float(el.get("y", 0))
                size = float(el.get("size", 19))
                rx = float(el.get("rx", max(
                    sketch.text_width(el.get("text", ""), size, True) / 2 + 14,
                    24)))
                ry = float(el.get("ry", size * 0.95))
                out.append(_base(eid + "-ring", "ellipse", x - rx,
                                 y - size * 0.32 - ry, rx * 2, ry * 2,
                                 C(el.get("ring", "structure"))))
                out.append(_text(eid, x, y, el.get("text", ""), size, C("ink")))

            elif kind in ("crossout", "cross-out", "strike"):
                x, y = float(el.get("x", 0)), float(el.get("y", 0))
                w, h = float(el.get("w", 100)), float(el.get("h", 40))
                red = C(el.get("color", "error"))
                out.append(_linear(eid + "-a", "line",
                                   [[x - 6, y - 6], [x + w + 6, y + h + 6]],
                                   red))
                if el.get("style", "x") != "strike":
                    out.append(_linear(eid + "-b", "line",
                                       [[x + w + 6, y - 6], [x - 6, y + h + 6]],
                                       red))
                if el.get("label"):
                    out.append(_text(eid + "-t", x + w / 2, y + h + 22,
                                     el["label"], 15, red))

            elif kind in ("badge", "step"):
                x, y = float(el.get("x", 0)), float(el.get("y", 0))
                r = float(el.get("r", 13))
                amber = C(el.get("color", "note"))
                out.append(_base(eid + "-c", "ellipse", x - r, y - r, r * 2,
                                 r * 2, amber, strokeWidth=1))
                out.append(_text(eid, x, y + r * 0.4,
                                 el.get("n", el.get("text", 1)), r * 1.2,
                                 amber))
        except Exception:
            continue  # one bad element must never break the export

    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://github.com/ (nexus tools/excalidraw.py)",
        "elements": out,
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": sketch.color("paper", "light"),
        },
        "files": {},
    }


def dumps(spec: dict) -> str:
    return json.dumps(to_scene(spec), indent=1, ensure_ascii=False) + "\n"
