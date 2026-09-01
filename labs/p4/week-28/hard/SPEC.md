# `hard` — LAB-P4-W28

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 6-8 h

## Constraint

Hit the quality target under both the latency and the cost budget in `hard/targets.md`, with
incremental re-indexing and a cache proven correct after a document update.

## Acceptance criteria

- Meet the quality target inside the stated latency and cost budgets, all three measured.
- Incremental re-indexing: a changed document updates in place without a full rebuild, with the
  time for both reported.
- Cache correctness after an update proven by test: a query cached before a document change must
  not return the stale answer.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
