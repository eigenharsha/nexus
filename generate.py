#!/usr/bin/env python3
"""
Generate the Nexus Mintlify docs site from PLAN/tasks/phase-*-tasks.md.

The task files are the single source of truth. Re-running this script rebuilds
every page shell and docs.json navigation without touching hand-written prose
that lives in `_body` blocks (see BODY_MARKER).

Hidden pages (https://www.mintlify.com/docs/organize/hidden-pages) are used for:
  - solution pages + answer keys        -> hidden: true, still in docs.json
  - instructor notes                    -> hidden tab
  - unreleased weeks (drip release)     -> hidden group, flipped as the cohort advances
"""
from __future__ import annotations
import json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS = ROOT / "PLAN" / "tasks"
SITE = ROOT

BODY_MARKER = "{/* --- hand-written body below this line is preserved on regeneration --- */}"
# A page containing this marker is owned by a human/agent author and is never regenerated.
AUTHORED_MARKER = "{/* AUTHORED */}"

WEEK_RE = re.compile(r"^## T-(P\d)-W(\d{2}) — Week (\d+): (.+)$")
MOD_RE = re.compile(r"^### `(P\d-W\d{2}-M\d)` — (.+)$")
LAB_RE = re.compile(r"^### `(LAB-P\d-W\d{2})` — \*\*(.+?)\*\*$")
FIELD_RE = re.compile(r"^- \*\*(L1 Ground|L2 Build|L3 Edge|VIS|REF|Hands-on|Ship it)\:?\*\*:?\s*(.+)$")
MICRO_RE = re.compile(r"^- Micro-lessons: (.+)$")
TRACK_RE = re.compile(r"^- `(basic|standard|hard)`: (.+)$")
OUTCOME_RE = re.compile(r"^\*\*Week outcome:\*\* (.+)$")

PHASE_TITLES = {
    "P1": "Phase 1 · Foundations",
    "P2": "Phase 2 · Systems & Data",
    "P3": "Phase 3 · Machine Learning",
    "P4": "Phase 4 · Generative AI",
}
# Extra pages inserted at the front of a week, ahead of its modules.
# Weeks 11-12 use NumPy on nearly every page but NumPy is not taught until
# week 16 - a real ordering fault found in a beginner read-through. Rather than
# reorder two phases, the week opens with a scoped primer.
PRIMERS = {
    11: ["curriculum/p2/week-11/0-numpy-in-20-minutes"],
    16: ["curriculum/p2/week-16/0-scikit-learn-just-enough"],
}

# Extra module pages appended after a week's five modules. Week 25 gained one
# in a Phase 4 coverage review: the 2025-26 reasoning-model shift (adaptive
# thinking, effort, task budgets, context editing) was absent from a course that
# teaches LLM engineering, and it changes cost, prompting and agent design.
EXTRAS = {25: ["curriculum/p4/week-25/6-reasoning-effort-and-thinking-budgets"]}

# Weeks released to the cohort. Everything after this is a hidden group.
RELEASED_THROUGH_WEEK = 32


def slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[`*_]", "", text)
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return re.sub(r"-{2,}", "-", text)[:60]


def esc(text: str) -> str:
    """Make a markdown fragment safe to drop into MDX prose."""
    return text.replace("{", "&#123;").replace("}", "&#125;").replace("<", "&lt;")


def parse(path: Path) -> list[dict]:
    weeks: list[dict] = []
    week = mod = lab = None
    for raw in path.read_text().splitlines():
        line = raw.rstrip()
        if m := WEEK_RE.match(line):
            week = {"phase": m[1], "num": int(m[3]), "id": f"{m[1]}-W{m[2]}",
                    "title": m[4].strip(), "outcome": "", "modules": [], "lab": None}
            weeks.append(week); mod = lab = None
            continue
        if week is None:
            continue
        if m := OUTCOME_RE.match(line):
            week["outcome"] = m[1].strip(); continue
        if m := MOD_RE.match(line):
            mod = {"id": m[1], "title": m[2].strip(), "micro": "", "fields": {}}
            week["modules"].append(mod); lab = None
            continue
        if m := LAB_RE.match(line):
            lab = {"id": m[1], "title": m[2].strip(), "tracks": {}, "ship": ""}
            week["lab"] = lab; mod = None
            continue
        if mod is not None:
            if m := MICRO_RE.match(line):
                mod["micro"] = m[1].strip()
            elif m := FIELD_RE.match(line):
                mod["fields"][m[1]] = m[2].strip()
        if lab is not None:
            if m := TRACK_RE.match(line):
                lab["tracks"][m[1]] = m[2].strip()
            elif m := FIELD_RE.match(line):
                if m[1] == "Ship it":
                    lab["ship"] = m[2].strip()
    return weeks


def split_micro(micro: str) -> list[str]:
    parts = re.split(r"\(([a-z])\)\s*", micro)
    out = []
    for i in range(1, len(parts) - 1, 2):
        item = parts[i + 1].strip().rstrip(";").strip()
        if item:
            out.append(item)
    return out or ([micro] if micro else [])


def write(path: Path, content: str) -> None:
    """Write, preserving anything after BODY_MARKER in an existing file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = path.read_text()
        if AUTHORED_MARKER in existing:
            return  # hand-authored page: never regenerate
        if BODY_MARKER in existing:
            content = content.split(BODY_MARKER)[0] + BODY_MARKER + existing.split(BODY_MARKER, 1)[1]
    path.write_text(content)


def module_page(week: dict, mod: dict, idx: int) -> str:
    f = mod["fields"]
    micro = split_micro(mod["micro"])
    micro_md = "\n".join(f"{i}. {esc(m)}" for i, m in enumerate(micro, 1)) or "_TBD_"
    dg = slug(mod["title"])
    vis = f.get("VIS", "Hand-drawn sketch of the core idea; build-up frames for each step.")
    ref = f.get("REF", "")
    ref_md = ("\n".join(f"- {esc(r.strip())}" for r in ref.split(";") if r.strip())
              if ref else "- _Primary docs, the source paper, and one 'go deeper' pick — see `PLAN/02-references-library.md`._")
    return f"""---
title: "{mod['title']}"
description: "Week {week['num']} · Module {idx} — taught at three depths, with a lab."
icon: "pen-line"
---

<Note>
**Week {week['num']} · Module {idx} · `{mod['id']}`** — start with 🟢 Ground if this page's words are not
second nature yet — even after years of shipping code. Move to 🔵 Build once they are, and 🟣 Edge
when Build has already hurt you. Nobody skips Ground the first time through.
</Note>

## What you'll be able to do

{micro_md}

<Frame caption="The whole idea on one whiteboard. Redraw it from memory before you move on.">
  <img src="/assets/diagrams/{dg}.svg" alt="Hand-drawn sketch: {esc(mod['title'])}" className="block dark:hidden" />
  <img src="/assets/diagrams/{dg}-dark.svg" alt="Hand-drawn sketch: {esc(mod['title'])}" className="hidden dark:block" />
</Frame>

<Tabs>
  <Tab title="🟢 Layer 1 — Ground">
    **For Aarav (student).** No assumptions. Every term defined where it appears.

    {esc(f.get('L1 Ground', '_TBD_'))}

    <Steps>
      <Step title="Mental model">The one-picture version, then the analogy.</Step>
      <Step title="Smallest working example">Runs in under a minute. Copy, run, break, fix.</Step>
      <Step title="Line-by-line walkthrough">Every line explained, nothing skipped.</Step>
      <Step title="Guided practice">60% written for you. Answers included.</Step>
    </Steps>

    <Accordion title="Checkpoint — 5 questions before you continue">
      _Generated from the assessment bank._
    </Accordion>
  </Tab>

  <Tab title="🔵 Layer 2 — Build">
    **For Meera (working professional).** Trade-offs, real tools, real versions.

    {esc(f.get('L2 Build', '_TBD_'))}

    <CardGroup cols={{2}}>
      <Card title="Reference implementation" icon="code">Complete and tested — not a snippet.</Card>
      <Card title="Trade-offs" icon="scale-balanced">Choose X when… / choose Y when…</Card>
      <Card title="What breaks in production" icon="triangle-alert">A real failure and its signature.</Card>
      <Card title="Design checkpoint" icon="circle-check">One design question, with a model answer.</Card>
    </CardGroup>
  </Tab>

  <Tab title="🟣 Layer 3 — Edge">
    **For anyone who has shipped this and been burned.** Internals, scale, numbers.

    {esc(f.get('L3 Edge', '_TBD_'))}

    <Warning>
      Every claim in this layer carries a measured number. If you cannot reproduce the
      number on your own machine, treat the claim as unproven and tell us.
    </Warning>
  </Tab>
</Tabs>

## Hands-on

<Card title="Do this now" icon="hammer" horizontal>
{esc(f.get('Hands-on', '_TBD_'))}
</Card>

## The whiteboard

{esc(vis)}

<Tip>
**Draw it yourself.** Reproduce the sketch above from memory on paper, then compare.
This is graded — it is the cheapest retention exercise in the course.
[Blank version](/assets/diagrams/{dg}-blank.svg) · [Editable source](/assets/diagrams/{dg}.excalidraw)
</Tip>

## Apply it at work

<AccordionGroup>
  <Accordion title="If you're a student" icon="graduation-cap">
    Portfolio framing, how to talk about it in an interview, and the resume line it earns.
  </Accordion>
  <Accordion title="If you're working" icon="briefcase">
    Three concrete places this shows up in a normal engineering week.
  </Accordion>
</AccordionGroup>

## Common mistakes

| Symptom | Cause | Fix |
| --- | --- | --- |
| _TBD_ | _TBD_ | _TBD_ |

## Sources & further reading

{ref_md}

<Card title="Solutions & answer key" icon="lock" href="/solutions/{week['phase'].lower()}/week-{week['num']:02d}/{mod['id'].lower()}">
  Attempt the lab first. Seriously.
</Card>

{BODY_MARKER}
"""


def lab_page(week: dict) -> str:
    lab = week["lab"]
    t = lab["tracks"]
    return f"""---
title: "Lab — {lab['title']}"
description: "Week {week['num']} lab · three tracks · self-graded"
icon: "flask-conical"
---

<Note>
**`{lab['id']}`** — one lab, three tracks. Beginners start at `basic` and climb.
Working professionals start at `standard`. `hard` is where the interview stories come from.
</Note>

## The ticket

> {esc(week['outcome'])}

<Tabs>
  <Tab title="basic">
    {esc(t.get('basic', '_TBD_'))}

    <Info>~60% of the code is written for you. TODOs are marked. Answers provided.</Info>
  </Tab>
  <Tab title="standard">
    {esc(t.get('standard', '_TBD_'))}

    <Info>Spec and tests only. You write the implementation.</Info>
  </Tab>
  <Tab title="hard">
    {esc(t.get('hard', '_TBD_'))}

    <Warning>There is a constraint here that the `standard` solution fails.</Warning>
  </Tab>
</Tabs>

## Ship it

<Card title="This is the part people skip" icon="rocket" horizontal>
{esc(lab['ship'] or 'Commit it, deploy it, or measure it. A lab never ends at "it printed the right thing".')}
</Card>

## Verify yourself

```bash
cd labs/{week['phase'].lower()}/week-{week['num']:02d}
make verify        # green on a correct solution, red on the starter
```

## Rubric

| Dimension | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Correctness | fails tests | happy path only | edge cases handled | adversarial inputs handled |
| Code quality | works | readable | tested + typed | a reviewer would approve unchanged |
| Performance | untested | measured | meets the budget | beats it, with evidence |
| Explanation | none | a README | reasoning documented | trade-offs defended |

<Card title="Reference solution" icon="lock" href="/solutions/{week['phase'].lower()}/week-{week['num']:02d}/lab">
  Hidden page. Open it after you have a failing attempt of your own.
</Card>

{BODY_MARKER}
"""


def week_index(week: dict) -> str:
    mods = "\n".join(
        f'  <Card title="{m["title"]}" icon="pen-line" '
        f'href="/curriculum/{week["phase"].lower()}/week-{week["num"]:02d}/{i}-{slug(m["title"])}">'
        f'{esc(split_micro(m["micro"])[0] if split_micro(m["micro"]) else "")}</Card>'
        for i, m in enumerate(week["modules"], 1))
    return f"""---
title: "Week {week['num']} — {week['title']}"
description: "{esc(week['outcome'])[:150]}"
icon: "calendar"
---

## Outcome

<Note>{esc(week['outcome'])}</Note>

## Modules

<CardGroup cols={{2}}>
{mods}
</CardGroup>

## This week's rhythm

| Day | Student (12–15 h) | Working professional (5–7 h) |
| --- | --- | --- |
| Mon–Tue | Layer 1 + Layer 2 | Layer 2 |
| Wed–Thu | Lab `basic` → `standard` | Lab `standard` |
| Fri | Layer 3 + stretch | Layer 3 skim |
| Sat | Lab `hard`, push to GitHub | Lab `hard` (optional) |
| Sun | Assessment + flashcards + draw-from-memory | Assessment |

{BODY_MARKER}
"""


def solution_page(week: dict, title: str, ident: str, kind: str) -> str:
    return f"""---
title: "{title}"
description: "Reference solution — Week {week['num']}"
hidden: true
icon: "lock"
---

<Warning>
**Hidden page.** It is not in the navigation, but it is not private either — anyone with the
URL can read it. Do not paste this link into the cohort chat.
</Warning>

<Note>Open this only after you have an attempt of your own that fails. Reading a solution
before struggling with the problem feels like learning and isn't.</Note>

## Reference solution — `{ident}`

_Full worked solution, the reasoning behind each decision, the two wrong turns worth knowing
about, and the measured numbers this solution produces._

## Why this solution and not the obvious one

_TBD_

## Grading notes

_What a 3/3 looks like on each rubric row, and the three most common ways submissions lose points._

{BODY_MARKER}
"""


def main() -> None:
    all_weeks: list[dict] = []
    for p in sorted(TASKS.glob("phase-*-tasks.md")):
        all_weeks.extend(parse(p))
    if not all_weeks:
        sys.exit("no weeks parsed — check the task files")

    tabs: list[dict] = [{
        "tab": "Start here",
        "groups": [
            {"group": "Orientation", "pages": [
                "index", "start/how-this-works", "start/three-layers",
                "start/who-this-is-for", "start/about-the-numbers",
                "start/setup", "start/how-to-study"]},
            {"group": "The map", "pages": ["start/curriculum-map", "start/portfolio", "start/faq"]},
        ],
    }]

    phase_tabs: dict[str, dict] = {}
    lab_groups: list[dict] = []
    solution_groups: list[dict] = []

    for w in all_weeks:
        ph, n = w["phase"], w["num"]
        base = f"curriculum/{ph.lower()}/week-{n:02d}"
        pages = [f"{base}/index"] + PRIMERS.get(n, [])
        for i, m in enumerate(w["modules"], 1):
            rel = f"{base}/{i}-{slug(m['title'])}"
            pages.append(rel)
            write(SITE / f"{rel}.mdx", module_page(w, m, i))
        pages += EXTRAS.get(n, [])
        if w["lab"]:
            pages.append(f"{base}/lab")
            write(SITE / f"{base}/lab.mdx", lab_page(w))
        write(SITE / f"{base}/index.mdx", week_index(w))

        grp = {"group": f"Week {n} — {w['title']}", "pages": pages}
        if n > RELEASED_THROUGH_WEEK:
            grp["hidden"] = True          # drip release: unhide as the cohort reaches it
        phase_tabs.setdefault(ph, {"tab": PHASE_TITLES[ph], "groups": []})
        phase_tabs[ph]["groups"].append(grp)

        if w["lab"]:
            lab_groups.append({"group": f"Week {n}", "pages": [f"{base}/lab"]})

        sol_pages = []
        for m in w["modules"]:
            sp = f"solutions/{ph.lower()}/week-{n:02d}/{m['id'].lower()}"
            sol_pages.append(sp)
            write(SITE / f"{sp}.mdx", solution_page(w, m["title"], m["id"], "module"))
        if w["lab"]:
            sp = f"solutions/{ph.lower()}/week-{n:02d}/lab"
            sol_pages.append(sp)
            write(SITE / f"{sp}.mdx", solution_page(w, f"Lab — {w['lab']['title']}", w["lab"]["id"], "lab"))
        solution_groups.append({"group": f"Week {n}", "pages": sol_pages})

    tabs.extend(phase_tabs[p] for p in ("P1", "P2", "P3", "P4") if p in phase_tabs)
    tabs.append({"tab": "Labs", "groups": [{"group": "Setup", "pages": ["labs/index", "labs/verify"]},
                                           *lab_groups]})
    tabs.append({"tab": "Projects", "groups": [{"group": "Portfolio gates", "pages": [
        "projects/midterm", "projects/capstone", "projects/defence"]}]})
    tabs.append({"tab": "Reference", "groups": [
        {"group": "Library", "pages": ["reference/papers", "reference/tools", "reference/glossary",
                                       "reference/diagram-index", "reference/cheatsheets"]}]})
    # Hidden tabs — present in docs.json, absent from the rendered nav.
    tabs.append({"tab": "Solutions", "hidden": True,
                 "groups": [{"group": "How to use these", "pages": ["solutions/index"]}, *solution_groups]})
    tabs.append({"tab": "Instructor", "hidden": True, "groups": [{"group": "Teaching", "pages": [
        "instructor/index", "instructor/session-plans", "instructor/rubrics",
        "instructor/release-schedule", "instructor/common-questions"]}]})

    docs = {
        "$schema": "https://mintlify.com/docs.json",
        "theme": "mint",
        "name": "Nexus",
        "description": "Systems, Machine Learning & Distributed AI — 0 to expert in 32 weeks.",
        "colors": {"primary": "#1971c2", "light": "#4dabf7", "dark": "#1864ab"},
        "favicon": "/favicon.svg",
        "seo": {"indexing": "navigable"},
        "navigation": {"tabs": tabs},
        "footer": {"socials": {"github": "https://github.com/nexus-course"}},
    }
    (SITE / "docs.json").write_text(json.dumps(docs, indent=2, ensure_ascii=False) + "\n")

    n_pages = sum(len(g["pages"]) for t in tabs for g in t.get("groups", []))
    hidden_groups = sum(1 for t in tabs for g in t.get("groups", []) if g.get("hidden"))
    hidden_tabs = sum(1 for t in tabs if t.get("hidden"))
    print(f"weeks={len(all_weeks)} tabs={len(tabs)} pages={n_pages} "
          f"hidden_tabs={hidden_tabs} hidden_groups={hidden_groups}")


if __name__ == "__main__":
    main()
