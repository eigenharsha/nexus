"""Convergence and agreement measurements for LAB-P3-W17.

    make bench IMPL=solution

Two questions this answers, both of which come up the first time your numbers do not
match a library's:

  1. How many iterations does gradient descent need before the coefficients agree
     with scikit-learn to a given tolerance?
  2. What does the choice of optimizer actually cost in wall time for the same
     quality?
"""
from __future__ import annotations

import time

import numpy as np
from sklearn.datasets import load_breast_cancer, make_classification, make_regression
from sklearn.linear_model import LogisticRegression as SkLogistic
from sklearn.preprocessing import StandardScaler

from scratchml import LinearRegression, LogisticRegression, SoftmaxRegression


def convergence_table() -> None:
    print("\n== logistic regression: iterations vs agreement with scikit-learn ==")
    X = StandardScaler().fit_transform(load_breast_cancer().data)
    y = load_breast_cancer().target
    sk = SkLogistic(C=1.0, max_iter=10_000).fit(X, y)
    print(f"  {'max_iter':>9} {'iters':>7} {'wall (s)':>9} {'max |dcoef|':>12} "
          f"{'max |dprob|':>12}")
    for max_iter in (100, 1_000, 10_000, 50_000, 200_000):
        t0 = time.perf_counter()
        m = LogisticRegression(C=1.0, max_iter=max_iter, tol=1e-16).fit(X, y)
        wall = time.perf_counter() - t0
        dc = float(np.max(np.abs(m.coef_ - sk.coef_[0])))
        dp = float(np.max(np.abs(m.predict_proba(X)[:, 1] - sk.predict_proba(X)[:, 1])))
        print(f"  {max_iter:>9} {m.n_iter_:>7} {wall:>9.2f} {dc:>12.2e} {dp:>12.2e}")
    print("  Predicted probabilities agree ~4x more tightly than coefficients do, and")
    print("  they get there sooner. Near the optimum the loss surface is flat: large")
    print("  parameter moves, tiny objective changes. If your coefficients are 1% off")
    print("  and your predictions match, you have converged — not found a bug.")


def optimizer_table() -> None:
    print("\n== optimizers on the same problem (linear regression, n=20,000, d=20) ==")
    X, y = make_regression(n_samples=20_000, n_features=20, noise=5.0, random_state=1)
    X = StandardScaler().fit_transform(X)
    closed = LinearRegression().fit(X, y)
    target = closed.score(X, y)
    print(f"  closed form R^2 = {target:.6f}")
    print(f"  {'solver':>11} {'iters':>7} {'wall (s)':>9} {'R^2':>10} {'gap':>10}")
    for solver, iters in (("gd", 20_000), ("minibatch", 200), ("sgd", 30)):
        t0 = time.perf_counter()
        m = LinearRegression(solver=solver, max_iter=iters, tol=1e-16,
                             random_state=0).fit(X, y)
        wall = time.perf_counter() - t0
        r2 = m.score(X, y)
        print(f"  {solver:>11} {m.n_iter_:>7} {wall:>9.2f} {r2:>10.6f} {target - r2:>10.2e}")


def softmax_table() -> None:
    print("\n== softmax: epochs vs label agreement with scikit-learn (4 classes) ==")
    X, y = make_classification(n_samples=2000, n_features=8, n_informative=6,
                               n_redundant=0, n_classes=4, random_state=21)
    X = StandardScaler().fit_transform(X)
    sk = SkLogistic(C=1.0, max_iter=5000).fit(X, y)
    print(f"  {'solver':>11} {'epochs':>7} {'wall (s)':>9} {'agreement':>10} {'acc':>8}")
    for solver, iters in (("minibatch", 400), ("minibatch", 2000), ("gd", 20_000)):
        t0 = time.perf_counter()
        m = SoftmaxRegression(C=1.0, solver=solver, max_iter=iters, tol=0.0,
                              batch_size=256).fit(X, y)
        wall = time.perf_counter() - t0
        agree = float(np.mean(m.predict(X) == sk.predict(X)))
        print(f"  {solver:>11} {iters:>7} {wall:>9.2f} {agree:>9.1%} {m.score(X, y):>8.4f}")
    print(f"  scikit-learn accuracy: {sk.score(X, y):.4f}")


if __name__ == "__main__":
    convergence_table()
    optimizer_table()
    softmax_table()
