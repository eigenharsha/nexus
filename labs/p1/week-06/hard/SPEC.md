# `hard` — LAB-P1-W06

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 4-6 h

## Constraint

p95 under **200 ms** with 50 concurrent users, and a repeated request with the same
idempotency key must never do the work twice.

## Acceptance criteria

- Idempotency keys: same key + same body returns the cached response; same key + different body
  returns 409.
- Background job processing with a status-polling endpoint (`202` + `Location`).
- Load test (`locust` or `k6`) at 50 concurrent users showing p95 < 200 ms, report committed.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
