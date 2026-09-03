#!/usr/bin/env python3
"""Convert the Mintlify MDX course into Astro Starlight MDX.

Starlight was chosen over MkDocs Material and VitePress after building all
three with real course content. It wins for one structural reason: its
component set maps almost 1:1 onto Mintlify's, and it takes MDX natively rather
than requiring a translation to Markdown syntax.

    Mintlify              Starlight
    <Tabs>/<Tab>      ->  <Tabs>/<TabItem>
    <Card>/<CardGroup>->  <Card>/<CardGrid>
    <Note|Tip|Info>   ->  <Aside type="note|tip|note">
    <Warning>         ->  <Aside type="caution">
    <Accordion>       ->  <details>/<summary>   (click to reveal, as before)
    <Steps>/<Step>    ->  bold step headings
    <Frame> + imgs    ->  a single <img>, dark variant dropped

Components are replaced innermost-first: a nested <Accordion> inside a <Tab>
cannot be matched until the inner one has been replaced, which is why this
loops rather than doing a single pass.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT
OUT = Path(__file__).resolve().parent / "src" / "content" / "docs"

ASIDE = {"Note": "note", "Info": "note", "Tip": "tip",
         "Check": "tip", "Warning": "caution"}

TAGS = ("Accordion", "Tab", "Note", "Info", "Tip", "Warning", "Check",
        "Card", "Step")
OPEN = re.compile(r"<(" + "|".join(TAGS) + r")(\s[^<>]*?)?>")
CLOSE = re.compile(r"</(" + "|".join(TAGS) + r")>")


def attr(tag: str, name: str) -> str:
    m = re.search(rf'{name}="([^"]*)"', tag)
    return m.group(1) if m else ""


def render(tag: str, attrs: str, inner: str) -> str:
    """Emit the Starlight equivalent of one Mintlify component."""
    full = f"<{tag}{attrs}>"
    title = attr(full, "title")
    inner = inner.strip()

    if tag in ASIDE:
        t = f' title="{title}"' if title else ""
        return f'\n<Aside type="{ASIDE[tag]}"{t}>\n\n{inner}\n\n</Aside>\n'
    if tag == "Accordion":
        return (f"\n<details>\n<summary>{title or 'Details'}</summary>\n\n"
                f"{inner}\n\n</details>\n")
    if tag == "Tab":
        return f'\n<TabItem label="{title}">\n\n{inner}\n\n</TabItem>\n'
    if tag == "Card":
        href = attr(full, "href")
        h = f' href="{href}"' if href else ""
        return f'\n<Card title="{title or "Open"}"{h}>\n{inner}\n</Card>\n'
    if tag == "Step":
        return f"\n**{title}**\n\n{inner}\n"
    return inner


def transform(body: str) -> str:
    """Rewrite components with a stack, not paired regexes.

    Regex pairing cannot reliably match an opening tag to its own closing tag
    once components nest, and the failures are silent: an orphaned </Accordion>
    or an unconverted <Tab> ships into the build and MDX rejects the page. A
    single left-to-right pass with a stack pairs them exactly.
    """
    out: list[str] = []
    stack: list[tuple[str, str, list]] = []
    buf = out
    i = 0

    while i < len(body):
        o = OPEN.search(body, i)
        c = CLOSE.search(body, i)
        if not o and not c:
            buf.append(body[i:])
            break

        nxt = min([m for m in (o, c) if m], key=lambda m: m.start())
        buf.append(body[i:nxt.start()])
        i = nxt.end()

        if nxt is o:
            stack.append((nxt.group(1), nxt.group(2) or "", buf))
            buf = []
        else:
            if not stack:
                continue                      # stray close: drop it
            tag, attrs, parent = stack.pop()
            if tag != nxt.group(1):
                # mismatched nesting - keep the text rather than lose content
                parent.append("".join(buf))
                buf = parent
                continue
            parent.append(render(tag, attrs, "".join(buf)))
            buf = parent

    while stack:                              # unclosed tag: keep its content
        tag, attrs, parent = stack.pop()
        parent.append("".join(buf))
        buf = parent
    return "".join(buf)


def frames(body: str) -> str:
    """A Frame holds a light and a dark <img>, switched by Tailwind classes
    Mintlify understands and Starlight does not.

    Dropping the dark one and keeping the light leaves a hand-drawn sketch on
    #fffdf7 paper glowing white in the middle of a dark page - the single worst
    thing on the page. Emit both and switch them with the theme instead."""
    def one(m: re.Match) -> str:
        inner = m.group(1)
        imgs = re.findall(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"', inner)
        if not imgs:
            return inner
        light = next((u for u, _ in imgs if "-dark" not in u), imgs[0][0])
        dark = next((u for u, _ in imgs if "-dark" in u), None)
        alt = imgs[0][1].replace('"', "&quot;")
        out = f'\n<img src="{light}" alt="{alt}" class="diagram diagram-light" />\n'
        if dark:
            out += f'<img src="{dark}" alt="{alt}" class="diagram diagram-dark" />\n'
        return out
    return re.sub(r"<Frame[^>]*>(.*?)</Frame>", one, body, flags=re.S)


def convert(raw: str) -> tuple[str, str, str]:
    fm, _, body = raw[3:].partition("---") if raw.startswith("---") else ("", "", raw)
    title = (re.search(r'title:\s*"?(.*?)"?\s*$', fm, re.M) or [None, "Untitled"])[1]
    desc = (re.search(r'description:\s*"?(.*?)"?\s*$', fm, re.M) or [None, ""])[1]

    # One Accordion title is literally 'HPA shows TARGETS as <unknown>'. Those
    # angle brackets break the tag pattern, so swap them for entities before
    # matching rather than widening the regex into a backtracking trap.
    body = re.sub(r'="([^"]*)"',
                  lambda m: '="' + m.group(1).replace("<", "&lt;").replace(">", "&gt;") + '"',
                  body)
    body = frames(body)
    body = transform(body)

    for w in ("Tabs", "Steps", "AccordionGroup", "CardGroup", "Columns", "Frame"):
        if w == "CardGroup":
            body = re.sub(r"<CardGroup[^>]*>", "<CardGrid>", body)
            body = body.replace("</CardGroup>", "</CardGrid>")
        elif w == "Tabs":
            body = re.sub(r"<Tabs[^>]*>", "<Tabs>", body)
        else:
            body = re.sub(rf"</?{w}[^>]*>", "", body)

    body = re.sub(r"\{/\*.*?\*/\}", "", body, flags=re.S)     # MDX comments
    body = body.replace("className=", "class=")
    body = re.sub(r"\n{4,}", "\n\n\n", body)

    used = [c for c in ("Tabs", "TabItem", "Aside", "Card", "CardGrid")
            if f"<{c}" in body]
    imports = (f'import {{ {", ".join(used)} }} from "@astrojs/starlight/components";\n'
               if used else "")
    return title, desc, imports + "\n" + body.lstrip()


def esc(s: str) -> str:
    """Escape once. Source frontmatter already contains \\" for embedded quotes,
    so unescape first or the result is \\\\" and the YAML parser rejects it."""
    return s.replace('\\"', '"').replace('"', '\\"')


def sidebar(docs: dict) -> list:
    """Build the Starlight sidebar from Mintlify's docs.json navigation."""
    def pages(node):
        out = []
        for p in node.get("pages", []):
            if isinstance(p, str):
                # Starlight addresses pages by slug, and an index.mdx takes
                # its directory's slug rather than ".../index".
                slug = p[:-6] if p.endswith("/index") else p
                out.append({"slug": slug} if slug != "index" else {"slug": ""})
            else:
                out.extend(walk(p))
        return out

    def walk(node):
        label = node.get("group") or node.get("tab") or node.get("dropdown")
        kids = pages(node)
        for g in node.get("groups", []):
            kids.extend(walk(g))
        return [{"label": label, "collapsed": True, "items": kids}] if label else kids

    out = []
    for tab in docs["navigation"]["tabs"]:
        kids = pages(tab)
        for g in tab.get("groups", []):
            kids.extend(walk(g))
        out.append({"label": tab["tab"], "collapsed": True, "items": kids})
    return out


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    n = 0
    for src in sorted(SITE.rglob("*.mdx")):
        rel = src.relative_to(SITE)
        title, desc, body = convert(src.read_text())
        dst = OUT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        head = f'---\ntitle: "{esc(title)}"\n'
        if desc:
            head += f'description: "{esc(desc)}"\n'
        head += "---\n\n"
        # The subtitle is rendered by src/components/PageTitle.astro, which
        # also adds the breadcrumb, so it must not be duplicated in the body.
        dst.write_text(head + body)
        n += 1

    pub = Path(__file__).resolve().parent / "public"
    if (SITE / "assets").exists():
        shutil.copytree(SITE / "assets", pub / "assets", dirs_exist_ok=True)

    docs = json.loads((SITE / "docs.json").read_text())
    (Path(__file__).resolve().parent / "sidebar.json").write_text(
        json.dumps(sidebar(docs), indent=2))
    print(f"converted {n} pages -> starlight/src/content/docs/")


if __name__ == "__main__":
    main()
