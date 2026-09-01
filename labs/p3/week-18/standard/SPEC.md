# `standard` — LAB-P3-W18

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 7-8 h

## Acceptance criteria

- A full workflow on the real churn dataset: a majority-class baseline, then logistic regression,
  then random forest, then XGBoost — each with the same validation strategy.
- A validation strategy chosen deliberately (stratified k-fold, or time-based if the data has a
  time axis) and documented, including why the other option is wrong here.
- Hyperparameter search with a stated budget, and the search space justified.
- Permutation feature importance (not just the impurity-based one) with the difference explained.
- A calibration check: reliability curve plus Brier score, before and after calibration.
- K-Means segmentation of the predicted churners, with the k chosen by a stated method and each
  cluster described in one business sentence.
- A business recommendation with an estimated £/$ impact and the assumptions written out.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Impurity-based feature importance is biased toward high-cardinality features, which is why
`customer_id` will show up as important if you leave it in. Permutation importance on the
validation set is what you report; the difference between the two is a good interview answer.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
