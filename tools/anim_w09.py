#!/usr/bin/env python3
"""Week-9 animations: a gate's truth table filling in (m1), a carry rippling
along an adder (m2), control bits selecting an ALU operation (m3), feedback
holding a bit on the clock (m4), and fetch-decode-execute (m5).
All content checked against the module pages: 16-bit Hack ALU, six control
bits, zr/ng flags, two's complement range -32768..+32767."""
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

def m1(ink, muted, blue, green, amber, bg):
    rows = [("0","0","0",1.2),("0","1","0",2.4),("1","0","0",3.6),("1","1","1",4.8)]
    out = ""
    for i,(a,b,y,t0) in enumerate(rows):
        yy = 130 + i*40
        col = green if y == "1" else muted
        out += (f'<g opacity="0"><text x="620" y="{yy}" font-size="20" fill="{ink}">{a}</text>'
                f'<text x="700" y="{yy}" font-size="20" fill="{ink}">{b}</text>'
                f'<text x="800" y="{yy}" font-size="20" fill="{col}">{y}</text>{fade(t0,11.4)}</g>')
    return head(1000, 340, "Two switches feed one bulb through an AND gate; the truth table fills in row by row, and the bulb lights only in the last case.", bg) + f'''
  <text x="240" y="56" font-size="22" fill="{muted}" text-anchor="middle">two switches, one bulb (AND)</text>
  <g><rect x="110" y="90" width="90" height="46" rx="6" fill="none" stroke="{ink}" stroke-width="3"/>
     <text x="155" y="120" font-size="18" fill="{ink}" text-anchor="middle">switch a</text>
     <rect x="110" y="160" width="90" height="46" rx="6" fill="none" stroke="{ink}" stroke-width="3"/>
     <text x="155" y="190" font-size="18" fill="{ink}" text-anchor="middle">switch b</text>
     <path d="M204 113 L260 130 M204 183 L260 166" stroke="{muted}" stroke-width="3"/>
     <rect x="264" y="120" width="90" height="56" rx="8" fill="{blue}" fill-opacity="0.12" stroke="{blue}" stroke-width="3.5"/>
     <text x="309" y="155" font-size="19" fill="{blue}" text-anchor="middle">AND</text>
     <path d="M358 148 L410 148" stroke="{muted}" stroke-width="3"/>
  </g>
  <g opacity="0"><circle cx="440" cy="148" r="24" fill="{green}" fill-opacity="0.35" stroke="{green}" stroke-width="3.5"/>
    <text x="440" y="200" font-size="18" fill="{green}" text-anchor="middle">lit</text>{fade(5.0,11.4)}</g>
  <circle cx="440" cy="148" r="24" fill="none" stroke="{muted}" stroke-width="3"/>
  <text x="620" y="96" font-size="19" fill="{muted}">a</text>
  <text x="700" y="96" font-size="19" fill="{muted}">b</text>
  <text x="800" y="96" font-size="19" fill="{muted}">out</text>
  <line x1="600" y1="108" x2="840" y2="108" stroke="{muted}" stroke-width="2"/>
  {out}
  <text x="500" y="316" font-size="22" fill="{amber}" text-anchor="middle" opacity="0">four rows describe this gate completely — and forever{fade(6.4,11.2)}</text>
</svg>'''

def m2(ink, muted, blue, green, amber, bg):
    cells = ""
    for i in range(6):
        x = 120 + i*130
        cells += (f'<rect x="{x}" y="120" width="100" height="70" rx="7" fill="{blue}" fill-opacity="0.10" '
                  f'stroke="{blue}" stroke-width="3"/><text x="{x+50}" y="162" font-size="16" fill="{blue}" '
                  f'text-anchor="middle">+ bit {6-i}</text>')
    carries = ""
    for i in range(5):
        x = 120 + (5-i)*130
        carries += (f'<g opacity="0"><path d="M{x} 155 L{x-26} 155" stroke="{amber}" stroke-width="4" '
                    f'stroke-dasharray="8 6"/><text x="{x-13}" y="136" font-size="15" fill="{amber}" '
                    f'text-anchor="middle">1</text>{fade(1.6+i*1.3, 11.4)}</g>')
    return head(1000, 320, "One-bit adders chained side by side: the carry from each ripples into its left-hand neighbour, like carrying when adding by hand.", bg) + f'''
  <text x="500" y="60" font-size="22" fill="{muted}" text-anchor="middle">1 + 1 = 10 — a digit that stays, and a carry that moves left</text>
  {cells}{carries}
  <text x="500" y="238" font-size="20" fill="{muted}" text-anchor="middle" opacity="0">chain sixteen of these and you can add any two 16-bit numbers{fade(7.6,11.4)}</text>
  <text x="500" y="286" font-size="22" fill="{amber}" text-anchor="middle" opacity="0">and subtraction is free: a − b = a + NOT(b) + 1{fade(9.0,11.2)}</text>
</svg>'''

def m3(ink, muted, blue, green, amber, bg):
    ops = [("000000","x + y",1.0),("010011","x − y",3.6),("000000","x AND y",6.2),("111010","−1",8.6)]
    out = ""
    for i,(bits,res,t0) in enumerate(ops):
        out += (f'<g opacity="0"><text x="500" y="118" font-size="26" fill="{amber}" text-anchor="middle">'
                f'{" ".join(bits)}</text><text x="500" y="238" font-size="30" fill="{green}" text-anchor="middle">'
                f'{res}</text>{fade(t0, t0+2.2)}</g>')
    return head(1000, 320, "The same box computes different operations as its six control bits change, with two status outputs reporting zero and negative.", bg) + f'''
  <text x="500" y="62" font-size="21" fill="{muted}" text-anchor="middle">six control wires — flip them, and the same hardware does something else</text>
  <rect x="330" y="140" width="340" height="80" rx="10" fill="{blue}" fill-opacity="0.10" stroke="{blue}" stroke-width="3.5"/>
  <text x="380" y="188" font-size="19" fill="{blue}">ALU</text>
  <text x="140" y="172" font-size="19" fill="{ink}">x[16]</text>
  <text x="140" y="206" font-size="19" fill="{ink}">y[16]</text>
  <path d="M196 166 L326 172 M196 200 L326 194" stroke="{muted}" stroke-width="3"/>
  {out}
  <g opacity="0"><text x="800" y="172" font-size="19" fill="{amber}">zr — the result is zero</text>
    <text x="800" y="204" font-size="19" fill="{amber}">ng — the result is negative</text>
    <text x="800" y="252" font-size="18" fill="{muted}">where every if and every</text>
    <text x="800" y="276" font-size="18" fill="{muted}">loop eventually comes from</text>{fade(4.4,11.4)}</g>
</svg>'''

def m4(ink, muted, blue, green, amber, bg):
    ticks = ""
    for i in range(6):
        x = 150 + i*120
        ticks += (f'<path d="M{x} 250 L{x} 210 L{x+60} 210 L{x+60} 250 L{x+120} 250" fill="none" '
                  f'stroke="{muted}" stroke-width="3"/>')
    return head(1000, 330, "An output wired back to an input holds a value in place, and the clock decides the only moments at which it may change.", bg) + f'''
  <g>
    <rect x="330" y="80" width="220" height="80" rx="9" fill="{blue}" fill-opacity="0.10" stroke="{blue}" stroke-width="3.5"/>
    <text x="440" y="128" font-size="20" fill="{blue}" text-anchor="middle">one-bit memory</text>
    <path d="M554 120 L620 120 L620 186 L300 186 L300 120 L326 120" fill="none" stroke="{amber}" stroke-width="4" stroke-dasharray="10 8">
      <animate attributeName="stroke-dashoffset" from="36" to="0" dur="1.4s" repeatCount="indefinite"/></path>
    <text x="460" y="212" font-size="18" fill="{amber}" text-anchor="middle">the output feeds itself — that is the memory</text>
  </g>
  <text x="80" y="230" font-size="19" fill="{muted}">clock</text>
  {ticks}
  <g opacity="0"><text x="500" y="300" font-size="21" fill="{green}" text-anchor="middle">the value may change only on the tick — between ticks, everything holds still{fade(2.4,11.4)}</text></g>
  <g opacity="0"><text x="760" y="118" font-size="19" fill="{muted}">16 of these = a register</text>
    <text x="760" y="146" font-size="19" fill="{muted}">many registers = RAM</text>{fade(6.4,11.4)}</g>
</svg>'''

def m5(ink, muted, blue, green, amber, bg):
    steps = [("fetch", "read the instruction at the program counter", 0.6, blue),
             ("decode", "work out what its bits mean", 3.0, amber),
             ("execute", "do it with the ALU and registers", 5.4, green)]
    out = ""
    for i,(name, desc, t0, col) in enumerate(steps):
        y = 110 + i*66
        out += (f'<g opacity="0"><rect x="120" y="{y}" width="180" height="50" rx="7" fill="{col}" fill-opacity="0.14" '
                f'stroke="{col}" stroke-width="3.5"/><text x="210" y="{y+32}" font-size="19" fill="{col}" '
                f'text-anchor="middle">{name}</text><text x="330" y="{y+32}" font-size="18" fill="{muted}">{desc}</text>'
                f'{fade(t0,11.4)}</g>')
    return head(1000, 330, "Memory holds numbers; some of them are instructions. The machine fetches, decodes and executes, then moves the program counter on, forever.", bg) + f'''
  <text x="60" y="62" font-size="21" fill="{muted}">memory holds numbers — and some of those numbers are instructions</text>
  {out}
  <g opacity="0"><path d="M210 292 Q 520 330 830 240" fill="none" stroke="{amber}" stroke-width="4" stroke-dasharray="11 9">
      <animate attributeName="stroke-dashoffset" from="40" to="0" dur="1.4s" repeatCount="indefinite"/></path>
    <text x="520" y="316" font-size="20" fill="{amber}" text-anchor="middle">…then move the counter on, and repeat — billions of times a second</text>{fade(7.6,11.4)}</g>
  <g opacity="0"><text x="820" y="120" font-size="19" fill="{muted}" text-anchor="middle">your Python becomes</text>
    <text x="820" y="146" font-size="19" fill="{muted}" text-anchor="middle">instructions, which become</text>
    <text x="820" y="172" font-size="19" fill="{muted}" text-anchor="middle">control bits, which become</text>
    <text x="820" y="198" font-size="19" fill="{green}" text-anchor="middle">the switches you wired</text>{fade(8.6,11.4)}</g>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",amber="#f08c00",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",amber="#ffb84d",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
W = "curriculum/p2/week-09/"
for slug, anchor, fn, caption in [
 (W+"1-boolean-algebra-logic-gates.mdx", "ANIM:W9M1", m1,
  "A gate, live: two switches feed one bulb, and the truth table fills in row by row — the bulb lights only when both are on. It repeats — watch it twice."),
 (W+"2-combinational-arithmetic.mdx", "ANIM:W9M2", m2,
  "The carry, live: one-bit adders chained side by side pass the carry left, exactly as you do adding by hand. It repeats — watch it ripple."),
 (W+"3-the-alu.mdx", "ANIM:W9M3", m3,
  "The ALU, live: the same box computes x+y, x−y, x AND y or −1 as its six control bits change, with zr and ng reporting on the result. It repeats."),
 (W+"4-sequential-logic-memory-clock.mdx", "ANIM:W9M4", m4,
  "Memory, live: an output wired back into its own input holds a value, and the clock decides the only moments it may change. It loops continuously."),
 (W+"5-from-cpu-to-program.mdx", "ANIM:W9M5", m5,
  "The cycle, live: fetch the instruction, decode what its bits mean, execute it — then move the counter on and repeat. It repeats — watch it twice."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
