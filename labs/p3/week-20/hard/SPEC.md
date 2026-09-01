# `hard` — LAB-P3-W20

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 5-7 h

## Constraint

Hit the target recall at the fixed false-positive budget in `hard/targets.md`, with end-to-end
per-prediction latency (including feature computation) under **10 ms**.

## Acceptance criteria

- Target recall at the fixed FP budget, reported with a bootstrap CI.
- Sub-10 ms p99 per-prediction latency including feature computation — which means the rolling
  aggregates must be maintained incrementally, not recomputed.
- Drift monitoring on the input features with a documented alert threshold.
- A serialization strategy that survives a dependency upgrade: a version-pinned artifact plus a
  loading test that runs against the next minor version of the library.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
