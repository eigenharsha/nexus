#!/usr/bin/env python3
"""Week-26 chapter covers — three-beat advance organizers in the whiteboard
language (see tools/covers_w25.py for the pattern and rules)."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from sketch import render  # noqa: E402

W, H = 1000, 340
COVERS = {

"curriculum/p4/week-26/index.mdx": {
  "id": "cover-w26", "width": W, "height": H, "hide_title": True,
  "alt": "The week's journey: shrink the model, teach it with a sticky note, make it fill forms, and move it into your own machine.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 55, "y": 62},
    {"type": "box", "id": "s1a", "x": 80, "y": 40, "w": 90, "h": 64, "label": "16 GB", "size": 18, "color": "structure"},
    {"type": "box", "id": "s1b", "x": 190, "y": 58, "w": 52, "h": 40, "label": "4.5", "size": 16, "color": "correct"},
    {"type": "text", "id": "t1", "x": 160, "y": 132, "text": "shrink it (quantize)", "size": 15, "color": "muted", "w": 170},
    {"type": "badge", "id": "b2", "n": 2, "x": 300, "y": 62},
    {"type": "box", "id": "s2", "x": 325, "y": 40, "w": 120, "h": 64, "label": "frozen brain", "size": 15, "color": "structure"},
    {"type": "box", "id": "s2n", "x": 415, "y": 30, "w": 58, "h": 34, "label": "note", "size": 14, "color": "note", "fill": "hachure", "fill_gap": 9},
    {"type": "text", "id": "t2", "x": 395, "y": 132, "text": "teach it (LoRA)", "size": 15, "color": "muted", "w": 160},
    {"type": "badge", "id": "b3", "n": 3, "x": 540, "y": 62},
    {"type": "box", "id": "s3", "x": 565, "y": 40, "w": 130, "h": 64, "label": "name · qty · price", "size": 14, "color": "correct"},
    {"type": "text", "id": "t3", "x": 630, "y": 132, "text": "make it fill forms", "size": 15, "color": "muted", "w": 160},
    {"type": "badge", "id": "b4", "n": 4, "x": 770, "y": 62},
    {"type": "box", "id": "s4", "x": 795, "y": 40, "w": 150, "h": 64, "label": "your machine", "size": 16, "color": "note"},
    {"type": "text", "id": "t4", "x": 870, "y": 132, "text": "move it home (serve)", "size": 15, "color": "muted", "w": 160},
    {"type": "box", "id": "lab", "x": 300, "y": 180, "w": 400, "h": 60, "label": "the lab: the whole move, end to end", "size": 19, "color": "correct", "fill": "hachure", "fill_gap": 15},
    {"type": "circled", "id": "term", "x": 140, "y": 210, "text": "week 26", "ring": "note"},
    {"type": "note", "id": "n", "x": 730, "y": 195, "w": 240, "text": "stop paying rent per tile. The model becomes yours."},
    {"type": "text", "id": "dq", "x": 640, "y": 306, "text": "it starts at the front door: the friend does not fit…", "size": 19, "color": "note"},
  ],
  "arrow": (150, 300, 360, 300)},

"curriculum/p4/week-26/1-numeric-precision-quantization.mdx": {
  "id": "cover-w26m1", "width": W, "height": H, "hide_title": True,
  "alt": "The friend weighs 16 GB and the card holds 24; the MP3 idea shrinks each number's box; the measured result: 4.5 GB at ninety-nine percent quality, and 1-bit crossed out in red.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "brain", "x": 72, "y": 42, "w": 150, "h": 90, "label": "the brain: 8,000,000,000 numbers", "size": 14, "color": "structure"},
    {"type": "text", "id": "t1", "x": 150, "y": 162, "text": "16 GB in fat boxes —", "size": 15, "color": "muted", "w": 180},
    {"type": "text", "id": "t1b", "x": 150, "y": 184, "text": "your card holds 24", "size": 15, "color": "muted", "w": 180},
    {"type": "badge", "id": "b2", "n": 2, "x": 330, "y": 62},
    {"type": "text", "id": "cd", "x": 470, "y": 66, "text": "CD → MP3:", "size": 20, "w": 240},
    {"type": "text", "id": "cd2", "x": 470, "y": 104, "text": "10× smaller — and you", "size": 16, "color": "muted", "w": 999},
    {"type": "text", "id": "cd3", "x": 470, "y": 128, "text": "cannot hear the difference", "size": 16, "color": "muted", "w": 999},
    {"type": "text", "id": "cd4", "x": 470, "y": 166, "text": "same trick, on numbers", "size": 16, "color": "correct", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 660, "y": 62},
    {"type": "bar", "id": "q1", "x": 740, "y": 52, "w": 160, "h": 18, "label": "fp16", "value": "16 GB", "color": "structure"},
    {"type": "bar", "id": "q2", "x": 740, "y": 90, "w": 45, "h": 18, "label": "4-bit", "value": "4.5 GB · ~99%", "color": "correct"},
    {"type": "text", "id": "q3", "x": 800, "y": 146, "text": "1-bit: the song breaks", "size": 16, "color": "error"},
    {"type": "crossout", "id": "x", "x": 712, "y": 128, "w": 180, "h": 26, "style": "strike"},
    {"type": "circled", "id": "term", "x": 350, "y": 240, "text": "quantization", "ring": "note"},
    {"type": "note", "id": "n", "x": 620, "y": 222, "w": 330, "text": "a sliver of accuracy for a lot of memory — always measured, never assumed."},
    {"type": "text", "id": "dq", "x": 700, "y": 306, "text": "how small is too small? You will find the cliff.", "size": 19, "color": "note"},
  ],
  "arrow": (140, 300, 360, 300)},

"curriculum/p4/week-26/2-fine-tuning-when-and-why.mdx": {
  "id": "cover-w26m2", "width": W, "height": H, "hide_title": True,
  "alt": "Three ways to change the new hire: tell them (cheap, green), hand them the handbook, or send them to training — which needs 132 GB against your 24 and is crossed out in red.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "o1", "x": 72, "y": 42, "w": 190, "h": 58, "label": "just tell them (prompt)", "size": 16, "color": "correct"},
    {"type": "text", "id": "t1", "x": 165, "y": 130, "text": "free · instant · start here", "size": 15, "color": "muted", "w": 200},
    {"type": "badge", "id": "b2", "n": 2, "x": 330, "y": 62},
    {"type": "box", "id": "o2", "x": 355, "y": 42, "w": 200, "h": 58, "label": "hand them the handbook", "size": 16, "color": "structure"},
    {"type": "text", "id": "t2", "x": 455, "y": 138, "text": "facts live in the prompt —", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t2x", "x": 455, "y": 160, "text": "and, in Week 27, retrieval", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 625, "y": 62},
    {"type": "box", "id": "o3", "x": 650, "y": 42, "w": 190, "h": 58, "label": "send them to training", "size": 16, "color": "error"},
    {"type": "text", "id": "t3", "x": 748, "y": 130, "text": "needs 132 GB of GPU memory", "size": 16, "color": "error", "w": 999},
    {"type": "text", "id": "t3b", "x": 748, "y": 154, "text": "you own: 24", "size": 16, "color": "error", "w": 999},
    {"type": "crossout", "id": "x", "x": 650, "y": 42, "w": 190, "h": 58, "style": "strike"},
    {"type": "circled", "id": "term", "x": 200, "y": 235, "text": "fine-tuning", "ring": "note"},
    {"type": "note", "id": "n", "x": 400, "y": 215, "w": 330, "text": "change what the model DOES before you change what it IS. Habits deserve training; facts never do."},
    {"type": "text", "id": "dq", "x": 730, "y": 306, "text": "and when training is right — the sticky-note trick.", "size": 19, "color": "note"},
  ],
  "arrow": (150, 300, 370, 300)},

"curriculum/p4/week-26/3-lora-qlora.mdx": {
  "id": "cover-w26m3", "width": W, "height": H, "hide_title": True,
  "alt": "A giant frozen matrix stays read-only; a thin column times a flat row — the sticky note — attaches beside it; half a percent of the numbers trained, the whole model steered, on a 24 GB card.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "w", "x": 72, "y": 42, "w": 190, "h": 170, "label": "W — frozen ❄", "size": 18, "color": "structure", "fill": "hachure", "fill_gap": 16},
    {"type": "text", "id": "t1", "x": 165, "y": 244, "text": "8 billion numbers, read-only", "size": 15, "color": "muted", "w": 200},
    {"type": "badge", "id": "b2", "n": 2, "x": 330, "y": 62},
    {"type": "text", "id": "plus", "x": 320, "y": 135, "text": "+", "size": 40},
    {"type": "box", "id": "a", "x": 360, "y": 42, "w": 30, "h": 170, "label": "", "color": "note"},
    {"type": "box", "id": "bb", "x": 400, "y": 112, "w": 170, "h": 30, "label": "", "color": "correct"},
    {"type": "text", "id": "t2", "x": 470, "y": 190, "text": "the sticky note:", "size": 16, "color": "muted", "w": 200},
    {"type": "text", "id": "t2b", "x": 470, "y": 212, "text": "one column × one row", "size": 16, "color": "muted", "w": 200},
    {"type": "badge", "id": "b3", "n": 3, "x": 640, "y": 62},
    {"type": "text", "id": "s1", "x": 815, "y": 70, "text": "trained: 0.5% of the numbers", "size": 16, "color": "correct", "w": 999},
    {"type": "text", "id": "s2", "x": 815, "y": 98, "text": "steered: all of them", "size": 16, "color": "correct", "w": 999},
    {"type": "text", "id": "s3", "x": 815, "y": 138, "text": "QLoRA: the note on the", "size": 16, "color": "structure", "w": 999},
    {"type": "text", "id": "s3b", "x": 815, "y": 162, "text": "shrunken brain — fits 24 GB ✓", "size": 16, "color": "structure", "w": 999},
    {"type": "circled", "id": "term", "x": 700, "y": 225, "text": "LoRA", "ring": "note"},
    {"type": "note", "id": "n", "x": 330, "y": 262, "w": 340, "text": "do not repaint the house. Put up removable film."},
    {"type": "text", "id": "dq", "x": 760, "y": 306, "text": "Week 11's rank-1 trick, finally paying its rent.", "size": 19, "color": "note"},
  ],
  "arrow": (150, 300, 370, 300)},

"curriculum/p4/week-26/4-structured-output-tool-calling-behaviour.mdx": {
  "id": "cover-w26m4", "width": W, "height": H, "hide_title": True,
  "alt": "The friendly essay answer is crossed out in red; the form with exact fields gets a green tick; and the friend is handed labelled buttons — check price, send email — which is tool calling.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "essay", "x": 72, "y": 42, "w": 210, "h": 84, "label": "“Sure! Here is the JSON you asked for…”", "size": 14},
    {"type": "crossout", "id": "x", "x": 72, "y": 42, "w": 210, "h": 84, "style": "strike"},
    {"type": "text", "id": "t1", "x": 175, "y": 158, "text": "the essay: your parser dies", "size": 15, "color": "error", "w": 220},
    {"type": "badge", "id": "b2", "n": 2, "x": 350, "y": 62},
    {"type": "box", "id": "form", "x": 375, "y": 42, "w": 200, "h": 84, "label": "name: ___  qty: ___  price: ___", "size": 14, "color": "correct"},
    {"type": "text", "id": "t2", "x": 475, "y": 158, "text": "the form: exact shape, every time ✓", "size": 15, "color": "correct", "w": 210},
    {"type": "badge", "id": "b3", "n": 3, "x": 645, "y": 62},
    {"type": "box", "id": "btn1", "x": 670, "y": 42, "w": 130, "h": 40, "label": "check_price", "size": 14, "color": "structure"},
    {"type": "box", "id": "btn2", "x": 670, "y": 92, "w": 130, "h": 40, "label": "send_email", "size": 14, "color": "structure"},
    {"type": "text", "id": "t3", "x": 895, "y": 60, "text": "buttons, not prose —", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t3b", "x": 897, "y": 84, "text": "each says what it needs", "size": 15, "color": "muted", "w": 999},
    {"type": "circled", "id": "term", "x": 855, "y": 160, "text": "tool calling", "ring": "note"},
    {"type": "note", "id": "n", "x": 300, "y": 235, "w": 360, "text": "constrained decoding makes bad JSON impossible — and guarantees nothing about it being TRUE. Measure both."},
    {"type": "text", "id": "dq", "x": 740, "y": 306, "text": "count the failure rate yourself — script included.", "size": 19, "color": "note", "w": 460},
  ],
  "arrow": (290, 84, 370, 84)},

"curriculum/p4/week-26/5-local-self-hosted-serving.mdx": {
  "id": "cover-w26m5", "width": W, "height": H, "hide_title": True,
  "alt": "Moving day: one command gives a local model; then ten users knock at once and a queue forms; the break-even bars decide when owning beats renting.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "cmd", "x": 72, "y": 42, "w": 200, "h": 52, "label": "$ ollama run llama3", "size": 15, "color": "correct"},
    {"type": "box", "id": "home", "x": 100, "y": 130, "w": 140, "h": 80, "label": "your machine", "size": 15, "color": "structure"},
    {"type": "text", "id": "t1", "x": 170, "y": 244, "text": "the easy hour: it just works", "size": 15, "color": "muted", "w": 220},
    {"type": "badge", "id": "b2", "n": 2, "x": 340, "y": 62},
    {"type": "ellipse", "id": "u1", "cx": 390, "cy": 70, "rx": 20, "ry": 14, "label": "", "color": "note"},
    {"type": "ellipse", "id": "u2", "cx": 430, "cy": 60, "rx": 20, "ry": 14, "label": "", "color": "note"},
    {"type": "ellipse", "id": "u3", "cx": 470, "cy": 72, "rx": 20, "ry": 14, "label": "", "color": "note"},
    {"type": "ellipse", "id": "u4", "cx": 510, "cy": 62, "rx": 20, "ry": 14, "label": "", "color": "note"},
    {"type": "text", "id": "t2", "x": 460, "y": 122, "text": "…then ten users knock at once", "size": 16, "color": "muted", "w": 999},
    {"type": "text", "id": "t2b", "x": 460, "y": 150, "text": "batching, queues, and the", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t2c", "x": 460, "y": 172, "text": "memory bill from Module 1", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 640, "y": 62},
    {"type": "bar", "id": "r1", "x": 730, "y": 52, "w": 70,  "h": 18, "label": "rent (API)", "value": "$ / tile", "color": "structure"},
    {"type": "bar", "id": "r2", "x": 730, "y": 90, "w": 150, "h": 18, "label": "own (GPU)", "value": "$ / hour", "color": "note"},
    {"type": "text", "id": "t3", "x": 830, "y": 140, "text": "the lines cross at a volume —", "size": 15, "color": "muted", "w": 250},
    {"type": "text", "id": "t3b", "x": 830, "y": 162, "text": "you will compute where", "size": 15, "color": "muted", "w": 250},
    {"type": "circled", "id": "term", "x": 700, "y": 225, "text": "serving", "ring": "note"},
    {"type": "note", "id": "n", "x": 320, "y": 262, "w": 340, "text": "self-hosting is an engineering job, not a checkbox. This page is the honest version."},
    {"type": "text", "id": "dq", "x": 790, "y": 306, "text": "after moving day: what can it still not do?", "size": 19, "color": "note"},
  ],
  "arrow": (172, 96, 172, 128)},
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

BEGIN, END = "{/* HERO:BEGIN generated by tools/covers_w26.py */}", "{/* HERO:END */}"

if __name__ == "__main__":
    for slug, spec in COVERS.items():
        spec = dict(spec); arrow = spec.pop("arrow")
        variants = {}
        for theme in ("light", "dark"):
            svg = render(spec, theme).replace("</svg>", live_arrow(*arrow, theme) + "</svg>")
            variants[theme] = mdx_safe(svg)
        block = (f'{BEGIN}\n<Frame>\n  <div className="block dark:hidden w-full">\n    {variants["light"]}\n  </div>'
                 f'\n  <div className="hidden dark:block w-full">\n    {variants["dark"]}\n  </div>\n</Frame>\n{END}')
        p = ROOT / slug; t = p.read_text()
        if BEGIN in t:
            t = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), block, t, flags=re.S)
        else:
            i = t.index("<Note>") if "<Note>" in t else t.index("## ")
            t = t[:i] + block + "\n\n" + t[i:]
        p.write_text(t)
        print("cover inlined:", slug)
