#!/usr/bin/env python3
"""Week-21 animations: XOR defeating a straight line then solved by a bend
(m1), blame flowing backwards (m2), three learning rates (m3), the ball versus
the hiker (m4), and a graph building itself (m5)."""
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
    pts = [(200,100,"✓",green),(380,240,"✓",green),(200,240,"✗",red),(380,100,"✗",red)]
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="16" fill="{c}" fill-opacity="0.18" stroke="{c}" stroke-width="3"/>'
                   f'<text x="{x}" y="{y+8}" font-size="22" fill="{c}" text-anchor="middle">{s}</text>' for x,y,s,c in pts)
    return head(1000, 340, "Ticks in opposite corners cannot be separated by any straight line; bending between two layers curves the boundary and separates them.", bg) + f'''
  <rect x="140" y="60" width="300" height="220" rx="10" fill="none" stroke="{muted}" stroke-width="2.5" stroke-dasharray="6 7"/>
  {dots}
  <g opacity="0"><path d="M150 250 L430 90" stroke="{red}" stroke-width="4"/>
    <text x="290" y="308" font-size="20" fill="{red}" text-anchor="middle">no straight line works. None. ✗</text>{fade(0.6,5.2)}</g>
  <g opacity="0"><path d="M150 170 Q 290 60 430 170 Q 290 280 150 170" fill="none" stroke="{green}" stroke-width="4"/>
    <text x="290" y="308" font-size="20" fill="{green}" text-anchor="middle">bend it, and the ticks separate ✓</text>{fade(6.0,11.4)}</g>
  <g opacity="0"><text x="700" y="110" font-size="21" fill="{ink}" text-anchor="middle">line → bend → line</text>
    <text x="700" y="150" font-size="19" fill="{muted}" text-anchor="middle">the bend is one line of code:</text>
    <text x="700" y="180" font-size="19" fill="{blue}" text-anchor="middle">keep positives, zero the rest</text>
    <text x="700" y="230" font-size="19" fill="{amber}" text-anchor="middle">without it, 100 layers collapse</text>
    <text x="700" y="258" font-size="19" fill="{amber}" text-anchor="middle">back into a single line</text>{fade(7.2,11.4)}</g>
</svg>'''

def m2(ink, muted, blue, green, red, amber, bg):
    layers = [(160,"input"),(370,"layer 1"),(580,"layer 2"),(790,"prediction")]
    nodes = "".join(f'<rect x="{x-70}" y="120" width="140" height="60" rx="8" fill="{blue}" fill-opacity="0.10" '
                    f'stroke="{blue}" stroke-width="3"/><text x="{x}" y="{157}" font-size="18" fill="{blue}" '
                    f'text-anchor="middle">{n}</text>' for x,n in layers)
    fwd = "".join(f'<g opacity="0"><path d="M{layers[i][0]+72} 150 L{layers[i+1][0]-72} 150" stroke="{green}" '
                  f'stroke-width="3.5" stroke-dasharray="9 7"/>{fade(0.4+i*0.7, 5.0)}</g>' for i in range(3))
    back = "".join(f'<g opacity="0"><path d="M{layers[i+1][0]-72} 196 L{layers[i][0]+72} 196" stroke="{red}" '
                   f'stroke-width="4" stroke-dasharray="10 8"><animate attributeName="stroke-dashoffset" from="36" '
                   f'to="0" dur="1.2s" repeatCount="indefinite"/></path>'
                   f'<text x="{(layers[i][0]+layers[i+1][0])//2}" y="228" font-size="16" fill="{red}" '
                   f'text-anchor="middle">×{["0.4","0.7","1.0"][i]}</text>{fade(6.2+ (2-i)*1.1, 11.4)}</g>' for i in range(3))
    return head(1000, 320, "The forward pass computes a prediction and one error number; the backward pass sends each layer its share of the blame, multiplied along the chain.", bg) + f'''
  {nodes}{fwd}{back}
  <text x="500" y="66" font-size="22" fill="{green}" text-anchor="middle" opacity="0">forwards: compute the prediction, then one error number{fade(0.4,5.0)}</text>
  <text x="500" y="66" font-size="22" fill="{red}" text-anchor="middle" opacity="0">backwards: each layer's share = its own effect × the blame from in front{fade(6.0,11.4)}</text>
  <text x="500" y="288" font-size="23" fill="{amber}" text-anchor="middle" opacity="0">one sweep, every parameter — the reason this scales{fade(9.2,11.2)}</text>
</svg>'''

def m3(ink, muted, blue, green, red, amber, bg):
    def curve(pts, col):
        return "M" + " L".join(f"{x} {y}" for x,y in pts)
    explode = [(80,240),(180,200),(280,250),(380,150),(480,260),(580,90),(680,270),(780,60)]
    flat    = [(80,150),(180,148),(280,150),(380,149),(480,150),(580,148),(680,150),(780,149)]
    good    = [(80,250),(180,190),(280,155),(380,132),(480,118),(580,110),(680,105),(780,102)]
    return head(1000, 330, "Three loss curves: too large a learning rate explodes, too small stays flat, and the right one descends and settles.", bg) + f'''
  <line x1="70" y1="280" x2="850" y2="280" stroke="{muted}" stroke-width="2.5"/>
  <line x1="70" y1="280" x2="70" y2="50" stroke="{muted}" stroke-width="2.5"/>
  <text x="40" y="160" font-size="18" fill="{muted}" transform="rotate(-90 40 160)">loss</text>
  <g opacity="0"><path d="{curve(explode, red)}" fill="none" stroke="{red}" stroke-width="4"/>
    <text x="500" y="40" font-size="22" fill="{red}" text-anchor="middle">learning rate too big — it bounces out of the valley</text>{fade(0.4,3.8)}</g>
  <g opacity="0"><path d="{curve(flat, blue)}" fill="none" stroke="{blue}" stroke-width="4"/>
    <text x="500" y="40" font-size="22" fill="{blue}" text-anchor="middle">too small — nothing is happening</text>{fade(4.2,7.6)}</g>
  <g opacity="0"><path d="{curve(good, green)}" fill="none" stroke="{green}" stroke-width="4"/>
    <text x="500" y="40" font-size="22" fill="{green}" text-anchor="middle">right — noisy, descending, settling ✓</text>{fade(8.0,11.4)}</g>
  <text x="500" y="310" font-size="22" fill="{amber}" text-anchor="middle" opacity="0">the learning rate matters more than the architecture{fade(9.6,11.2)}</text>
</svg>'''

def m4(ink, muted, blue, green, amber, bg):
    return head(1000, 320, "A hiker feeling only the local slope zig-zags and stops in dips; a ball carrying momentum rolls through them to the bottom.", bg) + f'''
  <path d="M70 90 Q 220 250 320 170 Q 420 90 520 220 Q 640 300 860 250" fill="none" stroke="{muted}" stroke-width="3"/>
  <g opacity="0"><path d="M90 100 L150 180 L200 140 L250 200 L300 168" fill="none" stroke="{blue}" stroke-width="4" stroke-dasharray="8 6"/>
    <circle cx="300" cy="168" r="10" fill="{blue}"/>
    <text x="300" y="60" font-size="21" fill="{blue}" text-anchor="middle">the hiker: zig-zags, stops in the first dip</text>{fade(0.5,5.2)}</g>
  <g opacity="0"><path d="M90 100 Q 250 250 420 130 Q 600 260 830 248" fill="none" stroke="{green}" stroke-width="4"/>
    <circle cx="830" cy="248" r="12" fill="{green}"/>
    <text x="500" y="60" font-size="21" fill="{green}" text-anchor="middle">the ball: carries speed, rolls through, reaches the bottom ✓</text>{fade(5.8,11.4)}</g>
  <text x="500" y="296" font-size="22" fill="{amber}" text-anchor="middle" opacity="0">momentum = each step remembers the last one{fade(8.4,11.2)}</text>
</svg>'''

def m5(ink, muted, blue, green, amber, bg):
    return head(1000, 320, "Each operation records where its result came from, so the forward pass silently builds the graph that backpropagation walks.", bg) + f'''
  <g opacity="0"><rect x="70" y="130" width="110" height="50" rx="7" fill="{blue}" fill-opacity="0.12" stroke="{blue}" stroke-width="3"/>
    <text x="125" y="162" font-size="19" fill="{blue}" text-anchor="middle">x</text>{fade(0.4,11.4)}</g>
  <g opacity="0"><rect x="70" y="200" width="110" height="50" rx="7" fill="{blue}" fill-opacity="0.12" stroke="{blue}" stroke-width="3"/>
    <text x="125" y="232" font-size="19" fill="{blue}" text-anchor="middle">w</text>{fade(0.4,11.4)}</g>
  <g opacity="0"><path d="M184 155 L300 178 M184 225 L300 190" stroke="{muted}" stroke-width="3"/>
    <rect x="304" y="158" width="120" height="50" rx="7" fill="{green}" fill-opacity="0.12" stroke="{green}" stroke-width="3"/>
    <text x="364" y="190" font-size="19" fill="{green}" text-anchor="middle">x · w</text>
    <text x="364" y="238" font-size="16" fill="{muted}" text-anchor="middle">“I came from x and w,</text>
    <text x="364" y="260" font-size="16" fill="{muted}" text-anchor="middle">by multiplication”</text>{fade(2.0,11.4)}</g>
  <g opacity="0"><path d="M428 183 L520 183" stroke="{muted}" stroke-width="3"/>
    <rect x="524" y="158" width="130" height="50" rx="7" fill="{green}" fill-opacity="0.12" stroke="{green}" stroke-width="3"/>
    <text x="589" y="190" font-size="19" fill="{green}" text-anchor="middle">+ b → loss</text>{fade(4.2,11.4)}</g>
  <g opacity="0"><path d="M654 210 Q 400 300 130 250" fill="none" stroke="{amber}" stroke-width="4" stroke-dasharray="11 9">
      <animate attributeName="stroke-dashoffset" from="40" to="0" dur="1.4s" repeatCount="indefinite"/></path>
    <text x="420" y="298" font-size="21" fill="{amber}" text-anchor="middle">.backward() walks it for you</text>{fade(6.4,11.4)}</g>
  <text x="820" y="120" font-size="20" fill="{muted}" text-anchor="middle" opacity="0">you never write{fade(8.0,11.4)}</text>
  <text x="820" y="148" font-size="20" fill="{muted}" text-anchor="middle" opacity="0">a derivative again{fade(8.0,11.4)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",red="#e03131",amber="#f08c00",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",red="#ff8787",amber="#ffb84d",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
W = "curriculum/p3/week-21/"
for slug, anchor, fn, caption in [
 (W+"1-from-linear-models-to-neural-networks.mdx", "ANIM:W21M1", m1,
  "The bend, live: ticks in opposite corners defeat every straight line, and a single bend between two layers separates them. It repeats — watch both."),
 (W+"2-forward-pass-loss-backpropagation.mdx", "ANIM:W21M2", m2,
  "Backpropagation, live: forwards to a prediction and one error number, then backwards giving each layer its share of the blame. It repeats — watch both directions."),
 (W+"3-training-dynamics.mdx", "ANIM:W21M3", m3,
  "Loss curves, live: too large a learning rate explodes, too small stays flat, and the right one descends and settles. It repeats — watch all three."),
 (W+"4-optimizers-regularization-in-practice.mdx", "ANIM:W21M4", m4,
  "Momentum, live: the hiker zig-zags and stops in the first dip; the ball carries speed and rolls through to the bottom. It repeats — watch both."),
 (W+"5-pytorch-fundamentals.mdx", "ANIM:W21M5", m5,
  "Autograd, live: each operation records where its result came from, so the forward pass builds the graph that backward() walks for you. It repeats — watch it twice."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
