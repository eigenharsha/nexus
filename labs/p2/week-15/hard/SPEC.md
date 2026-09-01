# `hard` — LAB-P2-W15

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 5-7 h

## Constraint

5M rows, partitioned Parquet output, an SCD2 dimension, and a proof of exactly-once semantics
for the merge — a naive append-then-dedupe will not give you that.

## Acceptance criteria

- 5M rows written as partitioned Parquet with a documented partition key.
- An SCD2 dimension with `valid_from` / `valid_to` / `is_current`, tested across three updates to
  the same business key.
- A backfill script that can re-process an arbitrary date range without touching other partitions.
- A written proof of exactly-once merge semantics: the mechanism, and the test that demonstrates
  it under a mid-merge crash.
- Cost and latency analysis: seconds per million rows, bytes written, and the projected monthly cost.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
