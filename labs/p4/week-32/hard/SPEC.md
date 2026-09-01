# `hard` — LAB-P4-W32

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 6-8 h

## Constraint

>=50% cost reduction with **no quality regression**, plus tail sampling under load and a
published TCO analysis.

## Acceptance criteria

- >= 50% cost reduction with no quality regression, both measured against the Week-31 eval suite.
- A documented game-day: an injected failure, the alert that fired, the time to detection and the
  time to resolution.
- Tail-based sampling under load, keeping the slow and failed traces while dropping the rest, with
  the retained fraction and the storage saving reported.
- A published TCO analysis: infrastructure, model, storage and engineering time, per 1,000
  incidents handled.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
