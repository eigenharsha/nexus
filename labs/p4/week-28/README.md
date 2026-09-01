# LAB-P4-W28 — Production hybrid RAG

> Week 28 · Phase 4 · Generative AI · time box: **14-16 h**
> Language: python · `make verify` grades you · no instructor required

> **Status: scaffold.** The ticket, the three track specs with their acceptance criteria, the
> Makefile and the test skeleton are complete — `tests/` has one named, documented test per
> acceptance criterion. The assertions inside them, and `starter/` and `solution/`, are what
> you write. `make verify` is red until you do, which is the correct starting state for a lab.
> Six labs in the course ship a fully worked solution as well; see
> [labs/README.md](../../README.md#which-labs-ship-a-worked-solution).

## The ticket

The Week-27 system answers 71% of the eval set correctly and takes 2.3 seconds per query.
Product wants 85% and under 800 ms. Finance wants the per-query cost down, having noticed we
re-embed the same three questions forty times a day.

Every improvement you make has to be ablated against the Week-27 eval set. The final table is the
deliverable — it is the thing a hiring manager will actually read.

## What "done" looks like

- A quality/latency/cost table with one row per stage added.
- A semantic cache that is provably correct after a document update.
- The stage that did not help, kept in the table with its number.

## Tracks

Pick the one that matches where you are. You can climb mid-lab; the tests for the lower track
keep passing.

| Track | You get | You write | Spec |
|---|---|---|---|
| `basic` | ~60% of the code, TODOs marked | the marked TODOs | [basic/SPEC.md](basic/SPEC.md) |
| `standard` | a spec and a test suite | the implementation | [standard/SPEC.md](standard/SPEC.md) |
| `hard` | the same spec plus a constraint the standard solution fails | a better implementation | [hard/SPEC.md](hard/SPEC.md) |

## Getting started

```bash
cd labs/p4/week-28
make help                    # what this lab can do
cat standard/SPEC.md         # the acceptance criteria
$EDITOR starter/             # your work goes here
make verify                  # TRACK=standard against starter/  -> red until you finish
make verify TRACK=basic      # the scaffolded track
make verify IMPL=solution    # proves the tests are honest
make contract                # asserts solution green AND starter red
```

You edit **`starter/`**. `basic/`, `standard/` and `hard/` hold the specs and any track-specific
scaffolding; `solution/` is the reference. Open `solution/` only after you have a failing
attempt of your own — reading it first converts a 6-hour skill into a 6-minute read.

## Verify

```bash
make verify                  # your work, standard track — red until you finish
make verify TRACK=basic
make contract                # once solution/ exists, asserts it is green and starter/ is red
```

`tests/` currently holds one named test per acceptance criterion, each with the criterion as
its docstring and a `pytest.fail("not implemented yet")` body. Turning those into real
assertions is the first half of the lab; passing them is the second. Paste your own
`make verify` output here when it goes green — that transcript is what a reader of your
portfolio repo will look at first.

## Ship it

Repo plus `RAG-REPORT.md`. The ablation table is the artifact — put it at the top.

A lab never ends at "it printed the right thing".

## Rubric

See [RUBRIC.md](RUBRIC.md). Grade yourself before you look at `solution/`.

## If you get stuck

1. Twenty minutes stuck, then read the *Common mistakes* table in the week's module pages.
2. Then re-read Layer 1 of the module this lab tests.
3. Then `solution/`, one function at a time — and delete-and-rewrite the function you read.
