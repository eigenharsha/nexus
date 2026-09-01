# `hard` — LAB-P3-W23

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 5-7 h

## Constraint

p95 under **300 ms** including cold starts, with a canary deployment and an automatic rollback
on an error-rate threshold.

## Acceptance criteria

- p95 < 300 ms measured including cold starts, with the cold-start mitigation you chose
  (provisioned concurrency, a smaller runtime, or a warming ping) and its cost.
- A canary deployment routing a percentage of traffic to the new version.
- Automatic rollback triggered by an error-rate threshold, demonstrated by deliberately deploying
  a broken version and showing the rollback in the logs.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
