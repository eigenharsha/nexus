# `hard` — LAB-P4-W27

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 6-8 h

## Constraint

Scale to **10M chunks** (synthetically extended), reporting index build time, memory, p95 query
latency and recall — and prove filtered search is still correct at that scale.

## Acceptance criteria

- 10M chunks indexed; report build time, index memory, p95 query latency and Recall@10, with the
  recall/latency trade-off curve across `ef_search`.
- Correct filtered search at scale: demonstrate the post-filter recall collapse that naive
  filtering causes, then fix it, with the numbers for both.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
