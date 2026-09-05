#!/usr/bin/env python3
"""Animations for the four new Phase-4 chapters: the anatomy of a request
(w25 m0), the ReAct loop transcript (w29 m6), the quality/cost/speed triangle
(w26 m0), and an image becoming patches (w27 m0)."""
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

def prompt_anatomy(ink, muted, blue, green, amber, red, bg):
    parts = [("system prompt — sent every time, invisibly", blue, 0.5),
             ("user message — what the person typed", green, 2.0),
             ("assistant message — what it said before", amber, 3.5),
             ("user message — the new question", green, 5.0)]
    out = ""
    for i,(lab,col,t0) in enumerate(parts):
        y = 92 + i*52
        out += (f'<g opacity="0"><rect x="90" y="{y}" width="520" height="42" rx="6" fill="{col}" '
                f'fill-opacity="0.12" stroke="{col}" stroke-width="3"/><text x="106" y="{y+27}" '
                f'font-size="16" fill="{ink}">{lab}</text>{fade(t0,11.4)}</g>')
    return head(1000, 340, "Every request re-sends the whole bundle: the system prompt, then all previous messages, then the new question — the model remembers nothing on its own.", bg) + f'''
  <text x="90" y="60" font-size="21" fill="{muted}">what your program actually sends, every single turn:</text>
  {out}
  <g opacity="0"><rect x="650" y="92" width="280" height="202" rx="9" fill="none" stroke="{ink}" stroke-width="3.5" stroke-dasharray="8 6"/>
    <text x="790" y="176" font-size="20" fill="{ink}" text-anchor="middle">one bundle</text>
    <text x="790" y="208" font-size="18" fill="{muted}" text-anchor="middle">→ the model</text>{fade(6.4,11.4)}</g>
  <text x="500" y="322" font-size="21" fill="{red}" text-anchor="middle" opacity="0">take a message out and it never happened — there is no memory{fade(8.6,11.2)}</text>
</svg>'''

def react_loop(ink, muted, blue, green, amber, bg):
    lines = [("Thought: I need Berlin's August revenue.", blue, 0.5),
             ("Action:  run_sql(...august...)", amber, 1.8),
             ("Observation: 184,220", green, 3.0),
             ("Thought: I also need July to compare.", blue, 4.4),
             ("Action:  run_sql(...july...)", amber, 5.6),
             ("Observation: 201,540", green, 6.8),
             ("Thought: down 8.6%. I have what I need.", blue, 8.0),
             ("Answer:  Berlin fell 8.6% in August.", green, 9.2)]
    out = ""
    for i,(txt,col,t0) in enumerate(lines):
        y = 88 + i*30
        out += (f'<g opacity="0"><text x="110" y="{y}" font-size="17" fill="{col}">{txt}</text>'
                f'{fade(t0,11.4)}</g>')
    return head(1000, 340, "A ReAct transcript: a written thought, a real tool call, a real observation, repeated until the model answers instead of asking for a tool.", bg) + f'''
  <text x="110" y="52" font-size="21" fill="{muted}">think · act · observe — written into the transcript, so the next step can use it</text>
  {out}
  <g opacity="0"><rect x="700" y="80" width="250" height="70" rx="8" fill="{amber}" fill-opacity="0.10" stroke="{amber}" stroke-width="3"/>
    <text x="825" y="112" font-size="17" fill="{amber}" text-anchor="middle">the observation is real —</text>
    <text x="825" y="136" font-size="17" fill="{amber}" text-anchor="middle">your code ran the query</text>{fade(3.4,11.4)}</g>
  <g opacity="0"><rect x="700" y="176" width="250" height="70" rx="8" fill="{green}" fill-opacity="0.10" stroke="{green}" stroke-width="3"/>
    <text x="825" y="208" font-size="17" fill="{green}" text-anchor="middle">it ends when no tool</text>
    <text x="825" y="232" font-size="17" fill="{green}" text-anchor="middle">is asked for ✓</text>{fade(9.4,11.4)}</g>
</svg>'''

def triangle(ink, muted, blue, green, amber, red, bg):
    return head(1000, 340, "Quality, cost and speed pull against each other: a big model is better and slower and dearer, a small one the reverse, so real systems route between them.", bg) + f'''
  <path d="M500 70 L820 268 L180 268 Z" fill="none" stroke="{muted}" stroke-width="3" stroke-dasharray="7 6"/>
  <text x="500" y="56" font-size="21" fill="{green}" text-anchor="middle">quality</text>
  <text x="852" y="288" font-size="21" fill="{amber}" text-anchor="middle">cost</text>
  <text x="150" y="288" font-size="21" fill="{blue}" text-anchor="middle">speed</text>
  <g opacity="0"><circle cx="520" cy="130" r="14" fill="{green}" fill-opacity="0.5" stroke="{green}" stroke-width="3"/>
    <text x="560" y="136" font-size="18" fill="{green}">the big model — best, slowest, dearest</text>{fade(0.6,4.6)}</g>
  <g opacity="0"><circle cx="330" cy="242" r="14" fill="{blue}" fill-opacity="0.5" stroke="{blue}" stroke-width="3"/>
    <text x="360" y="248" font-size="18" fill="{blue}">the small model — fast and cheap, gives something up</text>{fade(5.0,8.6)}</g>
  <g opacity="0"><text x="500" y="316" font-size="21" fill="{amber}" text-anchor="middle">so route: the small one by default, the big one for the hard 5% ✓{fade(9.0,11.4)}</text></g>
</svg>'''

def patches(ink, muted, blue, green, amber, bg):
    grid = ""
    for r in range(4):
        for c in range(6):
            x, y = 120 + c*46, 110 + r*40
            t0 = 1.4 + (r*6 + c)*0.12
            grid += (f'<g opacity="0"><rect x="{x}" y="{y}" width="42" height="36" rx="4" fill="{blue}" '
                     f'fill-opacity="0.18" stroke="{blue}" stroke-width="2"/>{fade(t0,11.4)}</g>')
    tiles = "".join(f'<g opacity="0"><rect x="{560+i*64}" y="150" width="56" height="40" rx="5" fill="{amber}" '
                    f'fill-opacity="0.2" stroke="{amber}" stroke-width="2.5"/>'
                    f'<text x="{588+i*64}" y="176" font-size="14" fill="{amber}" text-anchor="middle">{v}</text>'
                    f'{fade(4.4+i*0.3,11.4)}</g>' for i,v in enumerate(["0.41","1.02","0.07","…"]))
    return head(1000, 330, "A picture is cut into small patches, each patch becomes numbers, and those numbers join the same sequence as the text tiles.", bg) + f'''
  <text x="60" y="60" font-size="21" fill="{muted}">the picture is cut into patches…</text>
  <rect x="112" y="102" width="290" height="168" rx="6" fill="none" stroke="{ink}" stroke-width="3"/>
  {grid}
  <g opacity="0"><path d="M420 186 L540 186" stroke="{amber}" stroke-width="4" stroke-dasharray="9 7">
      <animate attributeName="stroke-dashoffset" from="32" to="0" dur="1.2s" repeatCount="indefinite"/></path>{fade(4.0,11.4)}</g>
  <text x="700" y="120" font-size="20" fill="{muted}" text-anchor="middle" opacity="0">…each becomes numbers{fade(4.2,11.4)}</text>
  {tiles}
  <g opacity="0"><text x="700" y="234" font-size="19" fill="{green}" text-anchor="middle">and joins the same sequence</text>
    <text x="700" y="260" font-size="19" fill="{green}" text-anchor="middle">as your text tiles ✓</text>{fade(6.6,11.4)}</g>
  <text x="500" y="308" font-size="21" fill="{amber}" text-anchor="middle" opacity="0">one model · one stream · several kinds of input{fade(8.6,11.2)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",red="#e03131",amber="#f08c00",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",red="#ff8787",amber="#ffb84d",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
for slug, anchor, fn, caption in [
 ("curriculum/p4/week-25/0-talking-to-the-model.mdx", "ANIM:W25M0", prompt_anatomy,
  "The bundle, live: every turn re-sends the system prompt and the whole history — take a message out and, for the model, it never happened. It repeats."),
 ("curriculum/p4/week-29/6-agent-architectures-and-harnesses.mdx", "ANIM:W29M6", react_loop,
  "ReAct, live: a written thought, a real tool call, a real observation — repeated until the model answers instead of asking for a tool. It repeats."),
 ("curriculum/p4/week-26/0-choosing-a-model.mdx", "ANIM:W26M0", triangle,
  "The triangle, live: the big model sits near quality and far from cost and speed, the small model the reverse — which is why real systems route between them. It repeats."),
 ("curriculum/p4/week-27/0-when-the-input-is-not-text.mdx", "ANIM:W27M0", patches,
  "Seeing, live: the picture is cut into patches, each patch becomes numbers, and they join the same sequence as your text tiles. It repeats — watch it twice."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
