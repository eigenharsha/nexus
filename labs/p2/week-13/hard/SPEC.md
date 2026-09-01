# `hard` — LAB-P2-W13

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 5-7 h

## Constraint

Beat CPython's built-in `dict` on a specialised workload — integer keys, known size, no
deletions — and prove it with a benchmark that anyone can rerun.

## Acceptance criteria

- An `IntHashMap` specialised for integer keys with a known capacity, measurably faster than
  `dict` on the stated workload. Report the ratio and be honest about what you gave up.
- A count-min sketch with configurable width and depth; empirically measure the error against the
  theoretical bound over at least 10,000 items, and plot measured vs predicted error.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
