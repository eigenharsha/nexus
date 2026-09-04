#!/usr/bin/env python3
"""Week-22 animations: a picture becoming numbers (m1), a filter sliding (m2),
one image becoming twenty (m3), frozen layers with a new head (m4), and a model
leaving the notebook (m5)."""
import re, inspect, random
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

def m1(ink, muted, blue, green, amber, bg):
    rng = random.Random(22)
    grid = ""
    for r in range(6):
        for c in range(8):
            v = rng.choice([12, 48, 96, 140, 190, 230])
            x, y = 470 + c*54, 90 + r*34
            grid += (f'<rect x="{x}" y="{y}" width="50" height="30" rx="3" fill="{ink}" fill-opacity="{v/300:.2f}" '
                     f'stroke="{muted}" stroke-width="1"/><text x="{x+25}" y="{y+21}" font-size="14" '
                     f'fill="{ink if v<120 else bg}" text-anchor="middle">{v}</text>')
    return head(1000, 340, "A photograph is a grid of brightness numbers; colour is three such grids stacked for red, green and blue.", bg) + f'''
  <g opacity="0"><rect x="80" y="90" width="280" height="200" rx="10" fill="{blue}" fill-opacity="0.10" stroke="{blue}" stroke-width="3.5"/>
    <text x="220" y="200" font-size="26" fill="{blue}" text-anchor="middle">a photo of a cat</text>{fade(0.4,11.4)}</g>
  <g opacity="0"><path d="M370 190 L455 190" stroke="{amber}" stroke-width="4" stroke-dasharray="10 8">
      <animate attributeName="stroke-dashoffset" from="36" to="0" dur="1.3s" repeatCount="indefinite"/></path>{fade(1.6,11.4)}</g>
  <g opacity="0">{grid}{fade(2.2,11.4)}</g>
  <text x="700" y="60" font-size="21" fill="{muted}" text-anchor="middle" opacity="0">to the machine: brightness numbers, 0–255{fade(2.6,11.4)}</text>
  <g opacity="0"><text x="700" y="316" font-size="21" fill="{green}" text-anchor="middle">colour = three of these grids stacked: red, green, blue{fade(6.4,11.4)}</text></g>
  <text x="220" y="316" font-size="21" fill="{amber}" text-anchor="middle" opacity="0">a 4MP colour photo = 12 million numbers{fade(8.4,11.2)}</text>
</svg>'''

def m2(ink, muted, blue, green, amber, bg):
    cells = ""
    for r in range(6):
        for c in range(9):
            x, y = 90 + c*46, 90 + r*36
            edge = c in (4,5)
            cells += (f'<rect x="{x}" y="{y}" width="42" height="32" rx="3" fill="{ink}" '
                      f'fill-opacity="{0.55 if edge else 0.10}" stroke="{muted}" stroke-width="1"/>')
    return head(1000, 340, "One small window of nine weights slides across the whole image, detecting the same vertical edge wherever it appears.", bg) + f'''
  {cells}
  <text x="290" y="66" font-size="21" fill="{muted}" text-anchor="middle">the image (a vertical edge in it)</text>
  <g>
    <rect x="90" y="90" width="134" height="104" rx="5" fill="none" stroke="{amber}" stroke-width="4">
      <animate attributeName="x" dur="{DUR}s" repeatCount="indefinite"
        keyTimes="0;0.10;0.28;0.46;0.64;0.82;1" values="90;90;228;320;136;274;90"/>
      <animate attributeName="y" dur="{DUR}s" repeatCount="indefinite"
        keyTimes="0;0.10;0.28;0.46;0.64;0.82;1" values="90;90;90;198;198;126;90"/>
    </rect>
  </g>
  <text x="640" y="86" font-size="21" fill="{amber}" text-anchor="middle" opacity="0">the same 9 numbers, applied everywhere{fade(1.0,11.4)}</text>
  <g opacity="0"><text x="700" y="140" font-size="20" fill="{green}" text-anchor="middle">→ parameters collapse: 9, not millions</text>{fade(3.4,11.4)}</g>
  <g opacity="0"><text x="700" y="180" font-size="20" fill="{green}" text-anchor="middle">→ position stops mattering</text>{fade(5.4,11.4)}</g>
  <g opacity="0"><text x="700" y="236" font-size="19" fill="{muted}" text-anchor="middle">stack them: edges → corners →</text>
    <text x="700" y="262" font-size="19" fill="{muted}" text-anchor="middle">textures → shapes → faces</text>
    <text x="700" y="296" font-size="19" fill="{amber}" text-anchor="middle">nobody designed that hierarchy</text>{fade(7.4,11.4)}</g>
</svg>'''

def m3(ink, muted, blue, green, red, amber, bg):
    tiles = ""
    variants = [("original",0.6,""),("flipped",1.4,"scale(-1,1) translate(-120,0)"),
                ("rotated",2.2,"rotate(7 60 45)"),("cropped",3.0,"scale(1.15) translate(-9,-6)"),
                ("brighter",3.8,"")]
    for i,(lab,t0,tf) in enumerate(variants):
        x = 90 + i*180
        op = "0.30" if lab == "brighter" else "0.14"
        tiles += (f'<g opacity="0"><g transform="translate({x},110)">'
                  f'<rect x="0" y="0" width="120" height="90" rx="7" fill="{blue}" fill-opacity="{op}" '
                  f'stroke="{blue}" stroke-width="3" transform="{tf}"/>'
                  f'<text x="60" y="55" font-size="17" fill="{blue}" text-anchor="middle">cat</text></g>'
                  f'<text x="{x+60}" y="228" font-size="17" fill="{muted}" text-anchor="middle">{lab}</text>{fade(t0,11.4)}</g>')
    return head(1000, 320, "One photo becomes many through flips, rotations, crops and brightness changes — all still cats; but a flipped digit 2 is not a 2.", bg) + f'''
  <text x="60" y="60" font-size="22" fill="{muted}">one photo, five training examples:</text>
  {tiles}
  <g opacity="0"><rect x="300" y="248" width="400" height="46" rx="7" fill="{red}" fill-opacity="0.08" stroke="{red}" stroke-width="3"/>
    <text x="500" y="278" font-size="20" fill="{red}" text-anchor="middle">but a flipped “2” is not a 2 ✗</text>{fade(6.4,11.4)}</g>
  <text x="500" y="90" font-size="20" fill="{amber}" text-anchor="middle" opacity="0">the transformation must preserve the label{fade(8.4,11.2)}</text>
</svg>'''

def m4(ink, muted, blue, green, amber, bg):
    layers = [("edges",0.4,True),("textures",0.9,True),("shapes",1.4,True),("objects",1.9,True)]
    out = ""
    for i,(lab,t0,frozen) in enumerate(layers):
        x = 90 + i*150
        out += (f'<g opacity="0"><rect x="{x}" y="120" width="130" height="80" rx="7" fill="{blue}" '
                f'fill-opacity="0.10" stroke="{blue}" stroke-width="3"/>'
                f'<text x="{x+65}" y="158" font-size="17" fill="{blue}" text-anchor="middle">{lab}</text>'
                f'<text x="{x+65}" y="184" font-size="18" fill="{blue}" text-anchor="middle">❄</text>{fade(t0,11.4)}</g>')
    return head(1000, 330, "The early layers of a pretrained network are frozen because they learned vision itself; only the final head is replaced and retrained.", bg) + f'''
  <text x="60" y="70" font-size="21" fill="{muted}">someone else trained this on 14,000,000 photos:</text>
  {out}
  <g opacity="0"><rect x="690" y="120" width="150" height="80" rx="7" fill="{green}" fill-opacity="0.16" stroke="{green}" stroke-width="3.5"/>
    <text x="765" y="152" font-size="16" fill="{green}" text-anchor="middle">your question</text>
    <text x="765" y="176" font-size="16" fill="{green}" text-anchor="middle">(retrained)</text>{fade(3.0,11.4)}</g>
  <g opacity="0"><text x="380" y="238" font-size="20" fill="{blue}" text-anchor="middle">frozen — these learned VISION, not “cat”</text>{fade(4.4,11.4)}</g>
  <g opacity="0"><text x="500" y="284" font-size="22" fill="{amber}" text-anchor="middle">a hundredth of the data · twenty minutes instead of a week ✓</text>{fade(7.0,11.4)}</g>
</svg>'''

def m5(ink, muted, blue, green, red, amber, bg):
    return head(1000, 320, "A checkpoint plus Python versions runs only on your laptop; exported to a portable format it runs in a phone app, a service or a browser.", bg) + f'''
  <g opacity="0"><rect x="70" y="90" width="290" height="130" rx="9" fill="{red}" fill-opacity="0.07" stroke="{red}" stroke-width="3.5"/>
    <text x="215" y="126" font-size="19" fill="{ink}" text-anchor="middle">model.pt + Python 3.13</text>
    <text x="215" y="154" font-size="19" fill="{ink}" text-anchor="middle">+ torch 2.4.1 + your notebook</text>
    <text x="215" y="192" font-size="19" fill="{red}" text-anchor="middle">runs where you are sitting ✗</text>{fade(0.4,11.4)}</g>
  <g opacity="0"><path d="M372 155 L470 155" stroke="{amber}" stroke-width="4" stroke-dasharray="10 8">
      <animate attributeName="stroke-dashoffset" from="36" to="0" dur="1.3s" repeatCount="indefinite"/></path>
    <text x="421" y="132" font-size="18" fill="{amber}" text-anchor="middle">export</text>{fade(3.0,11.4)}</g>
  <g opacity="0"><rect x="490" y="60" width="200" height="52" rx="7" fill="{green}" fill-opacity="0.12" stroke="{green}" stroke-width="3"/>
    <text x="590" y="92" font-size="18" fill="{green}" text-anchor="middle">a phone app</text>{fade(4.0,11.4)}</g>
  <g opacity="0"><rect x="490" y="128" width="200" height="52" rx="7" fill="{green}" fill-opacity="0.12" stroke="{green}" stroke-width="3"/>
    <text x="590" y="160" font-size="18" fill="{green}" text-anchor="middle">a C++ service</text>{fade(4.8,11.4)}</g>
  <g opacity="0"><rect x="490" y="196" width="200" height="52" rx="7" fill="{green}" fill-opacity="0.12" stroke="{green}" stroke-width="3"/>
    <text x="590" y="228" font-size="18" fill="{green}" text-anchor="middle">a browser</text>{fade(5.6,11.4)}</g>
  <g opacity="0"><text x="840" y="150" font-size="20" fill="{muted}" text-anchor="middle">no Python</text>
    <text x="840" y="176" font-size="20" fill="{muted}" text-anchor="middle">in sight</text>{fade(6.6,11.4)}</g>
  <text x="500" y="296" font-size="21" fill="{amber}" text-anchor="middle" opacity="0">shrinking it for a phone is your first meeting with quantization{fade(8.4,11.2)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",red="#e03131",amber="#f08c00",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",red="#ff8787",amber="#ffb84d",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
W = "curriculum/p3/week-22/"
for slug, anchor, fn, caption in [
 (W+"1-images-as-data-opencv.mdx", "ANIM:W22M1", m1,
  "A photo, live: what you see as a cat is a grid of brightness numbers, and colour is three such grids stacked. It repeats — watch it twice."),
 (W+"2-convolutional-neural-networks.mdx", "ANIM:W22M2", m2,
  "A filter, live: one small window of nine numbers slides across the whole image, finding the same edge wherever it sits. It loops continuously."),
 (W+"3-training-a-cnn-properly.mdx", "ANIM:W22M3", m3,
  "Augmentation, live: one photo becomes five training examples — flipped, rotated, cropped, brightened — but a flipped 2 is not a 2. It repeats."),
 (W+"4-transfer-learning.mdx", "ANIM:W22M4", m4,
  "Transfer learning, live: the early layers stay frozen because they learned vision itself, and only the final head is replaced for your question. It repeats."),
 (W+"5-beyond-classification-model-export.mdx", "ANIM:W22M5", m5,
  "Export, live: a checkpoint plus your Python versions runs only where you sit; exported, the same model runs in a phone app, a C++ service or a browser. It repeats."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
