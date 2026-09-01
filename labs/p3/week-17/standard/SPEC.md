# `standard` — LAB-P3-W17

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 6-7 h

## Acceptance criteria

- `LinearRegression` and `LogisticRegression` classes with a scikit-learn-compatible API:
  `fit(X, y)`, `predict(X)`, `predict_proba(X)` (classifier), `score(X, y)`, and the fitted
  attributes `coef_` and `intercept_`.
- Fully vectorized — no Python loop over samples anywhere in `fit`.
- L2 regularization (and L1 for the linear model), with the convention documented: is the penalty
  divided by n or not, and is the intercept penalized? Match scikit-learn's answer.
- Three optimizers: full-batch GD, SGD, and mini-batch, selected by parameter.
- Convergence tracking: a `loss_history_` attribute and a documented stopping criterion.
- A `check_gradient` utility comparing the analytic gradient to a central-difference
  approximation, with a relative error below 1e-6.
- Results matching scikit-learn on three datasets to a stated tolerance — coefficients for the
  linear model, and predicted probabilities for the classifier.
- Numerically stable: `log_loss` computed via `logaddexp`, sigmoid without `exp` overflow.
  The test feeds inputs at +/-800 and asserts no `nan`.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

The two places everyone loses a day:

1. **`exp` overflow.** `1/(1+exp(-z))` gives `inf` and then `nan` for z = -800. Use the piecewise
   form or `scipy.special.expit`'s trick. The test will find this.
2. **The regularization convention.** scikit-learn's `LogisticRegression` uses `C = 1/lambda`
   and does **not** penalize the intercept. If you penalize the intercept your coefficients will
   be close but never equal, and you will spend an hour on it.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
