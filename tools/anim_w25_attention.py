#!/usr/bin/env python3
"""Week-25 module-3 'the pull' animation: the same word 'bank', bent two ways.
Scene 1: the river pulls bank towards water (teal). Scene 2: the loan pulls
bank towards money (violet). Line thickness = attention weight; the word's
colour is its meaning, and you watch it change. Inlined via ANIM:W25M3."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DUR = 14.0

def fade(t_in, t_out, fl=0.5):
    pts = [(0,0),(t_in,0),(t_in+fl,1),(t_out,1),(min(t_out+fl,DUR-0.01),0),(DUR,0)]
    return (f'<animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="{";".join(f"{t/DUR:.4f}" for t,_ in pts)}" '
            f'values="{";".join(str(v) for _,v in pts)}"/>')

def recolor(t0, t1, c_from, c_to):
    pts = [(0,c_from),(t0,c_from),(t1,c_to),(DUR,c_to)]
    return (f'<animate attributeName="fill" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="{";".join(f"{t/DUR:.4f}" for t,_ in pts)}" '
            f'values="{";".join(c for _,c in pts)}"/>')

def scene(words, bank_i, puller_i, weak_i, col, ink, muted, t0, t1, label):
    """words: list of (word, x). Pull lines appear, then bank recolours."""
    y = 120
    out = f'<g opacity="0">'
    for i,(w,x) in enumerate(words):
        fill = col if i == puller_i else ink
        extra = recolor(t0+2.2, t0+3.4, ink, col) if i == bank_i else ""
        weight = ' font-weight="bold"' if i in (bank_i, puller_i) else ""
        out += f'<text x="{x}" y="{y}" font-size="34" fill="{fill}" text-anchor="middle"{weight}>{w}{extra}</text>'
    bx, px, wx = words[bank_i][1], words[puller_i][1], words[weak_i][1]
    out += f'''
    <g opacity="0"><path d="M{px} {y+14} Q {(px+bx)//2} {y+62} {bx} {y+16}" fill="none" stroke="{col}" stroke-width="6" stroke-dasharray="10 7">
      <animate attributeName="stroke-dashoffset" from="34" to="0" dur="1.2s" repeatCount="indefinite"/></path>
      {fade(t0+1.0, t1-0.2)}</g>
    <g opacity="0"><path d="M{wx} {y+14} Q {(wx+bx)//2} {y+48} {bx} {y+18}" fill="none" stroke="{muted}" stroke-width="2" stroke-dasharray="4 8"/>
      {fade(t0+1.4, t1-0.2)}</g>
    <text x="500" y="205" font-size="27" fill="{col}" text-anchor="middle" opacity="0">{label}{fade(t0+2.6, t1-0.2)}</text>
    {fade(t0, t1)}</g>'''
    return out

def build(ink, muted, water, money, amber, bg):
    style = re.search(r"<style>.*?</style>",
        (ROOT/"assets/diagrams/p4-w25-m1.svg").read_text(), re.S).group(0)
    A = [("she",90),("sat",180),("on",260),("the",330),("bank",430),("by",530),("the",600),("river",710)]
    B = [("she",90),("walked",190),("into",290),("the",370),("bank",470),("for",570),("a",630),("loan",720)]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 260" width="1000" height="260" role="img" aria-label="The word bank is pulled towards river in one sentence and towards loan in another; the strong pull recolours it each time." font-family="NexusHand, NexusSym, cursive">{style}
  <rect width="1000" height="260" rx="8" fill="{bg}"/>
  {scene(A, 4, 7, 1, water, ink, muted, 0.4, 6.4, "river pulls hard — bank turns to water")}
  {scene(B, 4, 7, 1, money, ink, muted, 7.0, 13.0, "loan pulls hard — the same bank turns to money")}
  <text x="500" y="245" font-size="26" fill="{amber}" text-anchor="middle" opacity="0">thick line = strong attention · the word's colour is its meaning{fade(3.4, 13.2)}</text>
</svg>'''

light = build("#1e1e1e","#adb5bd","#0ca678","#9c36b5","#f08c00","#fffdf7")
dark  = build("#e8e6e3","#5f5c57","#12b886","#da77f2","#ffb84d","#1a1a1a")
(ROOT/"assets/diagrams/p4-w25-m3-anim.svg").write_text(light)
(ROOT/"assets/diagrams/p4-w25-m3-anim-dark.svg").write_text(dark)

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    return re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()

frame = f'''<Frame caption="Attention, live: in one sentence the river pulls bank towards water; in the other, the loan pulls the same word towards money. Thick line = strong pull. It repeats — watch both scenes.">
  <div className="block dark:hidden w-full">
    {mdx_safe(light)}
  </div>
  <div className="hidden dark:block w-full">
    {mdx_safe(dark)}
  </div>
</Frame>'''

page = ROOT/"curriculum/p4/week-25/3-self-attention.mdx"
t = page.read_text()
m = re.search(r'<Frame caption="Attention, live.*?</Frame>', t, re.S)
if m: t = t[:m.start()] + frame + t[m.end():]
else:
    anchor = "{/* ANIM:W25M3 */}"
    assert anchor in t; t = t.replace(anchor, frame)
page.write_text(t)
print("attention animation generated and inlined")
