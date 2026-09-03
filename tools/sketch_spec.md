# The sketch spec format

`tools/sketch.py` turns a small declarative spec into three hand-drawn SVGs:

| file | what it is |
|---|---|
| `<id>.svg` | light — paper `#fffdf7`, ink `#1e1e1e` |
| `<id>-dark.svg` | dark — paper `#1a1a19`, ink `#e8e6e3` |
| `<id>-blank.svg` | light, **labels stripped** — the graded draw-from-memory version |

A spec is a JSON object (or a Python dict). Everything is optional except `id`
and `elements`. Coordinates are plain SVG user units with the origin top-left.

```json
{
  "id": "a03-binary-search",
  "title": "Binary search: the window halves",
  "alt": "One sentence of real alt text describing what the sketch shows.",
  "width": 900,
  "height": 560,
  "elements": [ ... ]
}
```

`alt` (or `desc`) becomes the SVG `<desc>`; `title` becomes the `<title>` and is
also hand-written across the top of the sketch with an amber rule under it.
The title survives into the blank variant — everything else labelled does not.

## Determinism

Every stroke's wobble is seeded from `spec.id` + the element's `id` (or its
index, if it has none). **Give elements ids** — then editing element 3 does not
re-roll the jitter on elements 4 through 20, and diffs stay readable.

## Colours

Use palette names, not hex, so light and dark both work:

| name | meaning | light |
|---|---|---|
| `ink` | default stroke and label | `#1e1e1e` |
| `structure` (`blue`) | boxes, the machinery | `#1971c2` |
| `correct` (`green`) | the path that works | `#2f9e44` |
| `error` (`red`) | the bug, the failure mode, a trust boundary | `#e03131` |
| `note` (`amber`) | margin notes, asides, badges | `#f08c00` |
| `highlight` (`yellow`) | the one thing that matters most | `#ffec99` |
| `muted` (`grey`) | captions, sub-labels | `#6b6b6b` |
| `paper` | background | `#fffdf7` |

A raw `#hex` is accepted but skips the dark-theme swap — avoid it.

## Element types

Shared optional keys: `id`, `color`, `width` (stroke weight), `roughness`
(wobble amplitude, default ~2.6), `dashed: true` or `dash: "6 5"`.

| `type` | keys | notes |
|---|---|---|
| `box` (`rect`, `card`) | `x y w h label` `sub` `fill` `fill_color` `fill_gap` `fill_angle` `bold` `size` | `fill` any truthy value gives hachure; label auto-wraps and shrinks to fit |
| `ellipse` (`circle`, `node`) | `cx cy rx ry label fill` | `ry` defaults to `rx` |
| `line` | `x1 y1 x2 y2` `curve` `label` `label_x/label_y` | `curve` bows it (±0.1–0.4 is a natural arc) |
| `arrow` | same as `line`, plus `head` | draws a two-stroke arrowhead at `x2,y2` |
| `text` (`label`) | `x y text` `size` `bold` `anchor` `w` `rotate` | `w` sets the wrap width; a slight random tilt is applied unless you set `rotate` |
| `note` (`margin-note`) | `x y text` `w` `leader: [x, y]` | amber, slanted, teacher's voice; `leader` draws a dashed pointer to what it's about |
| `circled` (`circled-term`) | `x y text` `ring` `rx` `ry` | the term with a lapped ring round it |
| `crossout` (`cross-out`) | `x y w h` `label` `style: "strike"` | red X over the region; `strike` draws one diagonal only |
| `badge` (`step`) | `x y n` `r` | numbered stroke badge ①②③ |
| `highlight` | `x y w h` | highlighter swipe — put it **before** the text it sits behind |
| `bar` | `x y w h` `label` `value` | hachured measurement bar, label left, value right |

Unknown types degrade to a small grey text stub rather than failing the render.

## House rules (from `PLAN/03-visual-spec.md`)

Every sketch must carry at least: **one amber margin note in a teacher's voice**
and **one circled key term**. Where a wrong approach is shown, cross it out in
red rather than omitting it. Hand-write real measured numbers. Leave one thing
unfinished — a dangling dashed arrow into the exercise.

---

## Worked example 1 — a flow with a bug crossed out

```json
{
  "id": "ex1-dangling-pointer",
  "title": "The pointer outlives the frame",
  "alt": "A call chain of three stack frames with a heap block; when the middle frame pops, the pointer still held by the caller is shown turning red.",
  "width": 820, "height": 460,
  "elements": [
    {"type": "badge", "id": "s1", "n": 1, "x": 46, "y": 96},
    {"type": "box", "id": "f-main", "x": 74, "y": 74, "w": 170, "h": 56,
     "label": "main()", "color": "structure"},
    {"type": "box", "id": "f-make", "x": 74, "y": 138, "w": 170, "h": 56,
     "label": "make_buf()", "color": "structure"},
    {"type": "text", "id": "t-stack", "x": 159, "y": 60, "text": "STACK", "size": 16, "color": "muted"},

    {"type": "box", "id": "heap", "x": 470, "y": 138, "w": 190, "h": 66,
     "label": "malloc(1024)", "color": "correct", "fill": "hachure", "fill_color": "correct"},
    {"type": "text", "id": "t-heap", "x": 565, "y": 124, "text": "HEAP", "size": 16, "color": "muted"},

    {"type": "arrow", "id": "a-alloc", "x1": 248, "y1": 166, "x2": 464, "y2": 166,
     "label": "returns a pointer", "color": "correct"},

    {"type": "crossout", "id": "x-pop", "x": 74, "y": 138, "w": 170, "h": 56,
     "label": "frame popped"},
    {"type": "arrow", "id": "a-dangle", "x1": 248, "y1": 190, "x2": 464, "y2": 210,
     "curve": 0.18, "color": "error", "label": "still points here"},

    {"type": "circled", "id": "c-term", "x": 620, "y": 290, "text": "dangling pointer", "ring": "error"},
    {"type": "note", "id": "n1", "x": 60, "y": 300, "w": 250,
     "text": "the memory is fine. The NAME for it is gone. That is the whole bug.",
     "leader": [330, 200]},
    {"type": "arrow", "id": "a-open", "x1": 300, "y1": 400, "x2": 420, "y2": 418,
     "dashed": true, "color": "note", "label": "...so who frees it?"}
  ]
}
```

## Worked example 2 — bars to scale, with real numbers

```json
{
  "id": "ex2-latency",
  "title": "Latency, actually to scale",
  "alt": "Four hachured bars whose lengths are proportional to real access latencies, from L1 cache at one nanosecond to an SSD read at ninety microseconds.",
  "width": 880, "height": 420,
  "elements": [
    {"type": "bar", "id": "b-l1",   "x": 180, "y": 90,  "w": 3,   "h": 22, "label": "L1",   "value": "~1 ns",   "color": "correct"},
    {"type": "bar", "id": "b-l3",   "x": 180, "y": 132, "w": 36,  "h": 22, "label": "L3",   "value": "~12 ns",  "color": "structure"},
    {"type": "bar", "id": "b-dram", "x": 180, "y": 174, "w": 240, "h": 22, "label": "DRAM", "value": "~80 ns",  "color": "note"},
    {"type": "bar", "id": "b-ssd",  "x": 180, "y": 216, "w": 620, "h": 22, "label": "SSD",  "value": "~90 us",  "color": "error"},
    {"type": "note", "id": "n1", "x": 180, "y": 300, "w": 320,
     "text": "the SSD bar is drawn 1000x SHORTER than true scale. It would be 68 metres long. Sit with that."},
    {"type": "circled", "id": "c1", "x": 700, "y": 330, "text": "cache miss"}
  ]
}
```

## Worked example 3 — two panels, right one ticked

```json
{
  "id": "ex3-blocking-vs-async",
  "title": "Blocking vs async: the same 3 requests",
  "alt": "Two timelines side by side; the blocking one is mostly idle waiting, the async one interleaves three requests into a third of the wall clock.",
  "width": 900, "height": 480,
  "elements": [
    {"type": "text", "id": "h1", "x": 230, "y": 80, "text": "blocking", "size": 22, "bold": true, "color": "error"},
    {"type": "bar", "id": "p1", "x": 90, "y": 100, "w": 200, "h": 18, "value": "waiting", "color": "error"},
    {"type": "bar", "id": "p2", "x": 90, "y": 128, "w": 200, "h": 18, "value": "waiting", "color": "error"},
    {"type": "bar", "id": "p3", "x": 90, "y": 156, "w": 200, "h": 18, "value": "waiting", "color": "error"},
    {"type": "text", "id": "t1", "x": 200, "y": 200, "text": "900 ms wall clock", "size": 18},

    {"type": "text", "id": "h2", "x": 680, "y": 80, "text": "async", "size": 22, "bold": true, "color": "correct"},
    {"type": "bar", "id": "q1", "x": 540, "y": 100, "w": 200, "h": 18, "value": "await", "color": "correct"},
    {"type": "bar", "id": "q2", "x": 560, "y": 128, "w": 200, "h": 18, "value": "await", "color": "correct"},
    {"type": "bar", "id": "q3", "x": 580, "y": 156, "w": 200, "h": 18, "value": "await", "color": "correct"},
    {"type": "highlight", "id": "hl", "x": 600, "y": 186, "w": 190, "h": 26},
    {"type": "text", "id": "t2", "x": 695, "y": 205, "text": "310 ms wall clock", "size": 18, "bold": true},

    {"type": "circled", "id": "c1", "x": 450, "y": 300, "text": "concurrency != parallelism"},
    {"type": "note", "id": "n1", "x": 90, "y": 360, "w": 300,
     "text": "nothing got faster. The waiter stopped standing still. One CPU, three tables."}
  ]
}
```

## Running it

```bash
python3 tools/sketch.py my-spec.json assets/diagrams/   # one spec -> 3 SVGs
python3 tools/sketch.py --selftest                           # renders + checks XML/size
python3 tools/build_diagrams.py                              # the whole course
```

## TEXT_SCALE — read this before positioning anything by coordinate

`tools/sketch.py` defines `TEXT_SCALE = 1.45`. Caveat has a small x-height for its nominal size,
so a 15 px label reads closer to 11 px of a normal face; every text size is multiplied by this
constant at emission so one knob controls legibility everywhere.

**What this means when you author by coordinate:**

| You write | What actually renders |
|---|---|
| `"size": 15` | ~21.8 px |
| `"size": 18` (default) | ~26.1 px |
| line step in a `note` or multi-line label | `size × lh × 1.45` — about `1.67 × size`, not `1.15 × size` |
| wrap width | computed against the scaled width, so labels wrap sooner than the raw size suggests |

This is the single biggest cause of unexpected overlap. A two-line box label needs
`h ≥ size × 3.34 + 10`. Budget roughly 1.5× the vertical room you would guess from the raw size.

## Two behaviours worth knowing

- **`note` blocks are vertically centred on `y`, not top-anchored**, and carry a default tilt of
  −3.5° to −1.2°. On a wide note the tilt lifts the far end by `w · sin θ` — around 20 px on a
  400 px note. Set `"rotate": -1.2` explicitly on wide notes to make them predictable.
- **`crossout` defaults to `style: "x"`**, whose diagonals sweep about 6 px past the region on
  both sides; on a wide box the legs cross neighbouring elements. Prefer `style: "strike"`
  whenever the crossed-out content is wider than it is tall.
