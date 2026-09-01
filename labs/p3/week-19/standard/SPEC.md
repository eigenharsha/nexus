# `standard` — LAB-P3-W19

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 6-7 h

## Acceptance criteria

- A reusable library, importable and tested, not a notebook.
- A CV strategy selector: given a dataset's shape (grouped? time-ordered? imbalanced?), it picks
  and justifies stratified / grouped / time-series CV, and refuses to run plain k-fold on grouped
  data.
- Leakage audit checks: target leakage by correlation, train/test row duplication, preprocessing
  fit before split (detected by a fitted-transformer fingerprint), group spillover across folds,
  and a time-travel check on datetime features.
- A metric suite with bootstrap confidence intervals (10,000 resamples) on every metric.
- Slice analysis: metrics per category for every categorical feature, with the worst slice flagged.
- A calibration report and a threshold optimizer against a supplied cost matrix.
- An auto-generated HTML evaluation report.
- Validated on three datasets.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

The fitted-transformer check is the one that catches the real incident: hash the transformer's
learned parameters, refit it on the training fold only, and assert the hashes differ. If they are
identical, the transformer saw the test set.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
