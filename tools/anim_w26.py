#!/usr/bin/env python3
"""Week-26 animations.
M1 'the shrinking boxes': one parameter stored in 32 bit-cells, then 16, then
4 — model size falls 32 GB → 16 GB → 4.5 GB while the quality bar barely
moves. M3 'the sticky note': a frozen giant matrix stays read-only while a
tiny column-times-row adapter slides in beside it; only the note trains."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DUR = 12.0

def fade(t_in, t_out, fl=0.5):
    pts = [(0,0),(t_in,0),(t_in+fl,1),(t_out,1),(min(t_out+fl,DUR-0.01),0),(DUR,0)]
    return (f'<animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="{";".join(f"{t/DUR:.4f}" for t,_ in pts)}" '
            f'values="{";".join(str(v) for _,v in pts)}"/>')

def slide_in(t0, t1, dx):
    pts = [(0,dx),(t0,dx),(t1,0),(DUR,0)]
    return (f'<animateTransform attributeName="transform" type="translate" dur="{DUR}s" '
            f'repeatCount="indefinite" keyTimes="{";".join(f"{t/DUR:.4f}" for t,_ in pts)}" '
            f'values="{";".join(f"{x} 0" for _,x in pts)}" calcMode="spline" '
            f'keySplines="0 0 1 1;0.35 0 0.2 1;0 0 1 1"/>')

def style():
    return re.search(r"<style>.*?</style>", (ROOT/"assets/diagrams/p4-w25-m1.svg").read_text(), re.S).group(0)

def cells(x, y, n, w_total, col, t0, dead_from=None, dead_col=None):
    out, cw = "", w_total / n
    for i in range(n):
        c = dead_col if (dead_from is not None and i >= dead_from) else col
        out += (f'<rect x="{x+i*cw+1:.1f}" y="{y}" width="{cw-2:.1f}" height="26" rx="3" '
                f'fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="2"/>')
    return f'<g opacity="0">{out}{fade(t0, 11.4)}</g>'

def build_m1(ink, muted, blue, red, green, amber, bg):
    rows = [("fp32 — the fat box", 32, "32 GB", 0.6, "100%", 300),
            ("fp16 — half the box", 16, "16 GB", 3.4, "99.9%", 299),
            ("4-bit — the MP3",     4, "4.5 GB", 6.2, "~99%", 296)]
    body = ""
    for i,(label, n, size, t0, q, qw) in enumerate(rows):
        y = 70 + i*74
        body += f'''<text x="60" y="{y+18}" font-size="24" fill="{ink}" opacity="0">{label}{fade(t0, 11.4)}</text>
  {cells(320, y, n, 320, blue, t0)}
  <text x="672" y="{y+18}" font-size="26" fill="{amber}" opacity="0" font-weight="bold">{size}{fade(t0+0.5, 11.4)}</text>
  <g opacity="0"><rect x="780" y="{y}" width="{qw*0.55:.0f}" height="24" rx="4" fill="{green}" fill-opacity="0.3" stroke="{green}" stroke-width="2.5"/>
  <text x="{790+qw*0.55:.0f}" y="{y+18}" font-size="20" fill="{green}">{q}</text>{fade(t0+1.2, 11.4)}</g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" width="100%" role="img" aria-label="One parameter stored in 32 bit cells, then 16, then 4: the model shrinks from 32 GB to 4.5 GB while the quality bar barely moves." font-family="NexusHand, NexusSym, cursive">{style()}
  <rect width="1000" height="360" rx="8" fill="{bg}"/>
  <text x="60" y="44" font-size="26" fill="{muted}">one number from the brain, three ways to box it:</text>
  <text x="845" y="44" font-size="22" fill="{green}">quality</text>
  {body}
  <text x="500" y="340" font-size="27" fill="{amber}" text-anchor="middle" opacity="0">8× smaller — and you can barely hear the difference{fade(8.6, 11.2)}</text>
</svg>'''

def build_m3(ink, muted, blue, violet, green, amber, bg):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" width="100%" role="img" aria-label="A huge frozen weight matrix stays read-only while a tiny column and row — the LoRA adapter — slide in beside it; only the adapter trains." font-family="NexusHand, NexusSym, cursive">{style()}
  <rect width="1000" height="360" rx="8" fill="{bg}"/>
  <g>
    <rect x="90" y="60" width="270" height="220" rx="8" fill="{blue}" fill-opacity="0.10" stroke="{blue}" stroke-width="4"/>
    <text x="225" y="150" font-size="30" fill="{blue}" text-anchor="middle">W — frozen</text>
    <text x="225" y="186" font-size="20" fill="{muted}" text-anchor="middle">4,096 × 4,096 numbers</text>
    <text x="225" y="214" font-size="20" fill="{muted}" text-anchor="middle">read-only ❄</text>
  </g>
  <text x="420" y="180" font-size="44" fill="{ink}" opacity="0">+{fade(2.2, 11.4)}</text>
  <g opacity="0"><g>
    <rect x="480" y="60" width="34" height="220" rx="6" fill="{violet}" fill-opacity="0.25" stroke="{violet}" stroke-width="3.5"/>
    <text x="497" y="300" font-size="20" fill="{violet}" text-anchor="middle">A</text>
    {slide_in(1.4, 2.8, 320)}</g>{fade(1.4, 11.4)}</g>
  <text x="548" y="180" font-size="40" fill="{ink}" opacity="0">×{fade(3.2, 11.4)}</text>
  <g opacity="0"><g>
    <rect x="590" y="152" width="220" height="34" rx="6" fill="{green}" fill-opacity="0.25" stroke="{green}" stroke-width="3.5"/>
    <text x="700" y="215" font-size="20" fill="{green}" text-anchor="middle">B</text>
    {slide_in(3.0, 4.4, 300)}</g>{fade(3.0, 11.4)}</g>
  <text x="700" y="100" font-size="22" fill="{violet}" opacity="0">the sticky note: one column × one row{fade(4.8, 11.4)}</text>
  <g opacity="0">
    <text x="500" y="322" font-size="26" fill="{amber}" text-anchor="middle">answer = frozen W  +  A×B · only the note trains — 0.5% of the numbers, 100% of the steering</text>
    {fade(6.4, 11.2)}
  </g>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)

JOBS = [
 ("curriculum/p4/week-26/1-numeric-precision-quantization.mdx", "ANIM:W26M1", build_m1,
  dict(light=dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",red="#e03131",green="#2f9e44",amber="#f08c00",bg="#fffdf7"),
       dark=dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",red="#ff8787",green="#6cc47a",amber="#ffb84d",bg="#1a1a1a")),
  "The shrinking boxes, live: the same number stored in 32 cells, 16, then 4 — the model falls from 32 GB to 4.5 GB and the quality bar barely moves. It repeats — watch it twice."),
 ("curriculum/p4/week-26/3-lora-qlora.mdx", "ANIM:W26M3", build_m3,
  dict(light=dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",violet="#9c36b5",green="#2f9e44",amber="#f08c00",bg="#fffdf7"),
       dark=dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",violet="#da77f2",green="#6cc47a",amber="#ffb84d",bg="#1a1a1a")),
  "The sticky note, live: the giant matrix stays frozen; a thin column and a flat row slide in beside it, and only they train. It repeats — watch it twice."),
]
for slug, anchor, builder, themes, caption in JOBS:
    light, dark = mdx_safe(builder(**themes["light"])), mdx_safe(builder(**themes["dark"]))
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
    p.write_text(t)
    print("animation inlined:", slug)
