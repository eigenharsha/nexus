#!/usr/bin/env python3
"""The week-25 'door machine' animation: generate light+dark SVGs and inline
them into curriculum/p4/week-25/1-text-tokens.mdx (Mintlify's CDN strips SMIL
from image assets, so animations must live inline in the page).
Each chunk of text has its own colour, carried to its number tile — the colour
teaches the chunk-to-number mapping without a single word."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DUR = 12.0

def fade(t_in, t_out, fl=0.6):
    pts = [(0,0),(t_in,0),(t_in+fl,1),(t_out,1),(min(t_out+fl,DUR-0.01),0),(DUR,0)]
    kt = ";".join(f"{t/DUR:.4f}" for t,_ in pts); kv = ";".join(str(v) for _,v in pts)
    return (f'<animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="{kt}" values="{kv}"/>')

def slide(t0, t1, dx):
    pts = [(0,(0,0)),(t0,(0,0)),(t1,(dx,0)),(DUR,(dx,0))]
    kt = ";".join(f"{t/DUR:.4f}" for t,_ in pts); kv = ";".join(f"{x} {y}" for _,(x,y) in pts)
    return (f'<animateTransform attributeName="transform" type="translate" dur="{DUR}s" '
            f'repeatCount="indefinite" keyTimes="{kt}" values="{kv}" calcMode="spline" '
            f'keySplines="0 0 1 1;0.4 0 0.2 1;0 0 1 1"/>')

def build(ink, muted, amber, door_accent, chunk_colors, bg):
    style = re.search(r"<style>.*?</style>",
        (ROOT/"assets/diagrams/p4-w25-m1.svg").read_text(), re.S).group(0)
    chunks = [("the","1820",120),(" cat","8415",320),(" sat","7731",520)]
    tiles = ""
    for i,((chunk,tid,x), col) in enumerate(zip(chunks, chunk_colors)):
        d = 0.35*i
        tiles += f'''
  <g opacity="0">
    <rect x="{x}" y="118" width="150" height="64" rx="10" fill="{col}" fill-opacity="0.10" stroke="{col}" stroke-width="4" stroke-dasharray="9 7" transform="rotate({-1.2+0.9*i} {x+75} 150)"/>
    {fade(2.2+d, 11.4)}
  </g>
  <text x="{x+75}" y="162" font-size="40" fill="{ink}" text-anchor="middle" opacity="0">{chunk.strip()}{fade(0.4+0.2*i, 11.4)}</text>
  <g opacity="0">
    <g>
      <rect x="{x+15}" y="215" width="120" height="56" rx="9" fill="{col}" fill-opacity="0.14" stroke="{col}" stroke-width="4" transform="rotate({1.1-0.8*i} {x+75} 243)"/>
      <text x="{x+75}" y="253" font-size="34" fill="{col}" text-anchor="middle" font-weight="bold">{tid}</text>
      {slide(6.2+d, 8.2+d, 700-x)}
    </g>
    {fade(4.4+d, 11.4)}
  </g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" width="1000" height="360" role="img" aria-label="The sentence 'the cat sat' is cut into three coloured pieces, each piece becomes a number tile of the same colour, and only the tiles slide through the slot to the model." font-family="NexusHand, NexusSym, cursive">{style}
  <rect x="0" y="0" width="1000" height="360" rx="8" fill="{bg}"/>
  <text x="30" y="52" font-size="30" fill="{muted}" opacity="0">1. your sentence{fade(0.4, 11.4)}</text>
  <text x="30" y="205" font-size="30" fill="{muted}" opacity="0">2. cut into tokens{fade(2.2, 11.4)}</text>
  <text x="30" y="300" font-size="30" fill="{muted}" opacity="0">3. only numbers go through{fade(4.4, 11.4)}</text>
  {tiles}
  <g>
    <rect x="790" y="60" width="170" height="240" rx="6" fill="none" stroke="{ink}" stroke-width="4" transform="rotate(0.6 875 180)"/>
    <text x="875" y="130" font-size="34" fill="{ink}" text-anchor="middle">the</text>
    <text x="875" y="172" font-size="34" fill="{ink}" text-anchor="middle">model</text>
    <text x="868" y="222" font-size="22" fill="{door_accent}" text-anchor="middle">slot</text>
    <rect x="808" y="228" width="120" height="26" rx="6" fill="{door_accent}" fill-opacity="0.12" stroke="{door_accent}" stroke-width="3.5"/>
  </g>
  <text x="500" y="335" font-size="28" fill="{amber}" text-anchor="middle" opacity="0">the model never sees your letters — only the numbers{fade(8.8, 11.2)}</text>
</svg>'''

light = build(ink="#1e1e1e", muted="#6b6b6b", amber="#f08c00", door_accent="#2f9e44",
              chunk_colors=["#e8590c","#1971c2","#9c36b5"], bg="#fffdf7")
dark  = build(ink="#e8e6e3", muted="#9a9791", amber="#ffb84d", door_accent="#6cc47a",
              chunk_colors=["#ffa94d","#4dabf7","#da77f2"], bg="#1a1a1a")
(ROOT/"assets/diagrams/p4-w25-m1-anim.svg").write_text(light)
(ROOT/"assets/diagrams/p4-w25-m1-anim-dark.svg").write_text(dark)

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    # responsive: fixed width crops in narrow columns; viewBox keeps the ratio
    s = re.sub(r'(<svg[^>]*?)\swidth="\d+"\sheight="\d+"', r'\1 width="100%"', s, count=1)
    # one line: multi-line JSX inside MDX trips micromark; single-line always compiles
    return re.sub(r"\s*\n\s*", " ", s)

frame = f'''<Frame caption="The door machine, live: your sentence is cut into coloured pieces, each piece becomes a number tile of the same colour, and only the numbers reach the model. It repeats — watch it twice.">
  <div className="block dark:hidden w-full">
    {mdx_safe(light)}
  </div>
  <div className="hidden dark:block w-full">
    {mdx_safe(dark)}
  </div>
</Frame>'''

page = ROOT/"curriculum/p4/week-25/1-text-tokens.mdx"
t = page.read_text()
m = re.search(r'<Frame caption="The door machine.*?</Frame>', t, re.S)
assert m, "frame anchor not found"
page.write_text(t[:m.start()] + frame + t[m.end():])
print("animation v2 generated and inlined")
