#!/usr/bin/env python3
"""Lint the Nexus MDX pages for the rules in AGENT-BRIEF.md."""
import re, sys, pathlib

KNOWN = {"Note","Warning","Tip","Info","Check","Card","CardGroup","Accordion","AccordionGroup",
         "Steps","Step","Tabs","Tab","Frame","CodeGroup","Expandable","ParamField",
         "ResponseField","Columns","img","br","hr"}
SELF_CLOSING = {"img","br","hr"}

def strip_code(text):
    """Remove fenced code blocks and inline code, returning (prose, n_code_words)."""
    code_words = 0
    def _f(m):
        nonlocal code_words
        code_words += len(m.group(0).split())
        return "\n"
    prose = re.sub(r"```.*?```", _f, text, flags=re.S)
    prose = re.sub(r"`[^`\n]*`", "", prose)
    return prose, code_words

def check(path):
    errs, warns = [], []
    raw = path.read_text()
    if not raw.startswith("---"):
        errs.append("no frontmatter")
        return errs, warns, 0
    fm_end = raw.index("\n---", 3) + 4
    fm, body = raw[:fm_end], raw[fm_end:]

    if "{/* AUTHORED */}" not in body:
        errs.append("missing AUTHORED marker")

    prose, code_words = strip_code(body)
    # remove JSX comments {/* ... */}
    prose_nc = re.sub(r"\{/\*.*?\*/\}", "", prose, flags=re.S)
    # remove JSX tags entirely (props may legally contain braces / <)
    prose_nt = re.sub(r"<[A-Za-z/][^>]*>", "", prose_nc)

    for i, line in enumerate(prose_nt.splitlines(), 1):
        if "{" in line or "}" in line:
            errs.append(f"raw brace in prose: {line.strip()[:90]}")
        for m in re.finditer(r"<", line):
            errs.append(f"raw < in prose: {line.strip()[:90]}")
            break

    # tag balance
    stack = []
    for m in re.finditer(r"<(/?)([A-Za-z][A-Za-z0-9]*)([^>]*?)(/?)>", prose_nc):
        closing, name, attrs, selfclose = m.groups()
        if name not in KNOWN:
            continue
        if selfclose or name in SELF_CLOSING:
            continue
        if closing:
            if not stack or stack[-1] != name:
                errs.append(f"unbalanced close </{name}> (open: {stack[-3:]})")
            else:
                stack.pop()
        else:
            stack.append(name)
    if stack:
        errs.append(f"unclosed tags: {stack}")

    # diagram spec
    if "/curriculum/" in str(path) and path.stem not in ("index","lab"):
        if "DIAGRAM-SPEC" not in body:
            errs.append("missing DIAGRAM-SPEC block")
        for key in ("one-sentence-goal:","numbers-to-write-in:","alt:","tier:"):
            if key not in body:
                errs.append(f"DIAGRAM-SPEC missing {key}")

    prose_words = len(prose_nt.split())
    return errs, warns, prose_words

if __name__ == "__main__":
    root = pathlib.Path(sys.argv[1] if len(sys.argv)>1 else ".")
    files = sorted(root.rglob("*.mdx")) if root.is_dir() else [root]
    total = 0; bad = 0
    for f in files:
        if "{/* AUTHORED */}" not in f.read_text():
            continue
        e, w, pw = check(f)
        total += pw
        status = "OK  " if not e else "FAIL"
        if e: bad += 1
        print(f"{status} {pw:>5}w  {f}")
        for x in e[:6]: print(f"       ! {x}")
    print(f"\nauthored prose words: {total}   files failing: {bad}")
