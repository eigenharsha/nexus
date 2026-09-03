# Nexus — Course Content Production Spec (v1)

This is the contract every lesson file must satisfy. No content gets written until it maps to this spec.
If a lesson does not have all 10 sections below, it is **not done**.

---

## 1. Who we are writing for

| # | Persona | Name we use internally | Starting point | What "success" means for them |
|---|---|---|---|---|
| P1 | College student, beginner in AI | **Aarav** (3rd-year CS student) | Can use a computer. May have seen one `for` loop. No job experience. Learns 12–15 h/week. | Can build + explain a working system in an interview, and defend design choices. Gets an internship/first job. |
| P2 | Working professional | **Meera** (5 yrs backend/data/QA/analyst experience) | Ships code at a job. Weak on ML/AI internals, strong on delivery pressure. Learns 5–7 h/week, mostly nights/weekends. | Can take a Monday-morning problem at work and solve it with what she learned last night. Moves into an AI/ML role internally. |

**Every lesson must serve both.** The mechanism is the 3-layer structure below — Aarav walks Layer 1 fully and attempts Layer 2; Meera skims Layer 1, lives in Layer 2, and stretches into Layer 3.

---

## 2. The 3-layer model (non-negotiable structure)

Every topic — no exceptions, including "easy" ones — is written three times, at three altitudes.

### Layer 1 — **GROUND** (Beginner)
- **Assumes:** nothing. Every term defined at first use. No unexplained jargon, ever.
- **Voice:** patient, concrete, analogy-first. "Imagine a locker room…" then the real definition.
- **Contains:** the mental model, one physical/visual analogy, the smallest possible working example (runs in < 60 s), a line-by-line walkthrough of that example, and a *guided* lab where 60% of the code is given.
- **Length target:** 1,200–1,800 words of *prose* + 1 diagram + 1 runnable snippet.
- **Exit test:** a beginner can re-explain the idea to a friend without notes.

### Layer 2 — **BUILD** (Experienced / practitioner)
- **Assumes:** Layer 1 is understood; reader has shipped software before.
- **Voice:** direct, trade-off driven, production-oriented. Names real tools, real versions, real defaults.
- **Contains:** the proper theory (with the math where math is the point), the API/library surface used in industry, 2–4 design trade-offs written as "choose X when…, choose Y when…", a realistic failure story, and an *unguided* lab with acceptance criteria + tests.
- **Length target:** 1,800–2,800 words of *prose* + 1 architecture diagram + a full working reference implementation.
- **Exit test:** the reader can implement it at work without opening docs for the happy path.

### Layer 3 — **EDGE** (Expert)
- **Assumes:** Layer 2 shipped and hurt.
- **Voice:** peer-to-peer, no hand-holding. Cites papers, source code, RFCs, benchmark numbers.
- **Contains:** internals (what the library actually does under the hood), behavior at scale (10×/100×/1000× load or data), the failure modes that only show up in production, cost/latency/memory math, and a **stretch challenge** that has no single right answer.
- **Length target:** 1,200–2,000 words of *prose* + measurement/benchmark exercise.
- **Exit test:** reader can review someone else's design and find the flaw; can answer a senior/staff interview question on it.

> **Rule:** Layers are *cumulative depth on the same topic*, not three different topics. If Layer 3 introduces a brand-new concept the earlier layers never touched, it's mis-scoped.

---

## 3. Mandatory lesson file template

Every `content/**/LNN-*.md` file has exactly these sections, in this order:

```
# <Lesson title>
> Week X · Module Y · Lesson Z · ~<N> min read + ~<M> min lab

## 0. Where this sits
- Prereqs: <lesson IDs>
- Unlocks: <lesson IDs>
- One-line: <what you will be able to do after this>

## 1. Why you should care
### For Aarav (student)  — 3 bullets, one of them an interview/placement angle
### For Meera (professional) — 3 bullets, one of them a "this shows up in your job as…" angle

## 2. The mental model            <- the single idea, in <=120 words + 1 diagram

## 3. LAYER 1 — GROUND (Beginner)
   3.1 Plain-English explanation
   3.2 Analogy
   3.3 Smallest working example (runnable)
   3.4 Line-by-line walkthrough
   3.5 Guided practice (scaffolded, answers provided)
   3.6 Checkpoint: 5 self-check questions + answers

## 4. LAYER 2 — BUILD (Experienced)
   4.1 The real theory / the real math
   4.2 The production API surface (tool, version, idiomatic usage)
   4.3 Trade-offs table: choose X when… / choose Y when…
   4.4 Reference implementation (complete, tested)
   4.5 What breaks in the real world (a short war story)
   4.6 Checkpoint: design question + model answer

## 5. LAYER 3 — EDGE (Expert)
   5.1 Under the hood (internals / source / spec)
   5.2 At scale: numbers, limits, cost & latency math
   5.3 Production failure modes + how you detect them
   5.4 Frontier / research pointers (papers, with the one-line takeaway of each)
   5.5 Stretch challenge (open-ended, no single right answer)

## 6. HANDS-ON LAB   <- see section 4 of this spec for the lab contract

## 7. Apply it at work on Monday
   - Student version: portfolio/resume framing + how to talk about it
   - Professional version: 3 concrete places in a normal job where this plugs in

## 8. Common mistakes & debugging playbook   <- symptom -> cause -> fix table

## 9. Assessment
   - 8 concept questions (MCQ/short) with answers
   - 1 coding challenge with hidden tests
   - 3 interview questions (junior / mid / senior phrasing of the same topic)
   - 1 "draw it from memory" diagram reproduction task

## 9b. The whiteboard
   - The full sketch set for this module (see PLAN/03-visual-spec.md for tiers)
   - "Draw it yourself" prompt + a blank (unlabelled) version of the key diagram
   - Link to the editable .excalidraw source

## 10. Sources & further reading
   Three buckets, each entry with a one-line "read this for…":
   - **Primary docs** — official documentation / specs / RFCs, version-pinned
   - **Papers** — the paper(s) the idea comes from, with the one-sentence takeaway
   - **Go deeper** — the single best book chapter, lecture or blog post, and why
   Nothing goes in this section that the author has not actually read.
```

**Every section from 3 to 5 opens with its diagram.** Prose supports the picture, not the reverse — see `PLAN/03-visual-spec.md`.

---

## 4. Hands-on lab contract

Every lesson ships a lab. Every lab must have:

1. **`README.md`** — problem statement written as a ticket, not as homework ("Payments team is seeing duplicate charges under load. Fix it.").
2. **Starter repo** — `labs/<phase>/<week>/<lab-id>/` with `starter/` and `solution/`.
3. **Three difficulty tracks in the same lab**, so one lab serves all three layers:
   - `basic/` — scaffolded, TODOs marked, ~60% written for you.
   - `standard/` — spec + tests only, you write the implementation.
   - `hard/` — spec + a performance/scale/robustness constraint that the standard solution fails.
4. **Automated acceptance tests** (`pytest`/`bats`/`make verify`) so the learner self-grades with no instructor.
5. **Rubric** — 0/1/2/3 scoring across: correctness, code quality, performance, explanation.
6. **Time box** — an honest estimate. If it's 6 hours, say 6 hours.
7. **"Ship it" step** — every lab ends with something committed, containerized, deployed, or measured. Never ends at "it printed the right thing".

**Portfolio rule:** at least one lab per *week* must be publishable to GitHub with a written README the learner can link from a resume.

---

## 5. Quality bar (reject criteria)

A lesson is rejected in review if any of these are true:
- [ ] Any code block that was never executed.
- [ ] Any claim about performance/cost with no number attached.
- [ ] Layer 1 uses a term not defined in Layer 1.
- [ ] Layer 3 is just Layer 2 with harder words.
- [ ] The lab can be passed by copy-pasting the lesson's reference implementation.
- [ ] Fewer than one hand-drawn sketch per module, or a diagram that is not in the house style.
- [ ] A "hero concept" (see visual spec §6) shipped without its animation.
- [ ] No paper or primary source cited on a topic that has one.
- [ ] A cited source the author did not read.
- [ ] "Apply it at work" is generic ("this is useful in many companies").
- [ ] Tool versions unpinned.
- [ ] No failure mode discussed.

---

## 5b. How to count length (corrected 2026-09-01)

The per-layer targets above count **prose only** — the sentences that explain. They do **not**
count code blocks, tables, `DIAGRAM-SPEC` blocks, the assessment bank, the checkpoint answers,
or the common-mistakes table. Those are mandated separately by the §3 template and are not padding.

A complete module page that satisfies the full 10-section template therefore lands at roughly
**5,500–8,000 total words**, of which **4,000–5,000 is prose**. That is expected and correct.

Two independent authors flagged the original target as unreachable while meeting the other
non-negotiables. They were right. Never trim a section the template requires in order to hit a
word count — cut repetition instead, and if a page is genuinely bloated it will show up as
prose that restates the tables rather than as a high total.

## 5c. Number provenance (added 2026-09-01, after a course-wide audit)

Every numeric claim must be labelled as one of three classes. The learner-facing statement of
this policy is `start/about-the-numbers.mdx`; this section is the authoring rule.

| Class | Means | Test |
|---|---|---|
| **Measured** | Actually executed, here, and reproducible by the learner | The toolchain is installed and the artifact exists |
| **Derived** | Computed from first principles; arithmetic shown term by term | A reader can check it with a pencil |
| **Cited finding** | Someone else measured it; we are reporting their result | Names who measured it, and where |
| **Reference figure** | Modelled from published benchmarks or vendor specs | Right ratio, wrong decimal |

**Cited finding** is the class for a result taken from the literature — "SMOTE rarely beats class
weights" from Elor & Averbuch-Elor 2022, say. It outranks a reference figure, because a real
experiment stands behind it, but it is not ours and must never be dressed as ours. Attribute it.

### Telling a real negative result from a borrowed one

They look identical on the page, and only the first is worth what it claims. Five tells:

1. **Does the result move with this dataset's specifics?** A measured SMOTE loss interacts with
   prevalence, `n` and the classifier. A borrowed claim states a direction and stops.
2. **Is seed or fold variance attached?** Whoever ran it has a spread. A borrowed conclusion
   arrives as a bare point estimate, because the source's variance was never theirs to quote.
3. **Precision that is awkward to invent.** `+0.0031 AP, CI crossing zero` is the shape of a real
   null. Round numbers and canonical phrasings are the shape of a remembered one.
4. **Does the harness exist?** The lab or solution should contain the comparison as runnable code,
   not just its verdict.
5. **An adjacent citation is a tell in the wrong direction.** A paper reference next to a negative
   result more often means the conclusion came *from* the paper than that it was independently
   confirmed.

**Never write "measured" for something you did not run.** An audit of the first build relabelled
roughly 285 claim sites, including invented GPUs (RTX 4090, A100, H100, A10G), a 1,000-PDF corpus
that never existed, CI pipelines that never ran, and — the subtlest case — *invented elapsed
time*: "measured over four months" for a system that was never deployed.

### The evidentiary rule

> A Postgres container is ephemeral and leaves no trace when torn down, so its absence proves
> nothing. A pip install into a persistent venv leaves a trace by default. **Absence of a Python
> package from a venv whose siblings all persisted is evidence; absence of a running service is
> not.**

This is a sharper test than "could this have run on this machine", and it is the rule that
distinguishes a genuine measurement whose environment is gone from a fabricated one.

**Apply it only after an exhaustive search.** This rule produced one wrong verdict during the
audit because the search behind it was too narrow: two venvs were checked when ten existed. A
week-18 claim was downgraded, then reinstated when `lightgbm 4.7.0` and `umap-learn 0.5.12` turned
up in `/private/tmp/nexus-env` at exactly the cited versions. Before concluding a package was
never installed:

**enumerate the environments first, then look inside them:**

```bash
# find every environment, then read its parent - depth is what matters
find / -maxdepth 10 -type d -name site-packages 2>/dev/null
```

Search depth is the whole game. On this machine `-maxdepth 5` finds **3** site-packages
directories; `-maxdepth 10` finds **96**. A venv nested one level deeper than you guessed is
invisible, and that is exactly how the wrong verdict happened. Do not reach for a path list
instead — on macOS `/tmp` is a symlink to `/private/tmp`, so searching both double-counts and
gives a false sense of coverage while the real gap (depth) stays open.

Then confirm the **version matches** what the page cites. A package present at a different
version in an unrelated project is not evidence that this page's number was measured. The rule is
sound; the evidence it consumes has to be complete.

**A version mismatch can be evidence *for* a measurement, not against it.** Some lessons are
*about* version drift — Week 20's pickle-fragility module requires deliberately breaking a
serialized pipeline across a library upgrade, so a page there citing scikit-learn 1.5.2 against
the 1.9.0 used everywhere else is doing its job. During the audit a second environment
(`/private/tmp/nexus-old`: numpy 2.0.2, scikit-learn 1.5.2, pandas 2.2.3) appeared for exactly
this purpose. Read the *pair* of environments before judging: an old-version venv sitting beside
the current one is positive evidence that a compatibility demonstration was really run. Applying
the mismatch rule naively here would reach precisely the wrong verdict.

### Two corollaries

1. **Corrections run both ways.** Four claims moved *up* to Derived during the audit — UTF-8 byte
   counts, IEEE-754 results and a FLOP count are fixed by standards, so "measured" was
   *understating* them. A reader can reproduce the digits, not merely the magnitude.
2. **An anecdote is not a fabrication.** A third-person industry story carrying a timeline
   ("a team retrained monthly for two years") is a standard teaching device and claims nothing
   about our own system. Only a *measurement label* on a history that never happened is a
   fabrication. Do not strip the anecdotes.

## 6. Conventions

- **Python** 3.12 · **uv** for envs · `ruff` + `mypy` · `pytest`
- **C** C17, gcc/clang, `-Wall -Wextra -fsanitize=address`
- **Node** 20 LTS for the JS week
- **Postgres** 16 · **Docker** 24+ · **Kubernetes** via `kind`
- **PyTorch** 2.x · **transformers** / **peft** / **trl** pinned in each lab's `requirements.txt`
- Diagrams: **Excalidraw hand-drawn house style** (`PLAN/03-visual-spec.md`) as the default; Mermaid only for large structural graphs. Light + dark SVG exports, `.excalidraw` source committed.
- Every runnable artifact must work on **macOS (Apple Silicon)** and **Linux x86-64**; GPU labs must have a CPU/Colab fallback path.
- Cost rule: the whole 32 weeks must be completable for **< $50** of cloud spend. Anything expensive gets a free-tier or local alternative documented.

---

## 7. Weekly rhythm (what a learner actually does)

| Day | Student (12–15 h/wk) | Professional (5–7 h/wk) |
|---|---|---|
| Mon–Tue | Layer 1 + Layer 2 reading | Layer 2 reading only |
| Wed–Thu | Lab `basic` → `standard` | Lab `standard` |
| Fri | Layer 3 + stretch | Layer 3 skim |
| Sat | Lab `hard` + push to GitHub | Lab `hard` (optional) |
| Sun | Assessment + spaced-repetition deck | Assessment |

Each week also produces: **1 flashcard deck (Anki-format)**, **1 "explain it in 5 minutes" recording prompt**, and **1 peer-review task**.
