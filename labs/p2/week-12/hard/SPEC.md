# `hard` — LAB-P2-W12

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 4-6 h

## Constraint

Show numerically that CUPED reduces the required sample size for the same MDE and power — with
the variance-reduction ratio you measured on the provided pre-period data.

## Acceptance criteria

- Sequential testing with an alpha-spending correction; demonstrate on simulated data that naive
  peeking inflates the false-positive rate to a measured value, and that yours does not.
- CUPED variance reduction using a pre-period covariate; report the measured variance reduction
  and the resulting reduction in required n.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
