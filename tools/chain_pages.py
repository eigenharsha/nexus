#!/usr/bin/env python3
"""Apply the doctrine's structural laws to every three-layer module page.

Mechanical, idempotent, and factual: the depth invitations name each page's
REAL Build and Edge section headings, and the "next module" link comes from
docs.json's own reading order. Authored prose (story cold opens, answer beats)
is written per page by hand — this tool never invents it.

What it does per page:
  - page order: drop the "Where this sits" / "Why you should care" blocks from
    the top; move "The mental model" (and its diagram) to the bottom, beside
    the whiteboard, where it summarises instead of spoiling
  - persona lines: speak to the reader, not about internal personas
  - Ground ends with a depth invitation (what Build and Edge hold here) plus a
    pointer to this page's Assessment questions
  - Build ends with a hand-off naming what Edge holds
  - Edge ends with "The floor of this topic": Assessment, then the next module

    python3 tools/chain_pages.py [--dry]
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRY = "--dry" in sys.argv
B, E = "{/* CHAIN:BEGIN */}", "{/* CHAIN:END */}"

docs = json.loads((ROOT / "docs.json").read_text())
order, titles = [], {}
def walk(n):
    if isinstance(n, dict):
        if n.get("hidden"): return
        [walk(n[k]) for k in ("groups", "pages", "tabs") if k in n]
    elif isinstance(n, list):
        for x in n: walk(x)
    elif isinstance(n, str) and n not in order:
        order.append(n)
walk(docs["navigation"])
oidx = {s: i for i, s in enumerate(order)}

def page_title(slug):
    p = ROOT / (slug + ".mdx")
    if p.exists():
        m = re.search(r'^title:\s*"?(.*?)"?\s*$', p.read_text(), re.M)
        if m: return m.group(1)
    return slug.split("/")[-1].replace("-", " ")

def next_slug(slug):
    i = oidx.get(slug)
    if i is None: return None
    for s in order[i+1:]:
        if (ROOT / (s + ".mdx")).exists():
            return s
    return None

def tab_spans(t):
    """(name, start_of_body, end_index) for each layer tab present."""
    out = []
    for m in re.finditer(r'<Tab title="[^"]*Layer (\d)[^"]*">', t):
        out.append((int(m.group(1)), m.end()))
    spans = []
    for k, (n, start) in enumerate(out):
        nxt = out[k+1][1] if k+1 < len(out) else len(t)
        close = t.rfind("</Tab>", start, nxt)
        if close == -1: return []
        spans.append((n, start, close))
    return spans

def headings(seg, limit=3):
    hs = [h.strip().rstrip(".") for h in re.findall(r"^\s*###\s+(.+)$", seg, re.M)]
    hs = [h for h in hs if not h.lower().startswith(("answers", "checkpoint"))]
    return hs[:limit]

def anchor(h):
    """Mintlify's heading id: lowercase, punctuation dropped, spaces to hyphens.
    Linking to a heading inside an inactive tab switches to that tab."""
    s = re.sub(r"[^a-z0-9 -]", "", h.lower())
    return re.sub(r"\s+", "-", s.strip())

def phrase(hs, link=True):
    """Each named section becomes a link straight into its layer."""
    if not hs: return None
    out = []
    for h in hs:
        label = h[0].lower() + h[1:] if not h[:2].isupper() else h
        out.append(f"[{label}](#{anchor(h)})" if link else label)
    return " · ".join(out)

def strip_block(t):
    return re.sub(re.escape(B) + r".*?" + re.escape(E), "", t, flags=re.S)

def restructure(t):
    """Top matter off the page; mental model down to the whiteboard."""
    for head in ("## Where this sits", "## Why you should care"):
        m = re.search(re.escape(head) + r"\n(.*?)(?=\n## |\n<Tabs>)", t, re.S)
        if m: t = t[:m.start()] + t[m.end():]
    m = re.search(r"## The mental model\n(.*?)(?=\n<Tabs>)", t, re.S)
    if m and "## The whiteboard" in t:
        body = m.group(1).strip()
        t = t[:m.start()] + t[m.end():]
        t = t.replace("## The whiteboard",
                      "## The whole idea on one whiteboard\n\n" + body + "\n\n## The whiteboard", 1)
    return t

def personas(t):
    def swap(pat, lead, drop, s):
        def f(m):
            tail = m.group(1).strip()
            for d in drop:
                if tail.startswith(d): tail = tail[len(d):].strip()
            return lead + ((" " + tail) if tail else "")
        return re.sub(pat, f, s)
    t = swap(r"\*\*For Aarav \(student\)\.\*\*([^\n]*)",
             "**New to all of this?** This layer is yours. No assumptions — every term is discovered the moment you need it.",
             ["No assumptions. Every term is defined where it first appears.",
              "No assumptions. Every term defined where it appears.",
              "No assumptions. Every term is discovered the moment you need it."], t)
    t = swap(r"\*\*For Meera \(working professional\)\.\*\*([^\n]*)",
             "**You ship code for a living?** This layer is yours — trade-offs, real tools, real versions.",
             ["Trade-offs, real tools, real versions."], t)
    return t

changed = skipped = 0
PAGES = sorted(ROOT.glob("curriculum/p*/week-*/[1-9]-*.mdx"))
only = [a for a in sys.argv[1:] if not a.startswith("--")]
if only:
    PAGES = [q for q in PAGES if any(o in str(q) for o in only)]
for p in PAGES:
    slug = str(p.relative_to(ROOT))[:-4]
    raw = p.read_text()
    t = strip_block(raw)
    spans = tab_spans(t)
    if len({n for n, _, _ in spans}) < 3:
        skipped += 1
        continue
    hand_authored = "The floor of this topic" in t
    t = personas(restructure(t))
    spans = tab_spans(t)
    segs = {n: t[s:e] for n, s, e in spans}
    b_hs, e_hs = headings(segs.get(2, "")), headings(segs.get(3, ""))
    build_p = phrase(b_hs) or "the real tools, the trade-offs and a working reference implementation"
    edge_p  = phrase(e_hs) or "the internals, the numbers at scale and the production failure modes"
    # the layer name itself links to that layer's first section
    build_link = f"[🔵 **Build**](#{anchor(b_hs[0])})" if b_hs else "🔵 **Build**"
    edge_link  = f"[🟣 **Edge**](#{anchor(e_hs[0])})" if e_hs else "🟣 **Edge**"
    has_assess = "## Assessment" in t
    ask = ("\n    - 🎯 **Prove it** — the concept, coding and interview questions this chapter"
           "\n      produces are waiting in [Assessment](#assessment) at the bottom of this page." if has_assess else "")
    nxt = next_slug(slug)
    nxt_line = (f"carry on to [{page_title(nxt)}](/{nxt}), where the story continues at every depth."
                if nxt else "carry the thread into the next module.")

    ground = (f"\n{B}\n    <Info>\n    **You do not have to stop here.** This chapter goes two levels deeper — every"
              f"\n    link below jumps straight there:\n\n    - {build_link} — {build_p}.\n    - {edge_link} — {edge_p}.{ask}\n    </Info>\n{E}\n")
    build  = (f"\n{B}\n    <Info>\n    **One level further down.** {edge_link} holds {edge_p} — and the senior"
              f"\n    interview question in [Assessment](#assessment) assumes you have read it.\n    </Info>\n{E}\n")
    edge   = (f"\n{B}\n    ### The floor of this topic\n\n    You have read as deep as this course goes here — the story, the"
              f"\n    machinery, and the scars. Two ways out: prove it against the senior questions in"
              f"\n    [Assessment](#assessment) below, or {nxt_line}\n{E}\n")

    # insert bottom-up so earlier offsets stay valid
    for n, block in (() if hand_authored else ((3, edge), (2, build), (1, ground))):
        sp = [s for s in tab_spans(t) if s[0] == n]
        if not sp: continue
        _, _, close = sp[0]
        t = t[:close] + block + t[close:]

    if t != raw:
        changed += 1
        if not DRY: p.write_text(t)

print(f"{'would change' if DRY else 'chained'}: {changed} pages · skipped (not three-layer): {skipped}")
