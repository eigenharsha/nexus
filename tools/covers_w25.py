#!/usr/bin/env python3
"""Week-25 chapter covers v2 — rendered by the house sketch renderer.

Each cover is a three-beat advance organizer in the whiteboard language:
numbered badges walk the chapter's arc, real numbers appear where the chapter
earns them, the failure is crossed out in red, one amber note speaks in the
teacher's voice, and a dashed amber arrow (continuously redrawing itself, the
only motion) dangles into the question the chapter answers. Responsive,
inline, one line of MDX."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from sketch import render  # noqa: E402

W, H = 1000, 340
COVERS = {

"curriculum/p4/week-25/index.mdx": {
  "id": "cover-w25", "width": W, "height": H, "hide_title": True,
  "alt": "The week's journey in six numbered stops — the door, the map, the pull, the stack, the tray, the scratch paper — ending at the lab where you build the whole room.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 60,  "y": 60},
    {"type": "box", "id": "s1", "x": 84,  "y": 40, "w": 130, "h": 56, "label": "the door", "size": 19, "color": "structure"},
    {"type": "badge", "id": "b2", "n": 2, "x": 240, "y": 60},
    {"type": "box", "id": "s2", "x": 264, "y": 40, "w": 130, "h": 56, "label": "the map", "size": 19, "color": "correct"},
    {"type": "badge", "id": "b3", "n": 3, "x": 420, "y": 60},
    {"type": "box", "id": "s3", "x": 444, "y": 40, "w": 130, "h": 56, "label": "the pull", "size": 19, "color": "note"},
    {"type": "badge", "id": "b4", "n": 4, "x": 600, "y": 60},
    {"type": "box", "id": "s4", "x": 624, "y": 40, "w": 130, "h": 56, "label": "the stack ×32", "size": 19, "color": "structure"},
    {"type": "badge", "id": "b5", "n": 5, "x": 780, "y": 60},
    {"type": "box", "id": "s5", "x": 804, "y": 40, "w": 150, "h": 56, "label": "the tray + dial", "size": 19, "color": "correct"},
    {"type": "text", "id": "t1", "x": 148, "y": 122, "text": "your words become numbers", "size": 15, "color": "muted", "w": 150},
    {"type": "text", "id": "t2", "x": 328, "y": 122, "text": "numbers get meaning", "size": 15, "color": "muted", "w": 150},
    {"type": "text", "id": "t3", "x": 508, "y": 122, "text": "meanings bend each other", "size": 15, "color": "muted", "w": 150},
    {"type": "text", "id": "t4", "x": 688, "y": 122, "text": "repeated 32 floors deep", "size": 15, "color": "muted", "w": 150},
    {"type": "text", "id": "t5", "x": 878, "y": 122, "text": "the reply, one bet at a time", "size": 15, "color": "muted", "w": 150},
    {"type": "box", "id": "lab", "x": 300, "y": 175, "w": 400, "h": 62, "label": "the lab: build the whole room yourself", "size": 20, "color": "correct", "fill": "hachure", "fill_gap": 15},
    {"type": "circled", "id": "term", "x": 140, "y": 210, "text": "week 25", "ring": "note"},
    {"type": "note", "id": "n", "x": 705, "y": 190, "w": 235, "text": "no AI knowledge needed. The story starts from zero."},
    {"type": "text", "id": "dq", "x": 640, "y": 305, "text": "it begins with a question the smartest AI got wrong…", "size": 19, "color": "note"},
  ],
  "arrow": (150, 300, 360, 300)},

"curriculum/p4/week-25/1-text-tokens.mdx": {
  "id": "cover-w25m1", "width": W, "height": H, "hide_title": True,
  "alt": "Beat one: a question card heads for the sealed room's slot. Beat two: the word strawberry arrives as three tiles, none of them a letter. Beat three: the reply 'two' is crossed out in red — the model has three r's to find and cannot see any of them.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "card", "x": 70, "y": 42, "w": 200, "h": 62, "label": "how many r's in strawberry?", "size": 17},
    {"type": "box", "id": "door", "x": 120, "y": 150, "w": 120, "h": 105, "label": "the room", "size": 17, "color": "structure"},
    {"type": "box", "id": "slot", "x": 148, "y": 232, "w": 64, "h": 14, "color": "correct"},
    {"type": "badge", "id": "b2", "n": 2, "x": 370, "y": 62},
    {"type": "text", "id": "t2", "x": 520, "y": 60, "text": "what actually goes in:", "size": 17, "color": "muted"},
    {"type": "box", "id": "tk1", "x": 400, "y": 82, "w": 74, "h": 44, "label": "str", "size": 19, "color": "note"},
    {"type": "box", "id": "tk2", "x": 484, "y": 82, "w": 74, "h": 44, "label": "aw", "size": 19, "color": "note"},
    {"type": "box", "id": "tk3", "x": 568, "y": 82, "w": 90, "h": 44, "label": "berry", "size": 19, "color": "note"},
    {"type": "text", "id": "t2b", "x": 528, "y": 150, "text": "3 tiles — none is a letter", "size": 16, "color": "muted", "w": 360},
    {"type": "text", "id": "t2c", "x": 528, "y": 176, "text": "(the box holds 100,277 different tiles)", "size": 15, "color": "muted", "w": 360},
    {"type": "badge", "id": "b3", "n": 3, "x": 730, "y": 62},
    {"type": "box", "id": "rep", "x": 760, "y": 44, "w": 110, "h": 50, "label": "“two”", "size": 20, "color": "error"},
    {"type": "crossout", "id": "x", "x": 760, "y": 44, "w": 110, "h": 50, "style": "strike"},
    {"type": "text", "id": "t3", "x": 855, "y": 130, "text": "st r awbe rr y — three!", "size": 17, "color": "correct"},
    {"type": "circled", "id": "term", "x": 815, "y": 190, "text": "tokens", "ring": "note"},
    {"type": "note", "id": "n", "x": 330, "y": 262, "w": 340, "text": "your letters never enter the room. Only tile numbers do — and that explains everything."},
    {"type": "text", "id": "dq", "x": 700, "y": 306, "text": "so who decides where to cut? You build the cutter.", "size": 19, "color": "note"},
  ],
  "arrow": (272, 72, 395, 100)},

"curriculum/p4/week-25/2-embeddings-positional-information.mdx": {
  "id": "cover-w25m2", "width": W, "height": H, "hide_title": True,
  "alt": "Beat one: word pins on a map, animals clustered, banana far away. Beat two: real closeness numbers — king–queen 0.72, king–banana 0.13. Beat three: 'dog bites man' and 'man bites dog' are the same bag of tiles, crossed in red — order is missing.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "map", "x": 66, "y": 46, "w": 250, "h": 165, "color": "muted", "dashed": True},
    {"type": "ellipse", "id": "cat", "cx": 130, "cy": 95, "rx": 36, "ry": 20, "label": "cat", "color": "correct"},
    {"type": "ellipse", "id": "dog", "cx": 205, "cy": 130, "rx": 36, "ry": 20, "label": "dog", "color": "correct"},
    {"type": "ellipse", "id": "kit", "cx": 135, "cy": 165, "rx": 42, "ry": 20, "label": "kitten", "color": "correct"},
    {"type": "ellipse", "id": "ban", "cx": 268, "cy": 85, "rx": 44, "ry": 20, "label": "banana", "color": "note"},
    {"type": "text", "id": "t1", "x": 190, "y": 248, "text": "every tile gets a pin — position IS meaning", "size": 16, "color": "muted", "w": 300},
    {"type": "badge", "id": "b2", "n": 2, "x": 372, "y": 52},
    {"type": "text", "id": "p1", "x": 548, "y": 80, "text": "king ↔ queen   0.72  ✓ close", "size": 19, "color": "correct", "w": 320},
    {"type": "text", "id": "p2", "x": 548, "y": 118, "text": "king ↔ banana  0.13  far", "size": 19, "color": "muted", "w": 320},
    {"type": "text", "id": "t2", "x": 520, "y": 158, "text": "you will measure these yourself", "size": 15, "color": "muted"},
    {"type": "badge", "id": "b3", "n": 3, "x": 692, "y": 52},
    {"type": "text", "id": "s1", "x": 838, "y": 80, "text": "dog bites man", "size": 20},
    {"type": "text", "id": "s2", "x": 830, "y": 116, "text": "man bites dog", "size": 20},
    {"type": "crossout", "id": "x", "x": 740, "y": 58, "w": 185, "h": 72, "style": "strike"},
    {"type": "text", "id": "t3", "x": 838, "y": 156, "text": "same tiles! a bag has no order", "size": 16, "color": "error", "w": 300},
    {"type": "circled", "id": "term", "x": 500, "y": 212, "text": "embeddings", "ring": "note"},
    {"type": "note", "id": "n", "x": 715, "y": 228, "w": 250, "text": "nobody placed the pins — training did."},
    {"type": "text", "id": "dq", "x": 680, "y": 306, "text": "so where does word order come from? This chapter.", "size": 19, "color": "note"},
  ],
  "arrow": (160, 300, 400, 300)},

"curriculum/p4/week-25/3-self-attention.mdx": {
  "id": "cover-w25m3", "width": W, "height": H, "hide_title": True,
  "alt": "Beat one: the word bank means river-bank in one sentence and money-bank in another. Beat two: in 'the tired cat slept', cat pulls on slept with weight 0.650 while 'the' barely registers at 0.077. Beat three: the full hand-computed weight table with cat's row highlighted.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "highlight", "id": "h1", "x": 96, "y": 52, "w": 74, "h": 30},
    {"type": "text", "id": "s1", "x": 175, "y": 74, "text": "bank of the river", "size": 21, "color": "correct", "anchor": "middle", "w": 280},
    {"type": "highlight", "id": "h2", "x": 96, "y": 104, "w": 74, "h": 30},
    {"type": "text", "id": "s2", "x": 178, "y": 126, "text": "bank gave a loan", "size": 21, "color": "structure", "anchor": "middle", "w": 280},
    {"type": "text", "id": "t1", "x": 175, "y": 170, "text": "one pin, two meanings —", "size": 16, "color": "muted"},
    {"type": "text", "id": "t1b", "x": 175, "y": 192, "text": "the neighbours decide", "size": 16, "color": "muted"},
    {"type": "badge", "id": "b2", "n": 2, "x": 365, "y": 62},
    {"type": "text", "id": "m1", "x": 520, "y": 76, "text": "the  tired  cat  slept", "size": 24, "w": 300},
    {"type": "line", "id": "pull", "x1": 512, "y1": 92, "x2": 588, "y2": 92, "curve": 0.45, "color": "correct", "width": 4},
    {"type": "text", "id": "w1", "x": 545, "y": 132, "text": "cat → slept: 0.650", "size": 18, "color": "correct"},
    {"type": "text", "id": "w2", "x": 545, "y": 160, "text": "the → slept: 0.077", "size": 16, "color": "muted"},
    {"type": "badge", "id": "b3", "n": 3, "x": 700, "y": 62},
    {"type": "text", "id": "tbl0", "x": 840, "y": 66, "text": "the weights, by hand:", "size": 16, "color": "muted"},
    {"type": "highlight", "id": "h3", "x": 764, "y": 120, "w": 150, "h": 26},
    {"type": "text", "id": "tbl1", "x": 840, "y": 96,  "text": "the 0.077 · tired 0.082", "size": 17},
    {"type": "text", "id": "tbl2", "x": 840, "y": 138, "text": "cat 0.650 ←", "size": 19, "bold": True},
    {"type": "text", "id": "tbl3", "x": 840, "y": 176, "text": "slept 0.191   (sum = 1.000)", "size": 17, "w": 300},
    {"type": "circled", "id": "term", "x": 200, "y": 250, "text": "attention", "ring": "note"},
    {"type": "note", "id": "n", "x": 430, "y": 228, "w": 340, "text": "the most important mechanism in modern AI — and you will score it on paper."},
    {"type": "text", "id": "dq", "x": 690, "y": 306, "text": "how does a word ask a question? Queries, keys, folders.", "size": 19, "color": "note"},
  ],
  "arrow": (140, 300, 380, 300)},

"curriculum/p4/week-25/4-the-transformer-block-the-full-decoder.mdx": {
  "id": "cover-w25m4", "width": W, "height": H, "hide_title": True,
  "alt": "Beat one: a hall of tables asking different questions — who, when, what mood. Beat two: one floor — talk to the others, think alone, add and never erase. Beat three: the floor repeats 32 times, and two thirds of all parameters live in the think step.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "ellipse", "id": "h1", "cx": 130, "cy": 78,  "rx": 52, "ry": 22, "label": "who did it?", "color": "structure"},
    {"type": "ellipse", "id": "h2", "cx": 210, "cy": 130, "rx": 46, "ry": 22, "label": "when?", "color": "correct"},
    {"type": "ellipse", "id": "h3", "cx": 120, "cy": 170, "rx": 56, "ry": 22, "label": "what mood?", "color": "note"},
    {"type": "text", "id": "t1", "x": 165, "y": 225, "text": "32 conversations at once,", "size": 16, "color": "muted"},
    {"type": "text", "id": "t1b", "x": 165, "y": 246, "text": "each one a “head”", "size": 16, "color": "muted"},
    {"type": "badge", "id": "b2", "n": 2, "x": 355, "y": 62},
    {"type": "box", "id": "k1", "x": 390, "y": 46,  "w": 250, "h": 48, "label": "talk to the others", "size": 18, "color": "structure"},
    {"type": "box", "id": "k2", "x": 390, "y": 106, "w": 250, "h": 48, "label": "think alone", "size": 18, "color": "correct"},
    {"type": "box", "id": "k3", "x": 390, "y": 166, "w": 250, "h": 48, "label": "add — never erase", "size": 18, "color": "note"},
    {"type": "text", "id": "t2", "x": 515, "y": 246, "text": "one floor of the building", "size": 16, "color": "muted"},
    {"type": "badge", "id": "b3", "n": 3, "x": 700, "y": 62},
    {"type": "text", "id": "x32", "x": 800, "y": 96, "text": "× 32", "size": 46, "bold": True, "color": "error"},
    {"type": "text", "id": "t3", "x": 830, "y": 150, "text": "same shape in, same shape", "size": 16, "color": "muted"},
    {"type": "text", "id": "t3b", "x": 830, "y": 172, "text": "out — that is why it stacks", "size": 16, "color": "muted"},
    {"type": "text", "id": "t3c", "x": 830, "y": 210, "text": "66% of all parameters", "size": 17, "color": "structure"},
    {"type": "text", "id": "t3d", "x": 830, "y": 232, "text": "live in “think alone”", "size": 17, "color": "structure"},
    {"type": "circled", "id": "term", "x": 200, "y": 300, "text": "the Transformer block", "ring": "note"},
    {"type": "text", "id": "dq", "x": 720, "y": 306, "text": "you will count every parameter yourself.", "size": 19, "color": "note"},
  ],
  "arrow": (515, 285, 515, 40)},

"curriculum/p4/week-25/5-generation-decoding-inference-cost.mdx": {
  "id": "cover-w25m5", "width": W, "height": H, "hide_title": True,
  "alt": "Beat one: the reply comes out one tile per round, re-reading everything each time. Beat two: the tray of candidates with real probabilities. Beat three: dial low gives 'cold, cold, cold', dial high gives frozen potatoes — same model, different product.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "o1", "x": 70,  "y": 50, "w": 62, "h": 40, "label": "The", "size": 16, "color": "note"},
    {"type": "box", "id": "o2", "x": 142, "y": 50, "w": 62, "h": 40, "label": "best", "size": 16, "color": "note"},
    {"type": "box", "id": "o3", "x": 214, "y": 50, "w": 62, "h": 40, "label": "…", "size": 16, "color": "muted", "dashed": True},
    {"type": "text", "id": "t1", "x": 175, "y": 128, "text": "one tile per round — and it re-reads everything, every round", "size": 15, "color": "muted", "w": 230},
    {"type": "badge", "id": "b2", "n": 2, "x": 355, "y": 62},
    {"type": "bar", "id": "c1", "x": 430, "y": 52,  "w": 190, "h": 18, "label": "cold",   "value": "64%", "color": "structure"},
    {"type": "bar", "id": "c2", "x": 430, "y": 88,  "w": 72,  "h": 18, "label": "snow",   "value": "24%", "color": "structure"},
    {"type": "bar", "id": "c3", "x": 430, "y": 124, "w": 26,  "h": 18, "label": "tea",    "value": "8%",  "color": "structure"},
    {"type": "bar", "id": "c4", "x": 430, "y": 160, "w": 13,  "h": 18, "label": "potato", "value": "4%",  "color": "error"},
    {"type": "text", "id": "t2", "x": 520, "y": 208, "text": "the tray: 100,000 tiles, each with a score", "size": 15, "color": "muted", "w": 380},
    {"type": "badge", "id": "b3", "n": 3, "x": 694, "y": 52},
    {"type": "text", "id": "d1", "x": 858, "y": 76, "text": "dial low: “cold, cold, cold…”", "size": 17, "color": "structure", "w": 280},
    {"type": "text", "id": "d2", "x": 848, "y": 112, "text": "dial high: “potatoes freeze", "size": 17, "color": "error"},
    {"type": "text", "id": "d2b", "x": 856, "y": 134, "text": "slower under tarps”", "size": 17, "color": "error"},
    {"type": "text", "id": "t3", "x": 852, "y": 172, "text": "same model — different product", "size": 15, "color": "muted", "w": 270},
    {"type": "circled", "id": "term", "x": 210, "y": 250, "text": "decoding", "ring": "note"},
    {"type": "note", "id": "n", "x": 640, "y": 240, "w": 320, "text": "the dial is yours, not the model's. Temperature, top-k, top-p — all here."},
    {"type": "text", "id": "dq", "x": 660, "y": 306, "text": "and why does the 400th tile cost more than the 4th?", "size": 19, "color": "note"},
  ],
  "arrow": (130, 300, 350, 300)},

"curriculum/p4/week-25/6-reasoning-effort-and-thinking-budgets.mdx": {
  "id": "cover-w25m6", "width": W, "height": H, "hide_title": True,
  "alt": "Beat one: a page of scratch working, one path crossed out in red. Beat two: only then, the clean answer. Beat three: the bill — a hard question can spend 4,000 tiles thinking and 200 answering, and you pay for both.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "scr", "x": 72, "y": 46, "w": 200, "h": 150, "label": "scratch paper", "size": 17, "color": "muted", "fill": "hachure", "fill_gap": 15},
    {"type": "crossout", "id": "x", "x": 96, "y": 70, "w": 150, "h": 55, "style": "strike"},
    {"type": "text", "id": "t1", "x": 172, "y": 232, "text": "tries a path, crosses it out, tries again", "size": 15, "color": "muted"},
    {"type": "badge", "id": "b2", "n": 2, "x": 355, "y": 62},
    {"type": "box", "id": "ans", "x": 385, "y": 46, "w": 200, "h": 150, "label": "the answer", "size": 18, "color": "correct"},
    {"type": "text", "id": "t2", "x": 485, "y": 232, "text": "only then does it write", "size": 15, "color": "muted"},
    {"type": "badge", "id": "b3", "n": 3, "x": 645, "y": 50},
    {"type": "bar", "id": "bill1", "x": 700, "y": 60, "w": 240, "h": 18, "label": "thinking", "value": "4,000 tiles", "color": "note"},
    {"type": "bar", "id": "bill2", "x": 700, "y": 100, "w": 14, "h": 18, "label": "answer", "value": "200", "color": "correct"},
    {"type": "text", "id": "t3", "x": 815, "y": 150, "text": "a hard question's bill —", "size": 16, "color": "muted"},
    {"type": "text", "id": "t3b", "x": 815, "y": 172, "text": "and you pay for both rows", "size": 16, "color": "muted"},
    {"type": "circled", "id": "term", "x": 810, "y": 225, "text": "thinking tokens", "ring": "note"},
    {"type": "note", "id": "n", "x": 300, "y": 282, "w": 340, "text": "the scribbles are real tiles. Usually you never see them."},
    {"type": "text", "id": "dq", "x": 790, "y": 306, "text": "four dials control the spend — all four, here.", "size": 19, "color": "note"},
  ],
  "arrow": (280, 120, 380, 120)},
}

def live_arrow(x1, y1, x2, y2, theme):
    col = "#f08c00" if theme == "light" else "#ffb84d"
    return (f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{col}" stroke-width="3.5" '
            f'stroke-dasharray="12 9" opacity="0.9">'
            f'<animate attributeName="stroke-dashoffset" from="42" to="0" dur="1.6s" repeatCount="indefinite"/></path>')

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    s = re.sub(r'(<svg[^>]*?)\swidth="\d+"\sheight="\d+"', r'\1 width="100%"', s, count=1)
    return re.sub(r"\s*\n\s*", " ", s)

BEGIN, END = "{/* HERO:BEGIN generated by tools/covers_w25.py */}", "{/* HERO:END */}"

if __name__ == "__main__":
    for slug, spec in COVERS.items():
        spec = dict(spec)
        arrow = spec.pop("arrow")
        variants = {}
        for theme in ("light", "dark"):
            svg = render(spec, theme)
            svg = svg.replace("</svg>", live_arrow(*arrow, theme) + "</svg>")
            variants[theme] = mdx_safe(svg)
        block = (f'{BEGIN}\n<Frame>\n  <div className="block dark:hidden w-full">\n    {variants["light"]}\n  </div>'
                 f'\n  <div className="hidden dark:block w-full">\n    {variants["dark"]}\n  </div>\n</Frame>\n{END}')
        p = ROOT / slug; t = p.read_text()
        assert BEGIN in t, slug
        t = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), block, t, flags=re.S)
        p.write_text(t)
        print("cover inlined:", slug)
