#!/usr/bin/env python3
"""Apply authored story content to module pages (doctrine sections 10.x).

A week's content lives in tools/stories/<week>.py as PAGES = {slug: {...}} with
keys: glimpse, story, answer, dangler, build_open, edge_open (all optional).
This module inserts each in its doctrinal place, idempotently.

    python3 tools/story_apply.py week-28
"""
import importlib.util, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GI = "**New to all of this?** This layer is yours. No assumptions — every term is discovered the moment you need it."
BI = "**You ship code for a living?** This layer is yours — trade-offs, real tools, real versions."
EI = "**For anyone who has shipped this and been burned.** Internals, scale, numbers."
MARK = "{/* STORY */}"

def apply(slug, d):
    p = ROOT / slug
    t = p.read_text()
    if MARK in t:
        print("  already storied, skipping:", slug.split("/")[-1]); return False
    if d.get("glimpse") and "</Note>\n" in t:
        t = t.replace("</Note>\n", "</Note>\n\n" + d["glimpse"] + "\n", 1)
    if d.get("story"):
        if GI in t:                      # doctrine pages: after the layer intro line
            i = t.index(GI) + len(GI); nl = t.index("\n", i) + 1
        else:                            # older pages: straight after the Ground tab opens
            m = re.search(r'<Tab title="[^"]*Layer 1[^"]*">\n', t)
            nl = m.end() if m else None
        if nl:
            t = t[:nl] + "\n" + MARK + "\n" + d["story"] + t[nl:]
    if d.get("answer") and '<Accordion title="Checkpoint' in t:
        ck = t.index('<Accordion title="Checkpoint')
        t = t[:ck] + ('<Check>\n    **The answer to the opening question, plainly.** '
                      + d["answer"] + '\n    </Check>\n\n    ') + t[ck:]
    if d.get("dangler") and "{/* CHAIN:BEGIN */}" in t:
        cb = t.index("{/* CHAIN:BEGIN */}")
        t = t[:cb] + d["dangler"] + "\n" + t[cb:]
    for key, intro in (("build_open", BI), ("edge_open", EI)):
        if d.get(key) and intro in t:
            i = t.index(intro) + len(intro); nl = t.index("\n", i) + 1
            t = t[:nl] + f'\n    {d[key]}\n' + t[nl:]
    p.write_text(t)
    print("  storied:", slug.split("/")[-1])
    return True

def main(week):
    spec = ROOT / "tools" / "stories" / f"{week}.py"
    s = importlib.util.spec_from_file_location("wk", spec)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    n = sum(apply(slug, d) for slug, d in m.PAGES.items())
    print(f"{week}: {n} pages storied")

if __name__ == "__main__":
    main(sys.argv[1])
