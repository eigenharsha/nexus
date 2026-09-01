# `hard` — LAB-P2-W09

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 4-6 h

## Constraint

The ripple-carry `Add16` has a critical path of 16 full-adder delays. Build a carry-lookahead
variant and show — in gate delays, not wall time — that it is shorter, and say what it costs in
gate count.

## Acceptance criteria

- A carry-lookahead `Add16CLA` passing the same test script as `Add16`.
- A written critical-path analysis: gate delays for both adders, gate counts for both, and the
  point at which the trade stops being worth it.
- Plus the companion C cache-locality benchmark (`hard/cache_bench.c`): row-major vs column-major
  traversal of a 4096x4096 matrix, with measured numbers and the cache-line explanation.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
