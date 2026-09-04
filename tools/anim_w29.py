#!/usr/bin/env python3
"""Week-29 animations: the agent loop turning (m1) and a tool call round-trip (m2)."""
import re, sys, inspect
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

def m1(ink, muted, blue, green, amber, red, bg):
    cx, cy, r = 500, 165, 105
    return head(1000, 340, "The agent loop turns: think, act, observe, repeat — and exits only when the model stops asking for tools.", bg) + f'''
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{muted}" stroke-width="2.5" stroke-dasharray="7 8"/>
  <g opacity="0"><rect x="{cx-90}" y="{cy-r-32}" width="180" height="46" rx="7" fill="{blue}" fill-opacity="0.12" stroke="{blue}" stroke-width="3.5"/>
    <text x="{cx}" y="{cy-r-2}" font-size="21" fill="{blue}" text-anchor="middle">1. think (the model)</text>{fade(0.4,11.4)}</g>
  <g opacity="0"><rect x="{cx+r-30}" y="{cy-22}" width="170" height="46" rx="7" fill="{green}" fill-opacity="0.12" stroke="{green}" stroke-width="3.5"/>
    <text x="{cx+r+55}" y="{cy+8}" font-size="21" fill="{green}" text-anchor="middle">2. act (your code)</text>{fade(2.0,11.4)}</g>
  <g opacity="0"><rect x="{cx-90}" y="{cy+r-14}" width="180" height="46" rx="7" fill="{amber}" fill-opacity="0.12" stroke="{amber}" stroke-width="3.5"/>
    <text x="{cx}" y="{cy+r+16}" font-size="21" fill="{amber}" text-anchor="middle">3. observe</text>{fade(3.6,11.4)}</g>
  <g opacity="0"><text x="{cx-r-60}" y="{cy+6}" font-size="21" fill="{muted}" text-anchor="middle">4. repeat</text>{fade(5.0,11.4)}</g>
  <path d="M{cx} {cy-r} A {r} {r} 0 1 1 {cx-2} {cy-r}" fill="none" stroke="{amber}" stroke-width="4" stroke-dasharray="12 10">
    <animate attributeName="stroke-dashoffset" from="44" to="0" dur="1.5s" repeatCount="indefinite"/></path>
  <g opacity="0"><rect x="760" y="120" width="200" height="60" rx="7" fill="none" stroke="{green}" stroke-width="3.5"/>
    <text x="860" y="146" font-size="20" fill="{green}" text-anchor="middle">no tool asked for</text>
    <text x="860" y="170" font-size="20" fill="{green}" text-anchor="middle">→ stop, answer ✓</text>{fade(6.6,11.4)}</g>
  <g opacity="0"><text x="180" y="150" font-size="20" fill="{red}" text-anchor="middle">every turn multiplies</text>
    <text x="180" y="176" font-size="20" fill="{red}" text-anchor="middle">the chance of a wrong step</text>{fade(8.0,11.4)}</g>
  <text x="500" y="322" font-size="25" fill="{amber}" text-anchor="middle" opacity="0">the model never runs anything — it only asks{fade(9.4,11.2)}</text>
</svg>'''

def m2(ink, muted, blue, green, amber, bg):
    return head(1000, 320, "The model asks for a tool by name and arguments; your code validates and runs it; the result goes back into the conversation and the model answers.", bg) + f'''
  <g opacity="0"><rect x="60" y="70" width="200" height="150" rx="8" fill="{blue}" fill-opacity="0.10" stroke="{blue}" stroke-width="3.5"/>
    <text x="160" y="120" font-size="22" fill="{blue}" text-anchor="middle">the model</text>
    <text x="160" y="160" font-size="18" fill="{ink}" text-anchor="middle">“please run</text>
    <text x="160" y="186" font-size="18" fill="{ink}" text-anchor="middle">get_order(TX-4471)”</text>{fade(0.4,11.4)}</g>
  <g opacity="0"><path d="M270 130 L400 130" stroke="{amber}" stroke-width="4" stroke-dasharray="10 8">
      <animate attributeName="stroke-dashoffset" from="36" to="0" dur="1.3s" repeatCount="indefinite"/></path>
    <text x="335" y="112" font-size="18" fill="{amber}" text-anchor="middle">asks</text>{fade(1.6,11.4)}</g>
  <g opacity="0"><rect x="410" y="70" width="200" height="150" rx="8" fill="{green}" fill-opacity="0.10" stroke="{green}" stroke-width="3.5"/>
    <text x="510" y="112" font-size="22" fill="{green}" text-anchor="middle">your code</text>
    <text x="510" y="150" font-size="18" fill="{ink}" text-anchor="middle">validate the args</text>
    <text x="510" y="176" font-size="18" fill="{ink}" text-anchor="middle">then run the function</text>
    <text x="510" y="204" font-size="17" fill="{green}" text-anchor="middle">— you stay in charge</text>{fade(3.0,11.4)}</g>
  <g opacity="0"><path d="M620 170 L750 170" stroke="{amber}" stroke-width="4" stroke-dasharray="10 8">
      <animate attributeName="stroke-dashoffset" from="36" to="0" dur="1.3s" repeatCount="indefinite"/></path>
    <text x="685" y="152" font-size="18" fill="{amber}" text-anchor="middle">result</text>{fade(5.4,11.4)}</g>
  <g opacity="0"><rect x="760" y="70" width="200" height="150" rx="8" fill="none" stroke="{ink}" stroke-width="3.5"/>
    <text x="860" y="118" font-size="20" fill="{ink}" text-anchor="middle">back into the</text>
    <text x="860" y="144" font-size="20" fill="{ink}" text-anchor="middle">conversation</text>
    <text x="860" y="186" font-size="19" fill="{green}" text-anchor="middle">→ then it answers ✓</text>{fade(6.6,11.4)}</g>
  <text x="500" y="292" font-size="25" fill="{amber}" text-anchor="middle" opacity="0">the schema is the instruction manual — vague card, wrong call{fade(8.4,11.2)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",amber="#f08c00",red="#e03131",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",amber="#ffb84d",red="#ff8787",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}

for slug, anchor, fn, caption in [
 ("curriculum/p4/week-29/1-what-an-agent-actually-is.mdx", "ANIM:W29M1", m1,
  "The loop, live: think, act, observe, repeat — and it exits only when the model stops asking for tools. It repeats — watch it twice."),
 ("curriculum/p4/week-29/2-tools-function-calling.mdx", "ANIM:W29M2", m2,
  "A tool call, live: the model asks by name and arguments, your code validates and runs it, and the result goes back into the conversation. It repeats — watch it twice."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
