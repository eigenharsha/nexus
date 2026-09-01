# `standard` — LAB-P3-W20

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 7-8 h

## Acceptance criteria

- Leakage-free preprocessing: every transformer fit inside the CV fold. The Week-19 harness
  should pass this pipeline.
- Engineered temporal and aggregate features: time since the account's previous transaction,
  rolling count and amount in 1 h / 24 h / 7 d windows, and amount relative to the account's own
  history — all computed **without** looking forward in time. The test plants a future-leaking
  feature and your pipeline must reject it.
- XGBoost with `scale_pos_weight`, tuned, compared against a logistic-regression baseline.
- PR-curve threshold optimization against the explicit cost matrix in `standard/costs.yaml`.
- Probability calibration (isotonic or Platt), with the reliability curve before and after.
- Slice analysis across merchant category and transaction amount bands.
- A report stating expected annual savings with the arithmetic shown.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

ROC-AUC on a 0.17% positive rate is close to meaningless — you can move from 0.97 to 0.98 while
precision at your operating point halves. Report average precision, and put the operating point
on the plot.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
