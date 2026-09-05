# LAB-P3-W19 — Evaluation harness

> Week 19 · Phase 3 · Machine Learning · time box: **10-12 h**
> Language: python · `make verify` grades you · no instructor required

> **Status: scaffold.** The ticket, the three track specs with their acceptance criteria, the
> Makefile and the test skeleton are complete — `tests/` has one named, documented test per
> acceptance criterion. The assertions inside them, and `starter/` and `solution/`, are what
> you write. `make verify` is red until you do, which is the correct starting state for a lab.
> Six labs in the course ship a fully worked solution as well; see
> [labs/README.md](../../README.md#which-labs-ship-a-worked-solution).

## The ticket

Two models went to production last year reporting 0.94 AUC. One of them was leaking the
target through a preprocessing step that fit the scaler before the split. We found out because a
customer noticed the predictions were suspiciously good for accounts that had already churned.

Build the harness that would have caught it, and make passing it the gate every model has to
clear before review. `standard/leaks/` contains five planted leaks — your harness has to find
all five.

## What "done" looks like

- All five planted leaks detected, each with a message that names the offending column.
- Metrics reported with bootstrap confidence intervals, never as a bare number.
- Slice analysis that surfaces the group where the model is worst.

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
cd labs/p3/week-19
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

The harness is reused in the Midterm and again in Week 33 — package it properly, because you
are going to import it three more times.

A lab never ends at "it printed the right thing".

## Rubric

See [RUBRIC.md](RUBRIC.md). Grade yourself before you look at `solution/`.

## If you get stuck

1. Twenty minutes stuck, then read the *Common mistakes* table in the week's module pages.
2. Then re-read Layer 1 of the module this lab tests.
3. Then `solution/`, one function at a time — and delete-and-rewrite the function you read.
