#!/usr/bin/env python3
"""Week-27 chapter covers — three-beat advance organizers in the whiteboard
language (see tools/covers_w25.py for the pattern and rules)."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from sketch import render  # noqa: E402

W, H = 1000, 340
COVERS = {

"curriculum/p4/week-27/index.mdx": {
  "id": "cover-w27", "width": W, "height": H, "hide_title": True,
  "alt": "The week's journey: messy documents become clean text, get cut into pieces, pinned on the map, indexed for fast search, and measured — ending in an answer with a citation.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 55, "y": 60},
    {"type": "box", "id": "s1", "x": 80, "y": 40, "w": 120, "h": 62, "label": "your PDFs", "size": 16, "color": "structure"},
    {"type": "text", "id": "t1", "x": 140, "y": 128, "text": "ingest", "size": 15, "color": "muted", "w": 140},
    {"type": "badge", "id": "b2", "n": 2, "x": 250, "y": 60},
    {"type": "box", "id": "s2", "x": 275, "y": 40, "w": 110, "h": 62, "label": "chunks", "size": 16, "color": "correct"},
    {"type": "text", "id": "t2", "x": 330, "y": 128, "text": "cut on the seams", "size": 15, "color": "muted", "w": 150},
    {"type": "badge", "id": "b3", "n": 3, "x": 435, "y": 60},
    {"type": "box", "id": "s3", "x": 460, "y": 40, "w": 110, "h": 62, "label": "pins", "size": 16, "color": "note"},
    {"type": "text", "id": "t3", "x": 515, "y": 128, "text": "map of meanings", "size": 15, "color": "muted", "w": 150},
    {"type": "badge", "id": "b4", "n": 4, "x": 620, "y": 60},
    {"type": "box", "id": "s4", "x": 645, "y": 40, "w": 110, "h": 62, "label": "index", "size": 16, "color": "structure"},
    {"type": "text", "id": "t4", "x": 700, "y": 128, "text": "fast among 10M", "size": 15, "color": "muted", "w": 150},
    {"type": "badge", "id": "b5", "n": 5, "x": 805, "y": 60},
    {"type": "box", "id": "s5", "x": 830, "y": 40, "w": 130, "h": 62, "label": "recall@k", "size": 16, "color": "correct"},
    {"type": "text", "id": "t5", "x": 895, "y": 128, "text": "prove it works", "size": 15, "color": "muted", "w": 150},
    {"type": "box", "id": "ans", "x": 290, "y": 178, "w": 420, "h": 60, "label": "“30 days — see §4.2” ✓ with the receipt", "size": 18, "color": "correct", "fill": "hachure", "fill_gap": 15},
    {"type": "circled", "id": "term", "x": 140, "y": 205, "text": "week 27 · RAG", "ring": "note"},
    {"type": "note", "id": "n", "x": 730, "y": 190, "w": 240, "text": "stop guessing. Look it up, then answer."},
    {"type": "text", "id": "dq", "x": 650, "y": 306, "text": "it starts with an answer that was confidently invented…", "size": 19, "color": "note"},
  ],
  "arrow": (150, 300, 370, 300)},

"curriculum/p4/week-27/1-why-rag-and-the-ingestion-problem.mdx": {
  "id": "cover-w27m1", "width": W, "height": H, "hide_title": True,
  "alt": "Asked about the refund policy the model invents an answer, crossed out in red; with the documents fetched first the same question gets a cited answer; the ingestion pile is the real work.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "q", "x": 70, "y": 44, "w": 190, "h": 54, "label": "“our refund policy?”", "size": 16},
    {"type": "box", "id": "inv", "x": 70, "y": 118, "w": 240, "h": 54, "label": "“60 days, no receipt…”", "size": 15, "color": "error"},
    {"type": "crossout", "id": "x", "x": 70, "y": 118, "w": 240, "h": 54, "style": "strike"},
    {"type": "text", "id": "t1", "x": 190, "y": 200, "text": "fluent · specific · invented", "size": 15, "color": "error", "w": 260},
    {"type": "badge", "id": "b2", "n": 2, "x": 380, "y": 62},
    {"type": "box", "id": "lib", "x": 405, "y": 44, "w": 150, "h": 78, "label": "your documents", "size": 15, "color": "correct", "fill": "hachure", "fill_gap": 14},
    {"type": "text", "id": "t2", "x": 480, "y": 148, "text": "1. look it up", "size": 16, "color": "correct", "w": 200},
    {"type": "text", "id": "t2b", "x": 480, "y": 172, "text": "2. then answer", "size": 16, "color": "correct", "w": 200},
    {"type": "badge", "id": "b3", "n": 3, "x": 640, "y": 62},
    {"type": "box", "id": "ans", "x": 665, "y": 44, "w": 280, "h": 78, "label": "“30 days — see §4.2” ✓", "size": 17, "color": "correct"},
    {"type": "text", "id": "t3", "x": 805, "y": 150, "text": "the receipt is the point —", "size": 15, "color": "muted", "w": 300},
    {"type": "text", "id": "t3b", "x": 805, "y": 172, "text": "a human can check the work", "size": 15, "color": "muted", "w": 300},
    {"type": "circled", "id": "term", "x": 300, "y": 250, "text": "RAG", "ring": "note"},
    {"type": "note", "id": "n", "x": 560, "y": 225, "w": 380, "text": "the idea is one sentence. The work is PDFs, scans and tables — that half decides whether it works."},
    {"type": "text", "id": "dq", "x": 700, "y": 306, "text": "but a 250-page manual will not fit. Where do you cut?", "size": 19, "color": "note"},
  ],
  "arrow": (150, 300, 360, 300)},

"curriculum/p4/week-27/2-chunking-strategies.mdx": {
  "id": "cover-w27m2", "width": W, "height": H, "hide_title": True,
  "alt": "A cut at 500 characters splits a sentence and reverses the policy, crossed in red; cutting on the paragraph seam with overlap keeps rule and exception together.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "c1", "x": 72, "y": 44, "w": 190, "h": 50, "label": "“…the customer may not”", "size": 14},
    {"type": "box", "id": "c2", "x": 72, "y": 104, "w": 190, "h": 50, "label": "“be charged twice…”", "size": 14},
    {"type": "crossout", "id": "x", "x": 72, "y": 44, "w": 190, "h": 110, "style": "strike"},
    {"type": "text", "id": "t1", "x": 168, "y": 184, "text": "cut at 500 chars: the meaning flips", "size": 15, "color": "error", "w": 250},
    {"type": "badge", "id": "b2", "n": 2, "x": 350, "y": 62},
    {"type": "box", "id": "g1", "x": 375, "y": 44, "w": 230, "h": 50, "label": "“…may not be charged twice.”", "size": 13, "color": "correct"},
    {"type": "box", "id": "g2", "x": 420, "y": 104, "w": 230, "h": 50, "label": "“…twice. Exception: …”", "size": 13, "color": "note"},
    {"type": "text", "id": "t2", "x": 500, "y": 184, "text": "cut on the seam · overlap the edges ✓", "size": 15, "color": "correct", "w": 300},
    {"type": "badge", "id": "b3", "n": 3, "x": 700, "y": 62},
    {"type": "bar", "id": "s1", "x": 760, "y": 52, "w": 34,  "h": 18, "label": "small", "value": "precise", "color": "structure"},
    {"type": "bar", "id": "s2", "x": 760, "y": 96, "w": 100, "h": 18, "label": "big", "value": "more context", "color": "note"},
    {"type": "text", "id": "t3", "x": 830, "y": 148, "text": "no universal winner —", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t3b", "x": 830, "y": 170, "text": "you measure, on your docs", "size": 15, "color": "muted", "w": 999},
    {"type": "circled", "id": "term", "x": 250, "y": 250, "text": "chunking", "ring": "note"},
    {"type": "note", "id": "n", "x": 520, "y": 232, "w": 380, "text": "never separate a rule from the exception that follows it."},
    {"type": "text", "id": "dq", "x": 690, "y": 306, "text": "now find the piece that says “refund” — when they typed “money back”.", "size": 19, "color": "note"},
  ],
  "arrow": (150, 300, 350, 300)},

"curriculum/p4/week-27/3-embeddings-for-retrieval.mdx": {
  "id": "cover-w27m3", "width": W, "height": H, "hide_title": True,
  "alt": "Keyword search for money back returns nothing because the document says refund; on the map of meanings the two land beside each other and the right passage comes back.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "q", "x": 72, "y": 44, "w": 200, "h": 50, "label": "“how do I get my money back?”", "size": 13},
    {"type": "box", "id": "kw", "x": 72, "y": 110, "w": 200, "h": 46, "label": "keyword search: 0 results", "size": 14, "color": "error"},
    {"type": "crossout", "id": "x", "x": 72, "y": 110, "w": 200, "h": 46, "style": "strike"},
    {"type": "text", "id": "t1", "x": 172, "y": 186, "text": "not one word in common", "size": 15, "color": "error", "w": 240},
    {"type": "badge", "id": "b2", "n": 2, "x": 355, "y": 62},
    {"type": "box", "id": "map", "x": 380, "y": 44, "w": 280, "h": 130, "color": "muted", "dashed": True},
    {"type": "ellipse", "id": "e1", "cx": 470, "cy": 92, "rx": 62, "ry": 22, "label": "money back", "color": "note"},
    {"type": "ellipse", "id": "e2", "cx": 570, "cy": 132, "rx": 50, "ry": 22, "label": "refund", "color": "correct"},
    {"type": "text", "id": "t2", "x": 520, "y": 196, "text": "same map, neighbouring pins ✓", "size": 15, "color": "correct", "w": 300},
    {"type": "badge", "id": "b3", "n": 3, "x": 700, "y": 62},
    {"type": "text", "id": "t3", "x": 838, "y": 84, "text": "one model draws the pins:", "size": 16, "color": "muted", "w": 999},
    {"type": "text", "id": "t3b", "x": 838, "y": 112, "text": "the embedding model", "size": 18, "color": "structure", "w": 999},
    {"type": "text", "id": "t3c", "x": 838, "y": 152, "text": "index and query must use", "size": 15, "color": "error", "w": 999},
    {"type": "text", "id": "t3d", "x": 838, "y": 174, "text": "the SAME one, or two maps", "size": 15, "color": "error", "w": 999},
    {"type": "circled", "id": "term", "x": 260, "y": 250, "text": "semantic search", "ring": "note"},
    {"type": "note", "id": "n", "x": 560, "y": 232, "w": 380, "text": "meaning is position — Week 25's map, finally doing a job."},
    {"type": "text", "id": "dq", "x": 700, "y": 306, "text": "ten million pins, one question. Check them all?", "size": 19, "color": "note"},
  ],
  "arrow": (150, 300, 350, 300)},

"curriculum/p4/week-27/4-vector-indexes-flat-ivf-hnsw.mdx": {
  "id": "cover-w27m4", "width": W, "height": H, "hide_title": True,
  "alt": "Flat search checks all ten million pins and is exact but slow; IVF goes to the right neighbourhood; HNSW follows signposts; both shortcuts can miss, and that miss rate is recall.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "flat", "x": 72, "y": 44, "w": 190, "h": 56, "label": "check all 10,000,000", "size": 15, "color": "structure"},
    {"type": "text", "id": "t1", "x": 168, "y": 126, "text": "always right · seconds per query", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t1b", "x": 168, "y": 152, "text": "your users will not wait", "size": 15, "color": "error", "w": 999},
    {"type": "badge", "id": "b2", "n": 2, "x": 345, "y": 62},
    {"type": "ellipse", "id": "ivf", "cx": 470, "cy": 76, "rx": 90, "ry": 30, "label": "the right area", "color": "structure"},
    {"type": "text", "id": "t2", "x": 470, "y": 128, "text": "IVF: the right neighbourhood first", "size": 15, "color": "muted", "w": 999},
    {"type": "line", "id": "hn", "x1": 380, "y1": 168, "x2": 560, "y2": 152, "curve": 0.3, "color": "note", "width": 3.5, "dashed": True},
    {"type": "text", "id": "t2b", "x": 470, "y": 200, "text": "HNSW: signposts, hop by hop", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 660, "y": 62},
    {"type": "bar", "id": "r1", "x": 740, "y": 52, "w": 110, "h": 18, "label": "speed", "value": "100× faster", "color": "correct"},
    {"type": "bar", "id": "r2", "x": 740, "y": 96, "w": 80, "h": 18, "label": "recall", "value": "0.95, your dial", "color": "note"},
    {"type": "text", "id": "t3", "x": 830, "y": 150, "text": "sometimes the true nearest", "size": 15, "color": "error", "w": 300},
    {"type": "text", "id": "t3b", "x": 830, "y": 172, "text": "pin is in the area you skipped", "size": 15, "color": "error", "w": 300},
    {"type": "circled", "id": "term", "x": 210, "y": 252, "text": "approximate search", "ring": "note"},
    {"type": "note", "id": "n", "x": 560, "y": 236, "w": 380, "text": "you are buying speed with exactness. Know the price you paid."},
    {"type": "text", "id": "dq", "x": 700, "y": 306, "text": "it all works now. But is it any GOOD?", "size": 19, "color": "note"},
  ],
  "arrow": (150, 300, 350, 300)},

"curriculum/p4/week-27/5-building-evaluating-a-retrieval-system.mdx": {
  "id": "cover-w27m5", "width": W, "height": H, "hide_title": True,
  "alt": "The demo looks great and is crossed out as evidence; twenty known questions measure recall at 5; the answer arrives with citations a human can check.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "demo", "x": 72, "y": 44, "w": 190, "h": 54, "label": "“the demo looked great”", "size": 14, "color": "error"},
    {"type": "crossout", "id": "x", "x": 72, "y": 44, "w": 190, "h": 54, "style": "strike"},
    {"type": "text", "id": "t1", "x": 168, "y": 134, "text": "not evidence — the failures", "size": 15, "color": "error", "w": 999},
    {"type": "text", "id": "t1b", "x": 168, "y": 158, "text": "are the ones you did not try", "size": 15, "color": "error", "w": 999},
    {"type": "badge", "id": "b2", "n": 2, "x": 350, "y": 62},
    {"type": "box", "id": "set", "x": 375, "y": 44, "w": 200, "h": 54, "label": "20 questions, answers known", "size": 13, "color": "correct"},
    {"type": "bar", "id": "r1", "x": 430, "y": 118, "w": 150, "h": 18, "label": "recall@5", "value": "0.85", "color": "correct"},
    {"type": "bar", "id": "r2", "x": 430, "y": 156, "w": 60,  "h": 18, "label": "MRR", "value": "0.61", "color": "structure"},
    {"type": "text", "id": "t2", "x": 470, "y": 200, "text": "did the right passage come back at all?", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 660, "y": 62},
    {"type": "box", "id": "cite", "x": 685, "y": 44, "w": 260, "h": 78, "label": "“30 days — §4.2, p.47” ✓", "size": 16, "color": "correct"},
    {"type": "text", "id": "t3", "x": 815, "y": 150, "text": "citations: a human can check", "size": 15, "color": "muted", "w": 300},
    {"type": "text", "id": "t3b", "x": 815, "y": 172, "text": "the work instead of trusting it", "size": 15, "color": "muted", "w": 300},
    {"type": "circled", "id": "term", "x": 250, "y": 250, "text": "recall@k", "ring": "note"},
    {"type": "note", "id": "n", "x": 540, "y": 232, "w": 400, "text": "a perfect writer with the wrong passage still writes a wrong answer."},
    {"type": "text", "id": "dq", "x": 700, "y": 306, "text": "so why do exact codes like TX-4471 still fail?", "size": 19, "color": "note"},
  ],
  "arrow": (150, 300, 350, 300)},
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

BEGIN, END = "{/* HERO:BEGIN generated by tools/covers_w27.py */}", "{/* HERO:END */}"

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
