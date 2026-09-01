# Nexus content-production brief — READ THIS FIRST

You are writing production course content for **Nexus**, a 32-week curriculum taking absolute
beginners to expert level in systems, ML and distributed AI. Read these three files before
writing anything:

1. `PLAN/00-content-spec.md` — the lesson contract. Non-negotiable.
2. `PLAN/03-visual-spec.md` — the hand-drawn diagram house style.
3. `PLAN/tasks/phase-N-tasks.md` — the exact module list, layer angles, labs and references for your weeks.

## Your two readers (every page serves both)

- **Aarav** — 3rd-year CS student, beginner in AI, no job experience, 12–15 h/week.
- **Meera** — engineer with ~5 years' experience, thin on ML internals, 5–7 h/week, has a backlog.

## The three layers (the whole point of this course)

- **Layer 1 GROUND** — assumes nothing, defines every term at first use, one analogy, smallest
  runnable example, line-by-line walkthrough, guided practice.
- **Layer 2 BUILD** — real theory, real tools with pinned versions, a trade-offs table
  ("choose X when… choose Y when…"), a complete tested reference implementation, one true war story.
- **Layer 3 EDGE** — internals, behaviour at scale, **every claim carries a measured number**,
  production failure modes, papers, and an open-ended stretch challenge.

Layers are cumulative depth on ONE topic. If Layer 3 introduces a new topic, it's wrong.

## Where you write

Files already exist as shells at `site/curriculum/pN/week-NN/*.mdx`. **Edit them in place.**
Keep the frontmatter (title/description/icon). Replace the placeholder body with real content
following the shell's existing structure (Tabs for the three layers, Hands-on, The whiteboard,
Apply it at work, Common mistakes, Sources).

**Add the literal line `{/* AUTHORED */}` immediately after the frontmatter** — this marks the
page as owned by you so the generator never overwrites it.

## MDX rules (Mintlify) — violating these breaks the build

- Mintlify components available: `<Note> <Warning> <Tip> <Info> <Check>`, `<Card> <CardGroup>`,
  `<Accordion> <AccordionGroup>`, `<Steps> <Step>`, `<Tabs> <Tab>`, `<Frame>`, `<CodeGroup>`,
  `<Expandable>`, `<ParamField>`, `<ResponseField>`, `<Columns>`.
- Curly braces in prose must be escaped as `&#123;` `&#125;` — but braces inside fenced code
  blocks are fine. A raw `{` in prose is a build error.
- `<` in prose must be `&lt;` (e.g. "less than 500 ms" or `&lt;500 ms`). Inside code fences it's fine.
- `cols={2}` inside a component prop is valid JSX and fine.
- Mermaid diagrams: use a ```mermaid fenced block. They render natively.
- Every page needs an `## ` heading structure; don't use `# ` (the frontmatter title is the h1).

## Quality bar — these are auto-reject conditions

- Any code block you did not mentally execute / could not run.
- Any performance or cost claim without a number.
- A term used in Layer 1 that Layer 1 never defined.
- Layer 3 that is Layer 2 in harder words.
- A "war story" or "apply at work" that is generic ("this is used at many companies").
- Unpinned tool versions.
- No failure mode discussed.
- A cited paper with no one-sentence takeaway.

## Diagrams

Every module needs at least one hand-drawn sketch. You do **not** draw it — you write the
**diagram spec** so the diagram agent can render it. In the module page, keep the `<Frame>`
block pointing at `/assets/diagrams/<slug>.svg`, and add an HTML comment block immediately
after it in this exact format:

```
{/* DIAGRAM-SPEC
id: <module-id>
tier: T1|T2|T3|T4
one-sentence-goal: <the single thing this picture must make obvious>
elements:
  - box "label" at top-left
  - arrow from X to Y labelled "..."
  - red cross-out over Z  (the wrong approach)
  - amber margin note: "careful — this is where everyone gets it wrong"
numbers-to-write-in: <real measured values that must appear in the sketch>
alt: <full-sentence alt text>
*/}
```

Style is always: whiteboard marker weight, visible wobble, rough work left in, mistakes crossed
out in red not erased, teacher's margin notes in amber, the key term circled.

## Length target per module page

2,500–4,500 words total across the three layers. Dense, not padded. Code blocks count little
toward that; prose that explains *why* counts most.

## Tone

A very good engineer explaining something to one person they respect. Direct. Specific.
No hype, no "in today's fast-paced world", no filler transitions, no emoji in prose.
Concrete numbers and named tools beat adjectives every time.

## When you finish a week

Run `cd site && python3 -c "import pathlib,sys;[print(p) for p in pathlib.Path('.').rglob('*.mdx') if '{' in p.read_text().split('---',2)[-1].replace('{/*','').replace('*/}','') and False]"` — or
more simply, sanity-check that every file you touched has: the AUTHORED marker, balanced
component tags, no raw `{` or `<` in prose outside code fences.

Report back: which files you completed, total word count, and anything in the task file you
judged wrong and changed (and why).
