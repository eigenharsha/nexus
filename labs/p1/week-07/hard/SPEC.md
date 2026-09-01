# `hard` — LAB-P1-W07

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 4-6 h

## Constraint

On 10M rows, the five queries listed in `hard/targets.md` must each come in under their stated
latency target. The unindexed schema misses every one of them.

## Acceptance criteria

- Hit every latency target in `hard/targets.md` on a 10M-row seed.
- `INDEXES.md` documents every index with: the query it serves, the plan before and after, the
  measured write-cost (INSERT throughput with and without it), and the disk size.
- At least one query must be fixed by a **rewrite** rather than an index — find it and say so.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
