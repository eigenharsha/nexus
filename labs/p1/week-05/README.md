# LAB-P1-W05 — Static frontend against a public API

> Week 5 · Phase 1 · Foundations · time box: **6-8 h**
> Language: python · `make verify` grades you · no instructor required

> **Status: scaffold.** The ticket, the three track specs with their acceptance criteria, the
> Makefile and the test skeleton are complete — `tests/` has one named, documented test per
> acceptance criterion. The assertions inside them, and `starter/` and `solution/`, are what
> you write. `make verify` is red until you do, which is the correct starting state for a lab.
> Six labs in the course ship a fully worked solution as well; see
> [labs/README.md](../../README.md#which-labs-ship-a-worked-solution).

## The ticket

Support keeps pasting raw API responses into Slack because there is no UI for the catalogue.
They have asked three times. Engineering has said "after the replatform" three times.

Give them one page. No framework, no build step, hosted free. It has to work on a five-year-old
laptop on hotel wifi, and it has to handle the four states properly — because the reason the last
attempt was abandoned was that it showed an empty list when the API was down.

## What "done" looks like

- All four UI states are visibly distinct: loading, empty, error, success.
- Keyboard-navigable and screen-reader-sane; Lighthouse accessibility >= 90.
- No framework, no bundler, one HTML file plus one CSS and one JS file.
- Deployed at a URL you can paste into the ticket.

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
cd labs/p1/week-05
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

Deploy free to GitHub Pages or Netlify and put the live URL at the top of the README, with the
Lighthouse screenshot underneath.

A lab never ends at "it printed the right thing".

## Rubric

See [RUBRIC.md](RUBRIC.md). Grade yourself before you look at `solution/`.

## If you get stuck

1. Twenty minutes stuck, then read the *Common mistakes* table in the week's module pages.
2. Then re-read Layer 1 of the module this lab tests.
3. Then `solution/`, one function at a time — and delete-and-rewrite the function you read.
