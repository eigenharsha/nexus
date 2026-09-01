#!/usr/bin/env python3
"""Idempotent link repair for generated/authored curriculum pages.

Mintlify serves a page at its docs.json path. A week directory is not itself a
page, so /curriculum/pN/week-NN 404s -- it must point at .../index.
Safe to run repeatedly; reports what it changed.
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent
PAT = re.compile(r"(/curriculum/p\d/week-\d{2})(?![/\w-])")

changed = 0
for path in SITE.rglob("*.mdx"):
    src = path.read_text()
    out = PAT.sub(r"\1/index", src)
    if out != src:
        path.write_text(out)
        changed += 1
        print(f"fixed {path.relative_to(SITE)}")
print(f"\n{changed} file(s) repaired")
