#!/usr/bin/env python3
"""Animations for the new prompting and agent-architecture weeks."""
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

def examples(ink, muted, green, red, amber, bg):
    return head(1000, 330, "Three worked examples teach a rule an instruction could not: the shouty letter that is not urgent is labelled ordinary.", bg) + f'''
  <text x="60" y="52" font-size="21" fill="{muted}">three examples, and the third does the real work:</text>
  <g opacity="0"><text x="80" y="100" font-size="18" fill="{ink}">“System down for all users.”</text>
    <text x="640" y="100" font-size="18" fill="{red}">→ URGENT</text>{fade(0.5,11.4)}</g>
  <g opacity="0"><text x="80" y="140" font-size="18" fill="{ink}">“Please update my postal address.”</text>
    <text x="640" y="140" font-size="18" fill="{green}">→ ORDINARY</text>{fade(1.6,11.4)}</g>
  <g opacity="0"><text x="80" y="180" font-size="18" fill="{ink}">“URGENT!!! When does the sale start?”</text>
    <text x="640" y="180" font-size="18" fill="{green}">→ ORDINARY</text>
    <rect x="66" y="158" width="700" height="32" rx="6" fill="none" stroke="{amber}" stroke-width="3" stroke-dasharray="8 6"/>{fade(3.0,11.4)}</g>
  <g opacity="0"><text x="500" y="228" font-size="21" fill="{amber}" text-anchor="middle">the word “urgent” is not the same as being urgent{fade(5.0,11.4)}</text></g>
  <g opacity="0"><text x="80" y="278" font-size="18" fill="{ink}">“Card payments failing since 09:00.”</text>
    <text x="640" y="278" font-size="18" fill="{red}">→ URGENT ✓</text>{fade(7.4,11.4)}</g>
  <text x="500" y="316" font-size="19" fill="{muted}" text-anchor="middle" opacity="0">no instruction expresses that distinction as cleanly{fade(9.0,11.2)}</text>
</svg>'''

def window(ink, muted, blue, green, amber, red, bg):
    rows = [("system prompt", 90, blue, 0.5), ("tool definitions", 150, blue, 1.4),
            ("retrieved passages", 320, green, 2.4), ("conversation history", 260, amber, 3.6),
            ("the user's question", 60, green, 4.6)]
    out, x = "", 120
    for lab, w, col, t0 in rows:
        out += (f'<g opacity="0"><rect x="{x}" y="120" width="{w}" height="60" rx="5" fill="{col}" '
                f'fill-opacity="0.18" stroke="{col}" stroke-width="2.5"/>'
                f'<text x="{x+w/2}" y="204" font-size="14" fill="{muted}" text-anchor="middle" '
                f'transform="rotate(20 {x+w/2} 204)">{lab}</text>{fade(t0,11.4)}</g>')
        x += w + 6
    return head(1000, 330, "The window fills with system prompt, tools, passages and history until the reserved answer space is threatened and something must be evicted.", bg) + f'''
  <rect x="115" y="115" width="770" height="70" rx="7" fill="none" stroke="{ink}" stroke-width="3.5"/>
  <text x="500" y="98" font-size="20" fill="{muted}" text-anchor="middle">one finite window, every single call</text>
  {out}
  <g opacity="0"><rect x="810" y="115" width="75" height="70" rx="6" fill="{red}" fill-opacity="0.12" stroke="{red}" stroke-width="3" stroke-dasharray="7 6"/>
    <text x="847" y="220" font-size="14" fill="{red}" text-anchor="middle" transform="rotate(20 847 220)">the answer</text>{fade(5.4,11.4)}</g>
  <g opacity="0"><text x="500" y="272" font-size="21" fill="{red}" text-anchor="middle">full — and it will not tell you what fell out{fade(7.0,11.4)}</text></g>
  <text x="500" y="308" font-size="20" fill="{amber}" text-anchor="middle" opacity="0">so budget it: stable first, question last, answer reserved{fade(8.8,11.2)}</text>
</svg>'''

def versions(ink, muted, blue, green, red, amber, bg):
    return head(1000, 320, "A prompt edited in place has no history; versioned prompts ship, get measured, and roll back in a minute.", bg) + f'''
  <g opacity="0"><rect x="70" y="80" width="280" height="80" rx="8" fill="{red}" fill-opacity="0.07" stroke="{red}" stroke-width="3.5" stroke-dasharray="8 6"/>
    <text x="210" y="116" font-size="19" fill="{ink}" text-anchor="middle">the recipe on an envelope</text>
    <text x="210" y="146" font-size="17" fill="{red}" text-anchor="middle">anyone edits · nobody signs · no copy</text>{fade(0.4,4.6)}</g>
  <g opacity="0"><rect x="70" y="180" width="130" height="50" rx="6" fill="{blue}" fill-opacity="0.12" stroke="{blue}" stroke-width="3"/>
    <text x="135" y="211" font-size="17" fill="{blue}" text-anchor="middle">triage@v2</text>
    <rect x="230" y="180" width="130" height="50" rx="6" fill="{green}" fill-opacity="0.16" stroke="{green}" stroke-width="3"/>
    <text x="295" y="211" font-size="17" fill="{green}" text-anchor="middle">triage@v3</text>{fade(5.0,11.4)}</g>
  <g opacity="0"><text x="560" y="120" font-size="19" fill="{muted}">run both on the same 20 cases:</text>
    <text x="580" y="156" font-size="19" fill="{green}">wins 4 · losses 0 · ties 16 → ship ✓</text>
    <text x="580" y="192" font-size="19" fill="{red}">wins 3 · losses 2 · ties 15 → do not ship</text>{fade(6.4,11.4)}</g>
  <g opacity="0"><path d="M295 244 Q 215 282 135 244" fill="none" stroke="{amber}" stroke-width="4" stroke-dasharray="10 8">
      <animate attributeName="stroke-dashoffset" from="36" to="0" dur="1.3s" repeatCount="indefinite"/></path>
    <text x="215" y="298" font-size="18" fill="{amber}" text-anchor="middle">rollback: one minute, no deploy</text>{fade(8.6,11.4)}</g>
</svg>'''

def buried(ink, muted, blue, green, red, amber, bg):
    return head(1000, 330, "A rule near the end is followed; the same rule buried among passages and history is not.", bg) + f'''
  <g opacity="0"><text x="60" y="66" font-size="20" fill="{green}">short input — the rule is near the end:</text>
    <rect x="60" y="82" width="240" height="40" rx="5" fill="{muted}" fill-opacity="0.10" stroke="{muted}" stroke-width="2"/>
    <rect x="308" y="82" width="200" height="40" rx="5" fill="{green}" fill-opacity="0.2" stroke="{green}" stroke-width="3"/>
    <text x="408" y="108" font-size="15" fill="{green}" text-anchor="middle">under 100 words</text>
    <text x="600" y="108" font-size="19" fill="{green}">obeyed ✓</text>{fade(0.5,5.0)}</g>
  <g opacity="0"><text x="60" y="186" font-size="20" fill="{red}">long input — the same rule, buried:</text>
    <rect x="60" y="202" width="150" height="40" rx="5" fill="{muted}" fill-opacity="0.10" stroke="{muted}" stroke-width="2"/>
    <rect x="216" y="202" width="120" height="40" rx="5" fill="{red}" fill-opacity="0.16" stroke="{red}" stroke-width="3"/>
    <text x="276" y="228" font-size="13" fill="{red}" text-anchor="middle">the rule</text>
    <rect x="342" y="202" width="480" height="40" rx="5" fill="{muted}" fill-opacity="0.10" stroke="{muted}" stroke-width="2"/>
    <text x="580" y="228" font-size="15" fill="{muted}" text-anchor="middle">…20 retrieved passages and 40 turns of history…</text>
    <text x="480" y="278" font-size="19" fill="{red}" text-anchor="middle">ignored — it wrote 300 words ✗</text>{fade(5.6,11.4)}</g>
  <text x="500" y="312" font-size="20" fill="{amber}" text-anchor="middle" opacity="0">nothing changed except where the rule sat{fade(9.0,11.2)}</text>
</svg>'''

def react_trace(ink, muted, blue, green, amber, bg):
    lines = [("Thought: I need Berlin's August revenue.", blue, 0.5),
             ("Action:  run_sql(august)", amber, 1.7),
             ("Observation: 184,220", green, 2.9),
             ("Thought: and July, to compare.", blue, 4.1),
             ("Action:  run_sql(july)", amber, 5.3),
             ("Observation: 201,540", green, 6.5),
             ("Answer:  down 8.6% ✓", green, 8.0)]
    out = "".join(f'<g opacity="0"><text x="110" y="{96+i*32}" font-size="17" fill="{c}">{t}</text>{fade(s,11.4)}</g>'
                  for i,(t,c,s) in enumerate(lines))
    return head(1000, 330, "The transcript grows line by line: a thought, a real tool call, a real result — until the model answers instead of asking.", bg) + f'''
  <text x="110" y="58" font-size="21" fill="{muted}">the notepad, filling up:</text>
  {out}
  <g opacity="0"><rect x="620" y="120" width="300" height="120" rx="8" fill="none" stroke="{amber}" stroke-width="3" stroke-dasharray="8 6"/>
    <text x="770" y="156" font-size="18" fill="{amber}" text-anchor="middle">every line is either</text>
    <text x="770" y="184" font-size="18" fill="{amber}" text-anchor="middle">the model thinking</text>
    <text x="770" y="212" font-size="18" fill="{amber}" text-anchor="middle">or your code acting</text>{fade(6.8,11.4)}</g>
  <text x="500" y="312" font-size="20" fill="{muted}" text-anchor="middle" opacity="0">the only natural exit: no tool asked for{fade(9.0,11.2)}</text>
</svg>'''

def runaway(ink, muted, blue, green, red, amber, bg):
    calls = "".join(f'<g opacity="0"><rect x="{100+i*80}" y="110" width="66" height="40" rx="5" fill="{red}" '
                    f'fill-opacity="0.2" stroke="{red}" stroke-width="2.5"/><text x="{133+i*80}" y="136" '
                    f'font-size="13" fill="{red}" text-anchor="middle">same</text>{fade(0.4+i*0.5,6.0)}</g>'
                    for i in range(9))
    return head(1000, 320, "Nine identical tool calls run the budget down; repeat detection returns a corrective observation and the loop recovers.", bg) + f'''
  <text x="60" y="70" font-size="20" fill="{red}">without a harness — the same call, nine times:</text>
  {calls}
  <g opacity="0"><text x="500" y="186" font-size="20" fill="{red}" text-anchor="middle">turn limit reached · £ spent · no answer ✗{fade(4.6,6.4)}</text></g>
  <g opacity="0"><text x="60" y="236" font-size="20" fill="{green}">with the harness:</text>
    <rect x="300" y="212" width="620" height="44" rx="7" fill="{green}" fill-opacity="0.12" stroke="{green}" stroke-width="3"/>
    <text x="610" y="240" font-size="16" fill="{ink}" text-anchor="middle">“You already called this and received the same result. Try something else.”</text>
    {fade(7.0,11.4)}</g>
  <text x="500" y="298" font-size="20" fill="{amber}" text-anchor="middle" opacity="0">the error message is the prompt — and it is what recovers the run{fade(9.0,11.2)}</text>
</svg>'''

def drawers(ink, muted, blue, green, amber, bg):
    many = "".join(f'<rect x="{70+(i%8)*38}" y="{92+(i//8)*34}" width="32" height="28" rx="3" fill="none" '
                   f'stroke="{muted}" stroke-width="2"/>' for i in range(40))
    few = "".join(f'<g opacity="0"><rect x="{600+(i%3)*90}" y="{100+(i//3)*54}" width="80" height="44" rx="5" '
                  f'fill="{green}" fill-opacity="0.14" stroke="{green}" stroke-width="3"/>'
                  f'<text x="{640+(i%3)*90}" y="{128+(i//3)*54}" font-size="12" fill="{green}" '
                  f'text-anchor="middle">{n}</text>{fade(4.0+i*0.3,11.4)}</g>'
                  for i,n in enumerate(["get_order","search","refund","notify","lookup","escalate"]))
    return head(1000, 320, "Forty unlabelled drawers slow the worker down; six clearly labelled ones do not.", bg) + f'''
  <text x="220" y="70" font-size="20" fill="{muted}" text-anchor="middle">40 unlabelled drawers</text>
  {many}
  <g opacity="0"><text x="220" y="246" font-size="19" fill="{ink}" text-anchor="middle">every task starts with a search,</text>
    <text x="220" y="272" font-size="19" fill="{ink}" text-anchor="middle">and sometimes the wrong drawer{fade(1.4,11.4)}</text></g>
  <text x="730" y="70" font-size="20" fill="{green}" text-anchor="middle" opacity="0">6 labelled ones{fade(3.8,11.4)}</text>
  {few}
  <g opacity="0"><text x="730" y="246" font-size="19" fill="{green}" text-anchor="middle">quick, and correct ✓{fade(6.4,11.4)}</text></g>
  <text x="500" y="304" font-size="20" fill="{amber}" text-anchor="middle" opacity="0">removing tools often makes an agent better{fade(8.6,11.2)}</text>
</svg>'''

def three_ways(ink, muted, blue, green, amber, bg):
    cols = [("your harness", blue, 0.5, ["80 lines", "you know it all", "debug: minutes"]),
            ("framework A", green, 2.4, ["12 lines", "graph + resume", "debug: ?"]),
            ("framework B", amber, 4.3, ["20 lines", "roles + tasks", "debug: ?"])]
    out = ""
    for i,(name,col,t0,rows) in enumerate(cols):
        x = 90 + i*300
        out += (f'<g opacity="0"><rect x="{x}" y="90" width="250" height="150" rx="8" fill="{col}" '
                f'fill-opacity="0.10" stroke="{col}" stroke-width="3.5"/>'
                f'<text x="{x+125}" y="122" font-size="19" fill="{col}" text-anchor="middle">{name}</text>'
                + "".join(f'<text x="{x+125}" y="{158+j*28}" font-size="16" fill="{ink}" '
                          f'text-anchor="middle">{r}</text>' for j,r in enumerate(rows))
                + f'{fade(t0,11.4)}</g>')
    return head(1000, 320, "The same task built three ways, compared on lines of code, capability and the column that decides: time to debug the first failure.", bg) + f'''
  <text x="500" y="58" font-size="21" fill="{muted}" text-anchor="middle">one real task, built three ways — everything else held fixed</text>
  {out}
  <g opacity="0"><rect x="90" y="256" width="850" height="46" rx="7" fill="{amber}" fill-opacity="0.10" stroke="{amber}" stroke-width="3"/>
    <text x="515" y="285" font-size="19" fill="{amber}" text-anchor="middle">now break a tool in each — the one that decides is time to debug the first failure</text>
    {fade(6.6,11.4)}</g>
</svg>'''

def two_runs(ink, muted, blue, green, red, amber, bg):
    a = "".join(f'<rect x="{120+i*60}" y="100" width="46" height="34" rx="4" fill="{green}" fill-opacity="0.2" '
                f'stroke="{green}" stroke-width="2.5"/>' for i in range(1))
    b = "".join(f'<rect x="{120+i*60}" y="196" width="46" height="34" rx="4" fill="{red}" fill-opacity="0.18" '
                f'stroke="{red}" stroke-width="2.5"/>' for i in range(9))
    return head(1000, 320, "Two runs reach the same correct answer: one used a single lookup, the other nine calls and a blocked destructive attempt.", bg) + f'''
  <text x="60" y="76" font-size="20" fill="{green}">run A — one lookup:</text>
  {a}
  <g opacity="0"><text x="700" y="128" font-size="20" fill="{green}">answer: correct ✓{fade(1.0,11.4)}</text></g>
  <text x="60" y="176" font-size="20" fill="{red}" opacity="0">run B — nine calls, one blocked refund:{fade(3.0,11.4)}</text>
  <g opacity="0">{b}<text x="700" y="224" font-size="20" fill="{green}">answer: correct ✓{fade(3.4,11.4)}</text></g>
  <g opacity="0"><text x="500" y="278" font-size="21" fill="{amber}" text-anchor="middle">score only the answer and these are identical{fade(6.4,11.4)}</text></g>
  <text x="500" y="308" font-size="20" fill="{muted}" text-anchor="middle" opacity="0">so score the path: tools, turns, repeats, unsafe attempts{fade(8.8,11.2)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",red="#e03131",amber="#f08c00",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",red="#ff8787",amber="#ffb84d",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
JOBS = [
 ("curriculum/p4/week-29/2-the-techniques-that-work.mdx", "ANIM:W29M2", examples,
  "Examples, live: three worked cases, and the third — a shouty letter that is not urgent — teaches what no instruction says cleanly. It repeats."),
 ("curriculum/p4/week-29/4-context-engineering.mdx", "ANIM:W29M4", window,
  "The window, live: system prompt, tools, passages and history fill the desk until the reserved answer space is threatened — and nothing tells you what fell out. It repeats."),
 ("curriculum/p4/week-29/5-prompts-are-code.mdx", "ANIM:W29M5", versions,
  "Versions, live: the envelope recipe has no history; two versioned prompts are scored on the same twenty cases, and rollback takes a minute. It repeats."),
 ("curriculum/p4/week-29/6-when-it-ignores-you.mdx", "ANIM:W29M6", buried,
  "Burial, live: the same rule obeyed near the end of a short input and ignored when buried among passages and history. It repeats — watch both."),
 ("curriculum/p4/week-31/2-react-built-from-scratch.mdx", "ANIM:W31M2", react_trace,
  "The transcript, live: thought, real call, real result, repeated — until the model answers instead of asking. It repeats — watch it twice."),
 ("curriculum/p4/week-31/3-the-harness.mdx", "ANIM:W31M3", runaway,
  "The harness, live: nine identical calls burn the budget with no answer; repeat detection returns a corrective observation and the run recovers. It repeats."),
 ("curriculum/p4/week-31/4-tool-and-context-design.mdx", "ANIM:W31M4", drawers,
  "Drawers, live: forty unlabelled ones make every task a search; six labelled ones do not. It repeats — watch both."),
 ("curriculum/p4/week-31/5-the-frameworks-compared.mdx", "ANIM:W31M5", three_ways,
  "The bake-off, live: the same task built three ways with everything else fixed, then broken on purpose — because time to debug decides. It repeats."),
 ("curriculum/p4/week-31/6-agent-evaluation-and-failure.mdx", "ANIM:W31M6", two_runs,
  "Two runs, live: both reach the correct answer, one in a single lookup and one in nine calls plus a blocked refund. It repeats — watch both."),
]
for slug, anchor, fn, caption in JOBS:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
