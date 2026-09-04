#!/usr/bin/env python3
"""Week-25 module-2 'map of meanings' animation: word pins drop onto a map,
colour = kind of thing (animals teal, fruit orange, machines blue), and a
measuring line shows that close = similar meaning. Inlined into the page."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DUR = 12.0

def fade(t_in, t_out, fl=0.6):
    pts = [(0,0),(t_in,0),(t_in+fl,1),(t_out,1),(min(t_out+fl,DUR-0.01),0),(DUR,0)]
    return (f'<animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="{";".join(f"{t/DUR:.4f}" for t,_ in pts)}" '
            f'values="{";".join(str(v) for _,v in pts)}"/>')

def drop(t0, t1, y_from=-40):
    pts = [(0,y_from),(t0,y_from),(t1,0),(DUR,0)]
    return (f'<animateTransform attributeName="transform" type="translate" dur="{DUR}s" '
            f'repeatCount="indefinite" keyTimes="{";".join(f"{t/DUR:.4f}" for t,_ in pts)}" '
            f'values="{";".join(f"0 {y}" for _,y in pts)}" calcMode="spline" '
            f'keySplines="0 0 1 1;0.3 0 0.2 1;0 0 1 1"/>')

def pin(word, x, y, col, t_in, t_out=11.4):
    return f'''
  <g opacity="0">
    <g>
      <circle cx="{x}" cy="{y}" r="9" fill="{col}"/>
      <text x="{x}" y="{y-16}" font-size="30" fill="{col}" text-anchor="middle" font-weight="bold">{word}</text>
      {drop(t_in, t_in+0.7)}
    </g>
    {fade(t_in, t_out)}
  </g>'''

def build(ink, muted, amber, animal, fruit, machine, bg):
    style = re.search(r"<style>.*?</style>",
        (ROOT/"assets/diagrams/p4-w25-m1.svg").read_text(), re.S).group(0)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 400" width="1000" height="400" role="img" aria-label="Word pins drop onto a map: cat, dog and kitten land close together, banana and laptop far away, and a measuring line shows that close means similar meaning." font-family="NexusHand, NexusSym, cursive">{style}
  <rect x="0" y="0" width="1000" height="400" rx="8" fill="{bg}"/>
  <rect x="40" y="60" width="920" height="280" rx="10" fill="none" stroke="{muted}" stroke-width="2.5" stroke-dasharray="4 6"/>
  <text x="60" y="46" font-size="30" fill="{muted}" opacity="0">the map on the wall — one pin per word{fade(0.3, 11.4)}</text>
  {pin("cat", 300, 170, animal, 1.2)}
  {pin("dog", 400, 210, animal, 1.7)}
  {pin("banana", 720, 140, fruit, 2.6)}
  {pin("laptop", 810, 280, machine, 3.1)}
  {pin("kitten", 330, 250, animal, 4.6)}
  <g opacity="0">
    <line x1="308" y1="178" x2="392" y2="203" stroke="{animal}" stroke-width="3.5" stroke-dasharray="7 6"/>
    <text x="345" y="155" font-size="26" fill="{animal}" text-anchor="middle">close = similar meaning</text>
    {fade(6.2, 11.4)}
  </g>
  <g opacity="0">
    <line x1="310" y1="176" x2="800" y2="274" stroke="{machine}" stroke-width="3" stroke-dasharray="3 8"/>
    <text x="565" y="215" font-size="26" fill="{machine}" text-anchor="middle">far = different meaning</text>
    {fade(7.6, 11.4)}
  </g>
  <text x="500" y="380" font-size="28" fill="{amber}" text-anchor="middle" opacity="0">nobody placed the pins — training did{fade(9.0, 11.2)}</text>
</svg>'''

light = build(ink="#1e1e1e", muted="#6b6b6b", amber="#f08c00",
              animal="#0ca678", fruit="#e8590c", machine="#1971c2", bg="#fffdf7")
dark  = build(ink="#e8e6e3", muted="#9a9791", amber="#ffb84d",
              animal="#12b886", fruit="#ffa94d", machine="#4dabf7", bg="#1a1a1a")
(ROOT/"assets/diagrams/p4-w25-m2-anim.svg").write_text(light)
(ROOT/"assets/diagrams/p4-w25-m2-anim-dark.svg").write_text(dark)

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    # one line: multi-line JSX inside MDX trips micromark; single-line always compiles
    return re.sub(r"\s*\n\s*", " ", s)

frame = f'''<Frame caption="The map of meanings, live: word pins drop onto the map — the animals land together, the banana and the laptop land far away — and distance on the map is meaning. It repeats — watch it twice.">
  <div className="block dark:hidden w-full">
    {mdx_safe(light)}
  </div>
  <div className="hidden dark:block w-full">
    {mdx_safe(dark)}
  </div>
</Frame>'''

page = ROOT/"curriculum/p4/week-25/2-embeddings-positional-information.mdx"
t = page.read_text()
m = re.search(r'<Frame caption="The map of meanings.*?</Frame>', t, re.S)
if m:
    t = t[:m.start()] + frame + t[m.end():]
else:
    anchor = "{/* ANIM:W25M2 */}"
    assert anchor in t, "anchor missing — add {/* ANIM:W25M2 */} where the animation goes"
    t = t.replace(anchor, frame)
page.write_text(t)
print("map animation generated and inlined")
