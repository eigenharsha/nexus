# `hard` — LAB-P1-W08

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 5-8 h

## Constraint

Sustain the RPS target in `hard/targets.md` with p95 < 150 ms **while** 200 buyers contend for
the same 12 units. Pessimistic locking on the hot row will not get there.

## Acceptance criteria

- Meet the throughput and p95 targets under contention.
- `CONCURRENCY.md`: pessimistic vs optimistic vs `SERIALIZABLE`, each with measured throughput,
  p95, and retry/abort rate from your own run.
- A reproducible deadlock (two transactions, opposite lock order) with the log evidence, and the
  fix — plus the ordering rule you adopted so it cannot recur.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
