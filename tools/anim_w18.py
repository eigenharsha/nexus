#!/usr/bin/env python3
"""Week-18 animations: a tree choosing splits (m1), a crowd's errors cancelling
(m2), boosting shrinking residuals (m3), k-means settling (m4), and a shadow
that keeps the shape (m5)."""
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
def box(x,y,w,h,label,col,t0,size=15):
    return (f'<g opacity="0"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{col}" fill-opacity="0.14" '
            f'stroke="{col}" stroke-width="3"/><text x="{x+w/2}" y="{y+h/2+5}" font-size="{size}" fill="{col}" '
            f'text-anchor="middle">{label}</text>{fade(t0,11.4)}</g>')
def line(x1,y1,x2,y2,col,t0,w=2.5):
    return f'<g opacity="0"><path d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="{w}"/>{fade(t0,11.4)}</g>'

def m1(ink, muted, blue, green, red, amber, bg):
    return head(1000, 340, "A tree grows itself: each question splits a mixed pile into two tidier ones, ending in leaves that decide.", bg) + f'''
  {box(390, 40, 220, 46, "employed?", blue, 0.4, 17)}
  {line(440, 86, 300, 128, muted, 1.4)}{line(560, 86, 700, 128, muted, 1.4)}
  <text x="352" y="112" font-size="17" fill="{muted}" opacity="0">no{fade(1.4,11.4)}</text>
  <text x="642" y="112" font-size="17" fill="{muted}" opacity="0">yes{fade(1.4,11.4)}</text>
  {box(200, 128, 200, 44, "decline", red, 1.8, 16)}
  {box(600, 128, 220, 44, "over a year?", blue, 2.4, 16)}
  {line(660, 172, 560, 214, muted, 3.4)}{line(760, 172, 860, 214, muted, 3.4)}
  {box(460, 214, 200, 44, "deposit > 20%?", blue, 3.8, 14)}
  {box(770, 214, 180, 44, "approve", green, 4.2, 16)}
  {line(510, 258, 440, 296, muted, 5.2)}{line(610, 258, 680, 296, muted, 5.2)}
  {box(340, 296, 170, 38, "decline", red, 5.6, 15)}
  {box(600, 296, 170, 38, "approve", green, 5.9, 15)}
  <g opacity="0"><text x="150" y="60" font-size="20" fill="{amber}">a good question</text>
    <text x="150" y="86" font-size="20" fill="{amber}">splits a messy pile</text>
    <text x="150" y="112" font-size="20" fill="{amber}">into two tidy ones</text>{fade(6.6,11.4)}</g>
  <g opacity="0"><text x="150" y="180" font-size="19" fill="{muted}">the machine tries every</text>
    <text x="150" y="204" font-size="19" fill="{muted}">possible question and</text>
    <text x="150" y="228" font-size="19" fill="{muted}">keeps the tidiest split</text>{fade(8.0,11.4)}</g>
</svg>'''

def m2(ink, muted, blue, green, red, amber, bg):
    rng = random.Random(18)
    truth = 170
    guesses = [truth + rng.randint(-90, 90) for _ in range(9)]
    marks = "".join(
        f'<g opacity="0"><circle cx="{140+i*80}" cy="{g}" r="8" fill="{blue}" fill-opacity="0.4" stroke="{blue}" stroke-width="2.5"/>'
        f'{fade(0.4+i*0.28, 11.4)}</g>' for i, g in enumerate(guesses))
    avg = sum(guesses)//len(guesses)
    return head(1000, 320, "Nine individually wrong guesses scatter above and below the truth; their average lands almost exactly on it.", bg) + f'''
  <line x1="100" y1="{truth}" x2="880" y2="{truth}" stroke="{green}" stroke-width="3" stroke-dasharray="9 7"/>
  <text x="920" y="{truth+6}" font-size="19" fill="{green}">truth</text>
  {marks}
  <g opacity="0"><text x="500" y="56" font-size="22" fill="{muted}" text-anchor="middle">nine guesses — every one of them wrong</text>{fade(2.8,6.4)}</g>
  <g opacity="0"><line x1="100" y1="{avg}" x2="880" y2="{avg}" stroke="{amber}" stroke-width="5"/>
    <text x="500" y="56" font-size="23" fill="{amber}" text-anchor="middle">their average — almost exactly right ✓</text>{fade(7.0,11.4)}</g>
  <text x="500" y="292" font-size="24" fill="{amber}" text-anchor="middle" opacity="0">mistakes made in different directions cancel out{fade(8.6,11.2)}</text>
</svg>'''

def m3(ink, muted, blue, green, red, amber, bg):
    rows = ""
    for i,(w,col,lab,t0) in enumerate([(300,red,"round 1: what is still wrong",0.4),
                                        (170,amber,"round 2: fix that",3.2),
                                        (80,amber,"round 3: fix what is left",5.6),
                                        (22,green,"round 200: nearly nothing left",8.0)]):
        y = 80 + i*54
        rows += (f'<g opacity="0"><rect x="300" y="{y}" width="{w}" height="26" rx="5" fill="{col}" fill-opacity="0.25" '
                 f'stroke="{col}" stroke-width="3"/><text x="288" y="{y+19}" font-size="17" fill="{ink}" text-anchor="end">{lab}</text>'
                 f'{fade(t0,11.4)}</g>')
    return head(1000, 340, "Each boosting round trains a small tree on the errors that remain, and the error bar shrinks round after round.", bg) + f'''
  <text x="60" y="48" font-size="22" fill="{muted}">the errors that are left over:</text>
  {rows}
  <g opacity="0"><text x="700" y="300" font-size="22" fill="{red}" text-anchor="middle">…and past some round, it starts fitting noise</text>{fade(9.4,11.4)}</g>
  <text x="300" y="300" font-size="22" fill="{amber}" opacity="0">so: small steps, and stop early{fade(9.4,11.2)}</text>
</svg>'''

def m4(ink, muted, blue, green, red, amber, bg):
    rng = random.Random(4)
    A = [(160+rng.randint(-45,45), 120+rng.randint(-40,40)) for _ in range(9)]
    B = [(480+rng.randint(-45,45), 210+rng.randint(-40,40)) for _ in range(9)]
    C = [(760+rng.randint(-45,45), 110+rng.randint(-40,40)) for _ in range(9)]
    def dots(pts, col, t0):
        return "".join(f'<g opacity="0"><circle cx="{x}" cy="{y}" r="7" fill="{col}" fill-opacity="0.55" stroke="{col}" stroke-width="2"/>{fade(t0,11.4)}</g>' for x,y in pts)
    grey = dots(A+B+C, muted, 0.4)
    return head(1000, 320, "Unlabelled points settle into three groups as the markers move to the middle of whichever points chose them.", bg) + f'''
  {grey}
  <g opacity="0"><text x="500" y="46" font-size="22" fill="{muted}" text-anchor="middle">no labels — nobody said which group anything belongs to</text>{fade(0.6,4.0)}</g>
  {dots(A, green, 4.4)}{dots(B, blue, 4.7)}{dots(C, amber, 5.0)}
  <g opacity="0">
    <path d="M160 120 m-9,0 a9,9 0 1,0 18,0 a9,9 0 1,0 -18,0" fill="{green}"/>
    <path d="M480 210 m-9,0 a9,9 0 1,0 18,0 a9,9 0 1,0 -18,0" fill="{blue}"/>
    <path d="M760 110 m-9,0 a9,9 0 1,0 18,0 a9,9 0 1,0 -18,0" fill="{amber}"/>
    <text x="500" y="46" font-size="22" fill="{ink}" text-anchor="middle">markers move to the middle of whoever chose them — until nothing moves</text>{fade(4.4,11.4)}</g>
  <text x="500" y="292" font-size="23" fill="{red}" text-anchor="middle" opacity="0">it will find three groups whether or not three groups exist{fade(8.6,11.2)}</text>
</svg>'''

def m5(ink, muted, blue, green, red, amber, bg):
    return head(1000, 330, "Light through a chair casts a readable shadow at a good angle and an unreadable smudge at a bad one — the same choice PCA makes.", bg) + f'''
  <g opacity="0"><text x="150" y="60" font-size="21" fill="{muted}">the same object, two angles:</text>{fade(0.4,11.4)}</g>
  <g opacity="0"><rect x="120" y="96" width="150" height="150" rx="10" fill="none" stroke="{ink}" stroke-width="3.5"/>
    <path d="M150 130 L240 220 M240 130 L150 220 M195 110 L195 240" stroke="{ink}" stroke-width="3"/>
    <text x="195" y="272" font-size="19" fill="{muted}" text-anchor="middle">the data (many dimensions)</text>{fade(0.6,11.4)}</g>
  <g opacity="0"><path d="M290 170 L430 140" stroke="{green}" stroke-width="4" stroke-dasharray="9 7"/>
    <rect x="440" y="100" width="150" height="90" rx="8" fill="{green}" fill-opacity="0.10" stroke="{green}" stroke-width="3.5"/>
    <path d="M470 130 L560 175 M470 175 L560 130" stroke="{green}" stroke-width="3"/>
    <text x="515" y="214" font-size="19" fill="{green}" text-anchor="middle">good angle: still readable ✓</text>{fade(2.4,11.4)}</g>
  <g opacity="0"><path d="M290 200 L430 250" stroke="{red}" stroke-width="4" stroke-dasharray="9 7"/>
    <rect x="440" y="216" width="150" height="60" rx="8" fill="{red}" fill-opacity="0.10" stroke="{red}" stroke-width="3.5"/>
    <path d="M470 246 L560 246" stroke="{red}" stroke-width="4"/>
    <text x="515" y="300" font-size="19" fill="{red}" text-anchor="middle">bad angle: a smudge ✗</text>{fade(5.0,11.4)}</g>
  <g opacity="0"><text x="800" y="120" font-size="21" fill="{amber}" text-anchor="middle">PCA finds the angle</text>
    <text x="800" y="148" font-size="21" fill="{amber}" text-anchor="middle">that keeps the most</text>
    <text x="800" y="176" font-size="21" fill="{amber}" text-anchor="middle">of the variation</text>
    <text x="800" y="222" font-size="19" fill="{muted}" text-anchor="middle">— and that is what an</text>
    <text x="800" y="248" font-size="19" fill="{muted}" text-anchor="middle">embedding is, learned</text>{fade(7.4,11.4)}</g>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",amber="#f08c00",red="#e03131",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",amber="#ffb84d",red="#ff8787",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
W = "curriculum/p3/week-18/"
for slug, anchor, fn, caption in [
 (W+"1-decision-trees.mdx", "ANIM:W18M1", m1,
  "A tree, live: each question splits a mixed pile into two tidier ones, and the machine picks the question by trying them all. It repeats — watch it twice."),
 (W+"2-bagging-random-forests.mdx", "ANIM:W18M2", m2,
  "The crowd, live: nine guesses, every one of them wrong, scattered either side of the truth — and their average lands almost exactly on it. It repeats — watch it twice."),
 (W+"3-gradient-boosting-xgboost.mdx", "ANIM:W18M3", m3,
  "Boosting, live: each round trains a small tree on what is still wrong, and the leftover error shrinks round after round — until it starts fitting noise. It repeats — watch it twice."),
 (W+"4-unsupervised-learning-clustering.mdx", "ANIM:W18M4", m4,
  "k-means, live: unlabelled points settle into groups as each marker moves to the middle of whoever chose it — and it finds three groups whether or not three exist. It repeats."),
 (W+"5-dimensionality-reduction-representation.mdx", "ANIM:W18M5", m5,
  "The shadow, live: the same object cast at a good angle stays readable and at a bad angle becomes a smudge — which is the choice PCA makes for you. It repeats — watch both."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
