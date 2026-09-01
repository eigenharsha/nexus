# LAB-P1-W07 — E-commerce schema & analytics suite

> Week 7 · Phase 1 · Foundations · time box: **10-12 h**
> Language: python · `make verify` grades you · no instructor required

> **Status: scaffold.** The ticket, the three track specs with their acceptance criteria, the
> Makefile and the test skeleton are complete — `tests/` has one named, documented test per
> acceptance criterion. The assertions inside them, and `starter/` and `solution/`, are what
> you write. `make verify` is red until you do, which is the correct starting state for a lab.
> Six labs in the course ship a fully worked solution as well; see
> [labs/README.md](../../README.md#which-labs-ship-a-worked-solution).

## The ticket

We inherited a store whose entire data model is three wide tables and a `notes` column that
contains, at last count, four different date formats.

Nobody can answer "what did the January cohort spend in month 3" without a two-hour export and a
spreadsheet. Model it properly, seed it with a realistic million rows, and write the queries the
business keeps asking for — with `EXPLAIN ANALYZE` evidence that they will still work when the
table is ten times bigger.

## What "done" looks like

- A normalized schema with real constraints, not just columns.
- 1M seeded rows that look like real data (skewed, not uniform).
- 20 analytical queries with plans attached.

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
cd labs/p1/week-07
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

Repo with `schema.sql`, `seed.py`, `queries/`, `INDEXES.md` and a performance write-up.

A lab never ends at "it printed the right thing".

## Rubric

See [RUBRIC.md](RUBRIC.md). Grade yourself before you look at `solution/`.

## If you get stuck

1. Twenty minutes stuck, then read the *Common mistakes* table in the week's module pages.
2. Then re-read Layer 1 of the module this lab tests.
3. Then `solution/`, one function at a time — and delete-and-rewrite the function you read.
