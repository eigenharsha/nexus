#!/usr/bin/env python3
"""Week-32 animations: one request drawn as a trace of nested timed bars (m1),
and a bill halved by caching and trimming rather than by changing model (m3)."""
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
    spans = [("the whole request", 0, 900, 0, green, "30.0 s"),
             ("retrieve", 20, 90, 1, blue, "0.4 s"),
             ("re-rank", 120, 70, 1, blue, "0.3 s"),
             ("tool: get_order", 210, 640, 1, red, "28.1 s"),
             ("generate", 860, 40, 1, blue, "1.2 s")]
    rows = ""
    for i,(label, x, w, depth, col, dur) in enumerate(spans):
        y = 92 + i*44
        rows += (f'<g opacity="0"><rect x="{60+x*0.9:.0f}" y="{y}" width="{max(w*0.9,10):.0f}" height="30" rx="5" '
                 f'fill="{col}" fill-opacity="0.22" stroke="{col}" stroke-width="3"/>'
                 f'<text x="{64+x*0.9:.0f}" y="{y+21}" font-size="16" fill="{ink}">{label}</text>'
                 f'<text x="{72+x*0.9+max(w*0.9,10):.0f}" y="{y+21}" font-size="16" fill="{col}">{dur}</text>'
                 f'{fade(0.4+i*0.7, 11.4)}</g>')
    return head(1000, 340, "One slow request drawn as a trace: nested timed bars show that a single tool call took 28 of the 30 seconds.", bg) + f'''
  <text x="60" y="52" font-size="23" fill="{muted}">“your assistant took thirty seconds yesterday”</text>
  {rows}
  <g opacity="0"><path d="M255 108 L255 300" stroke="{red}" stroke-width="3" stroke-dasharray="6 7"/>
    <path d="M840 108 L840 300" stroke="{red}" stroke-width="3" stroke-dasharray="6 7"/>
    <text x="548" y="322" font-size="24" fill="{red}" text-anchor="middle">28 of the 30 seconds, in one tool call</text>{fade(5.4,11.4)}</g>
</svg>'''

def m3(ink, muted, blue, green, amber, red, bg):
    def bars(x0, y0, items, t0):
        out = ""
        for i,(label, w, col, val) in enumerate(items):
            y = y0 + i*46
            out += (f'<rect x="{x0}" y="{y}" width="{w}" height="30" rx="5" fill="{col}" fill-opacity="0.22" '
                    f'stroke="{col}" stroke-width="3"/><text x="{x0-12}" y="{y+21}" font-size="16" fill="{ink}" '
                    f'text-anchor="end">{label}</text><text x="{x0+w+12}" y="{y+21}" font-size="16" fill="{col}">{val}</text>')
        return f'<g opacity="0">{out}{fade(t0,11.4)}</g>'
    before = [("repeat context", 300, red, "48%"), ("already answered", 190, red, "31%"),
              ("big model on easy work", 90, amber, "14%"), ("actual new work", 44, green, "7%")]
    after  = [("repeat context", 60, green, "trimmed + cached"), ("already answered", 20, green, "cached"),
              ("routed to a small model", 40, green, "routed"), ("actual new work", 44, green, "unchanged")]
    return head(1000, 340, "Where the money goes: nearly half is re-sent context and a third is questions already answered, so caching and trimming halve the bill without changing the model.", bg) + f'''
  <text x="60" y="46" font-size="22" fill="{muted}">where the money actually goes:</text>
  {bars(230, 62, before, 0.4)}
  <text x="60" y="270" font-size="22" fill="{muted}" opacity="0">after four levers — same model:{fade(6.0,11.4)}</text>
  {bars(230, 62, after, 6.4)}
  <text x="500" y="322" font-size="25" fill="{amber}" text-anchor="middle" opacity="0">most of the bill is repetition, not intelligence{fade(8.4,11.2)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",amber="#f08c00",red="#e03131",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",amber="#ffb84d",red="#ff8787",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
for slug, anchor, fn, caption in [
 ("curriculum/p4/week-32/1-tracing-opentelemetry.mdx", "ANIM:W32M1", m1,
  "A trace, live: the same slow request drawn as nested timed bars — and one tool call turns out to be 28 of the 30 seconds. It repeats — watch it twice."),
 ("curriculum/p4/week-32/3-cost-engineering.mdx", "ANIM:W32M3", m3,
  "The bill, live: nearly half is context you re-send and a third is questions already answered — cached, trimmed and routed, the same model costs half as much. It repeats — watch both."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
