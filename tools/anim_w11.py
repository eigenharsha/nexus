#!/usr/bin/env python3
"""Week-11 animations: the dot product agreeing and disagreeing (m1), a matrix
moving a square (m2), the direction that does not turn (m3), a slope read off a
curve (m4), and three step sizes (m5).
Numbers verified: [3,4] has length 5; [3,4]·[4,3]=24; [3,4]·[-4,3]=0."""
import re, inspect, math
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
    ox, oy = 220, 250
    def arrow(dx, dy, col, lab, t0, w=4):
        x2, y2 = ox + dx*30, oy - dy*30
        return (f'<g opacity="0"><path d="M{ox} {oy} L{x2} {y2}" stroke="{col}" stroke-width="{w}"/>'
                f'<circle cx="{x2}" cy="{y2}" r="6" fill="{col}"/>'
                f'<text x="{x2+14}" y="{y2-6}" font-size="17" fill="{col}">{lab}</text>{fade(t0,11.4)}</g>')
    return head(1000, 340, "Two arrows drawn from the origin: the dot product is large when they point the same way, zero when they are perpendicular, and negative when they oppose.", bg) + f'''
  <line x1="{ox-160}" y1="{oy}" x2="{ox+200}" y2="{oy}" stroke="{muted}" stroke-width="2.5"/>
  <line x1="{ox}" y1="{oy+60}" x2="{ox}" y2="60" stroke="{muted}" stroke-width="2.5"/>
  {arrow(3, 4, ink, "[3, 4]", 0.4)}
  {arrow(4, 3, green, "[4, 3]", 1.6)}
  <g opacity="0"><text x="620" y="110" font-size="21" fill="{green}">pointing the same way:</text>
    <text x="620" y="146" font-size="24" fill="{green}">3×4 + 4×3 = 24</text>
    <text x="620" y="178" font-size="18" fill="{muted}">a big positive number — “alike”</text>{fade(2.4,5.6)}</g>
  {arrow(-4, 3, red, "[−4, 3]", 6.0)}
  <g opacity="0"><text x="620" y="110" font-size="21" fill="{red}">at right angles:</text>
    <text x="620" y="146" font-size="24" fill="{red}">3×(−4) + 4×3 = 0</text>
    <text x="620" y="178" font-size="18" fill="{muted}">zero — completely unrelated</text>{fade(6.6,11.4)}</g>
  <text x="500" y="316" font-size="21" fill="{amber}" text-anchor="middle" opacity="0">“similar”, made of arithmetic — and used everywhere after this{fade(8.8,11.2)}</text>
</svg>'''

def m2(ink, muted, blue, green, amber, bg):
    return head(1000, 340, "A matrix moves the whole space at once: the unit square is stretched and rotated, and its columns say exactly where the corner arrows land.", bg) + f'''
  <g>
    <line x1="120" y1="250" x2="420" y2="250" stroke="{muted}" stroke-width="2.5"/>
    <line x1="120" y1="280" x2="120" y2="70" stroke="{muted}" stroke-width="2.5"/>
    <rect x="120" y="160" width="90" height="90" fill="{blue}" fill-opacity="0.14" stroke="{blue}" stroke-width="3.5"/>
    <path d="M120 250 L210 250" stroke="{green}" stroke-width="5"/>
    <path d="M120 250 L120 160" stroke="{amber}" stroke-width="5"/>
    <text x="168" y="274" font-size="16" fill="{green}">[1, 0]</text>
    <text x="60" y="206" font-size="16" fill="{amber}">[0, 1]</text>
    <text x="270" y="300" font-size="19" fill="{muted}">before</text>
  </g>
  <g opacity="0">
    <line x1="580" y1="250" x2="920" y2="250" stroke="{muted}" stroke-width="2.5"/>
    <line x1="580" y1="280" x2="580" y2="70" stroke="{muted}" stroke-width="2.5"/>
    <path d="M580 250 L740 214 L800 116 L640 152 Z" fill="{blue}" fill-opacity="0.14" stroke="{blue}" stroke-width="3.5"/>
    <path d="M580 250 L740 214" stroke="{green}" stroke-width="5"/>
    <path d="M580 250 L640 152" stroke="{amber}" stroke-width="5"/>
    <text x="756" y="212" font-size="16" fill="{green}">column 1</text>
    <text x="600" y="130" font-size="16" fill="{amber}">column 2</text>
    <text x="750" y="300" font-size="19" fill="{muted}">after</text>
    {fade(1.6,11.4)}</g>
  <text x="500" y="52" font-size="22" fill="{ink}" text-anchor="middle">one action, applied to every arrow at once</text>
  <text x="500" y="326" font-size="21" fill="{amber}" text-anchor="middle" opacity="0">the columns tell you where the corners land — that is the whole matrix{fade(5.0,11.2)}</text>
</svg>'''

def m3(ink, muted, blue, green, red, amber, bg):
    ox, oy = 300, 200
    def arr(dx, dy, col, t0, w=3.5, lab=""):
        return (f'<g opacity="0"><path d="M{ox} {oy} L{ox+dx} {oy-dy}" stroke="{col}" stroke-width="{w}"/>'
                f'<text x="{ox+dx+8}" y="{oy-dy-4}" font-size="15" fill="{col}">{lab}</text>{fade(t0,11.4)}</g>')
    turned = "".join(arr(dx, dy, muted, 0.4) for dx, dy in [(90,60),(40,100),(-60,80),(-100,10)])
    after  = "".join(arr(int(dx*1.5), int(dy*0.6), red, 3.0) for dx, dy in [(90,60),(40,100),(-60,80),(-100,10)])
    return head(1000, 340, "Stretching a sheet turns almost every arrow, except a few special directions that only get longer — the eigenvectors.", bg) + f'''
  <text x="300" y="60" font-size="21" fill="{muted}" text-anchor="middle">stretch the sheet — almost every arrow swings</text>
  {turned}{after}
  {arr(140, 0, green, 6.0, 5, "does not turn ✓")}
  <g opacity="0"><text x="700" y="120" font-size="21" fill="{green}">a few directions do not turn at all —</text>
    <text x="700" y="152" font-size="21" fill="{green}">they only get longer or shorter</text>
    <text x="700" y="196" font-size="19" fill="{muted}">those are the directions the</text>
    <text x="700" y="222" font-size="19" fill="{muted}">transformation really acts along</text>{fade(6.4,11.4)}</g>
  <text x="500" y="316" font-size="21" fill="{amber}" text-anchor="middle" opacity="0">keep the few that stretch most, drop the rest — that is compression{fade(9.0,11.2)}</text>
</svg>'''

def m4(ink, muted, blue, green, amber, bg):
    pts = [(120 + i*14, 250 - (0.012*((i*14)-260)**2)/6 - 40) for i in range(46)]
    curve = "M" + " L".join(f"{x:.0f} {y:.0f}" for x,y in pts)
    return head(1000, 330, "A tangent line slides along a curve: steep where the curve climbs, flat at the bottom, negative where it falls.", bg) + f'''
  <line x1="100" y1="270" x2="820" y2="270" stroke="{muted}" stroke-width="2.5"/>
  <path d="{curve}" fill="none" stroke="{blue}" stroke-width="4"/>
  <g>
    <path d="M-70 40 L70 -40" stroke="{amber}" stroke-width="4">
      <animateTransform attributeName="transform" type="translate" dur="{DUR}s" repeatCount="indefinite"
        keyTimes="0;0.35;0.5;0.85;1" values="180 128;380 74;420 70;660 120;180 128"/>
    </path>
  </g>
  <g opacity="0"><text x="700" y="120" font-size="21" fill="{amber}">steep here — a big number{fade(0.6,4.6)}</text></g>
  <g opacity="0"><text x="700" y="120" font-size="21" fill="{green}">flat at the bottom — zero{fade(5.0,8.0)}</text></g>
  <g opacity="0"><text x="700" y="120" font-size="21" fill="{blue}">going down — negative{fade(8.4,11.4)}</text></g>
  <text x="460" y="312" font-size="21" fill="{muted}" text-anchor="middle">a derivative is how steep the hill is, exactly here</text>
</svg>'''

def m5(ink, muted, blue, green, red, amber, bg):
    def bowl():
        pts = [(140 + i*16, 260 - ((i*16 - 340)**2)/900) for i in range(45)]
        return "M" + " L".join(f"{x:.0f} {y:.0f}" for x,y in pts)
    return head(1000, 340, "Three step sizes on the same bowl: too large diverges up the sides, too small crawls, and a sensible one settles at the bottom.", bg) + f'''
  <path d="{bowl()}" fill="none" stroke="{muted}" stroke-width="3.5"/>
  <g opacity="0"><circle cx="200" cy="140" r="11" fill="{red}"/>
    <path d="M200 140 L700 118 L240 96 L760 60" fill="none" stroke="{red}" stroke-width="3.5" stroke-dasharray="8 6"/>
    <text x="500" y="60" font-size="21" fill="{red}" text-anchor="middle">too big — it climbs out and runs to infinity ✗</text>{fade(0.5,4.2)}</g>
  <g opacity="0"><circle cx="200" cy="140" r="11" fill="{blue}"/>
    <path d="M200 140 L240 152 L272 162 L298 170" fill="none" stroke="{blue}" stroke-width="3.5" stroke-dasharray="8 6"/>
    <text x="500" y="60" font-size="21" fill="{blue}" text-anchor="middle">too small — you will give up before it arrives ✗</text>{fade(4.6,8.0)}</g>
  <g opacity="0"><circle cx="480" cy="258" r="11" fill="{green}"/>
    <path d="M200 140 L300 200 L400 240 L470 256" fill="none" stroke="{green}" stroke-width="4" stroke-dasharray="9 7"/>
    <text x="500" y="60" font-size="21" fill="{green}" text-anchor="middle">right — it settles at the bottom ✓</text>{fade(8.4,11.4)}</g>
  <text x="500" y="320" font-size="20" fill="{amber}" text-anchor="middle" opacity="0">and for a simple curve you can compute exactly where the boundary sits{fade(9.6,11.2)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",red="#e03131",amber="#f08c00",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",red="#ff8787",amber="#ffb84d",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
W = "curriculum/p2/week-11/"
for slug, anchor, fn, caption in [
 (W+"1-vectors-vector-spaces.mdx", "ANIM:W11M1", m1,
  "The dot product, live: two arrows pointing the same way score 24, and two at right angles score exactly zero. It repeats — watch both."),
 (W+"2-matrices-linear-transformations.mdx", "ANIM:W11M2", m2,
  "A matrix, live: the unit square is stretched and rotated in one step, and the columns show exactly where the corner arrows landed. It repeats."),
 (W+"3-eigen-decomposition-svd-pca.mdx", "ANIM:W11M3", m3,
  "Eigenvectors, live: stretching turns almost every arrow — except the few special directions that only get longer. It repeats — watch for the one that holds still."),
 (W+"4-calculus-the-chain-rule.mdx", "ANIM:W11M4", m4,
  "A slope, live: the tangent slides along the curve — steep on the climb, flat at the bottom, negative on the way down. It loops continuously."),
 (W+"5-optimization.mdx", "ANIM:W11M5", m5,
  "Step size, live: too big and the ball climbs out to infinity, too small and it crawls, and in between it settles at the bottom. It repeats — watch all three."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
