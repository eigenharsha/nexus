#!/usr/bin/env python3
"""
sketch.py - a dependency-free hand-drawn SVG renderer for the Nexus course.

Turns a small declarative spec (a dict, or JSON on disk) into whiteboard-style
SVG: every stroke is a jittered cubic bezier drawn twice, fills are hachure,
and the type is a handwriting stack loaded from Google Fonts.

  from sketch import render_all
  render_all(spec, out_dir)      # writes <id>.svg, <id>-dark.svg, <id>-blank.svg

Or from the shell:

  python3 tools/sketch.py spec.json out_dir/
  python3 tools/sketch.py --selftest          # renders a demo spec to /tmp

House style comes from PLAN/03-visual-spec.md. See tools/sketch_spec.md for the
spec format.
"""
from __future__ import annotations

import json
import math
import random
import re
import sys
import zlib
from pathlib import Path

# --------------------------------------------------------------------------
# palette
# --------------------------------------------------------------------------

PALETTE = {
    "ink":        {"light": "#1e1e1e", "dark": "#e8e6e3"},
    "structure":  {"light": "#1971c2", "dark": "#5aa9e6"},
    "correct":    {"light": "#2f9e44", "dark": "#6cc47a"},
    "error":      {"light": "#e03131", "dark": "#ff6b6b"},
    "note":       {"light": "#f08c00", "dark": "#ffb84d"},
    "highlight":  {"light": "#ffec99", "dark": "#5c5326"},
    "paper":      {"light": "#fffdf7", "dark": "#1a1a19"},
    "muted":      {"light": "#6b6b6b", "dark": "#9a9791"},
}
# friendly aliases people will inevitably type
ALIASES = {
    "blue": "structure", "green": "correct", "red": "error", "amber": "note",
    "orange": "note", "yellow": "highlight", "black": "ink", "default": "ink",
    "grey": "muted", "gray": "muted",
}

# Caveat has a small x-height for its nominal size, so a 15px label reads
# closer to 11px of a normal face. Every text size passes through this scale so
# one knob controls legibility across hand-authored and compiled diagrams alike.
TEXT_SCALE = 1.45

FONT_STACK = "'Caveat', 'Kalam', cursive, sans-serif"
FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Caveat:wght@400;700&amp;family=Kalam:wght@300;400;700&amp;display=swap');"
)

# Caveat is narrow; this is the empirical advance width as a fraction of size.
CHAR_W = 0.42
CHAR_W_BOLD = 0.45
# effective per-character width once TEXT_SCALE is applied at emission


def color(name: str | None, theme: str) -> str:
    """Resolve a palette name (or a raw #hex) for the given theme."""
    if not name:
        name = "ink"
    name = str(name).strip().lower()
    if name.startswith("#"):
        return name
    name = ALIASES.get(name, name)
    entry = PALETTE.get(name, PALETTE["ink"])
    return entry[theme]


def _rng(seed_parts) -> random.Random:
    """Deterministic RNG seeded from strings - hash() is salted, crc32 is not."""
    key = "|".join(str(p) for p in seed_parts).encode("utf-8")
    return random.Random(zlib.crc32(key))


def esc(text) -> str:
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _f(v: float) -> str:
    """Compact float formatting - keeps the SVG small."""
    return f"{v:.1f}".rstrip("0").rstrip(".") or "0"


# --------------------------------------------------------------------------
# the wobble primitives
# --------------------------------------------------------------------------

def rough_segment(x1, y1, x2, y2, rng, amp=2.0, overshoot=0.0):
    """One jittered cubic bezier standing in for a straight line."""
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy) or 1.0
    ux, uy = dx / length, dy / length
    # marker overshoot: real strokes start a hair early and end a hair late
    if overshoot:
        o1 = rng.uniform(0, overshoot)
        o2 = rng.uniform(0, overshoot)
        x1 -= ux * o1; y1 -= uy * o1
        x2 += ux * o2; y2 += uy * o2
        dx, dy = x2 - x1, y2 - y1
    a = min(amp, length * 0.22)
    j = lambda: rng.uniform(-a, a)
    c1x = x1 + dx * rng.uniform(0.2, 0.4) + j()
    c1y = y1 + dy * rng.uniform(0.2, 0.4) + j()
    c2x = x1 + dx * rng.uniform(0.6, 0.8) + j()
    c2y = y1 + dy * rng.uniform(0.6, 0.8) + j()
    return (f"M{_f(x1 + j() * 0.4)},{_f(y1 + j() * 0.4)} "
            f"C{_f(c1x)},{_f(c1y)} {_f(c2x)},{_f(c2y)} "
            f"{_f(x2 + j() * 0.4)},{_f(y2 + j() * 0.4)}")


def rough_path(points, rng, amp=2.4, closed=False, overshoot=2.6):
    """A jittered polyline (or polygon) as a list of bezier path fragments."""
    pts = list(points)
    if closed and pts[0] != pts[-1]:
        pts = pts + [pts[0]]
    return [rough_segment(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1],
                          rng, amp, overshoot)
            for i in range(len(pts) - 1)]


def rough_ellipse_path(cx, cy, rx, ry, rng, amp=2.0, steps=14, start_wrap=0.12):
    """A closed, slightly lumpy ellipse - drawn as a smoothed jittered loop."""
    total = steps
    pts = []
    phase = rng.uniform(0, math.tau)
    # slightly more than one full turn so the stroke visibly laps itself
    span = math.tau * (1.0 + start_wrap)
    for i in range(total + 1):
        t = phase + span * i / total
        r_jit = 1.0 + rng.uniform(-amp, amp) / max(rx, ry, 1) * 1.2
        pts.append((cx + math.cos(t) * rx * r_jit,
                    cy + math.sin(t) * ry * r_jit))
    # Catmull-Rom -> cubic bezier for smoothness
    d = [f"M{_f(pts[0][0])},{_f(pts[0][1])}"]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{_f(c1[0])},{_f(c1[1])} {_f(c2[0])},{_f(c2[1])} "
                 f"{_f(p2[0])},{_f(p2[1])}")
    return " ".join(d)


def hachure_rect(x, y, w, h, rng, gap=8.0, angle=-45.0):
    """Diagonal parallel fill lines clipped to a rectangle, endpoints jittered."""
    lines = []
    rad = math.radians(angle)
    dx, dy = math.cos(rad), math.sin(rad)
    # walk the perpendicular axis
    px, py = -dy, dx
    corners = [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]
    projs = [c[0] * px + c[1] * py for c in corners]
    lo, hi = min(projs), max(projs)
    n = 0
    p = lo + gap * 0.5
    while p < hi and n < 400:
        n += 1
        # intersect the infinite line {q : q.p == p} with the rect
        ts = []
        for (cx, cy, vx, vy, tmax) in ((x, y, 1, 0, w), (x, y + h, 1, 0, w),
                                       (x, y, 0, 1, h), (x + w, y, 0, 1, h)):
            denom = vx * px + vy * py
            if abs(denom) < 1e-9:
                continue
            t = (p - (cx * px + cy * py)) / denom
            if -0.01 <= t <= tmax + 0.01:
                ts.append((cx + vx * t, cy + vy * t))
        if len(ts) >= 2:
            (ax, ay), (bx, by) = ts[0], ts[-1]
            if math.hypot(bx - ax, by - ay) > 3:
                lines.append(rough_segment(ax, ay, bx, by, rng, amp=1.1,
                                           overshoot=1.2))
        p += gap * rng.uniform(0.85, 1.15)
    return lines


def hachure_ellipse(cx, cy, rx, ry, rng, gap=8.0, angle=-45.0):
    """Same idea, chords of an ellipse."""
    lines = []
    rad = math.radians(angle)
    dx, dy = math.cos(rad), math.sin(rad)
    px, py = -dy, dx
    # in the unit circle after scaling, the offset range is [-1, 1]
    reach = math.hypot(px * rx, py * ry)
    p0 = cx * px + cy * py
    p = p0 - reach + gap * 0.5
    n = 0
    while p < p0 + reach and n < 300:
        n += 1
        # parametrise the line and solve the ellipse quadratic
        # point = base + t*(dx,dy); base is the closest point on the line to c
        offset = p - p0
        bx, by = cx + px * offset, cy + py * offset
        A = (dx * dx) / (rx * rx) + (dy * dy) / (ry * ry)
        B = 2 * ((bx - cx) * dx / (rx * rx) + (by - cy) * dy / (ry * ry))
        C = ((bx - cx) ** 2) / (rx * rx) + ((by - cy) ** 2) / (ry * ry) - 1
        disc = B * B - 4 * A * C
        if disc > 0:
            sq = math.sqrt(disc)
            t1, t2 = (-B - sq) / (2 * A), (-B + sq) / (2 * A)
            ax, ay = bx + dx * t1, by + dy * t1
            ex, ey = bx + dx * t2, by + dy * t2
            if math.hypot(ex - ax, ey - ay) > 3:
                lines.append(rough_segment(ax, ay, ex, ey, rng, amp=1.0,
                                           overshoot=0.8))
        p += gap * rng.uniform(0.85, 1.15)
    return lines


# --------------------------------------------------------------------------
# text helpers
# --------------------------------------------------------------------------

def wrap_text(text, max_width, size, bold=False, max_lines=6):
    """Greedy wrap using an approximate advance width."""
    text = str(text)
    cw = (CHAR_W_BOLD if bold else CHAR_W) * size * TEXT_SCALE
    if cw <= 0:
        return [text]
    limit = max(1, int(max_width / cw))
    lines, out = [], []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if len(trial) <= limit or not cur:
                cur = trial
            else:
                out.append(cur)
                cur = w
        out.append(cur)
    lines = [l for l in out if l != ""] or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:max(0, limit - 1)] + "…"
    return lines


def text_width(text, size, bold=False):
    return len(str(text)) * (CHAR_W_BOLD if bold else CHAR_W) * size * TEXT_SCALE


# --------------------------------------------------------------------------
# renderer
# --------------------------------------------------------------------------

class Sketch:
    """Accumulates SVG fragments for one diagram in one theme."""

    def __init__(self, spec, theme="light", blank=False):
        self.spec = spec
        self.theme = theme
        self.blank = blank
        self.out = []
        self.sid = str(spec.get("id", "sketch"))

    # -- low level ---------------------------------------------------------

    def stroke(self, d_list, col, width=2.0, dash=None, opacity=1.0,
               offset=None):
        if isinstance(d_list, str):
            d_list = [d_list]
        d = " ".join(d_list)
        if not d.strip():
            return
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        op = f' stroke-opacity="{_f(opacity)}"' if opacity < 1 else ""
        tr = (f' transform="translate({_f(offset[0])} {_f(offset[1])})"'
              if offset else "")
        self.out.append(
            f'<path d="{d}" fill="none" stroke="{col}" '
            f'stroke-width="{_f(width)}" stroke-linecap="round" '
            f'stroke-linejoin="round"{extra}{op}{tr}/>')

    def double_stroke(self, builder, col, width=2.0, dash=None, seed=""):
        """Draw the same shape twice from two RNG streams - the money effect."""
        r1 = _rng([self.sid, seed, "pass1"])
        r2 = _rng([self.sid, seed, "pass2"])
        self.stroke(builder(r1), col, width, dash)
        ro = _rng([self.sid, seed, "offset"])
        ox, oy = ro.uniform(-1.4, 1.4), ro.uniform(-1.4, 1.4)
        self.stroke(builder(r2), col, width * 0.7, dash, opacity=0.5,
                    offset=(ox, oy))

    def text(self, x, y, s, size=18, col=None, anchor="middle", bold=False,
             rotate=0.0, opacity=1.0, italic=False):
        if self.blank or s is None or str(s) == "":
            return
        tr = f' transform="rotate({_f(rotate)} {_f(x)} {_f(y)})"' if rotate else ""
        weight = ' font-weight="700"' if bold else ""
        ital = ' font-style="italic"' if italic else ""
        op = f' fill-opacity="{_f(opacity)}"' if opacity < 1 else ""
        self.out.append(
            f'<text x="{_f(x)}" y="{_f(y)}" font-size="{_f(size * TEXT_SCALE)}" '
            f'fill="{col or color("ink", self.theme)}" text-anchor="{anchor}"'
            f'{weight}{ital}{tr}{op}>{esc(s)}</text>')

    def multiline(self, x, y, lines, size=18, col=None, anchor="middle",
                  bold=False, lh=1.15, rotate=0.0):
        if self.blank:
            return
        step = size * lh * TEXT_SCALE
        top = y - (len(lines) - 1) * step / 2
        for i, line in enumerate(lines):
            self.text(x, top + i * step, line, size, col, anchor, bold, rotate)

    # -- shapes ------------------------------------------------------------

    def draw_box(self, el, seed):
        x, y = float(el.get("x", 0)), float(el.get("y", 0))
        w, h = float(el.get("w", 120)), float(el.get("h", 60))
        col = color(el.get("color", "structure"), self.theme)
        r = el.get("r", 0)
        pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        amp = float(el.get("roughness", 2.6))

        fill = el.get("fill")
        if fill:
            fc = color(el.get("fill_color", el.get("fillColor", fill)), self.theme)
            rf = _rng([self.sid, seed, "fill"])
            lines = hachure_rect(x + 3, y + 3, max(w - 6, 1), max(h - 6, 1), rf,
                                 gap=float(el.get("fill_gap", 9)),
                                 angle=float(el.get("fill_angle", -45)))
            self.stroke(lines, fc, 1.4, opacity=0.85)

        dash = el.get("dash") or ("6 5" if el.get("dashed") else None)
        self.double_stroke(lambda rr: rough_path(pts, rr, amp, closed=True),
                           col, float(el.get("width", 2.0)), dash, seed)

        label = el.get("label") or el.get("text")
        if label:
            size = float(el.get("size", 18))
            lines = wrap_text(label, w - 14, size, bold=el.get("bold", False))
            # emission scales by TEXT_SCALE, so the fit test must too -
            # without it a two-line label silently overflows its box.
            while len(lines) * size * 1.15 * TEXT_SCALE > h - 6 and size > 9:
                size -= 1
                lines = wrap_text(label, w - 14, size, bold=el.get("bold", False))
            self.multiline(x + w / 2, y + h / 2, lines, size,
                           color(el.get("label_color", "ink"), self.theme),
                           bold=el.get("bold", False))
        sub = el.get("sub")
        if sub:
            self.text(x + w / 2, y + h + 15, sub, float(el.get("sub_size", 14)),
                      color(el.get("sub_color", "muted"), self.theme))

    def draw_ellipse(self, el, seed):
        cx, cy = float(el.get("cx", el.get("x", 0))), float(el.get("cy", el.get("y", 0)))
        rx, ry = float(el.get("rx", 60)), float(el.get("ry", el.get("rx", 40)))
        col = color(el.get("color", "structure"), self.theme)
        amp = float(el.get("roughness", 2.0))
        if el.get("fill"):
            fc = color(el.get("fill_color", el.get("fillColor", el["fill"])), self.theme)
            rf = _rng([self.sid, seed, "fill"])
            self.stroke(hachure_ellipse(cx, cy, rx - 3, ry - 3, rf,
                                        gap=float(el.get("fill_gap", 9)),
                                        angle=float(el.get("fill_angle", -45))),
                        fc, 1.4, opacity=0.85)
        dash = el.get("dash") or ("6 5" if el.get("dashed") else None)
        self.double_stroke(
            lambda rr: [rough_ellipse_path(cx, cy, rx, ry, rr, amp)],
            col, float(el.get("width", 2.0)), dash, seed)
        label = el.get("label") or el.get("text")
        if label:
            size = float(el.get("size", 17))
            lines = wrap_text(label, rx * 1.7, size)
            self.multiline(cx, cy, lines, size,
                           color(el.get("label_color", "ink"), self.theme))

    def _line_points(self, el):
        x1, y1 = float(el.get("x1", 0)), float(el.get("y1", 0))
        x2, y2 = float(el.get("x2", 0)), float(el.get("y2", 0))
        return x1, y1, x2, y2

    def draw_line(self, el, seed, arrow=False):
        x1, y1, x2, y2 = self._line_points(el)
        col = color(el.get("color", "ink"), self.theme)
        amp = float(el.get("roughness", 1.8))
        curve = float(el.get("curve", 0.0))
        dash = el.get("dash") or ("6 5" if el.get("dashed") else None)
        width = float(el.get("width", 2.0))

        if curve:
            # bow the line out perpendicular to its direction
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = x2 - x1, y2 - y1
            L = math.hypot(dx, dy) or 1
            nx, ny = -dy / L, dx / L
            cxp, cyp = mx + nx * curve * L, my + ny * curve * L
            pts = [(x1, y1), (cxp, cyp), (x2, y2)]
            build = lambda rr: [rough_ctrl_curve(pts, rr, amp)]
            # tangent at the end for the arrowhead
            ang = math.atan2(y2 - cyp, x2 - cxp)
        else:
            build = lambda rr: rough_path([(x1, y1), (x2, y2)], rr, amp,
                                          overshoot=1.0)
            ang = math.atan2(y2 - y1, x2 - x1)

        self.double_stroke(build, col, width, dash, seed)

        if arrow:
            head = float(el.get("head", 12))
            ra = _rng([self.sid, seed, "head"])
            for sign in (1, -1):
                a = ang + math.pi + sign * math.radians(ra.uniform(20, 30))
                hx, hy = x2 + math.cos(a) * head, y2 + math.sin(a) * head
                self.stroke(rough_segment(x2, y2, hx, hy, ra, 1.0, 0.6),
                            col, width)

        label = el.get("label")
        if label:
            lx = float(el.get("label_x", (x1 + x2) / 2))
            ly = float(el.get("label_y", (y1 + y2) / 2 - 8))
            if curve:
                ly = float(el.get("label_y", (cyp + (y1 + y2) / 2) / 2 - 8))
            size = float(el.get("label_size", 15))
            self.multiline(lx, ly, wrap_text(label, el.get("label_w", 160), size),
                           size, color(el.get("label_color", el.get("color", "ink")),
                                       self.theme))

    def draw_path(self, el, seed):
        """An open polyline / freehand curve through a list of points."""
        pts = [(float(a), float(b)) for a, b in el.get("points", [])]
        if len(pts) < 2:
            return
        col = color(el.get("color", "ink"), self.theme)
        amp = float(el.get("roughness", 1.6))
        dash = el.get("dash") or ("6 5" if el.get("dashed") else None)
        smooth = el.get("smooth", True)

        def build(rr):
            if not smooth:
                return rough_path(pts, rr, amp, overshoot=0.6)
            j = lambda: rr.uniform(-amp, amp)
            d = [f"M{_f(pts[0][0] + j())},{_f(pts[0][1] + j())}"]
            for i in range(len(pts) - 1):
                p0 = pts[i - 1] if i > 0 else pts[i]
                p1, p2 = pts[i], pts[i + 1]
                p3 = pts[i + 2] if i + 2 < len(pts) else p2
                c1 = (p1[0] + (p2[0] - p0[0]) / 6 + j() * .5,
                      p1[1] + (p2[1] - p0[1]) / 6 + j() * .5)
                c2 = (p2[0] - (p3[0] - p1[0]) / 6 + j() * .5,
                      p2[1] - (p3[1] - p1[1]) / 6 + j() * .5)
                d.append(f"C{_f(c1[0])},{_f(c1[1])} {_f(c2[0])},{_f(c2[1])} "
                         f"{_f(p2[0] + j() * .4)},{_f(p2[1] + j() * .4)}")
            return [" ".join(d)]

        self.double_stroke(build, col, float(el.get("width", 2.0)), dash, seed)
        if el.get("arrow"):
            (ax, ay), (bx, by) = pts[-2], pts[-1]
            ang = math.atan2(by - ay, bx - ax)
            ra = _rng([self.sid, seed, "head"])
            head = float(el.get("head", 12))
            for sign in (1, -1):
                a = ang + math.pi + sign * math.radians(ra.uniform(20, 30))
                self.stroke(rough_segment(bx, by, bx + math.cos(a) * head,
                                          by + math.sin(a) * head, ra, 1.0, .6),
                            col, float(el.get("width", 2.0)))
        if el.get("label"):
            self.text(float(el.get("label_x", pts[-1][0])),
                      float(el.get("label_y", pts[-1][1] - 10)), el["label"],
                      float(el.get("label_size", 15)),
                      color(el.get("label_color", el.get("color", "ink")),
                            self.theme))

    def draw_text(self, el, seed):
        col = color(el.get("color", "ink"), self.theme)
        size = float(el.get("size", 18))
        r = _rng([self.sid, seed, "tilt"])
        rot = float(el.get("rotate", r.uniform(-0.8, 0.8)))
        lines = wrap_text(el.get("text", ""), float(el.get("w", 320)), size,
                          bold=el.get("bold", False),
                          max_lines=int(el.get("max_lines", 8)))
        self.multiline(float(el.get("x", 0)), float(el.get("y", 0)), lines, size,
                       col, anchor=el.get("anchor", "middle"),
                       bold=el.get("bold", False), rotate=rot)

    def draw_note(self, el, seed):
        """Amber margin note in the teacher's voice, slightly slanted."""
        col = color(el.get("color", "note"), self.theme)
        size = float(el.get("size", 15))
        r = _rng([self.sid, seed, "note"])
        rot = float(el.get("rotate", r.uniform(-3.5, -1.2)))
        w = float(el.get("w", 210))
        lines = wrap_text(el.get("text", ""), w, size,
                          max_lines=int(el.get("max_lines", 12)))
        x, y = float(el.get("x", 0)), float(el.get("y", 0))
        anchor = el.get("anchor", "start")
        self.multiline(x, y, lines, size, col, anchor=anchor, rotate=rot)
        if el.get("leader"):
            lx, ly = el["leader"][0], el["leader"][1]
            self.double_stroke(
                lambda rr: rough_path([(x, y - size * 0.4), (lx, ly)], rr, 2.0),
                col, 1.4, "5 4", seed + "-leader")

    def draw_circled(self, el, seed):
        """A term with a hand-drawn ring round it, the way you'd circle a board."""
        text = el.get("text", "")
        size = float(el.get("size", 19))
        x, y = float(el.get("x", 0)), float(el.get("y", 0))
        col = color(el.get("color", "ink"), self.theme)
        ring = color(el.get("ring", el.get("ring_color", "structure")), self.theme)
        self.text(x, y, text, size, col, anchor="middle",
                  bold=el.get("bold", True))
        rx = float(el.get("rx", max(text_width(text, size, True) / 2 + 14, 24)))
        ry = float(el.get("ry", size * 0.95))
        self.double_stroke(
            lambda rr: [rough_ellipse_path(x, y - size * 0.32, rx, ry, rr,
                                           amp=2.6, steps=12, start_wrap=0.22)],
            ring, 2.0, None, seed + "-ring")

    def draw_crossout(self, el, seed):
        """Struck through in red - we cross out, we never erase."""
        col = color(el.get("color", "error"), self.theme)
        if "x" in el and "w" in el:
            x, y = float(el["x"]), float(el["y"])
            w, h = float(el["w"]), float(el.get("h", 40))
        else:
            x, y, w, h = 0, 0, 100, 40
        pad = 6
        d1 = lambda rr: rough_path([(x - pad, y - pad), (x + w + pad, y + h + pad)],
                                   rr, 2.5, overshoot=4)
        d2 = lambda rr: rough_path([(x + w + pad, y - pad), (x - pad, y + h + pad)],
                                   rr, 2.5, overshoot=4)
        self.double_stroke(d1, col, 2.6, None, seed + "-a")
        if el.get("style", "x") != "strike":
            self.double_stroke(d2, col, 2.6, None, seed + "-b")
        if el.get("label"):
            self.text(x + w / 2, y + h + 22, el["label"], 15, col)

    def draw_badge(self, el, seed):
        """Numbered stroke badge - replay the drawing in the right order."""
        n = el.get("n", el.get("text", 1))
        x, y = float(el.get("x", 0)), float(el.get("y", 0))
        rad = float(el.get("r", 13))
        col = color(el.get("color", "note"), self.theme)
        self.double_stroke(
            lambda rr: [rough_ellipse_path(x, y, rad, rad, rr, 1.6, steps=10)],
            col, 1.8, None, seed + "-badge")
        was_blank, self.blank = self.blank, False
        self.text(x, y + rad * 0.42, n, rad * 1.25, col, bold=True)
        self.blank = was_blank

    def draw_highlight(self, el, seed):
        """A highlighter swipe behind the one thing that matters most."""
        x, y = float(el.get("x", 0)), float(el.get("y", 0))
        w, h = float(el.get("w", 140)), float(el.get("h", 26))
        col = color(el.get("color", "highlight"), self.theme)
        r = _rng([self.sid, seed, "hl"])
        self.stroke(hachure_rect(x, y, w, h, r, gap=5.0, angle=-8),
                    col, 5.0, opacity=0.65)

    def draw_bar(self, el, seed):
        """A hachured measurement bar with the number hand-written beside it."""
        x, y = float(el.get("x", 0)), float(el.get("y", 0))
        w, h = float(el.get("w", 100)), float(el.get("h", 22))
        col = color(el.get("color", "structure"), self.theme)
        r = _rng([self.sid, seed, "bar"])
        self.stroke(hachure_rect(x, y, max(w, 1), h, r, gap=6.0, angle=-45),
                    col, 1.3, opacity=0.8)
        self.double_stroke(
            lambda rr: rough_path([(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
                                  rr, 1.4, closed=True),
            col, 1.8, None, seed)
        if el.get("label"):
            self.text(x - 8, y + h * 0.75, el["label"], float(el.get("size", 15)),
                      color("ink", self.theme), anchor="end")
        if el.get("value"):
            self.text(x + w + 8, y + h * 0.75, el["value"],
                      float(el.get("size", 15)), col, anchor="start", bold=True)

    # -- dispatch ----------------------------------------------------------

    DISPATCH = {
        "box": "draw_box", "rect": "draw_box", "card": "draw_box",
        "ellipse": "draw_ellipse", "circle": "draw_ellipse", "node": "draw_ellipse",
        "line": "draw_line", "arrow": "draw_line",
        "text": "draw_text", "label": "draw_text",
        "note": "draw_note", "margin-note": "draw_note", "margin_note": "draw_note",
        "circled": "draw_circled", "circled-term": "draw_circled",
        "circled_term": "draw_circled",
        "crossout": "draw_crossout", "cross-out": "draw_crossout",
        "strike": "draw_crossout",
        "badge": "draw_badge", "step": "draw_badge",
        "highlight": "draw_highlight", "highlighter": "draw_highlight",
        "bar": "draw_bar",
        "path": "draw_path", "polyline": "draw_path", "curve": "draw_path",
    }

    def draw(self, el, index):
        kind = str(el.get("type", "box")).strip().lower()
        method = self.DISPATCH.get(kind)
        seed = str(el.get("id", f"{kind}-{index}"))
        if method is None:
            # unknown type degrades to a text note rather than killing the run
            self.draw_text({"x": el.get("x", 20), "y": el.get("y", 20),
                            "text": el.get("label") or el.get("text") or kind,
                            "anchor": "start", "color": "muted", "size": 14}, seed)
            return
        if method == "draw_line":
            self.draw_line(el, seed, arrow=(kind == "arrow"))
        else:
            getattr(self, method)(el, seed)


def rough_ctrl_curve(pts, rng, amp=2.0):
    """A jittered quadratic-through-three-points, expressed as a cubic."""
    (x1, y1), (cx, cy), (x2, y2) = pts
    j = lambda: rng.uniform(-amp, amp)
    c1x, c1y = x1 + 2 / 3 * (cx - x1) + j(), y1 + 2 / 3 * (cy - y1) + j()
    c2x, c2y = x2 + 2 / 3 * (cx - x2) + j(), y2 + 2 / 3 * (cy - y2) + j()
    return (f"M{_f(x1 + j() * 0.4)},{_f(y1 + j() * 0.4)} "
            f"C{_f(c1x)},{_f(c1y)} {_f(c2x)},{_f(c2y)} {_f(x2)},{_f(y2)}")


# --------------------------------------------------------------------------
# document assembly
# --------------------------------------------------------------------------

def render(spec: dict, theme: str = "light", blank: bool = False) -> str:
    """Render one spec to an SVG string."""
    spec = dict(spec or {})
    w = float(spec.get("width", 900))
    h = float(spec.get("height", 600))
    sk = Sketch(spec, theme, blank)
    paper = color("paper", theme)
    ink = color("ink", theme)

    elements = spec.get("elements") or []
    if not isinstance(elements, list):
        elements = []

    title = spec.get("title") or spec.get("id") or "Sketch"
    desc = (spec.get("desc") or spec.get("alt")
            or f"Hand-drawn sketch: {title}.")
    if blank:
        desc = (f"Blank version of the sketch “{title}” with all labels "
                f"removed, for drawing from memory. " + str(desc))

    body = []

    # paper
    body.append(f'<rect width="{_f(w)}" height="{_f(h)}" fill="{paper}"/>')

    # title, hand-written top-left, with a wobbly underline
    ty = 0.0
    if title and not spec.get("hide_title"):
        sk.blank = False  # the title survives the blank variant
        sk.text(28, 40, title, float(spec.get("title_size", 26)), ink,
                anchor="start", bold=True)
        sk.double_stroke(
            lambda rr: rough_path(
                [(26, 50), (min(28 + text_width(title, 26, True) + 10, w - 20), 50)],
                rr, 2.0, overshoot=4),
            color("note", theme), 2.0, None, "title-rule")
        sk.blank = blank
        ty = 50
    body += sk.out
    sk.out = []

    for i, el in enumerate(elements):
        if not isinstance(el, dict):
            continue
        try:
            sk.draw(el, i)
        except Exception as exc:  # one bad element must never kill a diagram
            sk.out.append(f"<!-- element {i} failed: {esc(exc)} -->")
    body += sk.out
    sk.out = []

    # footer note for the blank variant
    if blank:
        sk.blank = False
        sk.text(w - 24, h - 18,
                "draw it from memory, then compare", 15,
                color("note", theme), anchor="end", rotate=-1.2)
        sk.blank = True
        body += sk.out
        sk.out = []

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {_f(w)} {_f(h)}" width="{_f(w)}" height="{_f(h)}" '
        f'role="img" aria-labelledby="t-{esc(spec.get("id","s"))} '
        f'd-{esc(spec.get("id","s"))}" font-family="{FONT_STACK}">',
        f'<title id="t-{esc(spec.get("id","s"))}">{esc(title)}</title>',
        f'<desc id="d-{esc(spec.get("id","s"))}">{esc(desc)}</desc>',
        f"<style>{FONT_IMPORT}text{{font-family:{FONT_STACK};}}</style>",
    ]
    parts += body
    parts.append("</svg>")
    return "\n".join(parts)


def render_all(spec: dict, out_dir, sid: str | None = None) -> dict:
    """Write the light / dark / blank triplet. Returns {variant: path}."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    sid = sid or str(spec.get("id") or "sketch")
    written = {}
    for suffix, theme, blank in (("", "light", False),
                                 ("-dark", "dark", False),
                                 ("-blank", "light", True)):
        path = out_dir / f"{sid}{suffix}.svg"
        path.write_text(render(spec, theme, blank), encoding="utf-8")
        written["light" if not suffix else suffix.strip("-")] = str(path)
    return written


# --------------------------------------------------------------------------
# self test
# --------------------------------------------------------------------------

DEMO = {
    "id": "sketch-selftest",
    "title": "Self-test: every element type",
    "alt": "A test sketch exercising boxes, ellipses, arrows, notes, a circled "
           "term, a red cross-out, numbered badges, a highlighter swipe and a bar.",
    "width": 900, "height": 520,
    "elements": [
        {"type": "badge", "id": "b1", "n": 1, "x": 40, "y": 96},
        {"type": "box", "id": "in", "x": 70, "y": 76, "w": 150, "h": 62,
         "label": "input", "color": "structure"},
        {"type": "arrow", "id": "a1", "x1": 224, "y1": 107, "x2": 296, "y2": 107,
         "label": "step"},
        {"type": "box", "id": "work", "x": 300, "y": 70, "w": 170, "h": 74,
         "label": "do the work", "color": "correct", "fill": "hachure",
         "fill_color": "correct"},
        {"type": "arrow", "id": "a2", "x1": 474, "y1": 107, "x2": 560, "y2": 107,
         "curve": 0.22, "label": "12x"},
        {"type": "ellipse", "id": "out", "cx": 640, "cy": 107, "rx": 78, "ry": 46,
         "label": "output", "color": "structure"},
        {"type": "box", "id": "bad", "x": 300, "y": 210, "w": 170, "h": 66,
         "label": "the naive way", "color": "error"},
        {"type": "crossout", "id": "x1", "x": 300, "y": 210, "w": 170, "h": 66,
         "label": "this is the bug"},
        {"type": "highlight", "id": "hl", "x": 296, "y": 320, "w": 180, "h": 28},
        {"type": "text", "id": "t1", "x": 386, "y": 340,
         "text": "~340 ms", "size": 20, "bold": True},
        {"type": "circled", "id": "c1", "x": 660, "y": 250, "text": "invariant"},
        {"type": "note", "id": "n1", "x": 60, "y": 330, "w": 220,
         "text": "careful - this is where everyone gets it wrong, every single "
                 "time. Remember week 11?", "leader": [290, 250]},
        {"type": "bar", "id": "bar1", "x": 560, "y": 360, "w": 240, "h": 22,
         "label": "DRAM", "value": "~80 ns", "color": "error"},
        {"type": "bar", "id": "bar2", "x": 560, "y": 400, "w": 40, "h": 22,
         "label": "L1", "value": "~1 ns", "color": "correct"},
        {"type": "arrow", "id": "a3", "x1": 200, "y1": 440, "x2": 330, "y2": 462,
         "dashed": True, "color": "note", "label": "...and then?"},
    ],
}


def _selftest() -> int:
    import xml.etree.ElementTree as ET
    out = Path("/tmp/sketch-selftest")
    written = render_all(DEMO, out)
    ok = True
    for variant, path in written.items():
        p = Path(path)
        raw = p.read_bytes()
        try:
            ET.fromstring(raw)
        except Exception as exc:
            print(f"FAIL  {p.name}: not well-formed XML: {exc}")
            ok = False
            continue
        kb = len(raw) / 1024
        flag = "OK " if kb < 200 else "BIG"
        print(f"{flag}  {p.name:34s} {kb:7.1f} KB")
        if kb >= 200:
            ok = False
    # determinism check
    a = render(DEMO, "light")
    b = render(DEMO, "light")
    print(("OK   deterministic" if a == b else "FAIL not deterministic"))
    ok = ok and a == b
    return 0 if ok else 1


def main(argv) -> int:
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 2:
        print(__doc__)
        return 2
    spec = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    out = argv[2] if len(argv) > 2 else "."
    for k, v in render_all(spec, out).items():
        print(f"{k:6s} {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
