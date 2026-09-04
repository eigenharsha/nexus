#!/usr/bin/env python3
"""Week-25 module-4 'one floor of the building' animation: three words flow
down their streams; in the TALK stage arrows cross between them (attention),
in the THINK stage each loops on itself (FFN), notes are added to the
whiteboard (residual), and the floor repeats ×32."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DUR = 12.0

def fade(t_in, t_out, fl=0.5):
    pts = [(0,0),(t_in,0),(t_in+fl,1),(t_out,1),(min(t_out+fl,DUR-0.01),0),(DUR,0)]
    return (f'<animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="{";".join(f"{t/DUR:.4f}" for t,_ in pts)}" '
            f'values="{";".join(str(v) for _,v in pts)}"/>')

def pulse(y0, y1, t0, t1, x, col):
    return f'''<circle cx="{x}" cy="{y0}" r="7" fill="{col}" opacity="0">
      <animate attributeName="cy" dur="{DUR}s" repeatCount="indefinite" keyTimes="0;{t0/DUR:.4f};{t1/DUR:.4f};1" values="{y0};{y0};{y1};{y1}"/>
      <animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" keyTimes="0;{t0/DUR:.4f};{(t0+0.3)/DUR:.4f};{t1/DUR:.4f};{min(t1+0.3,DUR-0.01)/DUR:.4f};1" values="0;0;1;1;0;0"/>
    </circle>'''

def build(ink, muted, talk, think, amber, bg):
    style = re.search(r"<style>.*?</style>",
        (ROOT/"assets/diagrams/p4-w25-m1.svg").read_text(), re.S).group(0)
    xs = [300, 480, 660]
    words = ["the", "cat", "slept"]
    streams = "".join(
        f'<line x1="{x}" y1="70" x2="{x}" y2="330" stroke="{muted}" stroke-width="2.5"/>'
        f'<text x="{x}" y="52" font-size="28" fill="{ink}" text-anchor="middle">{w}</text>'
        for x,w in zip(xs,words))
    cross = ""
    for i,x1 in enumerate(xs):
        for j,x2 in enumerate(xs):
            if i != j:
                cross += (f'<g opacity="0"><line x1="{x1}" y1="140" x2="{x2}" y2="170" stroke="{talk}" '
                          f'stroke-width="{3.5 if abs(i-j)==1 else 2}" stroke-dasharray="7 6" marker-end="none"/>'
                          + fade(2.0+0.15*(i+j), 5.2) + "</g>")
    loops = "".join(
        f'<g opacity="0"><path d="M{x} 225 C {x+45} 225 {x+45} 265 {x} 265" fill="none" stroke="{think}" stroke-width="3.5" stroke-dasharray="6 5"/>'
        + fade(5.8+0.2*i, 8.6) + "</g>" for i,x in enumerate(xs))
    pulses = "".join(pulse(70, 330, 0.8, 9.6, x, amber) for x in xs)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 400" width="1000" height="400" role="img" aria-label="Three words flow down through one floor: first arrows cross between them as they talk, then each loops on itself as it thinks alone, and the floor repeats thirty-two times." font-family="NexusHand, NexusSym, cursive">{style}
  <rect width="1000" height="400" rx="8" fill="{bg}"/>
  <rect x="200" y="100" width="560" height="240" rx="12" fill="none" stroke="{ink}" stroke-width="3.5" transform="rotate(-0.3 480 220)"/>
  {streams}{cross}{loops}{pulses}
  <text x="130" y="165" font-size="27" fill="{talk}" text-anchor="middle" opacity="0">1. talk{fade(2.0, 11.2)}</text>
  <text x="130" y="250" font-size="27" fill="{think}" text-anchor="middle" opacity="0">2. think{fade(5.8, 11.2)}</text>
  <text x="855" y="150" font-size="25" fill="{muted}" text-anchor="middle" opacity="0">nothing is{fade(3.0, 11.2)}</text>
  <text x="855" y="180" font-size="25" fill="{muted}" text-anchor="middle" opacity="0">ever erased{fade(3.0, 11.2)}</text>
  <text x="855" y="215" font-size="25" fill="{muted}" text-anchor="middle" opacity="0">— only added{fade(3.0, 11.2)}</text>
  <text x="480" y="380" font-size="30" fill="{amber}" text-anchor="middle" opacity="0">…and the whole floor repeats × 32{fade(9.2, 11.2)}</text>
</svg>'''

light = build("#1e1e1e","#adb5bd","#1971c2","#9c36b5","#f08c00","#fffdf7")
dark  = build("#e8e6e3","#5f5c57","#4dabf7","#da77f2","#ffb84d","#1a1a1a")
(ROOT/"assets/diagrams/p4-w25-m4-anim.svg").write_text(light)
(ROOT/"assets/diagrams/p4-w25-m4-anim-dark.svg").write_text(dark)

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    # responsive: fixed width crops in narrow columns; viewBox keeps the ratio
    s = re.sub(r'(<svg[^>]*?)\swidth="\d+"\sheight="\d+"', r'\1 width="100%"', s, count=1)
    # one line: multi-line JSX inside MDX trips micromark; single-line always compiles
    return re.sub(r"\s*\n\s*", " ", s)

frame = f'''<Frame caption="One floor, live: the words talk sideways (blue), then each thinks alone (violet), nothing on a whiteboard is ever erased — and the floor repeats thirty-two times. It loops — watch it twice.">
  <div className="block dark:hidden w-full">
    {mdx_safe(light)}
  </div>
  <div className="hidden dark:block w-full">
    {mdx_safe(dark)}
  </div>
</Frame>'''

page = ROOT/"curriculum/p4/week-25/4-the-transformer-block-the-full-decoder.mdx"
t = page.read_text()
m = re.search(r'<Frame caption="One floor, live.*?</Frame>', t, re.S)
if m: t = t[:m.start()] + frame + t[m.end():]
else:
    anchor = "{/* ANIM:W25M4 */}"
    assert anchor in t; t = t.replace(anchor, frame)
page.write_text(t)
print("block animation generated and inlined")
