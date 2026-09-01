# Diagram composition brief — READ FIRST

## The problem you are fixing

161 of the course's 173 diagrams are useless. They were "compiled" from English prose
`DIAGRAM-SPEC` blocks by a rule that turns quoted strings into boxes. The result is rows of
identical rectangles containing *the instruction text itself*, truncated mid-word — e.g. a hash
table diagram whose boxes read "Frame 3 (collision, open addressing): same fourth key, but drawn
walking right along the buckets - stroke ① tr". No hash table. No buckets. No collision. Nothing
a learner can look at and understand.

Your job: replace them with real, composed geometry that teaches the concept.

## What "good" looks like

Read `tools/specs/a37-hnsw.json` and `tools/specs/a32-attention.json`. These are hand-authored:
explicit x/y coordinates, real structure (an actual layered graph, an actual 4×4 matrix with
per-cell values), labelled axes, a teacher's margin note, a circled key term.

The test for every diagram: **could a learner who read nothing else look at this picture and
explain the idea?** If it is a row of boxes with words in them, the answer is no.

## The house style (non-negotiable)

Read `PLAN/03-visual-spec.md`. Summary: a good teacher at a whiteboard. Rough work left in,
mistakes crossed out in red rather than erased, amber margin notes in a teacher's voice, the key
term circled, real numbers written in. Never corporate, no gradients, no icon clip-art.

Palette: ink `#1e1e1e`, structure `#1971c2`, correct `#2f9e44`, error `#e03131`, note `#f08c00`,
highlight fill `#ffec99`.

## Spec format

JSON in `tools/specs/<id>.json`, same shape as the flagships. Element types available:
`box, ellipse, line, arrow, path/polyline, text, note, circled, crossout, badge, highlight, bar`.
Full reference: `tools/sketch_spec.md`. Canvas is typically 1000×660.

The build prefers `tools/specs/<id>.json` over the compiled prose block, so writing one replaces
the bad auto-generated diagram with no other change.

## YOU MUST LOOK AT YOUR OWN OUTPUT

This is the rule that matters most. Do not write a spec and assume it renders well.

```bash
source .venv/bin/activate
python3 tools/build_diagrams.py --only <id>
/tmp/svgcheck/shoot.sh <id>          # writes /tmp/svgcheck/<id>.png
```

Then **Read the PNG** with the Read tool and look at it. Iterate until it is genuinely clear.
Check specifically for: text overlapping other elements, leader lines drawn through labels,
text truncated at a box edge, large empty regions, and labels colliding with each other. Those
are the four failure modes in the current output.

## What each diagram needs

1. **Real structure for the concept.** A hash table needs buckets and a chain. A B-tree needs
   nodes and a descent path. A pipeline needs stages with data shapes between them.
2. **Real numbers written in**, taken from the module page's own measured figures.
3. **One amber margin note** in a teacher's voice ("careful — this is where everyone gets it wrong").
4. **One circled key term.**
5. **Where a wrong approach is instructive**, draw it and strike it through in red beside the fix.
6. **Alt text** that describes what the picture shows, not the topic name.

## Reading the source

Each diagram belongs to a module page under `site/curriculum/`. The manifest
(`site/assets/diagram-manifest.json`) maps id → page. **Read that page** before drawing: the
existing `DIAGRAM-SPEC` block states the intent, and the module body has the real numbers.

## Do not

- Do not edit anything under `site/curriculum/` or `site/solutions/` — content is finished.
- Do not touch `tools/sketch.py` or `tools/build_diagrams.py` unless you find a genuine renderer
  bug; if you do, report it rather than silently changing shared code.
- Do not exceed 200 KB per rendered SVG.
