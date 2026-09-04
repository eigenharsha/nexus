#!/usr/bin/env python3
"""Week-19 animations: accuracy lying on an imbalanced problem (m1),
cross-validation rotating the held-out fold (m3), and the answer leaking into
a feature column (m4)."""
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
    dots = ""
    for i in range(100):
        x, y = 80 + (i % 20)*36, 90 + (i//20)*34
        fraud = i in (23, 67)
        col = red if fraud else muted
        dots += (f'<circle cx="{x}" cy="{y}" r="{7 if fraud else 5}" fill="{col}" '
                 f'fill-opacity="{0.9 if fraud else 0.35}"/>')
    return head(1000, 340, "In a hundred transactions only two are fraud, so a model that always says 'not fraud' scores 99% and has caught none of them.", bg) + f'''
  <text x="60" y="50" font-size="22" fill="{muted}">100 transactions · 2 of them fraud (in red)</text>
  {dots}
  <g opacity="0"><rect x="60" y="256" width="380" height="52" rx="7" fill="{green}" fill-opacity="0.12" stroke="{green}" stroke-width="3.5"/>
    <text x="250" y="288" font-size="21" fill="{green}" text-anchor="middle">the model: 99% accurate ✓</text>{fade(1.2,11.4)}</g>
  <g opacity="0"><rect x="500" y="256" width="440" height="52" rx="7" fill="{red}" fill-opacity="0.10" stroke="{red}" stroke-width="3.5"/>
    <text x="720" y="288" font-size="21" fill="{red}" text-anchor="middle">it answers “not fraud” to everything</text>{fade(4.2,11.4)}</g>
  <g opacity="0"><text x="500" y="228" font-size="24" fill="{amber}" text-anchor="middle">caught: 0 of 2. Precision and recall would have said so.</text>{fade(7.4,11.4)}</g>
</svg>'''

def m3(ink, muted, blue, green, amber, bg):
    rows = ""
    for f in range(5):
        y = 78 + f*46
        for k in range(5):
            x = 300 + k*118
            held = (k == f)
            col = amber if held else blue
            rows += (f'<g opacity="0"><rect x="{x}" y="{y}" width="106" height="34" rx="5" fill="{col}" '
                     f'fill-opacity="{0.3 if held else 0.10}" stroke="{col}" stroke-width="{3 if held else 2}"/>'
                     f'<text x="{x+53}" y="{y+23}" font-size="15" fill="{col}" text-anchor="middle">'
                     f'{"exam" if held else "train"}</text>{fade(0.4+f*1.6, 11.4)}</g>')
        rows += (f'<text x="285" y="{y+23}" font-size="17" fill="{muted}" text-anchor="end" opacity="0">'
                 f'round {f+1}{fade(0.4+f*1.6, 11.4)}</text>')
    return head(1000, 340, "Cross-validation rotates which fifth of the data is the exam, so every row is examined once and the five scores are averaged.", bg) + f'''
  <text x="60" y="48" font-size="22" fill="{muted}">every row gets a turn as the exam:</text>
  {rows}
  <text x="500" y="318" font-size="24" fill="{amber}" text-anchor="middle" opacity="0">five scores, averaged — no single unlucky split can fool you{fade(8.6,11.2)}</text>
</svg>'''

def m4(ink, muted, blue, green, red, amber, bg):
    rows = [("Alice", "42", "yes", "moved abroad"), ("Bob", "31", "no", ""),
            ("Chen", "55", "yes", "too expensive"), ("Dara", "27", "no", "")]
    body = ""
    for i,(n,a,ch,reason) in enumerate(rows):
        y = 110 + i*44
        body += (f'<text x="120" y="{y}" font-size="18" fill="{ink}">{n}</text>'
                 f'<text x="250" y="{y}" font-size="18" fill="{ink}">{a}</text>'
                 f'<text x="380" y="{y}" font-size="18" fill="{green if ch=="no" else red}">{ch}</text>'
                 f'<text x="540" y="{y}" font-size="18" fill="{red}">{reason}</text>')
    return head(1000, 340, "A cancellation_reason column is empty for everyone who stayed and filled in for everyone who left, so the model reads the answer instead of predicting it.", bg) + f'''
  <text x="120" y="70" font-size="19" fill="{muted}">customer</text>
  <text x="250" y="70" font-size="19" fill="{muted}">age</text>
  <text x="380" y="70" font-size="19" fill="{muted}">cancelled?</text>
  <text x="540" y="70" font-size="19" fill="{muted}">cancellation_reason</text>
  <line x1="110" y1="82" x2="880" y2="82" stroke="{muted}" stroke-width="2"/>
  {body}
  <g opacity="0"><rect x="520" y="86" width="340" height="200" rx="8" fill="none" stroke="{red}" stroke-width="3.5" stroke-dasharray="8 6"/>
    <text x="690" y="308" font-size="21" fill="{red}" text-anchor="middle">filled in only for the ones who left</text>{fade(2.0,11.4)}</g>
  <g opacity="0"><text x="270" y="290" font-size="23" fill="{green}">AUC = 0.99</text>
    <path d="M255 275 L410 300 M410 275 L255 300" stroke="{red}" stroke-width="4"/>{fade(5.0,11.4)}</g>
  <g opacity="0"><text x="500" y="42" font-size="24" fill="{amber}" text-anchor="middle">it did not predict the answer — it read it off the back of the card{fade(7.2,11.4)}</text></g>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",red="#e03131",amber="#f08c00",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",red="#ff8787",amber="#ffb84d",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
W = "curriculum/p3/week-19/"
for slug, anchor, fn, caption in [
 (W+"1-classification-metrics.mdx", "ANIM:W19M1", m1,
  "Accuracy lying, live: two frauds in a hundred transactions, and a model that answers 'not fraud' to everything scores 99% while catching none of them. It repeats — watch it twice."),
 (W+"3-validation-strategy.mdx", "ANIM:W19M3", m3,
  "Cross-validation, live: the exam fifth rotates through the data so every row is examined once, and the five scores are averaged. It repeats — watch all five rounds."),
 (W+"4-data-leakage-the-career-defining-failure-mode.mdx", "ANIM:W19M4", m4,
  "Leakage, live: the cancellation_reason column is filled in only for customers who left, so a 0.99 score means the model read the answer rather than predicted it. It repeats."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
