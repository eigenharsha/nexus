#!/usr/bin/env python3
"""Week-20 animations: scale distorting distance (m1), one timestamp unpacking
into a dozen facts (m2), rare positives drowned out (m4), and the same feature
computed twice (m5)."""
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
    return head(1000, 330, "Unscaled, salary dominates every distance because of its units; scaled, age and salary contribute comparably.", bg) + f'''
  <text x="60" y="46" font-size="22" fill="{muted}">two customers, two columns:</text>
  <g opacity="0"><text x="70" y="92" font-size="19" fill="{ink}">age:    34  vs  38</text>
    <text x="70" y="124" font-size="19" fill="{ink}">salary: 52,000  vs  56,000</text>{fade(0.4,11.4)}</g>
  <g opacity="0"><text x="70" y="184" font-size="20" fill="{red}">raw distance:</text>
    <rect x="240" y="166" width="12" height="22" rx="3" fill="{blue}" fill-opacity="0.3" stroke="{blue}" stroke-width="2.5"/>
    <text x="262" y="184" font-size="17" fill="{blue}">age contributes 4</text>
    <rect x="240" y="200" width="420" height="22" rx="3" fill="{red}" fill-opacity="0.3" stroke="{red}" stroke-width="2.5"/>
    <text x="672" y="218" font-size="17" fill="{red}">salary contributes 4,000</text>
    <text x="70" y="260" font-size="20" fill="{red}">the model thinks salary is 1,000× more important ✗</text>{fade(1.6,6.4)}</g>
  <g opacity="0"><text x="70" y="184" font-size="20" fill="{green}">after scaling:</text>
    <rect x="240" y="166" width="150" height="22" rx="3" fill="{green}" fill-opacity="0.3" stroke="{green}" stroke-width="2.5"/>
    <text x="402" y="184" font-size="17" fill="{green}">age: 0.42</text>
    <rect x="240" y="200" width="170" height="22" rx="3" fill="{green}" fill-opacity="0.3" stroke="{green}" stroke-width="2.5"/>
    <text x="422" y="218" font-size="17" fill="{green}">salary: 0.47</text>
    <text x="70" y="260" font-size="20" fill="{green}">comparable — the units no longer decide ✓</text>{fade(7.0,11.4)}</g>
  <text x="500" y="308" font-size="23" fill="{amber}" text-anchor="middle" opacity="0">nothing about the customers changed — only the units{fade(9.0,11.2)}</text>
</svg>'''

def m2(ink, muted, blue, green, amber, bg):
    facts = [("Friday", 0.5), ("23:41 — nearly midnight", 1.1), ("first week of September", 1.7),
             ("4 days after payday", 2.3), ("90 min since last order", 2.9), ("14 days to renewal", 3.5)]
    out = ""
    for i,(f, t0) in enumerate(facts):
        y = 96 + i*38
        out += (f'<g opacity="0"><rect x="470" y="{y-22}" width="380" height="30" rx="5" fill="{green}" '
                f'fill-opacity="0.10" stroke="{green}" stroke-width="2.5"/>'
                f'<text x="484" y="{y-2}" font-size="17" fill="{ink}">{f}</text>{fade(t0,11.4)}</g>')
    return head(1000, 340, "The single value 2026-09-04 23:41 unpacks into a dozen separate facts a model can use.", bg) + f'''
  <g opacity="0"><rect x="60" y="140" width="330" height="60" rx="7" fill="{blue}" fill-opacity="0.12" stroke="{blue}" stroke-width="3.5"/>
    <text x="225" y="178" font-size="24" fill="{blue}" text-anchor="middle">2026-09-04 23:41</text>{fade(0.3,11.4)}</g>
  <text x="225" y="230" font-size="19" fill="{muted}" text-anchor="middle" opacity="0">to a model: one meaningless big number{fade(0.6,11.4)}</text>
  {out}
  <text x="500" y="316" font-size="23" fill="{amber}" text-anchor="middle" opacity="0">every one of these is invisible until somebody digs it out{fade(5.0,11.2)}</text>
</svg>'''

def m4(ink, muted, blue, green, red, amber, bg):
    dots = ""
    for i in range(200):
        x, y = 70 + (i % 25)*35, 100 + (i//25)*26
        rare = i in (58, 137)
        dots += (f'<circle cx="{x}" cy="{y}" r="{7 if rare else 4}" fill="{red if rare else muted}" '
                 f'fill-opacity="{0.95 if rare else 0.28}"/>')
    return head(1000, 340, "Two positives among a thousand rows: training signal is drowned out, resampling breaks calibration, and moving the threshold is the free win.", bg) + f'''
  <text x="60" y="52" font-size="22" fill="{muted}">1,000 rows · 3 positives (red)</text>
  {dots}
  <g opacity="0"><text x="70" y="288" font-size="20" fill="{red}">the training signal is drowned by the 997 boring rows{fade(1.2,5.0)}</text></g>
  <g opacity="0"><rect x="60" y="262" width="420" height="46" rx="6" fill="{amber}" fill-opacity="0.10" stroke="{amber}" stroke-width="3"/>
    <text x="270" y="292" font-size="19" fill="{amber}" text-anchor="middle">resample? it breaks your probabilities</text>{fade(5.4,8.4)}</g>
  <g opacity="0"><rect x="520" y="262" width="420" height="46" rx="6" fill="{green}" fill-opacity="0.12" stroke="{green}" stroke-width="3"/>
    <text x="730" y="292" font-size="19" fill="{green}" text-anchor="middle">move the threshold: free, and it works ✓</text>{fade(8.8,11.4)}</g>
</svg>'''

def m5(ink, muted, blue, green, red, amber, bg):
    return head(1000, 320, "The same feature written twice — pandas in training, service code in production — disagrees on cancelled orders, and the model is fed a number it has never seen.", bg) + f'''
  <g opacity="0"><rect x="60" y="70" width="360" height="110" rx="8" fill="{blue}" fill-opacity="0.10" stroke="{blue}" stroke-width="3.5"/>
    <text x="240" y="100" font-size="20" fill="{blue}" text-anchor="middle">training (pandas)</text>
    <text x="240" y="132" font-size="17" fill="{ink}" text-anchor="middle">avg_order_value =</text>
    <text x="240" y="158" font-size="17" fill="{ink}" text-anchor="middle">mean(all orders)</text>{fade(0.4,11.4)}</g>
  <g opacity="0"><rect x="580" y="70" width="360" height="110" rx="8" fill="{red}" fill-opacity="0.08" stroke="{red}" stroke-width="3.5"/>
    <text x="760" y="100" font-size="20" fill="{red}" text-anchor="middle">serving (the service)</text>
    <text x="760" y="132" font-size="17" fill="{ink}" text-anchor="middle">avg_order_value =</text>
    <text x="760" y="158" font-size="17" fill="{ink}" text-anchor="middle">mean(orders incl. cancelled)</text>{fade(1.8,11.4)}</g>
  <g opacity="0"><text x="500" y="132" font-size="30" fill="{red}" text-anchor="middle">≠</text>{fade(3.4,11.4)}</g>
  <g opacity="0"><text x="500" y="224" font-size="22" fill="{red}" text-anchor="middle">same name · different meaning · nothing fails loudly</text>{fade(4.6,8.0)}</g>
  <g opacity="0"><rect x="250" y="204" width="500" height="46" rx="7" fill="{green}" fill-opacity="0.12" stroke="{green}" stroke-width="3.5"/>
    <text x="500" y="234" font-size="20" fill="{green}" text-anchor="middle">compute it once — use that same code both times ✓</text>{fade(8.4,11.4)}</g>
  <text x="500" y="292" font-size="22" fill="{amber}" text-anchor="middle" opacity="0">the most common way a good model dies quietly{fade(9.6,11.2)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",red="#e03131",amber="#f08c00",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",red="#ff8787",amber="#ffb84d",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
W = "curriculum/p3/week-20/"
for slug, anchor, fn, caption in [
 (W+"1-numerical-categorical-features.mdx", "ANIM:W20M1", m1,
  "Scale, live: unscaled, salary contributes a thousand times more to every distance than age — purely because of its units; scaled, they compete fairly. It repeats — watch both."),
 (W+"2-temporal-text-interaction-features.mdx", "ANIM:W20M2", m2,
  "One timestamp, live: a single value unpacks into a dozen separate facts — weekday, hour, days since the last order, days to renewal. It repeats — watch it twice."),
 (W+"4-imbalanced-classification.mdx", "ANIM:W20M4", m4,
  "Imbalance, live: three positives in a thousand rows drown the training signal; resampling breaks your probabilities, while moving the threshold is free. It repeats."),
 (W+"5-production-feature-pipelines.mdx", "ANIM:W20M5", m5,
  "Skew, live: the same feature written twice disagrees about cancelled orders, and nothing fails loudly — until the model is fed a number it has never seen. It repeats."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
