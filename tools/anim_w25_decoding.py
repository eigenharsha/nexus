#!/usr/bin/env python3
"""Week-25 module-5 'the dial' animation: the same tray of candidate tiles,
two turns of the temperature dial. Cold: one bar towers, the safe word is
picked, twice. Hot: the bars flatten and a wild tile wins. Bar height is
probability; the picked tile lights amber."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DUR = 14.0

def fade(t_in, t_out, fl=0.5):
    pts = [(0,0),(t_in,0),(t_in+fl,1),(t_out,1),(min(t_out+fl,DUR-0.01),0),(DUR,0)]
    return (f'<animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="{";".join(f"{t/DUR:.4f}" for t,_ in pts)}" '
            f'values="{";".join(str(v) for _,v in pts)}"/>')

def grow(t0, t1, y_base, h):
    return (f'<animate attributeName="height" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="0;{t0/DUR:.4f};{t1/DUR:.4f};1" values="0;0;{h};{h}"/>'
            f'<animate attributeName="y" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="0;{t0/DUR:.4f};{t1/DUR:.4f};1" values="{y_base};{y_base};{y_base-h};{y_base-h}"/>')

def scene(t0, t1, heights, pick_i, dial_deg, label, words, ink, muted, col, amber):
    y = 300; xs = [180, 330, 480, 630, 780]
    bars = ""
    for i,(x,h,w) in enumerate(zip(xs, heights, words)):
        c = amber if i == pick_i else col
        bars += (f'<rect x="{x-38}" width="76" rx="5" fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="3.5" y="{y}" height="0">'
                 f'{grow(t0+0.6, t0+1.8, y, h)}</rect>'
                 f'<text x="{x}" y="{y+34}" font-size="27" fill="{amber if i==pick_i else ink}" text-anchor="middle"'
                 f'{" font-weight=\"bold\"" if i==pick_i else ""}>{w}</text>')
    star = (f'<text x="{xs[pick_i]}" y="{y-heights[pick_i]-14}" font-size="32" fill="{amber}" text-anchor="middle" opacity="0">✓ picked'
            f'{fade(t0+2.6, t1-0.2)}</text>')
    dial = (f'<g opacity="0"><circle cx="900" cy="90" r="38" fill="none" stroke="{ink}" stroke-width="4"/>'
            f'<line x1="900" y1="90" x2="{900+30* (1 if dial_deg>0 else -1) * 0.7:.0f}" y2="{90-30*0.7:.0f}" stroke="{col}" stroke-width="5"/>'
            f'<text x="900" y="152" font-size="25" fill="{col}" text-anchor="middle">{label}</text>{fade(t0, t1)}</g>')
    return f'<g opacity="0">{bars}{star}{fade(t0, t1)}</g>{dial}'

def build(ink, muted, cold, hot, amber, bg):
    style = re.search(r"<style>.*?</style>",
        (ROOT/"assets/diagrams/p4-w25-m1.svg").read_text(), re.S).group(0)
    words = ["cold","snow","quiet","tea","potato"]
    sA = scene(0.3, 6.6, [190, 60, 34, 22, 8], 0, -40, "dial low — plays it safe", words, ink, muted, cold, amber)
    sB = scene(7.2, 13.4, [92, 74, 62, 55, 48], 4, 40, "dial high — anything can win", words, ink, muted, hot, amber)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" width="1000" height="360" role="img" aria-label="The same five candidate tiles under two dial settings: dial low, one bar towers and the safe word wins; dial high, the bars flatten and the wild tile wins." font-family="NexusHand, NexusSym, cursive">{style}
  <rect width="1000" height="360" rx="8" fill="{bg}"/>
  <text x="60" y="52" font-size="28" fill="{muted}">"The best thing about winter is …"</text>
  {sA}{sB}
</svg>'''

light = build("#1e1e1e","#6b6b6b","#1971c2","#e8590c","#f08c00","#fffdf7")
dark  = build("#e8e6e3","#9a9791","#4dabf7","#ffa94d","#ffb84d","#1a1a1a")
(ROOT/"assets/diagrams/p4-w25-m5-anim.svg").write_text(light)
(ROOT/"assets/diagrams/p4-w25-m5-anim-dark.svg").write_text(dark)

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    # responsive: fixed width crops in narrow columns; viewBox keeps the ratio
    s = re.sub(r'(<svg[^>]*?)\swidth="\d+"\sheight="\d+"', r'\1 width="100%"', s, count=1)
    # one line: multi-line JSX inside MDX trips micromark; single-line always compiles
    return re.sub(r"\s*\n\s*", " ", s)

frame = f'''<Frame caption="The dial, live: the same five tiles on the tray. Dial low — one bar towers and 'cold' wins every time. Dial high — the bars flatten and 'potato' gets its day. Bar height is probability. It repeats — watch both settings.">
  <div className="block dark:hidden w-full">
    {mdx_safe(light)}
  </div>
  <div className="hidden dark:block w-full">
    {mdx_safe(dark)}
  </div>
</Frame>'''

page = ROOT/"curriculum/p4/week-25/5-generation-decoding-inference-cost.mdx"
t = page.read_text()
m = re.search(r'<Frame caption="The dial, live.*?</Frame>', t, re.S)
if m: t = t[:m.start()] + frame + t[m.end():]
else:
    anchor = "{/* ANIM:W25M5 */}"
    assert anchor in t; t = t.replace(anchor, frame)
page.write_text(t)
print("decoding animation generated and inlined")
