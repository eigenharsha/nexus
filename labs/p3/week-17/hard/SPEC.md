# `hard` — LAB-P3-W17

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 5-7 h

## Constraint

Softmax multiclass with early stopping, trained on **1M rows** within the memory budget in
`hard/targets.md`. Materialising the full one-hot target matrix will not fit.

## Acceptance criteria

- `SoftmaxRegression` for multiclass, numerically stable (subtract the row max), matching
  scikit-learn's multinomial solver within tolerance.
- Early stopping on a validation split with a documented patience.
- A learning-curve diagnostic tool: training and validation loss vs training-set size, with a
  written reading of whether the model is variance-limited or bias-limited.
- Trains on 1M rows inside the stated memory budget — mini-batch, and no full one-hot matrix.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
