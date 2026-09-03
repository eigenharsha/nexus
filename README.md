# Nexus — Systems, Machine Learning & Distributed AI

A 32-week curriculum taking absolute beginners to production-ready systems and AI engineering
mastery. Every topic is written at **three depths** and ends in something built, measured and
defended.

## Repository layout

```
.
├── PLAN/                       # the production plan — the source of truth
│   ├── 00-content-spec.md        the lesson contract (3 layers, template, reject criteria)
│   ├── 01-master-board.md        level 0–2 tasks: infrastructure, phases, weeks
│   ├── 02-references-library.md  citation rules (library lives in reference/papers.mdx)
│   ├── 03-visual-spec.md         hand-drawn diagram house style, 42 hero animations, 15 widgets
│   └── tasks/                    level 3–4 tasks: every module, its three layers, its lab
│       ├── phase-1-tasks.md      weeks 1–8   · foundations
│       ├── phase-2-tasks.md      weeks 9–16  · systems & data
│       ├── phase-3-tasks.md      weeks 17–24 · machine learning
│       └── phase-4-tasks.md      weeks 25–32 · generative AI
├── docs.json                   # Mintlify navigation, generated — includes hidden tabs/groups
├── generate.py                 # rebuilds page shells + docs.json from PLAN/tasks/
├── curriculum/pN/week-NN/      # 5 module pages + index + lab per week
├── solutions/                  # hidden pages: worked solutions and answer keys
├── instructor/                 # hidden pages: session plans, rubrics, release schedule
├── assets/diagrams/            # hand-drawn SVGs (light, dark, blank) + editable sources
├── labs/pN/week-NN/            # 32 labs · basic / standard / hard · make verify
├── templates/                  # lesson and lab templates
├── tools/                      # the hand-drawn sketch renderer and diagram build
├── bootstrap.sh                # environment installer (macOS ARM + Linux)
└── AGENT-BRIEF.md              # the brief every content author works from
```

## The three layers

Every topic is written three times:

- **🟢 Ground** — assumes nothing. Every term defined at first use. Guided practice.
- **🔵 Build** — real tools, real versions, trade-offs, a tested reference implementation.
- **🟣 Edge** — internals, scale, cost arithmetic, production failure modes, papers.

A first-year student and an engineer with eight years of experience read the same page and both
get their money's worth.

## Running the site

```bash
npx mint dev          # local preview at http://localhost:3000
python3 generate.py   # rebuild shells + docs.json from PLAN/tasks/
```

Pages containing `{/* AUTHORED */}` are owned by their author and are never regenerated.

## Hidden pages

The site uses [Mintlify hidden pages](https://www.mintlify.com/docs/organize/hidden-pages) for
three things:

| Use | Mechanism |
|---|---|
| Solutions and answer keys | `hidden: true` in frontmatter, linked from each module and lab |
| Instructor guide | a `"hidden": true` tab in `docs.json` |
| Drip release of future weeks | `"hidden": true` on the week's group; bump `RELEASED_THROUGH_WEEK` in `generate.py` to release |

Hidden is **not** private — anyone with the URL can read the page. Never put confidential
material on one.

## Diagrams

The house style is a whiteboard: hand-drawn, visible wobble, rough work left in, mistakes
crossed out in red rather than erased, teacher's margin notes in amber. Lesson authors write a
`DIAGRAM-SPEC` block; `tools/build_diagrams.py` renders light, dark and blank (unlabelled)
variants. The blank variant powers the weekly graded "draw it from memory" exercise.

## Labs

One lab per week, three tracks from the same problem:

```bash
cd labs/p1/week-01
make verify              # green on solution, red on starter
make verify TRACK=basic
```

Every lab ends in a **ship it** step — committed, deployed, containerized or measured.
