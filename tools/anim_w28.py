#!/usr/bin/env python3
"""Week-28 animations: the code the map cannot find (m1), two lists fused by
rank (m2), and the shortlist re-ordered by a sharper judge (m4)."""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"tools"))
DUR = 12.0

def fade(a, b, fl=0.5):
    pts = [(0,0),(a,0),(a+fl,1),(b,1),(min(b+fl,DUR-0.01),0),(DUR,0)]
    return (f'<animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="{";".join(f"{t/DUR:.4f}" for t,_ in pts)}" values="{";".join(str(v) for _,v in pts)}"/>')
def move(a, b, dx, dy=0):
    pts = [(0,(0,0)),(a,(0,0)),(b,(dx,dy)),(DUR,(dx,dy))]
    return (f'<animateTransform attributeName="transform" type="translate" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="{";".join(f"{t/DUR:.4f}" for t,_ in pts)}" values="{";".join(f"{x} {y}" for _,(x,y) in pts)}" '
            f'calcMode="spline" keySplines="0 0 1 1;0.35 0 0.2 1;0 0 1 1"/>')
def style():
    return re.search(r"<style>.*?</style>", (ROOT/"assets/diagrams/p4-w25-m1.svg").read_text(), re.S).group(0)
def head(w, h, label, bg):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" '
            f'aria-label="{label}" font-family="NexusHand, NexusSym, cursive">{style()}'
            f'<rect width="{w}" height="{h}" rx="8" fill="{bg}"/>')

def m1(ink, muted, blue, green, red, amber, bg):
    return head(1000, 320, "The code TX-4471 finds nothing on the map of meanings because a code has no neighbourhood; the inverted index finds it exactly.", bg) + f'''
  <g opacity="0"><text x="60" y="46" font-size="24" fill="{muted}">query: “TX-4471”</text>{fade(0.3,11.4)}</g>
  <text x="230" y="92" font-size="23" fill="{muted}" opacity="0">the map of meanings{fade(0.8,5.6)}</text>
  <g opacity="0"><rect x="70" y="106" width="330" height="130" rx="8" fill="none" stroke="{muted}" stroke-width="2.5" stroke-dasharray="5 7"/>
    {"".join(f'<circle cx="{110+i*38}" cy="{150+((i*37)%60)}" r="4" fill="{muted}" opacity="0.6"/>' for i in range(8))}
    <text x="235" y="200" font-size="21" fill="{red}" text-anchor="middle">no neighbourhood · no meaning</text>{fade(1.2,5.6)}</g>
  <g opacity="0"><text x="235" y="262" font-size="22" fill="{red}" text-anchor="middle">3 passages about shipping delays ✗</text>{fade(3.0,5.6)}</g>
  <text x="720" y="92" font-size="23" fill="{muted}" opacity="0">the inverted index{fade(6.2,11.4)}</text>
  <g opacity="0"><rect x="560" y="106" width="330" height="130" rx="8" fill="{green}" fill-opacity="0.08" stroke="{green}" stroke-width="3"/>
    <text x="725" y="140" font-size="21" fill="{ink}">“refund”  →  doc 3, doc 91</text>
    <text x="725" y="170" font-size="21" fill="{ink}">“shipping” →  doc 7, doc 12</text>
    <text x="725" y="204" font-size="21" fill="{green}" font-weight="bold">“TX-4471” →  doc 4,812</text>{fade(6.6,11.4)}</g>
  <g opacity="0"><text x="725" y="262" font-size="22" fill="{green}" text-anchor="middle">exactly the right document ✓</text>{fade(8.6,11.4)}</g>
  <text x="500" y="302" font-size="25" fill="{amber}" text-anchor="middle" opacity="0">the map threw the letters away — the index kept them{fade(9.6,11.2)}</text>
</svg>'''

def m2(ink, muted, blue, green, amber, red, bg):
    dense = ["refund policy §4.2", "money-back terms", "shipping delays", "returns FAQ"]
    sparse = ["order TX-4471", "refund policy §4.2", "invoice codes", "returns FAQ"]
    def col(x, items, title, c, t0):
        rows = "".join(
            f'<rect x="{x}" y="{92+i*46}" width="250" height="36" rx="5" fill="{c}" fill-opacity="0.10" stroke="{c}" stroke-width="2.5"/>'
            f'<text x="{x+12}" y="{116+i*46}" font-size="18" fill="{ink}">{i+1}. {s}</text>' for i, s in enumerate(items))
        return f'<g opacity="0"><text x="{x+125}" y="72" font-size="22" fill="{c}" text-anchor="middle">{title}</text>{rows}{fade(t0,11.4)}</g>'
    return head(1000, 360, "Two ranked lists in different score currencies are fused by rank: the document both lists ranked highly rises to the top.", bg) + f'''
  {col(60, dense, "by meaning (0–1)", blue, 0.4)}
  {col(360, sparse, "by letters (BM25)", green, 1.2)}
  <g opacity="0"><text x="500" y="316" font-size="22" fill="{red}" text-anchor="middle">0.83 + 14.7 = ? — different currencies, do not add ✗</text>{fade(2.6,5.8)}</g>
  <g opacity="0"><text x="845" y="72" font-size="22" fill="{amber}" text-anchor="middle">fused by RANK</text>
    <rect x="700" y="92" width="270" height="36" rx="5" fill="{amber}" fill-opacity="0.18" stroke="{amber}" stroke-width="3"/>
    <text x="712" y="116" font-size="18" fill="{ink}" font-weight="bold">1. refund policy §4.2</text>
    <rect x="700" y="138" width="270" height="36" rx="5" fill="{amber}" fill-opacity="0.10" stroke="{amber}" stroke-width="2.5"/>
    <text x="712" y="162" font-size="18" fill="{ink}">2. order TX-4471</text>
    <rect x="700" y="184" width="270" height="36" rx="5" fill="{amber}" fill-opacity="0.10" stroke="{amber}" stroke-width="2.5"/>
    <text x="712" y="208" font-size="18" fill="{ink}">3. returns FAQ</text>{fade(6.4,11.4)}</g>
  <g opacity="0"><text x="500" y="316" font-size="23" fill="{amber}" text-anchor="middle">1/(k+rank), added — what both lists liked rises ✓</text>{fade(7.8,11.2)}</g>
</svg>'''

def m4(ink, muted, blue, green, amber, bg):
    before = ["shipping FAQ", "returns overview", "refund form", "policy §4.2 — the answer", "invoice help"]
    after  = ["policy §4.2 — the answer", "refund form", "returns overview", "shipping FAQ", "invoice help"]
    def col(x, items, title, c, t0, hi):
        rows = ""
        for i, s in enumerate(items):
            is_hi = (s == hi)
            rows += (f'<rect x="{x}" y="{96+i*42}" width="300" height="34" rx="5" fill="{green if is_hi else c}" '
                     f'fill-opacity="{0.22 if is_hi else 0.08}" stroke="{green if is_hi else c}" stroke-width="{3 if is_hi else 2.2}"/>'
                     f'<text x="{x+12}" y="{119+i*42}" font-size="17" fill="{green if is_hi else ink}">{i+1}. {s}</text>')
        return f'<g opacity="0"><text x="{x+150}" y="76" font-size="22" fill="{muted}" text-anchor="middle">{title}</text>{rows}{fade(t0,11.4)}</g>'
    return head(1000, 360, "The fast search puts the right passage fourth; a cross-encoder reads each passage together with the question and moves it to first.", bg) + f'''
  {col(60, before, "fast search: top 5", blue, 0.4, "policy §4.2 — the answer")}
  <g opacity="0"><text x="500" y="180" font-size="26" fill="{amber}" text-anchor="middle">read each</text>
    <text x="500" y="210" font-size="26" fill="{amber}" text-anchor="middle">WITH the question</text>
    <path d="M430 232 L570 232" stroke="{amber}" stroke-width="4" stroke-dasharray="10 8">
      <animate attributeName="stroke-dashoffset" from="36" to="0" dur="1.3s" repeatCount="indefinite"/></path>{fade(3.4,11.4)}</g>
  {col(640, after, "after re-ranking", blue, 6.4, "policy §4.2 — the answer")}
  <text x="500" y="336" font-size="25" fill="{amber}" text-anchor="middle" opacity="0">slow and sharp — but only on five, never on ten million{fade(8.8,11.2)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)

L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",red="#e03131",amber="#f08c00",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",red="#ff8787",amber="#ffb84d",bg="#1a1a1a")
def only(d, fn):
    import inspect
    return {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}

JOBS = [
 ("curriculum/p4/week-28/1-sparse-retrieval-bm25.mdx", "ANIM:W28M1", m1,
  "The code, live: TX-4471 has no neighbourhood on the map so semantic search returns the wrong passages; the inverted index kept the letters and finds it exactly. It repeats — watch both."),
 ("curriculum/p4/week-28/2-hybrid-search-fusion.mdx", "ANIM:W28M2", m2,
  "Fusion, live: two lists in different score currencies cannot be added; fused by rank instead, the document both searches liked rises to the top. It repeats — watch it twice."),
 ("curriculum/p4/week-28/4-re-ranking-with-cross-encoders.mdx", "ANIM:W28M4", m4,
  "Re-ranking, live: the right passage sits fourth after fast search; a judge that reads each passage together with the question moves it to first. It repeats — watch it twice."),
]
for slug, anchor, fn, caption in JOBS:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    if m: t = t[:m.start()] + frame + t[m.end():]
    else:
        a = "{/* " + anchor + " */}"
        assert a in t, slug
        t = t.replace(a, frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
