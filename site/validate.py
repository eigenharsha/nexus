#!/usr/bin/env python3
"""
Pre-build validator for the Nexus Mintlify site.

Catches the failure modes that actually break a Mintlify build or ship a broken page:
  1. every page referenced in docs.json exists on disk
  2. every .mdx on disk is referenced by docs.json (orphans)
  3. frontmatter present, with title + description
  4. raw `{` / `}` / `<` in prose outside code fences (MDX build errors)
  5. unbalanced Mintlify component tags
  6. internal links pointing at pages that don't exist
  7. images referenced but missing from assets/
  8. content-spec compliance: three layers present, AUTHORED marker, sources section
Exit code 1 if any ERROR is found; WARNs do not fail the run.
"""
from __future__ import annotations
import json, re, sys
from collections import Counter
from pathlib import Path

SITE = Path(__file__).resolve().parent
PAIRED = ["Note", "Warning", "Tip", "Info", "Check", "Card", "CardGroup", "Accordion",
          "AccordionGroup", "Steps", "Step", "Tabs", "Tab", "Frame", "CodeGroup",
          "Expandable", "Columns", "Update"]

errors: list[str] = []
warns: list[str] = []


def strip_code(text: str) -> str:
    """Remove fenced blocks, inline code, JSX expressions and MDX comments."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    text = re.sub(r"\{/\*.*?\*/\}", "", text, flags=re.S)
    text = re.sub(r"<[A-Za-z][^>]*>", "", text)   # component tags & their props
    text = re.sub(r"</[A-Za-z][^>]*>", "", text)
    return text


def collect_pages(nav) -> list[str]:
    out = []
    if isinstance(nav, dict):
        for k, v in nav.items():
            if k == "pages" and isinstance(v, list):
                out += [p for p in v if isinstance(p, str)]
                out += [x for p in v if not isinstance(p, str) for x in collect_pages(p)]
            else:
                out += collect_pages(v)
    elif isinstance(nav, list):
        for item in nav:
            out += collect_pages(item)
    return out


def main() -> int:
    docs = json.loads((SITE / "docs.json").read_text())
    nav_pages = collect_pages(docs["navigation"])
    dupes = [p for p, n in Counter(nav_pages).items() if n > 1]
    nav_set = set(nav_pages)

    for p in sorted(nav_set):
        if not (SITE / f"{p}.mdx").exists() and not (SITE / f"{p}.md").exists():
            errors.append(f"docs.json references a missing page: {p}")

    on_disk = {str(p.relative_to(SITE).with_suffix("")) for p in SITE.rglob("*.mdx")}
    for p in sorted(on_disk - nav_set):
        warns.append(f"orphan page not in docs.json: {p}")

    for path in sorted(SITE.rglob("*.mdx")):
        rel = path.relative_to(SITE)
        raw = path.read_text()

        if not raw.startswith("---"):
            errors.append(f"{rel}: no frontmatter")
            continue
        fm, _, body = raw[3:].partition("---")
        if "title:" not in fm:
            errors.append(f"{rel}: frontmatter has no title")
        if "description:" not in fm:
            warns.append(f"{rel}: frontmatter has no description")

        prose = strip_code(body)
        for ch, name in (("{", "opening brace"), ("}", "closing brace")):
            if ch in prose:
                line = next((i for i, l in enumerate(strip_code(body).splitlines(), 1) if ch in l), "?")
                errors.append(f"{rel}: raw {name} in prose (line ~{line}) — escape it")
                break
        if re.search(r"<(?![A-Za-z/!])", prose):
            errors.append(f"{rel}: raw '<' in prose — write &lt;")
        # <https://x> is valid CommonMark but MDX parses it as JSX and the
        # build dies on the '/' in the scheme. Caught by `mint broken-links`,
        # so catch it here first.
        if re.search(r"<https?://", raw):
            errors.append(f"{rel}: autolink <https://…> breaks MDX — use [text](url)")
        # a nested " inside a JSX attribute terminates it early and the MDX
        # parser then reads the rest of the title as attribute names
        for m in re.finditer(r'<(\w+)\s+(?:title|caption|label)="([^"]*)"([^>]*)>', body):
            if re.match(r'\s*[^\s=/>]', m.group(3) or "") and "=" not in (m.group(3) or ""):
                errors.append(
                    f"{rel}: nested quote in <{m.group(1)}> title — use “ ” inside the attribute")

        # a raw | inside an inline code span silently splits a table cell
        infence = False
        for ln, line in enumerate(body.splitlines(), 1):
            if line.strip().startswith("```"):
                infence = not infence
                continue
            if infence:
                continue
            st = line.strip()
            if not (st.startswith("|") and st.count("|") >= 2):
                continue
            for span in re.findall(r"`[^`]*`", line):
                if re.search(r"(?<!\\)\|", span):
                    errors.append(f"{rel}:{ln}: unescaped | inside code span in a table row -> {span[:40]}")

        for tag in PAIRED:
            opens = len(re.findall(rf"<{tag}(?=[\s>])", body))
            selfclose = len(re.findall(rf"<{tag}[^>]*/>", body))
            closes = len(re.findall(rf"</{tag}>", body))
            if opens - selfclose != closes:
                errors.append(f"{rel}: unbalanced <{tag}> ({opens - selfclose} open, {closes} close)")

        for link in re.findall(r"href=\"(/[^\"#]+)", body) + re.findall(r"\]\((/[^)#\s]+)", body):
            target = link.lstrip("/")
            if target.startswith("assets/"):
                if not (SITE / target).exists():
                    warns.append(f"{rel}: link to missing asset {link}")
            elif target not in nav_set and target not in on_disk:
                errors.append(f"{rel}: internal link to non-existent page {link}")

        for src in re.findall(r"src=\"(/assets/[^\"]+)", body):
            if not (SITE / src.lstrip("/")).exists():
                warns.append(f"{rel}: missing image {src}")

        # Pages numbered 0- are primers: a scoped prerequisite bridge, not a
        # three-layer module, so the layer/sources contract does not apply.
        is_primer = rel.stem.startswith("0-")
        if rel.parts[0] == "curriculum" and rel.stem not in ("index", "lab") and not is_primer:
            if "{/* AUTHORED */}" not in raw:
                warns.append(f"{rel}: still a generated shell (no AUTHORED marker)")
            else:
                for layer in ("Layer 1", "Layer 2", "Layer 3"):
                    if layer not in body:
                        errors.append(f"{rel}: authored page missing {layer}")
                if "Sources" not in body and "further reading" not in body.lower():
                    errors.append(f"{rel}: authored page has no sources section")

    for d in dupes:
        warns.append(f"page listed in docs.json more than once (fine for labs): {d}")

    for w in warns:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(list(SITE.rglob('*.mdx')))} pages · {len(errors)} errors · {len(warns)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
