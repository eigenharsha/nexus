#!/usr/bin/env python3
"""
build_diagrams.py - walk the curriculum, render every DIAGRAM-SPEC block.

  python3 tools/build_diagrams.py            # build everything
  python3 tools/build_diagrams.py --only p4-w30-m1
  python3 tools/build_diagrams.py --list     # parse only, no rendering

The ~156 DIAGRAM-SPEC blocks in curriculum are written in prose by many
different authors, so this parses defensively: a malformed block is recorded as
an error and the run continues. It never raises on bad input.

Two sources of specs are rendered into assets/diagrams/:

  1. `{/* DIAGRAM-SPEC ... */}` blocks in curriculum/**/*.mdx.
     Their `elements:` list is English, not geometry, so it is *compiled* into a
     sketch spec by heuristics (quoted strings become boxes, `->` becomes a
     flow, "amber margin note" becomes a margin note, and so on). The result is
     a real, on-style whiteboard sketch, but a mechanical one - see
     assets/diagrams/README.md for how to replace one by hand.

  2. Hand-authored JSON specs in tools/specs/*.json - the flagship sketches.
     These always win over an auto-compiled block with the same id.

Writes assets/diagram-manifest.json.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sketch          # noqa: E402
import excalidraw      # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM = ROOT / "curriculum"
SPEC_DIR = ROOT / "tools" / "specs"
OUT_DIR = ROOT / "assets" / "diagrams"
MANIFEST = ROOT / "site" / "assets" / "diagram-manifest.json"

# ids whose SVGs are drawn by a human in Excalidraw and committed directly to
# assets/diagrams/. The build never overwrites these - it only records them
# in the manifest. See assets/diagrams/README.md.
HAND_DRAWN: set[str] = set()

BLOCK_RE = re.compile(r"\{/\*\s*DIAGRAM-SPEC\b(.*?)\*/\}", re.S)
KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9 _-]*)\s*:\s*(.*)$")
BULLET_RE = re.compile(r"^\s*[-*•]\s+(.*)$")
FM_TITLE_RE = re.compile(r"^title:\s*[\"']?(.+?)[\"']?\s*$", re.M)
# what the page actually asks for: /assets/diagrams/<base>{,-dark,-blank}.<ext>
ASSET_REF_RE = re.compile(r"/assets/diagrams/([A-Za-z0-9._-]+)")
VARIANT_RE = re.compile(r"(-dark|-blank)?\.(svg|excalidraw|png)$")

ARROW_SPLIT = re.compile(r"\s*(?:->|→|-->|=>)\s*")


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------

def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return s or "diagram"


def parse_block(body: str) -> dict:
    """Parse one DIAGRAM-SPEC body into {key: str | [str]}. Never raises."""
    data: dict = {}
    key = None
    for raw in body.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        bullet = BULLET_RE.match(line)
        indented = line[:1] in (" ", "\t")
        if bullet and (indented or key):
            if key:
                data.setdefault(key + "__list", []).append(bullet.group(1).strip())
                continue
        m = KEY_RE.match(line.strip()) if not indented else None
        if m and not bullet:
            key = m.group(1).strip().lower()
            value = m.group(2).strip()
            if value:
                data[key] = value
            continue
        # a continuation line of the previous scalar, or stray prose
        if key:
            if key + "__list" in data and data[key + "__list"]:
                data[key + "__list"][-1] += " " + line.strip()
            elif key in data:
                data[key] += " " + line.strip()
            else:
                data[key] = line.strip()
    # normalise: promote __list to the key when the key had no scalar
    for k in list(data):
        if k.endswith("__list"):
            base = k[:-6]
            if not data.get(base):
                data[base] = data.pop(k)
            else:
                data[base] = [data.pop(base)] + data.pop(k)
    return data


def find_blocks(mdx: Path) -> list[dict]:
    text = mdx.read_text(encoding="utf-8", errors="replace")
    fm = FM_TITLE_RE.search(text[:1200])
    page_title = fm.group(1).strip() if fm else mdx.stem.replace("-", " ")
    # the filenames this page links, deduplicated but kept in document order
    bases, seen_b = [], set()
    for name in ASSET_REF_RE.findall(text):
        base = VARIANT_RE.sub("", name)
        if base and base not in seen_b:
            seen_b.add(base)
            bases.append(base)

    out = []
    for i, m in enumerate(BLOCK_RE.finditer(text)):
        block = parse_block(m.group(1))
        block["_page"] = str(mdx.relative_to(ROOT / "site"))
        block["_page_title"] = page_title
        block["_index"] = i
        block["_bases"] = bases
        out.append(block)
    if not out and bases:
        # the page links a sketch but nobody wrote a DIAGRAM-SPEC for it
        out.append({"_page": str(mdx.relative_to(ROOT / "site")),
                    "_page_title": page_title, "_index": 0,
                    "_bases": bases, "_no_spec": True})
    return out


# --------------------------------------------------------------------------
# the prose -> sketch compiler
# --------------------------------------------------------------------------

QUOTE_RE = re.compile(r"[\"“”']([^\"“”']{2,90})[\"“”']")

NOTE_HINTS = ("amber margin note", "margin note", "amber note", "amber:",
              "note:", "teacher's voice")
CIRCLE_HINTS = ("circled", "circle the", "circling")
CROSS_HINTS = ("cross-out", "crossed out", "cross out", "struck through",
               "strike through", "struck-through", "red cross")
ERROR_HINTS = ("red", "error", "wrong", "bug", "fail", "broken", "naive",
               "anti-pattern", "silent", "irreversible")
OK_HINTS = ("green", "correct", "the fix", "tick", "works", "safe", "passes")
NOTE_COLOR_HINTS = ("amber", "warning", "careful", "remember")


def classify_color(text: str) -> str:
    t = text.lower()
    if any(h in t for h in CROSS_HINTS) or any(h in t for h in ERROR_HINTS):
        return "error"
    if any(h in t for h in OK_HINTS):
        return "correct"
    if any(h in t for h in NOTE_COLOR_HINTS):
        return "note"
    return "structure"


def clean_label(text: str) -> str:
    t = re.sub(r"\s+", " ", str(text)).strip(" ,.;:-")
    t = re.sub(r"^(a|an|the)\s+", "", t, flags=re.I)
    return t


def strip_quotes(text: str) -> str:
    return re.sub(r"^\s*[\"“”']|[\"“”']\s*$", "", str(text)).strip()


def compile_prose(block: dict) -> dict:
    """Turn a prose DIAGRAM-SPEC into a renderable sketch spec.

    Layout: a numbered column of rows down the left two-thirds, margin notes
    and circled terms down the right third, measured numbers along the bottom.
    """
    sid = str(block.get("id") or slugify(block.get("_page", "diagram")))
    title = clean_label(block.get("_page_title") or sid)
    goal = block.get("one-sentence-goal") or block.get("goal") or ""
    if isinstance(goal, list):
        goal = " ".join(goal)
    alt = block.get("alt") or block.get("alt-text") or goal or f"Sketch: {title}"
    if isinstance(alt, list):
        alt = " ".join(alt)

    raw_elements = block.get("elements") or []
    if isinstance(raw_elements, str):
        raw_elements = [raw_elements]
    raw_elements = [str(e) for e in raw_elements if str(e).strip()]

    numbers = block.get("numbers-to-write-in") or block.get("numbers") or ""
    if isinstance(numbers, list):
        numbers = "; ".join(numbers)

    W = 1000
    LEFT, MAIN_W = 46, 640
    RIGHT_X = LEFT + MAIN_W + 40
    RIGHT_W = W - RIGHT_X - 30

    els: list[dict] = []
    y = 74

    # the one-sentence goal, written under the title like a caption
    if goal:
        lines = sketch.wrap_text(goal, W - 100, 17)
        els.append({"type": "text", "id": "goal", "x": LEFT, "y": y + 8,
                    "text": goal, "size": 17, "color": "muted",
                    "anchor": "start", "w": W - 100, "rotate": 0})
        y += 14 + len(lines) * 20

    right_y = y + 6
    step = 0

    def push_note(text, seed):
        nonlocal right_y
        text = clean_label(text)
        if not text:
            return
        lines = sketch.wrap_text(text, RIGHT_W, 15, max_lines=8)
        els.append({"type": "note", "id": f"n{seed}", "x": RIGHT_X,
                    "y": right_y + 10, "w": RIGHT_W, "text": text})
        right_y += 24 + len(lines) * 18

    def push_circled(term, seed):
        nonlocal right_y
        term = clean_label(strip_quotes(term))[:34]
        if not term:
            return
        # shrink the term until the ring fits inside the right margin
        size = 18.0
        while (sketch.text_width(term, size, True) + 34 > RIGHT_W
               and size > 10.5):
            size -= 0.5
        els.append({"type": "circled", "id": f"c{seed}", "size": size,
                    "x": RIGHT_X + RIGHT_W / 2, "y": right_y + 26,
                    "text": term, "ring": "structure"})
        right_y += 62 + size

    for i, bullet in enumerate(raw_elements):
        low = bullet.lower()
        quotes = [strip_quotes(q) for q in QUOTE_RE.findall(bullet)]
        quotes = [q for q in quotes if q.strip()]

        # ---- margin note rows go to the right column -------------------
        if any(h in low[:40] for h in NOTE_HINTS):
            push_note(quotes[0] if quotes else re.sub(
                r"^[^:]{0,40}note[^:]{0,10}:\s*", "", bullet, flags=re.I), i)
            continue

        # ---- a bullet that is only about circling a term ---------------
        if any(h in low for h in CIRCLE_HINTS) and len(bullet) < 130:
            push_circled(quotes[-1] if quotes else bullet, i)
            continue

        is_cross = any(h in low for h in CROSS_HINTS)
        col = classify_color(bullet)

        # ---- a flow chain: "a -> b -> c" inside a quote or in the prose --
        chain = None
        for q in quotes:
            if ARROW_SPLIT.search(q):
                chain = [clean_label(p) for p in ARROW_SPLIT.split(q) if p.strip()]
                break
        if chain is None and ARROW_SPLIT.search(bullet) and len(quotes) >= 2:
            chain = [clean_label(q) for q in quotes]

        step += 1
        row_h = 66
        els.append({"type": "badge", "id": f"b{i}", "n": step,
                    "x": LEFT - 16, "y": y + row_h / 2})

        if chain and len(chain) >= 2:
            chain = chain[:5]
            gap = 30
            bw = max(74, (MAIN_W - gap * (len(chain) - 1)) / len(chain))
            for k, node in enumerate(chain):
                bx = LEFT + 14 + k * (bw + gap)
                els.append({"type": "box", "id": f"e{i}n{k}", "x": bx, "y": y,
                            "w": bw, "h": row_h, "label": node[:44],
                            "color": col, "size": 16})
                if k < len(chain) - 1:
                    els.append({"type": "arrow", "id": f"e{i}a{k}",
                                "x1": bx + bw + 3, "y1": y + row_h / 2,
                                "x2": bx + bw + gap - 3, "y2": y + row_h / 2,
                                "color": "ink"})
            if is_cross:
                els.append({"type": "crossout", "id": f"e{i}x",
                            "x": LEFT + 14, "y": y, "w": MAIN_W - 14,
                            "h": row_h})
            # prose left over from the bullet, written small underneath
            rest = clean_label(QUOTE_RE.sub("", bullet))
            if rest and len(rest) > 8:
                els.append({"type": "text", "id": f"e{i}s", "x": LEFT + 14,
                            "y": y + row_h + 26, "text": rest[:150],
                            "size": 14, "color": "muted", "anchor": "start",
                            "w": MAIN_W, "rotate": 0})
                row_h += 26 + 18 * len(sketch.wrap_text(rest[:150], MAIN_W, 14))

        elif len(quotes) >= 2:
            nodes = quotes[:4]
            gap = 26
            bw = max(84, (MAIN_W - gap * (len(nodes) - 1)) / len(nodes))
            for k, node in enumerate(nodes):
                els.append({"type": "box", "id": f"e{i}n{k}",
                            "x": LEFT + 14 + k * (bw + gap), "y": y,
                            "w": bw, "h": row_h, "label": clean_label(node)[:60],
                            "color": col, "size": 15,
                            "fill": "hachure" if col == "correct" else None,
                            "fill_color": col})
            if is_cross:
                els.append({"type": "crossout", "id": f"e{i}x",
                            "x": LEFT + 14, "y": y, "w": MAIN_W - 14, "h": row_h})

        else:
            label = clean_label(quotes[0]) if quotes else clean_label(bullet)
            sub = None
            if quotes:
                rest = clean_label(QUOTE_RE.sub("", bullet))
                sub = rest[:110] if len(rest) > 8 else None
            text = label[:220]
            lines = sketch.wrap_text(text, MAIN_W - 40, 16)
            row_h = max(58, 24 + len(lines) * 20)
            els.append({"type": "box", "id": f"e{i}n0", "x": LEFT + 14, "y": y,
                        "w": MAIN_W - 14, "h": row_h, "label": text,
                        "color": col, "size": 16, "sub": sub})
            if is_cross:
                els.append({"type": "crossout", "id": f"e{i}x", "x": LEFT + 14,
                            "y": y, "w": MAIN_W - 14, "h": row_h})
            if sub:
                row_h += 20

        # a term circled inside a longer bullet
        if any(h in low for h in CIRCLE_HINTS) and quotes:
            push_circled(quotes[-1], f"{i}z")

        y += row_h + 34

    # ---- guarantee the house-style minimums -----------------------------
    if not any(e["type"] == "note" for e in els):
        push_note(goal or "the point of this sketch is the one idea above - "
                          "redraw it from memory before moving on", "auto")
    if not any(e["type"] == "circled" for e in els):
        term = clean_label(title.split(":")[0])[:28]
        push_circled(term, "auto")

    bottom = max(y, right_y) + 10

    # measured numbers, hand-written along the foot of the board
    if numbers:
        els.append({"type": "text", "id": "nums", "x": LEFT, "y": bottom + 16,
                    "text": "measured: " + str(numbers), "size": 15,
                    "color": "ink", "anchor": "start", "w": W - 90,
                    "rotate": 0})
        bottom += 16 + len(sketch.wrap_text("measured: " + str(numbers),
                                            W - 90, 15)) * 18

    # leave one thing unfinished - the dangling arrow into the exercise
    els.append({"type": "arrow", "id": "open", "x1": W - 320, "y1": bottom + 30,
                "x2": W - 180, "y2": bottom + 48, "dashed": True,
                "color": "note", "label": "...now you draw it"})
    bottom += 78

    return {
        "id": sid,
        "title": title,
        "alt": alt,
        "width": W,
        "height": max(360, bottom),
        "elements": els,
    }


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

def check_svg(path: Path) -> tuple[bool, str]:
    import xml.etree.ElementTree as ET
    raw = path.read_bytes()
    try:
        ET.fromstring(raw)
    except Exception as exc:
        return False, f"malformed XML: {exc}"
    kb = len(raw) / 1024
    if kb > 200:
        return False, f"too big: {kb:.0f} KB"
    return True, f"{kb:.0f} KB"




def embed_fonts_everywhere() -> int:
    """Give every rendered SVG its own embedded font subset.

    An SVG loaded through <img src="..."> renders in secure static mode: it
    cannot fetch an external webfont, so the @import'ed handwriting face never
    arrives and the diagram silently falls back to a serif. Embedding a subset
    containing only the glyphs each file uses fixes that and keeps <text> real -
    selectable, searchable, accessible - unlike converting text to outlines.

    Runs before aliasing so the copies inherit the embedded font.
    """
    from embedfont import embed

    n = 0
    oversize = []
    for f in sorted(OUT_DIR.glob("*.svg")):
        src = f.read_text()
        if "@font-face" not in src:
            out = embed(src)
            if out != src:
                f.write_text(out)
                n += 1
        # The renderer's own 200 KB check runs BEFORE this step, so a file that
        # passed there can still ship oversize once the font subset is added.
        # Enforce the real cap against what actually lands on disk.
        size = f.stat().st_size
        if size > 200_000:
            oversize.append((f.name, size))
    for name, size in oversize:
        print(f"  OVERSIZE  {name} is {size/1024:.0f} KB (cap 200 KB) - simplify the spec")
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="render just this id")
    ap.add_argument("--list", action="store_true", help="parse only")
    ap.add_argument("--prune", action="store_true",
                    help="delete files in the output dir that this run did "
                         "not write (stale renames, hand patches)")
    args = ap.parse_args()

    errors: list[tuple[str, str]] = []
    warns: list[str] = []
    entries: dict[str, dict] = {}

    # ---- 1. hand-authored flagship specs (these win) --------------------
    hand: dict[str, dict] = {}
    for jf in sorted(SPEC_DIR.glob("*.json")) if SPEC_DIR.exists() else []:
        try:
            spec = json.loads(jf.read_text(encoding="utf-8"))
            sid = spec.get("id") or jf.stem
            spec["id"] = sid
            hand[sid] = spec
        except Exception as exc:
            errors.append((jf.name, f"bad JSON spec: {exc}"))

    # ---- 2. curriculum prose blocks ------------------------------------
    mdx_files = sorted(CURRICULUM.rglob("*.mdx"))
    blocks: list[dict] = []
    for mdx in mdx_files:
        try:
            blocks += find_blocks(mdx)
        except Exception as exc:
            errors.append((str(mdx), f"could not read/scan: {exc}"))

    seen: dict[str, str] = {}
    compiled: list[dict] = []
    no_spec: list[str] = []
    for block in blocks:
        page = block.get("_page", "?")
        if block.get("_no_spec"):
            no_spec.append(f"{page} -> links "
                           f"{', '.join(block.get('_bases', []))}")
            continue
        try:
            sid = str(block.get("id") or "").strip()
            # `id:` with an empty value swallows the next bare word - a spec
            # key name arriving as an id means the id was really missing
            if sid.lower() in {"tier", "elements", "alt", "one-sentence-goal",
                               "numbers-to-write-in", "goal", "numbers"}:
                sid = ""
            if not sid:
                sid = slugify(Path(page).with_suffix("").as_posix())
                if block.get("_index"):
                    sid = f"{sid}-{block['_index'] + 1}"
                warns.append(f"{page}: block has no id: -> fell back to '{sid}'")
            if not block.get("elements"):
                warns.append(f"{page} [{sid}]: no elements: list, "
                             f"rendering goal + numbers only")
            if sid in seen:
                warns.append(f"{page} [{sid}]: duplicate id, also in {seen[sid]}"
                             f" - suffixing")
                sid = f"{sid}-{Path(page).stem[:12]}"
            seen[sid] = page
            block["id"] = sid
            spec = compile_prose(block)
            spec["_page"] = page
            spec["_tier"] = str(block.get("tier", "T1")).strip()
            # pair the page's referenced filenames with its spec blocks in
            # document order, so the pages resolve without editing them
            bases = block.get("_bases") or []
            idx = block.get("_index", 0)
            spec["_aliases"] = [bases[idx]] if idx < len(bases) else []
            if bases and not spec["_aliases"]:
                warns.append(f"{page} [{sid}]: block #{idx + 1} but the page "
                             f"links only {len(bases)} filename(s) "
                             f"({', '.join(bases)}) - no alias assigned, so "
                             f"this diagram is rendered but unreachable")
            compiled.append(spec)
        except Exception as exc:
            errors.append((f"{page} [{block.get('id')}]",
                           f"compile failed: {exc.__class__.__name__}: {exc}"))
            if "-v" in sys.argv:
                traceback.print_exc()

    # hand-written specs override compiled ones with the same id
    by_id: dict[str, dict] = {}
    for spec in compiled:
        by_id[spec["id"]] = spec
    for sid, spec in hand.items():
        if sid in by_id:
            spec["_page"] = by_id[sid].get("_page")
            spec["_tier"] = by_id[sid].get("_tier", "T1")
            spec["_aliases"] = by_id[sid].get("_aliases", [])
        spec["_hand"] = True
        by_id[sid] = spec

    if args.list:
        for sid, spec in sorted(by_id.items()):
            print(f"{sid:28s} {'HAND' if spec.get('_hand') else 'auto'}  "
                  f"{len(spec.get('elements', []))} el  {spec.get('_page','-')}")
        print(f"\n{len(by_id)} specs, {len(errors)} parse errors, "
              f"{len(warns)} warnings")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok = 0
    skipped = 0
    aliased = 0
    for sid, spec in sorted(by_id.items()):
        if args.only and args.only != sid:
            continue
        if sid in HAND_DRAWN:
            entries[sid] = {
                "id": sid, "title": spec.get("title", sid),
                "alt": spec.get("alt", ""), "tier": spec.get("_tier", "T1"),
                "page": spec.get("_page"),
                "source": "hand-drawn in Excalidraw (not generated)",
                "elements": 0,
                "files": {"light": f"assets/diagrams/{sid}.svg",
                          "dark": f"assets/diagrams/{sid}-dark.svg",
                          "blank": f"assets/diagrams/{sid}-blank.svg",
                          "source": f"assets/diagrams/{sid}.excalidraw"},
                "aliases": [a for a in spec.get("_aliases", []) if a != sid],
            }
            skipped += 1
            continue
        try:
            written = sketch.render_all(spec, OUT_DIR, sid)
            bad = []
            for variant, path in written.items():
                good, info = check_svg(Path(path))
                if not good:
                    bad.append(f"{variant}: {info}")
            if bad:
                errors.append((sid, "; ".join(bad)))
                continue

            # the editable source the "Draw it yourself" block links to
            (OUT_DIR / f"{sid}.excalidraw").write_text(
                excalidraw.dumps(spec), encoding="utf-8")

            # The lesson pages were generated with filenames derived from the
            # module title, not from the spec id, so publish the same bytes
            # under every name the page actually links. The id stays canonical.
            aliases = [a for a in spec.get("_aliases", []) if a and a != sid]
            for alias in aliases:
                for suffix in ("", "-dark", "-blank"):
                    shutil.copyfile(OUT_DIR / f"{sid}{suffix}.svg",
                                    OUT_DIR / f"{alias}{suffix}.svg")
                shutil.copyfile(OUT_DIR / f"{sid}.excalidraw",
                                OUT_DIR / f"{alias}.excalidraw")
                aliased += 1

            entries[sid] = {
                "id": sid,
                "title": spec.get("title", sid),
                "alt": spec.get("alt", ""),
                "tier": spec.get("_tier", "T1"),
                "page": spec.get("_page"),
                "source": "hand-authored" if spec.get("_hand")
                          else "auto-compiled from DIAGRAM-SPEC",
                "elements": len(spec.get("elements", [])),
                "files": {
                    "light": f"assets/diagrams/{sid}.svg",
                    "dark": f"assets/diagrams/{sid}-dark.svg",
                    "blank": f"assets/diagrams/{sid}-blank.svg",
                    "source": f"assets/diagrams/{sid}.excalidraw",
                },
                "hero": spec.get("hero"),
                "week": spec.get("week"),
                "aliases": aliases,
                "alias_files": [f"assets/diagrams/{a}{s}"
                                for a in aliases
                                for s in (".svg", "-dark.svg", "-blank.svg",
                                          ".excalidraw")],
            }
            ok += 1
        except Exception as exc:
            errors.append((sid, f"render failed: {exc.__class__.__name__}: {exc}"))
            if "-v" in sys.argv:
                traceback.print_exc()

    if args.prune and not args.only:
        keep = {"README.md"}
        for sid, e in entries.items():
            keep |= {Path(f).name for f in e["files"].values()}
            keep |= {Path(f).name for f in e.get("alias_files", [])}
        gone = 0
        for f in sorted(OUT_DIR.iterdir()):
            if f.is_file() and f.name not in keep:
                f.unlink()
                gone += 1
        print(f"  pruned    {gone} stale files")

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    # A --only run renders one diagram, so `entries` holds one diagram. Writing
    # that as the whole manifest would discard the other 172 - and with several
    # agents each running --only concurrently, the manifest was being reduced to
    # a single entry. Merge into what is already on disk instead of replacing.
    if args.only and MANIFEST.exists():
        try:
            prev = json.loads(MANIFEST.read_text()).get("diagrams", {})
            prev.update(entries)
            entries = prev
        except (json.JSONDecodeError, OSError):
            pass

    MANIFEST.write_text(json.dumps({
        "generated_by": "tools/build_diagrams.py",
        "count": len(entries),
        "variants": ["light (<id>.svg)", "dark (<id>-dark.svg)",
                     "blank (<id>-blank.svg)"],
        "diagrams": entries,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # ---- summary --------------------------------------------------------
    print()
    print("=" * 66)
    print(f"  scanned   {len(mdx_files)} mdx files, found {len(blocks)} "
          f"DIAGRAM-SPEC blocks")
    print(f"  specs     {len(by_id)} total "
          f"({sum(1 for s in by_id.values() if s.get('_hand'))} hand-authored)")
    print(f"  rendered  {ok} diagrams x 3 variants = {ok * 3} SVGs "
          f"+ {ok} .excalidraw -> {OUT_DIR.relative_to(ROOT)}")
    print(f"  aliased   {aliased} page-referenced names "
          f"({aliased * 4} extra files)")
    print(f"  skipped   {skipped} hand-drawn (left alone)")
    print(f"  failed    {len(errors)}")
    print(f"  warnings  {len(warns)}")
    print("=" * 66)
    for name, why in errors[:40]:
        print(f"  FAIL  {name}: {why}")
    if len(errors) > 40:
        print(f"  ... and {len(errors) - 40} more failures")
    if no_spec:
        print(f"\n  {len(no_spec)} page(s) link a sketch but contain no "
              f"DIAGRAM-SPEC block - their author needs to add one:")
        for n in no_spec:
            print(f"  NOSPEC  {n}")
    for w in warns[:25]:
        print(f"  WARN  {w}")
    if len(warns) > 25:
        print(f"  ... and {len(warns) - 25} more warnings")
    embedded = embed_fonts_everywhere()
    print(f"  fonts     {embedded} SVGs given an embedded subset")
    print(f"\n  manifest  {MANIFEST.relative_to(ROOT)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
