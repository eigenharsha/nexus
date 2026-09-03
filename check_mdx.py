#!/usr/bin/env python3
"""Sanity-check authored MDX pages for Mintlify build hazards.

Checks, outside fenced code blocks and inline code spans:
  - raw '{' or '}'   (MDX expression start -> build error)
  - raw '<' not followed by a known component/HTML tag or '/'
  - empty inline code spans ``
Also checks:
  - the AUTHORED marker is present
  - fenced code blocks are balanced
  - JSX component tags are balanced
"""
import re
import sys
import pathlib
from collections import Counter

COMPONENTS = {
    "Note", "Warning", "Tip", "Info", "Check", "Card", "CardGroup", "Accordion",
    "AccordionGroup", "Steps", "Step", "Tabs", "Tab", "Frame", "CodeGroup",
    "Expandable", "ParamField", "ResponseField", "Columns", "img", "br", "sub", "sup",
}

TAG_RE = re.compile(r"<(/?)([A-Za-z][A-Za-z0-9]*)")


def strip_inline_code(line: str) -> str:
    # remove ``...`` and `...` spans
    line = re.sub(r"``[^`]*``", "", line)
    line = re.sub(r"`[^`]*`", "", line)
    return line


def check(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []
    if "{/* AUTHORED */}" not in text:
        problems.append("missing AUTHORED marker")

    lines = text.split("\n")
    in_fence = False
    fence_marker = ""
    in_comment = False
    stack: list[tuple[str, int]] = []
    tag_counts: Counter = Counter()

    for n, raw in enumerate(lines, 1):
        stripped = raw.strip()
        m = re.match(r"^(`{3,}|~{3,})", stripped)
        if m:
            if not in_fence:
                in_fence, fence_marker = True, m.group(1)[0] * 3
            elif stripped.startswith(fence_marker):
                in_fence = False
            continue
        if in_fence:
            continue

        # MDX comment blocks {/* ... */}
        if not in_comment and stripped.startswith("{/*") and "*/}" not in stripped:
            in_comment = True
            continue
        if in_comment:
            if "*/}" in stripped:
                in_comment = False
            continue
        if stripped.startswith("{/*") and stripped.endswith("*/}"):
            continue

        line = strip_inline_code(raw)
        # JSX attribute expressions like cols={2} are valid; drop them
        line = re.sub(r"=\{[^{}]*\}", "=", line)

        if "``" in raw:
            problems.append(f"L{n}: empty inline code span")

        for ch in "{}":
            if ch in line:
                problems.append(f"L{n}: raw '{ch}' in prose -> {raw.strip()[:90]}")
                break

        for slash, tag in TAG_RE.findall(line):
            if tag not in COMPONENTS:
                problems.append(f"L{n}: raw '<{tag}' in prose -> {raw.strip()[:90]}")
                continue
            tag_counts[("close" if slash else "open", tag)] += 1

        # bare '<' followed by space/digit in prose
        for mm in re.finditer(r"<(?![A-Za-z/!])", line):
            problems.append(f"L{n}: bare '<' in prose -> {raw.strip()[:90]}")
            break

    if in_fence:
        problems.append("unbalanced code fence")

    # self-closing tags counted as open; subtract them
    selfclosed = Counter()
    for m in re.finditer(r"<([A-Za-z][A-Za-z0-9]*)[^>]*?/>", text):
        selfclosed[m.group(1)] += 1
    for tag in COMPONENTS:
        opens = tag_counts[("open", tag)] - selfclosed[tag]
        closes = tag_counts[("close", tag)]
        if opens != closes:
            problems.append(f"tag <{tag}> unbalanced: {opens} open vs {closes} close")

    return problems


def main() -> int:
    targets = sys.argv[1:]
    paths: list[pathlib.Path] = []
    for t in targets:
        p = pathlib.Path(t)
        paths.extend(sorted(p.rglob("*.mdx")) if p.is_dir() else [p])
    bad = 0
    for p in paths:
        probs = check(p)
        words = len(re.sub(r"```.*?```", "", p.read_text(), flags=re.S).split())
        if probs:
            bad += 1
            print(f"\n=== {p}  ({words} words ex-code)")
            for q in probs:
                print("   ", q)
        else:
            print(f"ok  {p}  ({words} words ex-code)")
    print(f"\n{len(paths)} files, {bad} with problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
