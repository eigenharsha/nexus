#!/usr/bin/env python3
"""Week-10 animations: headers wrapping and unwrapping (m1), the handshake and
a retransmission (m2), the socket lifecycle (m3), framing a message (m4), and
the public-key handshake (m5). Content checked against the module pages."""
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
    wraps = [("your message", 0, green, 0.4), ("app header", 1, amber, 1.6),
             ("TCP header", 2, blue, 2.8), ("IP header", 3, muted, 4.0)]
    out = ""
    for lab, i, col, t0 in wraps:
        w, h = 200 + i*90, 70 + i*36
        x, y = 300 - i*45, 130 - i*18
        out += (f'<g opacity="0"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{col}" '
                f'fill-opacity="0.10" stroke="{col}" stroke-width="3"/>'
                f'<text x="{x+10}" y="{y+22}" font-size="15" fill="{col}">{lab}</text>{fade(t0,11.4)}</g>')
    return head(1000, 340, "A message is wrapped by each layer's header on the way out and unwrapped in reverse at the far end, so the app never sees the wire.", bg) + f'''
  <text x="60" y="52" font-size="21" fill="{muted}">going out — each layer adds its own wrapper:</text>
  {out}
  <text x="400" y="180" font-size="22" fill="{green}" text-anchor="middle" opacity="0">“happy birthday!”{fade(0.6,11.4)}</text>
  <g opacity="0"><path d="M640 180 L760 180" stroke="{amber}" stroke-width="4" stroke-dasharray="10 8">
      <animate attributeName="stroke-dashoffset" from="36" to="0" dur="1.3s" repeatCount="indefinite"/></path>
    <text x="700" y="158" font-size="17" fill="{amber}" text-anchor="middle">the wire</text>{fade(5.2,11.4)}</g>
  <g opacity="0"><rect x="790" y="146" width="170" height="66" rx="8" fill="{green}" fill-opacity="0.12" stroke="{green}" stroke-width="3.5"/>
    <text x="875" y="186" font-size="18" fill="{green}" text-anchor="middle">“happy birthday!”</text>
    <text x="875" y="238" font-size="17" fill="{muted}" text-anchor="middle">unwrapped in reverse</text>{fade(6.4,11.4)}</g>
  <text x="500" y="318" font-size="21" fill="{amber}" text-anchor="middle" opacity="0">each layer is deliberately ignorant of the others{fade(8.4,11.2)}</text>
</svg>'''

def m2(ink, muted, blue, green, red, amber, bg):
    def msg(y, text, t0, col, right=False):
        x1, x2 = (250, 720) if not right else (720, 250)
        return (f'<g opacity="0"><path d="M{x1} {y} L{x2} {y}" stroke="{col}" stroke-width="3.5" '
                f'stroke-dasharray="9 7"/><text x="485" y="{y-10}" font-size="17" fill="{col}" '
                f'text-anchor="middle">{text}</text>{fade(t0,11.4)}</g>')
    return head(1000, 340, "TCP's three-way handshake, then data acknowledged by sequence number, and a lost segment retransmitted after no ACK arrives.", bg) + f'''
  <text x="180" y="60" font-size="19" fill="{ink}" text-anchor="middle">sender</text>
  <text x="800" y="60" font-size="19" fill="{ink}" text-anchor="middle">receiver</text>
  <line x1="180" y1="72" x2="180" y2="300" stroke="{muted}" stroke-width="2.5"/>
  <line x1="800" y1="72" x2="800" y2="300" stroke="{muted}" stroke-width="2.5"/>
  {msg(100, "SYN — may I connect?", 0.4, blue)}
  {msg(134, "SYN-ACK — yes", 1.4, blue, right=True)}
  {msg(168, "ACK — thanks", 2.4, blue)}
  {msg(212, "bytes 1–500", 3.6, green)}
  {msg(246, "ACK: I have up to 500", 4.6, green, right=True)}
  <g opacity="0"><path d="M250 288 L560 288" stroke="{red}" stroke-width="3.5" stroke-dasharray="9 7"/>
    <path d="M548 274 L578 302 M578 274 L548 302" stroke="{red}" stroke-width="4"/>
    <text x="420" y="278" font-size="17" fill="{red}" text-anchor="middle">bytes 501–1000 — lost</text>{fade(6.0,11.4)}</g>
  <g opacity="0"><text x="880" y="290" font-size="17" fill="{amber}" text-anchor="middle">no ACK →</text>
    <text x="880" y="314" font-size="17" fill="{amber}" text-anchor="middle">send it again</text>{fade(8.4,11.4)}</g>
</svg>'''

def m3(ink, muted, blue, green, amber, bg):
    steps = [("create the socket", 0.5), ("bind — claim an address and port", 1.6),
             ("listen — open for business", 2.7), ("accept — a separate line per caller", 3.8)]
    out = ""
    for i,(lab,t0) in enumerate(steps):
        y = 96 + i*52
        out += (f'<g opacity="0"><rect x="90" y="{y}" width="380" height="40" rx="6" fill="{blue}" '
                f'fill-opacity="0.10" stroke="{blue}" stroke-width="3"/><text x="106" y="{y+27}" '
                f'font-size="17" fill="{ink}">{lab}</text>{fade(t0,11.4)}</g>')
    return head(1000, 340, "The server socket sequence — create, bind, listen, accept — and the short read, where asking for 1024 bytes returns 300.", bg) + f'''
  <text x="90" y="62" font-size="21" fill="{muted}">the server, in order:</text>
  {out}
  <g opacity="0"><text x="740" y="96" font-size="20" fill="{green}">the client is shorter:</text>
    <text x="740" y="126" font-size="18" fill="{ink}">create · connect</text>{fade(5.0,11.4)}</g>
  <g opacity="0"><rect x="560" y="176" width="380" height="110" rx="8" fill="{amber}" fill-opacity="0.08" stroke="{amber}" stroke-width="3.5"/>
    <text x="750" y="208" font-size="18" fill="{amber}" text-anchor="middle">you ask for 1,024 bytes…</text>
    <text x="750" y="240" font-size="18" fill="{amber}" text-anchor="middle">…and you get 300</text>
    <text x="750" y="272" font-size="17" fill="{muted}" text-anchor="middle">nothing failed — that is all that had arrived</text>{fade(6.6,11.4)}</g>
  <text x="300" y="318" font-size="20" fill="{amber}" opacity="0">one send ≠ one receive{fade(9.0,11.2)}</text>
</svg>'''

def m4(ink, muted, blue, green, red, amber, bg):
    return head(1000, 330, "A byte stream has no punctuation, so a message is framed either by a delimiter or, more robustly, by its length written at the front.", bg) + f'''
  <text x="60" y="52" font-size="21" fill="{muted}">what arrives is one stream of bytes:</text>
  <g opacity="0"><rect x="70" y="70" width="600" height="46" rx="6" fill="none" stroke="{ink}" stroke-width="3"/>
    <text x="370" y="100" font-size="19" fill="{ink}" text-anchor="middle">HELLOWORLDHOWAREYOU</text>
    <text x="370" y="146" font-size="19" fill="{red}" text-anchor="middle">where does one message end? ✗</text>{fade(0.4,4.8)}</g>
  <g opacity="0"><text x="60" y="196" font-size="20" fill="{green}">option 1 — a delimiter:</text>
    <rect x="330" y="172" width="340" height="40" rx="6" fill="{green}" fill-opacity="0.10" stroke="{green}" stroke-width="3"/>
    <text x="500" y="199" font-size="18" fill="{ink}" text-anchor="middle">HELLO⏎WORLD⏎</text>{fade(5.2,11.4)}</g>
  <g opacity="0"><text x="60" y="254" font-size="20" fill="{amber}">option 2 — the length first:</text>
    <rect x="330" y="230" width="340" height="40" rx="6" fill="{amber}" fill-opacity="0.12" stroke="{amber}" stroke-width="3"/>
    <text x="500" y="257" font-size="18" fill="{ink}" text-anchor="middle">[5]HELLO [5]WORLD</text>
    <text x="810" y="257" font-size="17" fill="{amber}" text-anchor="middle">read exactly 5 ✓</text>{fade(7.0,11.4)}</g>
  <text x="500" y="308" font-size="20" fill="{muted}" text-anchor="middle" opacity="0">and a heartbeat, so a dead connection stops looking like a quiet one{fade(9.0,11.2)}</text>
</svg>'''

def m5(ink, muted, blue, green, amber, bg):
    return head(1000, 330, "A public key is published openly, anyone can lock a message with it, and only the private key can unlock — then a fast shared key carries the conversation.", bg) + f'''
  <g opacity="0"><rect x="70" y="90" width="220" height="70" rx="8" fill="{green}" fill-opacity="0.10" stroke="{green}" stroke-width="3.5"/>
    <text x="180" y="132" font-size="19" fill="{green}" text-anchor="middle">public key — shouted</text>{fade(0.4,11.4)}</g>
  <g opacity="0"><rect x="70" y="180" width="220" height="70" rx="8" fill="{blue}" fill-opacity="0.10" stroke="{blue}" stroke-width="3.5"/>
    <text x="180" y="222" font-size="19" fill="{blue}" text-anchor="middle">private key — never shared</text>{fade(0.4,11.4)}</g>
  <g opacity="0"><path d="M300 125 L420 160" stroke="{amber}" stroke-width="4" stroke-dasharray="9 7"/>
    <rect x="430" y="132" width="220" height="60" rx="8" fill="none" stroke="{amber}" stroke-width="3.5"/>
    <text x="540" y="170" font-size="18" fill="{amber}" text-anchor="middle">locked with the public key</text>{fade(2.0,11.4)}</g>
  <g opacity="0"><path d="M300 215 L420 186" stroke="{blue}" stroke-width="4" stroke-dasharray="9 7"/>
    <text x="720" y="170" font-size="18" fill="{blue}">only the private key opens it ✓</text>{fade(4.0,11.4)}</g>
  <g opacity="0"><text x="500" y="248" font-size="19" fill="{muted}" text-anchor="middle">a certificate then says WHOSE public key that is —</text>
    <text x="500" y="272" font-size="19" fill="{muted}" text-anchor="middle">signed by an authority your machine already trusts</text>{fade(6.4,11.4)}</g>
  <text x="500" y="310" font-size="20" fill="{amber}" text-anchor="middle" opacity="0">slow maths once, to agree a fast key — then the real conversation{fade(8.8,11.2)}</text>
</svg>'''

def mdx_safe(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<style>(.*?)</style>", lambda m: "<style>{`"+m.group(1)+"`}</style>", s, flags=re.S).strip()
    return re.sub(r"\s*\n\s*", " ", s)
L = dict(ink="#1e1e1e",muted="#6b6b6b",blue="#1971c2",green="#2f9e44",red="#e03131",amber="#f08c00",bg="#fffdf7")
D = dict(ink="#e8e6e3",muted="#9a9791",blue="#4dabf7",green="#6cc47a",red="#ff8787",amber="#ffb84d",bg="#1a1a1a")
only = lambda d, fn: {k: v for k, v in d.items() if k in inspect.signature(fn).parameters}
W = "curriculum/p2/week-10/"
for slug, anchor, fn, caption in [
 (W+"1-the-network-stack.mdx", "ANIM:W10M1", m1,
  "Wrapping, live: each layer adds its own header on the way out, and everything is unwrapped in reverse at the far end. It repeats — watch it twice."),
 (W+"2-tcp-vs-udp.mdx", "ANIM:W10M2", m2,
  "TCP, live: the three-way handshake, then data acknowledged by byte number — and a lost segment sent again when no acknowledgement arrives. It repeats."),
 (W+"3-socket-programming.mdx", "ANIM:W10M3", m3,
  "Sockets, live: create, bind, listen, accept — and the short read, where you ask for 1,024 bytes and get 300 with nothing wrong. It repeats."),
 (W+"4-designing-an-application-protocol.mdx", "ANIM:W10M4", m4,
  "Framing, live: a byte stream has no punctuation, so you add it — a delimiter, or better, the length written at the front. It repeats — watch both."),
 (W+"5-network-security-operations-basics.mdx", "ANIM:W10M5", m5,
  "Keys, live: the public key is shouted to everyone and locks a message that only the private key can open — then a fast shared key carries the conversation. It repeats."),
]:
    light, dark = mdx_safe(fn(**only(L, fn))), mdx_safe(fn(**only(D, fn)))
    frame = (f'<Frame caption="{caption}">\n  <div className="block dark:hidden w-full">\n    {light}\n  </div>'
             f'\n  <div className="hidden dark:block w-full">\n    {dark}\n  </div>\n</Frame>')
    p = ROOT/slug; t = p.read_text()
    key = caption.split(",")[0]
    m = re.search(r'<Frame caption="' + re.escape(key) + r'.*?</Frame>', t, re.S)
    t = (t[:m.start()] + frame + t[m.end():]) if m else t.replace("{/* " + anchor + " */}", frame)
    p.write_text(t); print("  animation:", slug.split("/")[-1])
