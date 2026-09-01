# `hard` — LAB-P1-W03

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 4-6 h

## Constraint

Add a **third** storage backend — an append-only event log (`EventLogStorage`) with
replay-on-load — **without modifying a single line** of `ledger/ledger.py`, `ledger/models.py`
or `ledger/errors.py`. `make verify TRACK=hard` diffs those three files against the `standard`
versions and fails if they changed.

## Acceptance criteria

- `EventLogStorage` appends one JSON line per posted transaction and rebuilds state on load.
- The Open/Closed proof: core files byte-identical to the `standard` track (the test checks this).
- `hypothesis` invariant tests: for **any** sequence of valid postings, `trial_balance()` sums to
  zero and each account balance equals the sum of its own postings. At least 200 examples.
- A stateful `hypothesis` `RuleBasedStateMachine` that interleaves posts, reloads and balance
  queries against all three backends and asserts they agree.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
