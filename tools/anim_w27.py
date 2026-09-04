#!/usr/bin/env python3
"""Week-27 animations: the library card (RAG loop), the tear (chunking), and
the shortcut (vector index search)."""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
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
    return head(1000, 360, "A question goes to the model and gets an invented answer, crossed out in red; then the question goes to the library first, comes back with a passage, and the answer arrives with a citation.", bg) + f'''
  <text x="60" y="46" font-size="24" fill="{muted}">without a library card:</text>
  <g opacity="0"><rect x="60" y="66" width="180" height="50" rx="6" fill="none" stroke="{ink}" stroke-width="3"/><text x="150" y="98" font-size="22" fill="{ink}" text-anchor="middle">“refund policy?”</text>{fade(0.4,5.4)}</g>
  <g opacity="0"><path d="M250 92 L370 92" stroke="{ink}" stroke-width="3" stroke-dasharray="8 6"/>{fade(1.0,5.4)}</g>
  <g opacity="0"><rect x="380" y="60" width="130" height="62" rx="6" fill="{blue}" fill-opacity="0.10" stroke="{blue}" stroke-width="3.5"/><text x="445" y="98" font-size="22" fill="{blue}" text-anchor="middle">the model</text>{fade(1.2,5.4)}</g>
  <g opacity="0"><rect x="560" y="62" width="330" height="58" rx="6" fill="none" stroke="{red}" stroke-width="3"/><text x="725" y="97" font-size="22" fill="{red}" text-anchor="middle">“Orders over £500 get 60 days…”</text>
    <path d="M566 66 L884 116 M884 66 L566 116" stroke="{red}" stroke-width="4"/><text x="725" y="140" font-size="20" fill="{red}" text-anchor="middle">invented — it never saw your policy</text>{fade(2.6,5.4)}</g>
  <text x="60" y="196" font-size="24" fill="{muted}" opacity="0">with a library card:{fade(6.0,11.4)}</text>
  <g opacity="0"><rect x="60" y="216" width="180" height="50" rx="6" fill="none" stroke="{ink}" stroke-width="3"/><text x="150" y="248" font-size="22" fill="{ink}" text-anchor="middle">“refund policy?”</text>{fade(6.0,11.4)}</g>
  <g opacity="0"><rect x="290" y="206" width="150" height="70" rx="6" fill="{green}" fill-opacity="0.12" stroke="{green}" stroke-width="3.5"/><text x="365" y="240" font-size="21" fill="{green}" text-anchor="middle">your docs</text><text x="365" y="264" font-size="19" fill="{green}" text-anchor="middle">1. look it up</text>{fade(6.6,11.4)}</g>
  <g opacity="0"><g><rect x="470" y="216" width="120" height="50" rx="5" fill="{amber}" fill-opacity="0.15" stroke="{amber}" stroke-width="3"/><text x="530" y="247" font-size="19" fill="{amber}" text-anchor="middle">§4.2 passage</text>{move(7.6,8.8,0)}</g>{fade(7.4,11.4)}</g>
  <g opacity="0"><rect x="620" y="206" width="130" height="70" rx="6" fill="{blue}" fill-opacity="0.10" stroke="{blue}" stroke-width="3.5"/><text x="685" y="248" font-size="21" fill="{blue}" text-anchor="middle">the model</text>{fade(8.4,11.4)}</g>
  <g opacity="0"><rect x="780" y="206" width="180" height="70" rx="6" fill="none" stroke="{green}" stroke-width="3.5"/><text x="870" y="238" font-size="20" fill="{green}" text-anchor="middle">“30 days — see</text><text x="870" y="262" font-size="20" fill="{green}" text-anchor="middle">§4.2” ✓</text>{fade(9.2,11.4)}</g>
  <text x="500" y="336" font-size="26" fill="{amber}" text-anchor="middle" opacity="0">look it up first — then answer, with the receipt{fade(9.8,11.2)}</text>
</svg>'''

def m2(ink, muted, red, green, amber, bg):
    return head(1000, 340, "A paragraph cut at a fixed character count splits a sentence and reverses its meaning; cutting on the paragraph seam, with overlap, keeps the rule and its exception together.", bg) + f'''
  <text x="60" y="46" font-size="23" fill="{muted}">cut every 500 characters:</text>
  <g opacity="0"><rect x="60" y="66" width="380" height="54" rx="5" fill="none" stroke="{ink}" stroke-width="3"/><text x="250" y="100" font-size="20" fill="{ink}" text-anchor="middle">“…the customer may not”</text>{fade(0.5,5.2)}</g>
  <g opacity="0"><rect x="470" y="66" width="380" height="54" rx="5" fill="none" stroke="{ink}" stroke-width="3"/><text x="660" y="100" font-size="20" fill="{ink}" text-anchor="middle">“be charged twice…”</text>{fade(1.1,5.2)}</g>
  <g opacity="0"><path d="M455 56 L455 132" stroke="{red}" stroke-width="5" stroke-dasharray="7 6"/><text x="455" y="156" font-size="21" fill="{red}" text-anchor="middle">torn here</text>{fade(1.8,5.2)}</g>
  <g opacity="0"><text x="500" y="190" font-size="22" fill="{red}" text-anchor="middle">retrieve the first piece and it says the exact opposite ✗</text>{fade(2.8,5.2)}</g>
  <text x="60" y="222" font-size="23" fill="{muted}" opacity="0">cut on the seam, with overlap:{fade(5.8,11.4)}</text>
  <g opacity="0"><rect x="60" y="240" width="430" height="54" rx="5" fill="{green}" fill-opacity="0.10" stroke="{green}" stroke-width="3.5"/><text x="275" y="274" font-size="20" fill="{green}" text-anchor="middle">“…may not be charged twice.”</text>{fade(6.0,11.4)}</g>
  <g opacity="0"><rect x="430" y="240" width="430" height="54" rx="5" fill="{amber}" fill-opacity="0.10" stroke="{amber}" stroke-width="3.5"/><text x="645" y="274" font-size="20" fill="{amber}" text-anchor="middle">“…charged twice. Exception: …”</text>{fade(7.0,11.4)}</g>
  <g opacity="0"><text x="460" y="318" font-size="22" fill="{green}" text-anchor="middle">the shared edge is the overlap — the rule and its exception stay together ✓{fade(8.4,11.2)}</text></g>
</svg>'''

def m4(ink, muted, blue, green, amber, red, bg):
    import random
    rng = random.Random(27)
    dots = "".join(f'<circle cx="{rng.randint(70,900)}" cy="{rng.randint(70,250)}" r="3.5" fill="{muted}" opacity="0.55"/>' for _ in range(120))
    return head(1000, 340, "Ten million pins: checking every pin is exact and slow; going to the right neighbourhood first, or following signposts, finds it fast but can miss.", bg) + f'''
  {dots}
  <circle cx="700" cy="150" r="10" fill="{green}"/><text x="700" y="128" font-size="20" fill="{green}" text-anchor="middle">the answer</text>
  <circle cx="120" cy="210" r="10" fill="{amber}"/><text x="120" y="240" font-size="20" fill="{amber}" text-anchor="middle">your question</text>
  <g opacity="0"><text x="500" y="42" font-size="23" fill="{ink}" text-anchor="middle">flat: measure the distance to all 10,000,000 — always right, always slow</text>{fade(0.4,3.8)}</g>
  <g opacity="0"><text x="500" y="42" font-size="23" fill="{blue}" text-anchor="middle">IVF: go to the right neighbourhood first, then look around</text>
    <ellipse cx="690" cy="150" rx="130" ry="80" fill="{blue}" fill-opacity="0.10" stroke="{blue}" stroke-width="3.5" stroke-dasharray="9 7"/>{fade(4.2,7.6)}</g>
  <g opacity="0"><text x="500" y="42" font-size="23" fill="{amber}" text-anchor="middle">HNSW: follow the signposts, each hop closer</text>
    <path d="M120 210 L300 170 L480 190 L600 158 L690 150" fill="none" stroke="{amber}" stroke-width="4" stroke-dasharray="10 8">
      <animate attributeName="stroke-dashoffset" from="36" to="0" dur="1.4s" repeatCount="indefinite"/></path>{fade(8.0,11.4)}</g>
  <text x="500" y="312" font-size="25" fill="{red}" text-anchor="middle" opacity="0">both skip most of the map — and both can miss. That miss rate is recall.{fade(9.4,11.2)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)

JOBS = [
 ("curriculum/p4/week-27/1-why-rag-and-the-ingestion-problem.mdx", "ANIM:W27M1", m1,
  dict(light=dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",red="#e03131",amber="#f08c00",bg="#fffdf7"),
       dark=dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",red="#ff8787",amber="#ffb84d",bg="#1a1a1a")),
  "The library card, live: ask without one and the answer is invented (crossed in red); ask with one and the passage is fetched first, so the answer arrives with its receipt. It repeats — watch it twice."),
 ("curriculum/p4/week-27/2-chunking-strategies.mdx", "ANIM:W27M2", m2,
  dict(light=dict(ink="#1e1e1e",muted="#6b6b6b",red="#e03131",green="#2f9e44",amber="#f08c00",bg="#fffdf7"),
       dark=dict(ink="#e8e6e3",muted="#9a9791",red="#ff8787",green="#6cc47a",amber="#ffb84d",bg="#1a1a1a")),
  "The tear, live: cutting on a character count splits a sentence and reverses its meaning; cutting on the seam with overlap keeps the rule and its exception together. It repeats — watch both."),
 ("curriculum/p4/week-27/4-vector-indexes-flat-ivf-hnsw.mdx", "ANIM:W27M4", m4,
  dict(light=dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",amber="#f08c00",red="#e03131",bg="#fffdf7"),
       dark=dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",amber="#ffb84d",red="#ff8787",bg="#1a1a1a")),
  "The shortcut, live: check every pin (exact, slow), or go to the right neighbourhood (IVF), or follow signposts hop by hop (HNSW) — both shortcuts can miss. It repeats — watch all three."),
]
for slug, anchor, fn, themes, caption in JOBS:
    light, dark = mdx_safe(fn(**themes["light"])), mdx_safe(fn(**themes["dark"]))
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
    p.write_text(t); print("animation:", slug.split("/")[-1])
