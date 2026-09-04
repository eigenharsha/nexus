#!/usr/bin/env python3
"""Week-23 animations: a model gaining an address (m1), load-once versus
load-per-request (m2), image layers and cache (m3), push becoming deploy (m4),
and a cold start (m5)."""
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
    return head(1000, 320, "In a notebook the model has no address and dies with the session; as a service it has an endpoint other software can call.", bg) + f'''
  <g opacity="0"><rect x="70" y="80" width="300" height="150" rx="9" fill="{red}" fill-opacity="0.06" stroke="{red}" stroke-width="3.5" stroke-dasharray="8 6"/>
    <text x="220" y="124" font-size="21" fill="{ink}" text-anchor="middle">your notebook</text>
    <text x="220" y="160" font-size="18" fill="{muted}" text-anchor="middle">the model lives here</text>
    <text x="220" y="196" font-size="18" fill="{red}" text-anchor="middle">no address · dies with the session</text>{fade(0.4,11.4)}</g>
  <g opacity="0"><text x="470" y="120" font-size="20" fill="{muted}" text-anchor="middle">the app:</text>
    <text x="470" y="152" font-size="19" fill="{red}" text-anchor="middle">“how do I call it?”</text>
    <text x="470" y="184" font-size="24" fill="{red}" text-anchor="middle">…you cannot</text>{fade(1.6,5.2)}</g>
  <g opacity="0"><rect x="600" y="80" width="330" height="150" rx="9" fill="{green}" fill-opacity="0.10" stroke="{green}" stroke-width="3.5"/>
    <text x="765" y="118" font-size="21" fill="{green}" text-anchor="middle">the service</text>
    <text x="765" y="154" font-size="18" fill="{ink}" text-anchor="middle">POST /predict</text>
    <text x="765" y="190" font-size="18" fill="{muted}" text-anchor="middle">an address other software can call ✓</text>{fade(6.0,11.4)}</g>
  <g opacity="0"><path d="M470 155 L590 155" stroke="{amber}" stroke-width="4" stroke-dasharray="10 8">
      <animate attributeName="stroke-dashoffset" from="36" to="0" dur="1.3s" repeatCount="indefinite"/></path>{fade(6.4,11.4)}</g>
  <text x="500" y="292" font-size="22" fill="{amber}" text-anchor="middle" opacity="0">and everything implicit must now be written down{fade(8.6,11.2)}</text>
</svg>'''

def m2(ink, muted, blue, green, red, amber, bg):
    def bar(x, y, w, col, lab, val):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="4" fill="{col}" fill-opacity="0.25" '
                f'stroke="{col}" stroke-width="3"/><text x="{x-12}" y="{y+19}" font-size="16" fill="{ink}" '
                f'text-anchor="end">{lab}</text><text x="{x+w+12}" y="{y+19}" font-size="16" fill="{col}">{val}</text>')
    return head(1000, 320, "Loading the model inside the request handler spends two seconds per call to do twenty milliseconds of work; loading it once at startup does not.", bg) + f'''
  <g opacity="0"><text x="60" y="52" font-size="21" fill="{red}">model loaded inside the handler:</text>
    {bar(280, 70, 520, red, "load model", "2,000 ms")}
    {bar(280, 110, 8, blue, "predict", "20 ms")}
    <text x="500" y="166" font-size="19" fill="{red}">…on every single request</text>{fade(0.5,5.4)}</g>
  <g opacity="0"><text x="60" y="212" font-size="21" fill="{green}">model loaded once at startup:</text>
    {bar(280, 230, 8, blue, "predict", "20 ms")}
    <text x="380" y="286" font-size="19" fill="{green}">100× faster, same code, moved two lines up ✓</text>{fade(6.2,11.4)}</g>
</svg>'''

def m3(ink, muted, blue, green, amber, bg):
    layers = [("base OS", 0.4, green), ("python install", 1.0, green), ("dependencies", 1.6, green), ("your code", 2.2, amber)]
    out = ""
    for i,(lab,t0,col) in enumerate(layers):
        y = 210 - i*44
        out += (f'<g opacity="0"><rect x="120" y="{y}" width="300" height="36" rx="5" fill="{col}" fill-opacity="0.16" '
                f'stroke="{col}" stroke-width="3"/><text x="270" y="{y+24}" font-size="16" fill="{col}" '
                f'text-anchor="middle">{lab}</text>{fade(t0,11.4)}</g>')
    return head(1000, 320, "An image is a stack of cached layers; putting dependencies before your code means an edit rebuilds only the top layer.", bg) + f'''
  <text x="270" y="52" font-size="21" fill="{muted}" text-anchor="middle">the image, in layers</text>
  {out}
  <g opacity="0"><text x="620" y="90" font-size="20" fill="{green}">change your code →</text>
    <text x="620" y="118" font-size="20" fill="{green}">only the top layer rebuilds ✓</text>
    <text x="620" y="152" font-size="19" fill="{muted}">4 seconds</text>{fade(3.4,11.4)}</g>
  <g opacity="0"><text x="620" y="206" font-size="20" fill="{amber}">copy your code BEFORE deps →</text>
    <text x="620" y="234" font-size="20" fill="{amber}">every edit reinstalls everything</text>
    <text x="620" y="268" font-size="19" fill="{muted}">6 minutes, every time</text>{fade(6.4,11.4)}</g>
</svg>'''

def m4(ink, muted, blue, green, red, amber, bg):
    steps = [("push", 0.5, blue), ("run tests", 1.6, green), ("build image", 2.8, green),
             ("deploy", 4.0, green), ("rollback in 3 min", 6.4, amber)]
    out = ""
    for i,(lab,t0,col) in enumerate(steps[:4]):
        x = 70 + i*230
        out += (f'<g opacity="0"><rect x="{x}" y="120" width="180" height="56" rx="7" fill="{col}" fill-opacity="0.14" '
                f'stroke="{col}" stroke-width="3.5"/><text x="{x+90}" y="155" font-size="18" fill="{col}" '
                f'text-anchor="middle">{lab}</text>{fade(t0,11.4)}</g>')
        if i < 3:
            out += (f'<g opacity="0"><path d="M{x+184} 148 L{x+226} 148" stroke="{muted}" stroke-width="3" '
                    f'stroke-dasharray="7 6"/>{fade(t0+0.5,11.4)}</g>')
    return head(1000, 300, "A push runs the tests, builds the image and deploys — identically every time — and the same pipeline rolls back in three minutes.", bg) + f'''
  <text x="500" y="66" font-size="22" fill="{muted}" text-anchor="middle">every push · identically · Tuesday morning or Friday evening</text>
  {out}
  <g opacity="0"><path d="M760 196 Q 430 250 160 196" fill="none" stroke="{amber}" stroke-width="4" stroke-dasharray="11 9">
      <animate attributeName="stroke-dashoffset" from="40" to="0" dur="1.4s" repeatCount="indefinite"/></path>
    <text x="460" y="272" font-size="21" fill="{amber}" text-anchor="middle">…and it rolls back just as fast ✓</text>{fade(6.4,11.4)}</g>
</svg>'''

def m5(ink, muted, blue, green, red, amber, bg):
    return head(1000, 320, "A cold start boots a container, imports libraries and reads a 400 MB model before the first answer; a warm one answers immediately.", bg) + f'''
  <text x="60" y="50" font-size="21" fill="{red}">cold start — the function was asleep:</text>
  <g opacity="0"><rect x="200" y="68" width="150" height="26" rx="4" fill="{red}" fill-opacity="0.25" stroke="{red}" stroke-width="3"/>
    <text x="188" y="87" font-size="16" fill="{ink}" text-anchor="end">boot container</text>
    <rect x="200" y="104" width="190" height="26" rx="4" fill="{red}" fill-opacity="0.25" stroke="{red}" stroke-width="3"/>
    <text x="188" y="123" font-size="16" fill="{ink}" text-anchor="end">import libraries</text>
    <rect x="200" y="140" width="330" height="26" rx="4" fill="{red}" fill-opacity="0.25" stroke="{red}" stroke-width="3"/>
    <text x="188" y="159" font-size="16" fill="{ink}" text-anchor="end">read the 400 MB model</text>
    <rect x="200" y="176" width="10" height="26" rx="4" fill="{blue}" fill-opacity="0.3" stroke="{blue}" stroke-width="3"/>
    <text x="188" y="195" font-size="16" fill="{ink}" text-anchor="end">predict</text>
    <text x="560" y="160" font-size="20" fill="{red}">the first user waits several seconds</text>{fade(0.5,6.0)}</g>
  <g opacity="0"><text x="60" y="238" font-size="21" fill="{green}">warm — it is already up:</text>
    <rect x="200" y="252" width="10" height="26" rx="4" fill="{green}" fill-opacity="0.3" stroke="{green}" stroke-width="3"/>
    <text x="240" y="271" font-size="19" fill="{green}">predict — 20 ms ✓</text>{fade(6.6,11.4)}</g>
  <text x="700" y="292" font-size="21" fill="{amber}" text-anchor="middle" opacity="0">bursty traffic: taxis. Steady traffic: the company car.{fade(8.6,11.2)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",red="#e03131",amber="#f08c00",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",red="#ff8787",amber="#ffb84d",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
W = "curriculum/p3/week-23/"
for slug, anchor, fn, caption in [
 (W+"1-from-notebook-to-service.mdx", "ANIM:W23M1", m1,
  "An address, live: in a notebook the model cannot be called and dies with the session; as a service it has an endpoint other software can use. It repeats."),
 (W+"2-serving-with-fastapi.mdx", "ANIM:W23M2", m2,
  "Load once, live: loading inside the handler spends two seconds per request to do twenty milliseconds of work; loading at startup does not. It repeats — watch both."),
 (W+"3-docker.mdx", "ANIM:W23M3", m3,
  "Layers, live: the image is a stack of cached slices, so dependencies before code means an edit rebuilds only the top. It repeats — watch both orders."),
 (W+"4-ci-cd.mdx", "ANIM:W23M4", m4,
  "The pipeline, live: a push runs tests, builds the image and deploys — identically every time — and rolls back just as fast. It repeats — watch it twice."),
 (W+"5-serverless-deployment.mdx", "ANIM:W23M5", m5,
  "Cold start, live: a sleeping function boots, imports and reads a 400 MB model before it can answer, while a warm one answers in milliseconds. It repeats — watch both."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
