# `hard` — LAB-P3-W19

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 4-6 h

## Constraint

Nested CV plus adversarial validation, catching all five planted leaks, inside the runtime
budget in `hard/targets.md`.

## Acceptance criteria

- Nested cross-validation for unbiased performance estimation under hyperparameter search;
  report the optimism gap versus flat CV on the same data.
- Adversarial validation: train a classifier to distinguish train from test; an AUC above a stated
  threshold is reported as a distribution-shift warning.
- Automated leakage detection catching **all five** planted leaks in `standard/leaks/`.
- The whole harness runs inside the stated runtime budget.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
