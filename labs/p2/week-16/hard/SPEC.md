# `hard` — LAB-P2-W16

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 4-6 h

## Constraint

A 10M-row file processed inside a fixed memory budget in under **60 seconds**, plus a drift
comparison between two datasets with statistical tests.

## Acceptance criteria

- 10M rows within the memory budget in `hard/targets.md`, in under 60 s. Streaming or columnar
  chunking — a `pd.read_csv` of the whole file will not fit.
- Drift comparison between two datasets: PSI and KS per numeric feature, chi-square per
  categorical, with a documented threshold for "this has drifted".
- Runtime reported per section so the slow part is visible.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
