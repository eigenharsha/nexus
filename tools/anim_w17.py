#!/usr/bin/env python3
"""Week-17 animations: a line finding its own slope (m1) and a model that
memorises the training points while its unseen-data error climbs (m4)."""
import re, inspect
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DUR = 12.0
def fade(a,b,fl=0.5):
    pts=[(0,0),(a,0),(a+fl,1),(b,1),(min(b+fl,DUR-0.01),0),(DUR,0)]
    return (f'<animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="{";".join(f"{t/DUR:.4f}" for t,_ in pts)}" values="{";".join(str(v) for _,v in pts)}"/>')
def style():
    return re.search(r"<style>.*?</style>", (ROOT/"assets/diagrams/p4-w25-m1.svg").read_text(), re.S).group(0)
def head(w,h,label,bg):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" '
            f'aria-label="{label}" font-family="NexusHand, NexusSym, cursive">{style()}<rect width="{w}" height="{h}" rx="8" fill="{bg}"/>')

def m1(ink, muted, blue, green, red, amber, bg):
    pts = [(120,250),(220,214),(320,178),(420,142),(520,106)]
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{ink}"/>' for x,y in pts)
    # three successive guesses converging on the data
    lines = ""
    for i,(y1,y2,col,t0,lab) in enumerate([(90,90,red,0.6,"guess 1 — badly wrong"),
                                            (170,130,amber,3.4,"guess 2 — closer"),
                                            (258,98,green,6.4,"guess 3 — the rule, found")]):
        lines += (f'<g opacity="0"><path d="M100 {y1} L560 {y2}" stroke="{col}" stroke-width="4"/>'
                  f'<text x="600" y="{y2+6}" font-size="20" fill="{col}">{lab}</text>{fade(t0,11.4)}</g>')
    bars = ""
    for i,(w,col,t0,lab) in enumerate([(240,red,1.4,"loss: 41.2"),(120,amber,4.2,"loss: 12.6"),(24,green,7.2,"loss: 0.9")]):
        bars += (f'<g opacity="0"><rect x="640" y="{206+i*38}" width="{w}" height="22" rx="4" fill="{col}" '
                 f'fill-opacity="0.25" stroke="{col}" stroke-width="2.5"/>'
                 f'<text x="{652+w}" y="{223+i*38}" font-size="17" fill="{col}">{lab}</text>{fade(t0,11.4)}</g>')
    return head(1000, 340, "A line is guessed, scored and nudged three times until it passes through the data points, while the loss bar shrinks from 41 to 0.9.", bg) + f'''
  <line x1="100" y1="285" x2="600" y2="285" stroke="{muted}" stroke-width="2.5"/>
  <line x1="100" y1="285" x2="100" y2="60" stroke="{muted}" stroke-width="2.5"/>
  <text x="350" y="316" font-size="18" fill="{muted}" text-anchor="middle">size</text>
  {dots}{lines}{bars}
  <text x="760" y="185" font-size="19" fill="{muted}" text-anchor="middle" opacity="0">how wrong the guess is{fade(1.2,11.4)}</text>
  <text x="500" y="42" font-size="24" fill="{amber}" text-anchor="middle" opacity="0">guess · score · nudge · repeat{fade(8.6,11.2)}</text>
</svg>'''

def m4(ink, muted, blue, green, red, amber, bg):
    import random
    rng = random.Random(17)
    pts = [(120+i*46, 210 - i*7 + rng.randint(-16,16)) for i in range(10)]
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{ink}"/>' for x,y in pts)
    wiggly = "M" + " L".join(f"{x} {y}" for x,y in pts)
    return head(1000, 340, "A straight line misses some points but generalises; a wiggly curve passes through every training point while its error on unseen data climbs.", bg) + f'''
  <line x1="100" y1="270" x2="600" y2="270" stroke="{muted}" stroke-width="2.5"/>
  {dots}
  <g opacity="0"><path d="M110 216 L580 148" stroke="{green}" stroke-width="4"/>
    <text x="330" y="112" font-size="20" fill="{green}" text-anchor="middle">the rule: misses a little, works on anything new ✓</text>{fade(0.5,5.4)}</g>
  <g opacity="0"><path d="{wiggly}" fill="none" stroke="{red}" stroke-width="4"/>
    <text x="330" y="112" font-size="20" fill="{red}" text-anchor="middle">memorised: hits every training point ✗</text>{fade(6.0,11.4)}</g>
  <g opacity="0">
    <rect x="660" y="120" width="120" height="22" rx="4" fill="{green}" fill-opacity="0.25" stroke="{green}" stroke-width="2.5"/>
    <text x="660" y="112" font-size="17" fill="{muted}">error on data it has seen</text>
    <text x="792" y="137" font-size="17" fill="{green}">low</text>
    <rect x="660" y="180" width="30" height="22" rx="4" fill="{green}" fill-opacity="0.25" stroke="{green}" stroke-width="2.5"/>
    <text x="660" y="172" font-size="17" fill="{muted}">error on NEW data</text>
    <text x="702" y="197" font-size="17" fill="{green}">low ✓</text>{fade(1.4,5.4)}</g>
  <g opacity="0">
    <rect x="660" y="120" width="16" height="22" rx="4" fill="{red}" fill-opacity="0.25" stroke="{red}" stroke-width="2.5"/>
    <text x="660" y="112" font-size="17" fill="{muted}">error on data it has seen</text>
    <text x="688" y="137" font-size="17" fill="{red}">zero!</text>
    <rect x="660" y="180" width="250" height="22" rx="4" fill="{red}" fill-opacity="0.25" stroke="{red}" stroke-width="2.5"/>
    <text x="660" y="172" font-size="17" fill="{muted}">error on NEW data</text>
    <text x="700" y="228" font-size="18" fill="{red}">the only number that matters</text>{fade(6.8,11.4)}</g>
  <text x="500" y="318" font-size="24" fill="{amber}" text-anchor="middle" opacity="0">a perfect training score is not evidence of anything{fade(9.0,11.2)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",amber="#f08c00",red="#e03131",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",amber="#ffb84d",red="#ff8787",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
for slug, anchor, fn, caption in [
 ("curriculum/p3/week-17/1-what-learning-from-data-actually-is.mdx", "ANIM:W17M1", m1,
  "Learning, live: a line is guessed, scored and nudged three times until it fits the data, and the loss bar falls from 41 to 0.9. It repeats — watch it twice."),
 ("curriculum/p3/week-17/4-regularization-the-bias-variance-trade-off.mdx", "ANIM:W17M4", m4,
  "Overfitting, live: a straight line misses a little and works on anything new; a wiggly curve hits every training point and fails on everything else. It repeats — watch both."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
