#!/usr/bin/env python3
"""Convert the Mintlify MDX course into MkDocs Material Markdown.

Mintlify has no static export (`mint` offers dev/lint only), so publishing
anywhere other than Mintlify's own hosting means rendering the content with a
different generator. MkDocs Material is chosen because every component the
course actually uses has a direct equivalent - critically `<Accordion>`, which
carries the lab hint ladder and the 5-question checkpoints. Losing
click-to-reveal would remove the teaching, not just the styling.

Component mapping:
    <Accordion title="X">   -> ??? "X"            collapsible, click to reveal
    <Tabs>/<Tab title="X">  -> === "X"            content tabs
    <Note|Tip|Info|Check>   -> !!! note|tip|info|success
    <Warning>               -> !!! warning
    <Steps>/<Step title=>   -> numbered headings
    <Card|CardGroup>        -> grid cards
    <Frame>                 -> the bare <img>

Output goes to publish/docs/, which is disposable and git-ignored.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "publish" / "docs"

ADMONITION = {"Note": "note", "Tip": "tip", "Info": "info", "Check": "success",
              "Warning": "warning"}


def dedent(text: str) -> str:
    """Strip the common leading indent.

    Mintlify sources already indent content inside <Tab>/<Accordion> for
    readability. Re-indenting on top of that lands the body at 8 spaces, which
    Markdown reads as a code block - the tab set then never forms and the page
    silently loses its three layers. Always dedent before re-indenting.
    """
    lines = [l for l in text.split("\n") if l.strip()]
    if not lines:
        return text
    pad = min(len(l) - len(l.lstrip()) for l in lines)
    if not pad:
        return text
    return "\n".join(l[pad:] if l.strip() else l for l in text.split("\n"))


def indent(text: str, pad: str = "    ") -> str:
    text = dedent(text)
    return "\n".join(pad + l if l.strip() else l for l in text.split("\n"))


def attr(tag: str, name: str) -> str:
    m = re.search(rf'{name}="([^"]*)"', tag)
    return m.group(1) if m else ""


def convert_block(body: str) -> str:
    """Rewrite one page's JSX into Material markdown, innermost first."""
    # Frames hold a light <img> and a dark one, switched by Tailwind classes
    # Mintlify understands and Material does not. Material has its own
    # mechanism - a #only-light / #only-dark fragment on the image URL - so
    # rewrite to that instead of emitting two broken <img> tags.
    def frame(m: re.Match) -> str:
        inner = m.group(1)
        caption = attr(m.group(0).split(">", 1)[0] + ">", "caption")
        imgs = re.findall(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"[^>]*>', inner)
        if not imgs:
            return inner
        light = next((u for u, _ in imgs if "-dark" not in u), imgs[0][0])
        dark = next((u for u, _ in imgs if "-dark" in u), None)
        alt = imgs[0][1]
        out = f"![{alt}]({light}#only-light)\n"
        if dark:
            out += f"![{alt}]({dark}#only-dark)\n"
        if caption:
            out += f"\n*{caption}*\n"
        return "\n" + out

    body = re.sub(r"<Frame[^>]*>(.*?)</Frame>", frame, body, flags=re.S)

    # Repeatedly collapse the innermost component until none remain, so nested
    # structures (an Accordion inside a Tab inside a page) resolve correctly.
    pattern = re.compile(
        r"^([ \t]*)<(Accordion|Tab|Step|Card|Note|Tip|Info|Check|Warning)((?:[^<>]|\n)*?)>"
        r"((?:(?!<(?:Accordion|Tab|Step|Card|Note|Tip|Info|Check|Warning)[\s>]).)*?)"
        r"</\2>", re.S | re.M)

    for _ in range(12):                       # depth guard
        new = pattern.sub(_replace, body)
        if new == body:
            break
        body = new

    # Wrappers carry no output of their own
    for w in ("Tabs", "Steps", "AccordionGroup", "CardGroup", "Columns"):
        body = re.sub(rf"</?{w}[^>]*>", "", body)

    body = re.sub(r"\{/\*.*?\*/\}", "", body, flags=re.S)      # MDX comments
    body = body.replace("&#123;", "{").replace("&#125;", "}").replace("&lt;", "<")
    return re.sub(r"\n{4,}", "\n\n\n", body)


def _replace(m: re.Match) -> str:
    # Strip newlines only, not spaces: .strip() would flatten the first line's
    # indent, making dedent() compute a common indent of 0 and leaving the body
    # one level deeper than its heading.
    # Group 1 is the tag's own indentation. Replacements are emitted at column
    # 0 and then re-indented to it, so a component nested inside an already
    # indented body does not shift its siblings relative to each other - the
    # ragged result is what stops a tab set from forming.
    lead, tag, attrs = m.group(1), m.group(2), m.group(3)
    inner = dedent(m.group(4).strip("\n")).strip()
    full = f"<{tag}{attrs}>"

    def out(text: str) -> str:
        if not lead:
            return text
        return "\n".join(lead + l if l.strip() else l for l in text.split("\n"))
    title = attr(full, "title")

    if tag in ADMONITION:
        head = f'!!! {ADMONITION[tag]}' + (f' "{title}"' if title else "")
        return out(f"\n{head}\n\n{indent(inner)}\n")
    if tag == "Accordion":
        return out(f'\n??? note "{title or "Details"}"\n\n{indent(inner)}\n')
    if tag == "Tab":
        return out(f'\n=== "{title}"\n\n{indent(inner)}\n')
    if tag == "Step":
        return out(f"\n**{title}**\n\n{inner}\n")
    if tag == "Card":
        href = attr(full, "href")
        label = title or "Open"
        link = f"[{label}]({href})" if href else f"**{label}**"
        return out(f"\n- {link} — {inner}\n" if inner else f"\n- {link}\n")
    return inner


def relativise(md: str, page_rel: Path) -> str:
    """Turn Mintlify's absolute /a/b links into paths relative to this page.

    Mintlify serves from the domain root so /curriculum/... resolves. GitHub
    Pages serves a project site from /<repo>/, where the same link 404s. MkDocs
    also wants relative links to validate them. Depth is computed from the
    page's own location.
    """
    depth = len(page_rel.parts) - 1
    up = "../" * depth if depth else "./"

    def fix(m: re.Match) -> str:
        target = m.group(2).lstrip("/")
        if target.startswith("assets/"):
            return f"{m.group(1)}({up}{target})"
        return f"{m.group(1)}({up}{target}.md)"

    md = re.sub(r"(\[[^\]]*\])\((/[^)#\s]+)\)", fix, md)

    def fix_img(m: re.Match) -> str:
        return f"{m.group(1)}({up}{m.group(2).lstrip('/')}{m.group(3)})"

    return re.sub(r"(!\[[^\]]*\])\((/assets/[^)#\s]+)(#[a-z-]+)?\)", fix_img, md)



def normalise_blocks(md: str, depth: int = 0) -> str:
    """Re-indent tab and details blocks to exactly four spaces per level.

    JSX indentation in the source is not a consistent multiple of four - a <Tab>
    sits at 2 and an <Accordion> inside it at 8 - so shifting a block uniformly
    leaves nested markers at 6, which Markdown reads as neither a new block nor
    valid content. Recurse instead: place each marker at depth*4, its body at
    (depth+1)*4, and normalise that body at depth+1. This is what makes the
    three-layer tabs and the checkpoint accordions inside them both render.
    """
    marker = re.compile(r'^([ \t]*)((?:=== "|\?\?\? ).*)$')
    lines = md.split("\n")
    out: list[str] = []
    pad = "    " * depth
    i = 0
    while i < len(lines):
        m = marker.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue

        own = len(m.group(1))
        out.append(pad + m.group(2))
        i += 1

        body: list[str] = []
        while i < len(lines):
            nxt = lines[i]
            if nxt.strip() and (len(nxt) - len(nxt.lstrip())) <= own:
                break
            body.append(nxt)
            i += 1
        while body and not body[-1].strip():
            body.pop()

        if body:
            inner = normalise_blocks(dedent("\n".join(body)), 0)
            out.append("")
            for b in inner.split("\n"):
                out.append(pad + "    " + b if b.strip() else b)
            out.append("")
    return "\n".join(out)


def convert_page(src: Path) -> tuple[str, str]:
    raw = src.read_text()
    fm, _, body = raw[3:].partition("---") if raw.startswith("---") else ("", "", raw)
    title = (re.search(r'title:\s*"?(.*?)"?\s*$', fm, re.M) or [None, src.stem])[1]
    title = title.replace('\\"', '"')
    md = f"# {title}\n\n{normalise_blocks(convert_block(body)).lstrip()}"
    return title, md


def collect(nav) -> list:
    """Flatten docs.json navigation into a MkDocs nav tree."""
    out = []
    if isinstance(nav, dict):
        if "pages" in nav:
            label = nav.get("group") or nav.get("tab") or nav.get("dropdown")
            kids = []
            for p in nav["pages"]:
                if isinstance(p, str):
                    kids.append(f"{p}.md")
                else:
                    kids.extend(collect(p))
            return [{label: kids}] if label else kids
        for v in nav.values():
            out.extend(collect(v) if isinstance(v, (dict, list)) else [])
    elif isinstance(nav, list):
        for i in nav:
            out.extend(collect(i))
    return out


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    n = 0
    for src in sorted(SITE.rglob("*.mdx")):
        rel = src.relative_to(SITE).with_suffix(".md")
        dst = OUT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        _, md = convert_page(src)
        dst.write_text(relativise(md, rel))
        n += 1

    assets = SITE / "assets"
    if assets.exists():
        shutil.copytree(assets, OUT / "assets", dirs_exist_ok=True)

    docs = json.loads((SITE / "docs.json").read_text())
    nav = collect(docs["navigation"])
    (ROOT / "publish" / "nav.json").write_text(json.dumps(nav, indent=2))
    print(f"converted {n} pages -> publish/docs/")


if __name__ == "__main__":
    main()
