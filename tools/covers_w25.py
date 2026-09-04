#!/usr/bin/env python3
"""Week-25 chapter covers, drawn by the house sketch renderer (tools/sketch.py):
hand-drawn wobble, house palette, real labels — a miniature of the chapter's
story that is always visually complete. One dashed amber arrow per cover
continuously redraws itself for a touch of life; nothing ever fades to blank.
Inlined between the HERO markers (replaces the old geometric heroes)."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from sketch import render  # noqa: E402

H = 250
COVERS = {
"curriculum/p4/week-25/index.mdx": {
  "id": "cover-w25", "width": 1000, "height": H, "hide_title": True,
  "alt": "A sealed room with a slot in the door, a question card outside, and a promise that by Sunday you will build the room yourself.",
  "elements": [
    {"type": "box", "id": "room", "x": 620, "y": 40, "w": 220, "h": 170, "label": "the room", "color": "structure", "fill": "hachure", "fill_gap": 14},
    {"type": "box", "id": "slot", "x": 690, "y": 178, "w": 90, "h": 20, "color": "correct"},
    {"type": "box", "id": "card", "x": 90, "y": 80, "w": 250, "h": 70, "label": "how does ChatGPT actually work?", "color": "ink"},
    {"type": "circled", "id": "term", "x": 480, "y": 220, "text": "week 25", "ring": "note"},
    {"type": "note", "id": "n", "x": 90, "y": 195, "w": 300, "text": "by Sunday you build this room yourself."},
  ],
  "arrow": (350, 115, 680, 180)},
"curriculum/p4/week-25/1-text-tokens.mdx": {
  "id": "cover-w25m1", "width": 1000, "height": H, "hide_title": True,
  "alt": "A note asking how many r's are in strawberry heads for the door slot; the reply that came back, 'two', is crossed out in red.",
  "elements": [
    {"type": "box", "id": "door", "x": 700, "y": 30, "w": 190, "h": 185, "label": "the room", "size": 20, "color": "ink"},
    {"type": "box", "id": "slot", "x": 745, "y": 185, "w": 100, "h": 20, "color": "correct"},
    {"type": "box", "id": "note1", "x": 70, "y": 55, "w": 260, "h": 64, "label": "how many r's in strawberry?", "color": "ink"},
    {"type": "box", "id": "note2", "x": 380, "y": 165, "w": 120, "h": 54, "label": "“two”", "color": "error"},
    {"type": "crossout", "id": "x", "x": 380, "y": 165, "w": 120, "h": 54, "style": "strike"},
    {"type": "circled", "id": "term", "x": 560, "y": 60, "text": "tokens", "ring": "note"},
    {"type": "note", "id": "n", "x": 70, "y": 200, "w": 280, "text": "your letters never go in. Only numbers do.", "leader": [375, 195]},
  ],
  "arrow": (335, 88, 740, 190)},
"curriculum/p4/week-25/2-embeddings-positional-information.mdx": {
  "id": "cover-w25m2", "width": 1000, "height": H, "hide_title": True,
  "alt": "A wall map with word pins: cat, dog and kitten pinned close together, banana and laptop far away; close means similar meaning.",
  "elements": [
    {"type": "box", "id": "map", "x": 120, "y": 35, "w": 760, "h": 165, "color": "muted", "dashed": True},
    {"type": "ellipse", "id": "cat", "cx": 290, "cy": 100, "rx": 44, "ry": 26, "label": "cat", "color": "correct"},
    {"type": "ellipse", "id": "dog", "cx": 400, "cy": 140, "rx": 44, "ry": 26, "label": "dog", "color": "correct"},
    {"type": "ellipse", "id": "kit", "cx": 300, "cy": 170, "rx": 50, "ry": 25, "label": "kitten", "color": "correct"},
    {"type": "ellipse", "id": "ban", "cx": 700, "cy": 90, "rx": 56, "ry": 26, "label": "banana", "color": "note"},
    {"type": "ellipse", "id": "lap", "cx": 790, "cy": 165, "rx": 52, "ry": 26, "label": "laptop", "color": "structure"},
    {"type": "circled", "id": "term", "x": 545, "y": 225, "text": "the map of meanings", "ring": "note"},
    {"type": "note", "id": "n", "x": 490, "y": 145, "w": 200, "text": "close = similar meaning", "leader": [415, 130]},
  ],
  "arrow": (325, 108, 370, 128)},
"curriculum/p4/week-25/3-self-attention.mdx": {
  "id": "cover-w25m3", "width": 1000, "height": H, "hide_title": True,
  "alt": "The sentence 'she sat on the bank by the river'; a thick green arrow from river pulls on bank, a thin grey one from sat barely does.",
  "elements": [
    {"type": "text", "id": "s", "x": 500, "y": 95, "text": "she  sat  on  the  bank  by  the  river", "size": 30, "w": 900},
    {"type": "highlight", "id": "hl", "x": 468, "y": 70, "w": 96, "h": 36},
    {"type": "line", "id": "weak", "x1": 300, "y1": 112, "x2": 470, "y2": 110, "curve": 0.32, "color": "muted", "width": 1.6, "dashed": True},
    {"type": "circled", "id": "term", "x": 205, "y": 210, "text": "attention", "ring": "note"},
    {"type": "note", "id": "n", "x": 610, "y": 185, "w": 300, "text": "meaning bends towards the neighbour that pulls hardest."},
  ],
  "arrow": (742, 112, 528, 108)},
"curriculum/p4/week-25/4-the-transformer-block-the-full-decoder.mdx": {
  "id": "cover-w25m4", "width": 1000, "height": H, "hide_title": True,
  "alt": "Three stacked stages — talk to the others, think alone, add and never erase — with a multiplication sign showing the stack repeats 32 times.",
  "elements": [
    {"type": "box", "id": "b1", "x": 330, "y": 30, "w": 340, "h": 54, "label": "talk to the others (attention)", "color": "structure"},
    {"type": "box", "id": "b2", "x": 330, "y": 96, "w": 340, "h": 54, "label": "think alone (FFN)", "color": "correct"},
    {"type": "box", "id": "b3", "x": 330, "y": 162, "w": 340, "h": 54, "label": "add — never erase", "color": "note"},
    {"type": "text", "id": "x32", "x": 760, "y": 130, "text": "× 32", "size": 44, "bold": True, "color": "error"},
    {"type": "circled", "id": "term", "x": 180, "y": 120, "text": "one block", "ring": "note"},
    {"type": "note", "id": "n", "x": 700, "y": 200, "w": 260, "text": "same shape in, same shape out — that is why it stacks.", "leader": [670, 130]},
  ],
  "arrow": (500, 225, 500, 25)},
"curriculum/p4/week-25/5-generation-decoding-inference-cost.mdx": {
  "id": "cover-w25m5", "width": 1000, "height": H, "hide_title": True,
  "alt": "Four measurement bars for the candidate next words - cold, snow, tea, potato - with their probabilities, and the dial that decides which wins.",
  "elements": [
    {"type": "text", "id": "p", "x": 430, "y": 40, "text": "“the best thing about winter is …”", "size": 24, "color": "muted", "w": 700},
    {"type": "bar", "id": "b1", "x": 250, "y": 70,  "w": 380, "h": 22, "label": "cold",   "value": "64%", "color": "structure"},
    {"type": "bar", "id": "b2", "x": 250, "y": 112, "w": 140, "h": 22, "label": "snow",   "value": "24%", "color": "structure"},
    {"type": "bar", "id": "b3", "x": 250, "y": 154, "w": 50,  "h": 22, "label": "tea",    "value": "8%",  "color": "structure"},
    {"type": "bar", "id": "b4", "x": 250, "y": 196, "w": 24,  "h": 22, "label": "potato", "value": "4%",  "color": "error"},
    {"type": "circled", "id": "term", "x": 810, "y": 90, "text": "the dial", "ring": "note"},
    {"type": "note", "id": "n", "x": 730, "y": 165, "w": 240, "text": "one tile per round — and every round is a bet."},
  ],
  "arrow": (745, 112, 330, 202)},
"curriculum/p4/week-25/6-reasoning-effort-and-thinking-budgets.mdx": {
  "id": "cover-w25m6", "width": 1000, "height": H, "hide_title": True,
  "alt": "A page of crossed-out scratch working next to a clean answer page; the model thinks first, and you pay for the thinking too.",
  "elements": [
    {"type": "box", "id": "scr", "x": 200, "y": 40, "w": 220, "h": 160, "label": "scratch paper", "color": "muted", "fill": "hachure", "fill_gap": 16},
    {"type": "crossout", "id": "x", "x": 230, "y": 70, "w": 160, "h": 60, "style": "strike"},
    {"type": "box", "id": "ans", "x": 600, "y": 40, "w": 220, "h": 160, "label": "the answer", "color": "correct"},
    {"type": "circled", "id": "term", "x": 512, "y": 228, "text": "thinking tokens", "ring": "note"},
    {"type": "note", "id": "n", "x": 660, "y": 218, "w": 280, "text": "you pay for the scratch paper too."},
  ],
  "arrow": (425, 120, 595, 120)},
}

def live_arrow(x1, y1, x2, y2, theme):
    col = "#f08c00" if theme == "light" else "#ffb84d"
    return (f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{col}" stroke-width="3.5" '
            f'stroke-dasharray="12 9" opacity="0.9">'
            f'<animate attributeName="stroke-dashoffset" from="42" to="0" dur="1.6s" repeatCount="indefinite"/></path>')

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)

BEGIN, END = "{/* HERO:BEGIN generated by tools/covers_w25.py */}", "{/* HERO:END */}"
OLD_BEGIN = "{/* HERO:BEGIN generated by tools/heroes_w25.py */}"

for slug, spec in COVERS.items():
    arrow = spec.pop("arrow")
    variants = {}
    for theme in ("light", "dark"):
        svg = render(spec, theme)
        svg = svg.replace("</svg>", live_arrow(*arrow, theme) + "</svg>")
        variants[theme] = mdx_safe(svg)
    block = (f'{BEGIN}\n<Frame>\n  <div className="block dark:hidden w-full">\n    {variants["light"]}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {variants["dark"]}\n  </div>\n</Frame>\n{END}')
    p = ROOT / slug; t = p.read_text()
    for b in (BEGIN, OLD_BEGIN):
        if b in t:
            t = re.sub(re.escape(b) + r".*?" + re.escape(END), block, t, flags=re.S)
            break
    else:
        i = t.index("<Note>") if "<Note>" in t else t.index("## ")
        t = t[:i] + block + "\n\n" + t[i:]
    p.write_text(t)
    print("cover inlined:", slug)
