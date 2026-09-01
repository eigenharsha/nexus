# LAB-P1-W03 — `ledger` — a typed, tested, packaged Python library

> Week 3 · Phase 1 · Foundations · time box: **8-10 h**
> Language: python · `make verify` grades you · no instructor required

> **Status: verified.** `starter/`, `solution/` and the test suite are complete and were
> actually run to produce the output in *Verify* below. `make contract` passes on all three
> tracks: green on `solution/`, red on `starter/`.

## The ticket

Finance has been reconciling three spreadsheets by hand every month. Someone wrote "just a
small script" for it in March; it is now 900 lines, has two functions called `process`, and last
month it produced a balance that was off by £0.01 in a way nobody could reproduce.

Before this becomes a business-critical spreadsheet with a CLI attached, build it properly.
`ledger`: accounts, transactions, a storage backend we can swap, and a type system strict enough
that posting an unbalanced transaction is a compile-time error rather than a Tuesday.

## What "done" looks like

- Money is never a float. Not once.
- `mypy --strict` is clean on the whole package.
- Adding a new storage backend requires zero changes to the core module — proven by the fact that
  the `hard` track adds one.
- Every invariant the domain has (balances sum to zero, an account's balance equals the sum of its
  postings) is enforced in code and tested with property-based tests.

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
cd labs/p1/week-03
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

## Verify — real output from this repo

```
$ make verify IMPL=solution TRACK=hard
==> LAB-P1-W03 · track=hard · impl=solution
.........................                                                [100%]
25 passed in 3.13s

$ make verify            # starter/, standard track
FAILED tests/test_ledger.py::test_duplicate_transaction_id_raises_and_changes_nothing
FAILED tests/test_ledger.py::test_trial_balance_sums_to_zero - NotImplemented...
FAILED tests/test_ledger.py::test_json_file_storage_round_trips - NotImplemen...
FAILED tests/test_ledger.py::test_json_file_storage_writes_atomically - NotIm...
FAILED tests/test_ledger.py::test_both_backends_agree - NotImplementedError: ...
16 failed, 2 passed, 7 deselected in 0.24s
make[1]: *** [_verify_impl] Error 1
make: *** [verify] Error 2

$ make contract TRACK=hard
==> contract check: LAB-P1-W03 track=hard
  PASS  solution/ is green
  PASS  starter/ is red (as it must be)
contract holds

$ make typecheck IMPL=solution   # mypy --strict
Success: no issues found in 6 source files

$ .venv/bin/python -m ruff check solution
All checks passed!
```
25 tests green on `solution/` at the `hard` track (including 200 `hypothesis` examples per
property and the three-backend state machine), 16 failed / 2 passed on `starter/`.
`mypy --strict` and `ruff` are both clean on the reference implementation.

## What the property tests actually proved

`tests/test_properties.py` is the part worth putting in your README, because it makes a
stronger claim than any example-based test can:

- **For any sequence of up to 20 valid transactions over 5 accounts**, `trial_balance()` sums to
  exactly zero. 200 generated examples per run, shrunk to a minimal counterexample on failure.
- **For any such sequence**, each account's balance equals the sum of its own postings.
- **A stateful machine** interleaves posting, reloading `JsonFileStorage` from disk, and
  reloading `EventLogStorage` from its append-only log, asserting after every step that all
  three backends report an identical trial balance.

The state machine is the one worth writing yourself. Example-based tests check the states you
thought of; the machine checks the interleavings you did not — post, reload, post, reload — and
that is where a persistence bug actually lives.

## The Open/Closed proof

`make verify TRACK=hard` includes `test_open_closed_core_never_mentions_the_event_log`, which
reads the source of `ledger/ledger.py`, `ledger/models.py` and `ledger/errors.py` and asserts
none of them contains the string `EventLog` — and that `ledger/event_log.py` does not import
the core either. The principle is checked as a fact about the import graph, not asserted in a
comment.


## Ship it

Publish to TestPyPI (`uv build && uv publish --index testpypi`) and write the README as API
docs, with the invariant section explaining what `hypothesis` actually proved.

A lab never ends at "it printed the right thing".

## Rubric

See [RUBRIC.md](RUBRIC.md). Grade yourself before you look at `solution/`.

## If you get stuck

1. Twenty minutes stuck, then read the *Common mistakes* table in the week's module pages.
2. Then re-read Layer 1 of the module this lab tests.
3. Then `solution/`, one function at a time — and delete-and-rewrite the function you read.
