# The sketch set

Every SVG in this directory is **generated**. Do not hand-edit the `.svg` files —
the next build overwrites them. Edit the source, or replace the sketch entirely
(see "Replacing a generated sketch" below).

Each diagram ships as three files:

| file | use |
|---|---|
| `<id>.svg` | light theme — paper `#fffdf7`, ink `#1e1e1e` |
| `<id>-dark.svg` | dark theme — paper `#1a1a19`, ink `#e8e6e3` |
| `<id>-blank.svg` | **labels stripped**, for the graded "draw it from memory" exercise in §9b of every lesson |
| `<id>.excalidraw` | editable scene, what the "Editable source" link on each page points at — open it at excalidraw.com |

**Two names per diagram.** The canonical artifact is named after the
DIAGRAM-SPEC `id` (`p1-w01-m4.svg`), but the lesson pages were generated with a
filename derived from the module title (`algorithms-asymptotic-complexity.svg`).
The build publishes the same bytes under both, reading the alias straight out of
each page's `src="/assets/diagrams/..."` references — so if an author renames a
module and regenerates the shell, the next build follows the rename with no edit
here. The manifest records the alias list for every diagram.

`../diagram-manifest.json` lists every diagram with its id, title, alt text,
tier, source page and the three file paths. It is regenerated on every build.

## Regenerating

```bash
python3 tools/make_flagships.py       # rebuild the hand-authored flagship specs
python3 tools/build_diagrams.py       # render everything into this directory
python3 tools/build_diagrams.py --prune   # ...and delete anything stale
python3 validate.py              # must still report 0 errors
```

`build_diagrams.py` takes two inputs:

1. **`{/* DIAGRAM-SPEC ... */}` blocks** in `curriculum/**/*.mdx`. Their
   `elements:` list is English prose, not geometry, so the build *compiles* it
   into a sketch: quoted strings become boxes, `a -> b -> c` becomes a flow row,
   "amber margin note" becomes a margin note, "circled" becomes a circled term,
   "crossed out" draws a red X. It is honest, on-style and mechanical.
2. **Hand-authored JSON specs** in `tools/specs/`, written by
   `tools/make_flagships.py`. These always win over an auto-compiled block with
   the same `id`, and they are what the flagship diagrams look like when
   somebody actually places the geometry.

Useful flags:

```bash
python3 tools/build_diagrams.py --list           # parse only: what would render
python3 tools/build_diagrams.py --only a32-attention
python3 tools/sketch.py --selftest               # renderer smoke test
python3 tools/sketch.py my-spec.json out-dir/    # one spec -> 3 SVGs
```

The build never crashes on a bad block: it collects failures and prints a
summary. If your diagram did not appear, run `--list` and read the WARN lines.

## Which ones are hand-placed

These twelve have real geometry and are the reference for the house style:

`a01-stack-heap` · `a03-binary-search` · `a05-git-dag` · `a07-blocking-vs-async`
· `a12-btree-vs-scan` · `a15-memory-hierarchy` · `a18-gradient-descent` ·
`a28-backprop` · `a32-attention` · `a35-lora` · `a37-hnsw` ·
`a41-prompt-injection`

Everything else is auto-compiled and should be treated as a **good placeholder**:
correct content, correct palette, correct wobble, but a column-of-rows layout
rather than a composed picture. Upgrade them in the order the lessons need them.

## Improving a generated sketch (still generated)

Write a JSON spec and drop it in `tools/specs/<id>.json`, using the same `id` as
the DIAGRAM-SPEC block you want to replace. The format is documented with three
worked examples in **`tools/sketch_spec.md`**. Then:

```bash
python3 tools/build_diagrams.py --only <id>
```

For anything with a loop, a grid or bars-to-scale, add a function to
`tools/make_flagships.py` (or `tools/flagships_b.py`) instead and let Python
compute the coordinates — that is how the attention matrix and the latency bars
are built.

## Replacing a generated sketch by hand (Excalidraw)

When a sketch needs a human — a spatial metaphor, an illustration, anything the
compiler cannot infer — draw it in Excalidraw and check the export in here.

**Start from the generated scene, don't start from blank.** Every diagram already
ships a `<id>.excalidraw` (and a copy under the page's own filename) exported by
`tools/excalidraw.py` with the house style applied — hand-drawn font, hachure
fills, bold strokes, roughness 1. Drag it onto [excalidraw.com](https://excalidraw.com) and edit
what is wrong.

1. If you really are starting blank, open [excalidraw.com](https://excalidraw.com). Set the sidebar to the house style before you
   draw anything:
   - **Stroke** `#1e1e1e` for ink, `#1971c2` structure, `#2f9e44` correct,
     `#e03131` error, `#f08c00` margin notes, `#ffec99` highlighter fill
   - **Fill** → *Hachure* (never solid), **Stroke width** → *Bold*,
     **Sloppiness** → the middle setting (1–2), **Edges** → *Round*
   - **Font** → *Hand-drawn* (Excalifont/Virgil). Never Helvetica inside a sketch.
   - **Canvas background** `#fffdf7`
2. Draw it, then apply the authenticity rules from `PLAN/03-visual-spec.md` §4:
   cross out the wrong version in red rather than deleting it, add at least one
   amber margin note in a teacher's voice, circle the key term the first time it
   appears, number the strokes ①②③ where order matters, hand-write the real
   measured numbers, and leave one dangling "…and then?" arrow into the exercise.
3. Export three files with **File → Export image**, *SVG*, "background" on,
   "embed scene" **on** (that makes the SVG re-editable):
   - `<id>.svg` — light
   - `<id>-dark.svg` — switch Excalidraw to dark theme first, or tick *Dark mode*
     in the export dialog
   - `<id>-blank.svg` — delete every text element, keep the shapes, export again
4. Save the editable source as `<id>.excalidraw` **next to the SVGs in this
   directory**, overwriting the generated one. A diagram nobody can edit is
   technical debt.
5. Add `<id>` to the `HAND_DRAWN` set at the top of `tools/build_diagrams.py`
   so the build skips it and never overwrites your files. Re-run the build and
   confirm the summary line `skipped   N hand-drawn (left alone)` counts it.
6. Open both SVGs, confirm the `<title>` and `<desc>` elements carry real alt
   text — Excalidraw does not write them, so add them by hand:

   ```xml
   <title>Self-attention: the matrix and the causal mask</title>
   <desc>A four-by-four attention matrix for the sentence "the cat sat down"…</desc>
   ```

7. Re-run `python3 validate.py` and confirm 0 errors.

## Rules that are not negotiable

- Every SVG carries a `<title>` and a `<desc>` with a real sentence of alt text.
  Not "diagram of attention".
- Never encode meaning in colour alone: pair red with a ✗, green with a ✓, and
  label the lines.
- Under 200 KB per sketch. The build fails a diagram that goes over.
- No gradients, no drop shadows, no 3-D, no stock icons, no perfectly aligned
  boxes.
- Fonts are loaded from Google Fonts via an `@import` inside each SVG
  (`Caveat`, then `Kalam`, then `cursive`). No font binaries are embedded; a
  reader offline gets the cursive fallback and the sketch still reads.
