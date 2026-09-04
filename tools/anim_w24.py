#!/usr/bin/env python3
"""Week-24 animations: self-healing replicas (m1), a stable name in front of
moving copies (m2), autoscaling that arrives late (m3), dynamic batching (m4),
and silent drift (m5)."""
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
    def copy(x, col, t0, t1, label="copy"):
        return (f'<g opacity="0"><rect x="{x}" y="130" width="150" height="80" rx="8" fill="{col}" fill-opacity="0.12" '
                f'stroke="{col}" stroke-width="3.5"/><text x="{x+75}" y="176" font-size="17" fill="{col}" '
                f'text-anchor="middle">{label}</text>{fade(t0,t1)}</g>')
    return head(1000, 320, "One of three copies dies at 3 a.m.; with nothing watching it stays dead, and with an orchestrator a replacement starts automatically.", bg) + f'''
  <text x="500" y="58" font-size="22" fill="{muted}" text-anchor="middle">“I want three copies running, always.”</text>
  {copy(140, green, 0.4, 11.4)}
  {copy(330, green, 0.4, 4.6)}
  {copy(520, green, 0.4, 11.4)}
  <g opacity="0"><path d="M340 140 L470 200 M470 140 L340 200" stroke="{red}" stroke-width="5"/>
    <text x="405" y="244" font-size="19" fill="{red}" text-anchor="middle">died at 3 a.m.</text>{fade(3.6,7.0)}</g>
  <g opacity="0"><text x="800" y="160" font-size="20" fill="{red}" text-anchor="middle">nothing watching →</text>
    <text x="800" y="188" font-size="20" fill="{red}" text-anchor="middle">still dead on Monday ✗</text>{fade(4.4,7.0)}</g>
  {copy(330, amber, 7.6, 11.4, "restarted")}
  <g opacity="0"><text x="800" y="160" font-size="20" fill="{green}" text-anchor="middle">an orchestrator →</text>
    <text x="800" y="188" font-size="20" fill="{green}" text-anchor="middle">a replacement, in seconds ✓</text>{fade(7.8,11.4)}</g>
  <text x="500" y="294" font-size="21" fill="{amber}" text-anchor="middle" opacity="0">you declare an outcome, not instructions{fade(9.4,11.2)}</text>
</svg>'''

def m2(ink, muted, blue, green, amber, bg):
    return head(1000, 320, "Callers use one stable name; behind it a router keeps a live list of healthy copies whose own addresses keep changing.", bg) + f'''
  <g opacity="0"><rect x="60" y="130" width="170" height="70" rx="8" fill="none" stroke="{ink}" stroke-width="3.5"/>
    <text x="145" y="172" font-size="19" fill="{ink}" text-anchor="middle">the caller</text>{fade(0.4,11.4)}</g>
  <g opacity="0"><rect x="300" y="120" width="200" height="90" rx="8" fill="{green}" fill-opacity="0.12" stroke="{green}" stroke-width="3.5"/>
    <text x="400" y="156" font-size="18" fill="{green}" text-anchor="middle">one stable name</text>
    <text x="400" y="184" font-size="16" fill="{muted}" text-anchor="middle">predict.internal</text>{fade(1.0,11.4)}</g>
  <g opacity="0"><path d="M234 165 L294 165" stroke="{amber}" stroke-width="4" stroke-dasharray="9 7">
      <animate attributeName="stroke-dashoffset" from="32" to="0" dur="1.2s" repeatCount="indefinite"/></path>{fade(1.4,11.4)}</g>
  <g opacity="0"><rect x="600" y="70" width="150" height="52" rx="7" fill="{blue}" fill-opacity="0.12" stroke="{blue}" stroke-width="3"/>
    <text x="675" y="102" font-size="15" fill="{blue}" text-anchor="middle">10.2.4.19</text>{fade(2.4,7.0)}</g>
  <g opacity="0"><rect x="600" y="138" width="150" height="52" rx="7" fill="{blue}" fill-opacity="0.12" stroke="{blue}" stroke-width="3"/>
    <text x="675" y="170" font-size="15" fill="{blue}" text-anchor="middle">10.2.7.31</text>{fade(2.4,11.4)}</g>
  <g opacity="0"><rect x="600" y="206" width="150" height="52" rx="7" fill="{blue}" fill-opacity="0.12" stroke="{blue}" stroke-width="3"/>
    <text x="675" y="238" font-size="15" fill="{blue}" text-anchor="middle">10.2.9.02</text>{fade(2.4,11.4)}</g>
  <g opacity="0"><rect x="600" y="70" width="150" height="52" rx="7" fill="{amber}" fill-opacity="0.16" stroke="{amber}" stroke-width="3"/>
    <text x="675" y="102" font-size="15" fill="{amber}" text-anchor="middle">10.2.5.88 (new)</text>{fade(7.4,11.4)}</g>
  <g opacity="0"><text x="850" y="150" font-size="19" fill="{muted}" text-anchor="middle">copies come and go ·</text>
    <text x="850" y="176" font-size="19" fill="{muted}" text-anchor="middle">the caller never notices</text>{fade(8.2,11.4)}</g>
</svg>'''

def m3(ink, muted, blue, green, red, amber, bg):
    return head(1000, 320, "Traffic spikes; a web app scales in seconds while a model service takes ninety, so its new copies arrive after the spike has passed.", bg) + f'''
  <line x1="80" y1="250" x2="900" y2="250" stroke="{muted}" stroke-width="2.5"/>
  <path d="M80 240 L240 240 L280 90 L470 90 L510 240 L900 240" fill="none" stroke="{ink}" stroke-width="4"/>
  <text x="380" y="70" font-size="20" fill="{ink}" text-anchor="middle">traffic</text>
  <g opacity="0"><path d="M280 240 L300 150 L470 150" fill="none" stroke="{green}" stroke-width="4" stroke-dasharray="8 6"/>
    <text x="620" y="146" font-size="19" fill="{green}">web app: new copies in seconds ✓</text>{fade(1.6,11.4)}</g>
  <g opacity="0"><path d="M280 240 L560 240 L580 180 L900 180" fill="none" stroke="{red}" stroke-width="4" stroke-dasharray="8 6"/>
    <text x="620" y="212" font-size="19" fill="{red}">model service: ready 90 s later —</text>
    <text x="620" y="238" font-size="19" fill="{red}">after the spike has gone ✗</text>{fade(5.0,11.4)}</g>
  <text x="500" y="296" font-size="21" fill="{amber}" text-anchor="middle" opacity="0">so: leading signals, a warm floor, and generous cooldowns{fade(8.6,11.2)}</text>
</svg>'''

def m4(ink, muted, blue, green, amber, bg):
    ones = "".join(f'<g opacity="0"><rect x="{120+i*46}" y="90" width="36" height="36" rx="5" fill="{blue}" '
                   f'fill-opacity="0.2" stroke="{blue}" stroke-width="2.5"/>{fade(0.4+i*0.12, 5.4)}</g>' for i in range(10))
    batch = "".join(f'<rect x="{120+i*46}" y="200" width="36" height="36" rx="5" fill="{green}" fill-opacity="0.25" '
                    f'stroke="{green}" stroke-width="2.5"/>' for i in range(10))
    return head(1000, 320, "Ten requests processed one at a time barely use the GPU; batched together they cost barely more than one.", bg) + f'''
  <text x="60" y="66" font-size="21" fill="{muted}">one at a time:</text>
  {ones}
  <g opacity="0"><text x="640" y="118" font-size="20" fill="{blue}">10 × 20 ms = 200 ms</text>
    <text x="640" y="146" font-size="19" fill="{red if False else muted}">and the GPU is barely used</text>{fade(1.8,5.4)}</g>
  <text x="60" y="176" font-size="21" fill="{muted}" opacity="0">batched — wait 3 ms, then run them together:{fade(6.0,11.4)}</text>
  <g opacity="0">{batch}
    <rect x="112" y="192" width="470" height="52" rx="7" fill="none" stroke="{amber}" stroke-width="3.5" stroke-dasharray="9 7"/>
    <text x="640" y="228" font-size="20" fill="{green}">≈ 24 ms for all ten ✓</text>{fade(6.4,11.4)}</g>
  <text x="500" y="292" font-size="21" fill="{amber}" text-anchor="middle" opacity="0">3 ms of latency bought a large multiple of throughput{fade(8.8,11.2)}</text>
</svg>'''

def m5(ink, muted, blue, green, red, amber, bg):
    bars_a = "".join(f'<rect x="{140+i*40}" y="{200-h}" width="30" height="{h}" rx="3" fill="{blue}" fill-opacity="0.28" stroke="{blue}" stroke-width="2"/>'
                     for i,h in enumerate([20,45,80,110,80,45,20]))
    bars_b = "".join(f'<rect x="{560+i*40}" y="{200-h}" width="30" height="{h}" rx="3" fill="{amber}" fill-opacity="0.28" stroke="{amber}" stroke-width="2"/>'
                     for i,h in enumerate([70,105,85,45,25,15,8]))
    return head(1000, 320, "Uptime and latency stay green while the input distribution shifts away from the training data and accuracy quietly decays.", bg) + f'''
  <g opacity="0"><text x="280" y="58" font-size="20" fill="{blue}" text-anchor="middle">your training data</text>{bars_a}
    <line x1="130" y1="202" x2="420" y2="202" stroke="{muted}" stroke-width="2.5"/>{fade(0.4,11.4)}</g>
  <g opacity="0"><text x="700" y="58" font-size="20" fill="{amber}" text-anchor="middle">this month's traffic</text>{bars_b}
    <line x1="550" y1="202" x2="840" y2="202" stroke="{muted}" stroke-width="2.5"/>{fade(3.0,11.4)}</g>
  <g opacity="0"><text x="500" y="252" font-size="21" fill="{green}" text-anchor="middle">uptime 99.98% · latency flat · zero errors</text>{fade(5.4,11.4)}</g>
  <g opacity="0"><text x="500" y="286" font-size="22" fill="{red}" text-anchor="middle">and the model is quietly, steadily worse ✗</text>{fade(7.6,11.4)}</g>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",red="#e03131",amber="#f08c00",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",red="#ff8787",amber="#ffb84d",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
W = "curriculum/p3/week-24/"
for slug, anchor, fn, caption in [
 (W+"1-why-orchestration-exists.mdx", "ANIM:W24M1", m1,
  "Self-healing, live: one of three copies dies at 3 a.m. — with nothing watching it is still dead on Monday; with an orchestrator a replacement starts in seconds. It repeats."),
 (W+"2-deployments-services-configuration.mdx", "ANIM:W24M2", m2,
  "Service discovery, live: callers use one stable name while the copies behind it come, go and change address. It repeats — watch a copy be replaced."),
 (W+"3-resources-scheduling-autoscaling.mdx", "ANIM:W24M3", m3,
  "Autoscaling, live: a web app's new copies arrive within the spike, while a model service's arrive ninety seconds later — after it has passed. It repeats."),
 (W+"4-model-serving-frameworks.mdx", "ANIM:W24M4", m4,
  "Batching, live: ten requests one at a time cost ten times as much as ten run together through the model. It repeats — watch both."),
 (W+"5-operating-an-ml-service.mdx", "ANIM:W24M5", m5,
  "Drift, live: the traffic's shape moves away from the training data while uptime, latency and error rate all stay perfectly green. It repeats — watch it twice."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
