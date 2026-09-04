#!/usr/bin/env python3
"""Week-30 animations: a graph running with parallel branches (m1), and a run
that dies at node 7 then resumes there instead of restarting (m3)."""
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
def node(x,y,w,h,label,col,t0,size=17):
    return (f'<g opacity="0"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{col}" fill-opacity="0.14" '
            f'stroke="{col}" stroke-width="3.5"/><text x="{x+w/2}" y="{y+h/2+6}" font-size="{size}" fill="{col}" '
            f'text-anchor="middle">{label}</text>{fade(t0,11.4)}</g>')
def edge(x1,y1,x2,y2,col,t0):
    return (f'<g opacity="0"><path d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="3" stroke-dasharray="8 6"/>'
            f'{fade(t0,11.4)}</g>')

def m1(ink, muted, blue, green, amber, bg):
    return head(1000, 340, "Three research nodes run in parallel, each feeding a draft, all feeding review and then assembly — the dependencies are the shape of the work.", bg) + f'''
  {node(60,140,130,54,"pull our numbers",blue,0.4,14)}
  {node(250,60,130,50,"research A",green,1.2,15)}
  {node(250,140,130,50,"research B",green,1.5,15)}
  {node(250,220,130,50,"research C",green,1.8,15)}
  <text x="315" y="42" font-size="19" fill="{muted}" text-anchor="middle" opacity="0">these three run at the same time{fade(2.4,11.4)}</text>
  {edge(190,167,246,85,muted,2.0)}{edge(190,167,246,165,muted,2.0)}{edge(190,167,246,245,muted,2.0)}
  {node(440,140,120,50,"draft",blue,3.6)}
  {edge(384,85,436,158,muted,3.4)}{edge(384,165,436,165,muted,3.4)}{edge(384,245,436,172,muted,3.4)}
  {node(620,140,120,50,"review",amber,5.2)}
  {edge(562,165,616,165,muted,5.0)}
  {node(800,140,140,50,"assemble & send",green,6.8,14)}
  {edge(742,165,796,165,muted,6.6)}
  <text x="500" y="312" font-size="25" fill="{amber}" text-anchor="middle" opacity="0">the arrows are the truth — anything unjoined can run at once{fade(8.2,11.2)}</text>
</svg>'''

def m3(ink, muted, blue, green, red, amber, bg):
    def row(y, states, t0, label):
        out = f'<text x="60" y="{y+22}" font-size="19" fill="{muted}">{label}</text>'
        for i, s in enumerate(states):
            x = 250 + i*76
            col = {"ok": green, "dead": red, "todo": muted, "skip": blue}[s]
            fill = 0.22 if s in ("ok", "dead") else 0.06
            out += (f'<rect x="{x}" y="{y}" width="60" height="42" rx="6" fill="{col}" fill-opacity="{fill}" '
                    f'stroke="{col}" stroke-width="3"/><text x="{x+30}" y="{y+28}" font-size="17" fill="{col}" '
                    f'text-anchor="middle">{i+1}</text>')
            if s == "dead":
                out += f'<path d="M{x+8} {y+8} L{x+52} {y+34} M{x+52} {y+8} L{x+8} {y+34}" stroke="{red}" stroke-width="3.5"/>'
        return f'<g opacity="0">{out}{fade(t0,11.4)}</g>'
    return head(1000, 320, "A nine-node run dies at node seven; restarting from node one repeats six paid steps, while resuming skips them and restarts at seven.", bg) + f'''
  {row(50, ["ok"]*6 + ["dead"] + ["todo"]*2, 0.4, "3 a.m.:")}
  <text x="880" y="78" font-size="19" fill="{red}" opacity="0">node 7 dies{fade(1.6,11.4)}</text>
  {row(140, ["todo"]*9, 3.2, "restart:")}
  <text x="880" y="168" font-size="19" fill="{red}" opacity="0">90 min + £ again ✗{fade(4.0,11.4)}</text>
  {row(230, ["skip"]*6 + ["ok"] + ["todo"]*2, 6.4, "resume:")}
  <text x="880" y="258" font-size="19" fill="{green}" opacity="0">picks up at 7 ✓{fade(7.4,11.4)}</text>
  <text x="500" y="300" font-size="24" fill="{amber}" text-anchor="middle" opacity="0">write down each node's result the moment it succeeds{fade(8.8,11.2)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",amber="#f08c00",red="#e03131",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",amber="#ffb84d",red="#ff8787",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
for slug, anchor, fn, caption in [
 ("curriculum/p4/week-30/1-graphs-as-the-right-abstraction.mdx", "ANIM:W30M1", m1,
  "The graph, live: three researches run at the same time because nothing joins them, then the draft, the review and the send follow their arrows. It repeats — watch it twice."),
 ("curriculum/p4/week-30/3-durable-execution-checkpoint-resume.mdx", "ANIM:W30M3", m3,
  "Resume, live: node seven dies at 3 a.m.; restarting repeats six paid steps, while resuming skips them and picks up exactly where it stopped. It repeats — watch both."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
