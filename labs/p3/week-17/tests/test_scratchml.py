"""Acceptance tests for LAB-P3-W17 — `scratchml`.

The bar is not "it trains". The bar is "it agrees with scikit-learn", which is the
only way to know your regularization convention, your intercept handling and your
gradient are all right at the same time.
"""
from __future__ import annotations

import numpy as np
import pytest

from scratchml import (
    LinearRegression,
    LogisticRegression,
    SoftmaxRegression,
    check_gradient,
    learning_curve,
    log_loss,
    sigmoid,
    softmax,
)

sklearn = pytest.importorskip("sklearn")
from sklearn.datasets import (  # noqa: E402
    load_breast_cancer,
    load_diabetes,
    make_classification,
    make_regression,
)
from sklearn.linear_model import LogisticRegression as SkLogistic  # noqa: E402
from sklearn.linear_model import LinearRegression as SkLinear  # noqa: E402
from sklearn.linear_model import Ridge as SkRidge  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402


def standardized(X: np.ndarray) -> np.ndarray:
    return StandardScaler().fit_transform(X)


# ============================================================== basic
@pytest.mark.basic
def test_single_feature_linear_regression_matches_closed_form() -> None:
    rng = np.random.default_rng(0)
    x = rng.normal(size=(200, 1))
    y = 3.5 * x[:, 0] - 1.25 + rng.normal(scale=0.1, size=200)

    model = LinearRegression(solver="gd", max_iter=50_000).fit(x, y)
    assert model.coef_.shape == (1,)
    assert model.coef_[0] == pytest.approx(3.5, abs=1e-2)
    assert model.intercept_ == pytest.approx(-1.25, abs=1e-2)
    assert model.score(x, y) > 0.99


@pytest.mark.basic
def test_loss_history_decreases_monotonically() -> None:
    X, y = make_regression(n_samples=200, n_features=3, noise=5.0, random_state=1)
    model = LinearRegression(solver="gd", max_iter=500).fit(X, y)
    history = model.loss_history_
    assert len(history) > 10
    assert all(b <= a + 1e-9 for a, b in zip(history, history[1:], strict=False)), (
        "gradient descent with a 1/L step must never increase the loss"
    )


@pytest.mark.basic
def test_sigmoid_and_softmax_are_numerically_stable() -> None:
    extreme = np.array([-800.0, -50.0, 0.0, 50.0, 800.0])
    p = sigmoid(extreme)
    assert np.all(np.isfinite(p)), "sigmoid overflowed — use the piecewise form"
    assert p[0] == pytest.approx(0.0, abs=1e-300)
    assert p[-1] == pytest.approx(1.0)
    assert p[2] == pytest.approx(0.5)

    z = np.array([[1000.0, 1001.0, 999.0], [-1000.0, -1001.0, -999.0]])
    s = softmax(z)
    assert np.all(np.isfinite(s)), "softmax overflowed — subtract the row max"
    assert np.allclose(s.sum(axis=1), 1.0)

    assert np.isfinite(log_loss(np.array([1.0, 0.0]), np.array([-800.0, 800.0])))


# ============================================================== standard
@pytest.mark.standard
def test_ols_matches_sklearn_linear_regression() -> None:
    X, y = make_regression(n_samples=400, n_features=6, noise=10.0, random_state=3)
    mine = LinearRegression().fit(X, y)
    theirs = SkLinear().fit(X, y)
    assert np.allclose(mine.coef_, theirs.coef_, atol=1e-8)
    assert mine.intercept_ == pytest.approx(theirs.intercept_, abs=1e-8)
    assert mine.score(X, y) == pytest.approx(theirs.score(X, y), abs=1e-10)


@pytest.mark.standard
@pytest.mark.parametrize("alpha", [0.5, 3.0, 25.0])
def test_ridge_matches_sklearn_and_never_penalizes_the_intercept(alpha: float) -> None:
    X, y = make_regression(n_samples=300, n_features=8, noise=15.0, random_state=4)
    y = y + 500.0                     # a big constant shift
    mine = LinearRegression(alpha=alpha).fit(X, y)
    theirs = SkRidge(alpha=alpha).fit(X, y)
    assert np.allclose(mine.coef_, theirs.coef_, atol=1e-8), (
        "coefficients differ from sklearn Ridge — check the penalty convention"
    )
    assert mine.intercept_ == pytest.approx(theirs.intercept_, abs=1e-6), (
        "the intercept moved with the target shift — you are penalizing the intercept"
    )


@pytest.mark.standard
def test_gradient_descent_agrees_with_the_closed_form() -> None:
    """Two independent routes to the same answer. If they disagree, one of them is
    wrong and the closed form is almost never the one."""
    X, y = make_regression(n_samples=300, n_features=5, noise=8.0, random_state=5)
    closed = LinearRegression(alpha=2.0).fit(X, y)
    gd = LinearRegression(alpha=2.0, solver="gd", max_iter=100_000, tol=1e-16).fit(X, y)
    assert np.allclose(gd.coef_, closed.coef_, atol=1e-4)
    assert gd.intercept_ == pytest.approx(closed.intercept_, abs=1e-3)


@pytest.mark.standard
@pytest.mark.parametrize("solver", ["gd", "minibatch", "sgd"])
def test_all_three_optimizers_reach_the_same_place(solver: str) -> None:
    X, y = make_regression(n_samples=400, n_features=4, noise=5.0, random_state=6)
    X = standardized(X)
    closed = LinearRegression().fit(X, y)
    iters = {"gd": 60_000, "minibatch": 400, "sgd": 60}[solver]
    approx = LinearRegression(solver=solver, max_iter=iters, tol=1e-16,
                              random_state=0).fit(X, y)
    assert approx.score(X, y) == pytest.approx(closed.score(X, y), abs=2e-3)


@pytest.mark.standard
def test_logistic_matches_sklearn_on_three_datasets() -> None:
    """Coefficients, not just accuracy. Accuracy hides a wrong regularization
    convention; coefficients do not."""
    datasets = []

    Xa, ya = make_classification(n_samples=800, n_features=6, n_informative=5,
                                 n_redundant=0, random_state=11)
    datasets.append(("synthetic", standardized(Xa), ya))

    bc = load_breast_cancer()
    datasets.append(("breast_cancer", standardized(bc.data), bc.target))

    rng = np.random.default_rng(2)
    Xc = rng.normal(size=(600, 4))
    yc = (Xc @ np.array([1.5, -2.0, 0.5, 0.0]) + rng.normal(scale=0.5, size=600) > 0).astype(int)
    datasets.append(("linear_separable_ish", standardized(Xc), yc))

    for name, X, y in datasets:
        mine = LogisticRegression(C=1.0, max_iter=200_000, tol=1e-16).fit(X, y)
        theirs = SkLogistic(C=1.0, max_iter=10_000).fit(X, y)

        coef_diff = float(np.max(np.abs(mine.coef_ - theirs.coef_[0])))
        proba_diff = float(np.max(np.abs(
            mine.predict_proba(X)[:, 1] - theirs.predict_proba(X)[:, 1]
        )))
        assert coef_diff < 2e-2, f"{name}: max coefficient difference {coef_diff:.2e}"
        assert proba_diff < 5e-3, f"{name}: max probability difference {proba_diff:.2e}"
        assert mine.score(X, y) == pytest.approx(theirs.score(X, y), abs=1e-3), name

        # The stronger claim, and the one that makes the tolerances above defensible:
        # evaluate BOTH parameter vectors under OUR objective. If ours scores at least
        # as low, the remaining coefficient difference is flatness of the optimum, not
        # a wrong convention. On breast_cancer the coefficients differ by ~1.6e-2 and
        # our objective is lower by ~2e-6: gradient descent walked further down a very
        # flat valley than L-BFGS bothered to.
        Xd = np.hstack([np.ones((X.shape[0], 1)), X])
        probe = LogisticRegression(C=1.0)
        probe._n = X.shape[0]
        ours = probe._loss(np.concatenate([[mine.intercept_], mine.coef_]), Xd, y.astype(float))
        sk = probe._loss(np.concatenate([theirs.intercept_, theirs.coef_[0]]), Xd, y.astype(float))
        assert ours <= sk + 1e-6, (
            f"{name}: our objective {ours:.9f} is worse than sklearn's {sk:.9f} — "
            f"that is a convergence bug, not a tolerance question"
        )


@pytest.mark.standard
@pytest.mark.parametrize("C", [0.05, 1.0, 100.0])
def test_C_behaves_like_the_inverse_of_lambda(C: float) -> None:
    X, y = make_classification(n_samples=500, n_features=8, n_informative=6,
                               n_redundant=0, random_state=12)
    X = standardized(X)
    mine = LogisticRegression(C=C, max_iter=200_000, tol=1e-16).fit(X, y)
    theirs = SkLogistic(C=C, max_iter=10_000).fit(X, y)
    assert np.allclose(mine.coef_, theirs.coef_[0], atol=1e-2), (
        f"C={C}: your regularization strength does not match sklearn's"
    )


@pytest.mark.standard
def test_smaller_C_shrinks_the_coefficients() -> None:
    X, y = make_classification(n_samples=500, n_features=8, n_informative=6,
                               n_redundant=0, random_state=13)
    X = standardized(X)
    norms = [
        float(np.linalg.norm(LogisticRegression(C=C, max_iter=50_000).fit(X, y).coef_))
        for C in (0.01, 0.1, 1.0, 10.0)
    ]
    assert norms == sorted(norms), f"||w|| should grow with C, got {norms}"


@pytest.mark.standard
def test_analytic_gradients_pass_a_numerical_gradient_check() -> None:
    """The single most valuable test in the file: it localises a wrong gradient to a
    line, instead of leaving you staring at a loss curve that almost converges."""
    rng = np.random.default_rng(7)
    n, d = 200, 4
    Xd = np.hstack([np.ones((n, 1)), rng.normal(size=(n, d))])
    y_bin = (rng.random(n) > 0.5).astype(float)
    theta0 = rng.normal(size=d + 1) * 0.3

    logistic = LogisticRegression(C=2.0)
    logistic._n = n
    err = check_gradient(
        lambda t: logistic._loss(t, Xd, y_bin),
        lambda t: logistic._grad(t, Xd, y_bin),
        theta0,
    )
    assert err < 1e-6, f"logistic gradient relative error {err:.2e}"

    y_cont = rng.normal(size=n)
    linear = LinearRegression(alpha=1.5, solver="gd")
    err = check_gradient(
        lambda t: linear._loss(t, Xd, y_cont),
        lambda t: linear._grad(t, Xd, y_cont),
        theta0,
    )
    assert err < 1e-6, f"linear gradient relative error {err:.2e}"


@pytest.mark.standard
def test_no_python_loop_over_samples_in_fit() -> None:
    """Vectorized means vectorized. 20,000 rows x 50 features must fit in well under
    a second; a per-sample Python loop takes tens of seconds."""
    import time

    X, y = make_regression(n_samples=20_000, n_features=50, noise=1.0, random_state=8)
    t0 = time.perf_counter()
    LinearRegression(solver="gd", max_iter=200).fit(X, y)
    elapsed = time.perf_counter() - t0
    assert elapsed < 5.0, f"200 full-batch iterations took {elapsed:.1f}s — not vectorized"


@pytest.mark.standard
def test_fit_rejects_mismatched_shapes() -> None:
    with pytest.raises(ValueError):
        LinearRegression().fit(np.zeros((10, 3)), np.zeros(9))


@pytest.mark.standard
def test_r2_matches_sklearn_on_a_real_dataset() -> None:
    data = load_diabetes()
    mine = LinearRegression().fit(data.data, data.target)
    theirs = SkLinear().fit(data.data, data.target)
    assert mine.score(data.data, data.target) == pytest.approx(
        theirs.score(data.data, data.target), abs=1e-10
    )


# ============================================================== hard
@pytest.mark.hard
def test_softmax_multiclass_agrees_with_sklearn() -> None:
    X, y = make_classification(n_samples=2000, n_features=8, n_informative=6,
                               n_redundant=0, n_classes=4, random_state=21)
    X = standardized(X)
    # Full-batch, run to convergence: mini-batch SGD at 400 epochs agrees with
    # sklearn on only ~86% of labels, which is a convergence question rather than a
    # correctness one. Run `make bench` to see the epochs-vs-agreement curve.
    mine = SoftmaxRegression(C=1.0, solver="gd", max_iter=20_000, tol=0.0).fit(X, y)
    theirs = SkLogistic(C=1.0, max_iter=5000).fit(X, y)
    assert mine.classes_.tolist() == theirs.classes_.tolist()
    assert mine.predict_proba(X).shape == (2000, 4)
    assert np.allclose(mine.predict_proba(X).sum(axis=1), 1.0)
    agreement = float(np.mean(mine.predict(X) == theirs.predict(X)))
    assert agreement > 0.98, f"only {agreement:.1%} label agreement with sklearn"
    assert mine.score(X, y) > theirs.score(X, y) - 0.01


@pytest.mark.hard
def test_early_stopping_halts_before_max_iter_and_keeps_the_best_weights() -> None:
    X, y = make_classification(n_samples=1500, n_features=10, n_informative=5,
                               n_redundant=3, n_classes=3, random_state=22)
    X = standardized(X)
    model = SoftmaxRegression(C=100.0, max_iter=400, early_stopping=True,
                              patience=5, batch_size=64).fit(X, y)
    assert model.n_iter_ < 400, "early stopping never triggered"
    assert model.converged_
    assert model.best_iter_ <= model.n_iter_
    assert len(model.val_loss_history_) == model.n_iter_
    best = min(model.val_loss_history_)
    assert model.val_loss_history_[model.best_iter_ - 1] == pytest.approx(best)


@pytest.mark.hard
def test_softmax_never_materialises_a_full_one_hot_matrix() -> None:
    """1M rows x 20 classes of float64 one-hot is 160 MB of mostly zeros. The
    mini-batch path must allocate per batch, not per dataset."""
    import tracemalloc

    rng = np.random.default_rng(31)
    n, d, k = 60_000, 6, 40
    X = rng.normal(size=(n, d))
    y = rng.integers(0, k, size=n)

    model = SoftmaxRegression(C=1.0, max_iter=2, batch_size=256)
    tracemalloc.start()
    tracemalloc.reset_peak()
    model.fit(X, y)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    one_hot_bytes = n * k * 8
    assert peak < one_hot_bytes / 2, (
        f"peak allocation {peak / 1e6:.1f} MB vs {one_hot_bytes / 1e6:.1f} MB for a full "
        f"one-hot matrix — the target is being materialised for the whole dataset"
    )


@pytest.mark.hard
def test_learning_curve_distinguishes_bias_from_variance() -> None:
    rng = np.random.default_rng(41)
    n = 800
    X = rng.normal(size=(n, 12))

    # High variance: many features, few informative, no regularization.
    y_noisy = X[:, 0] * 2 + rng.normal(scale=3.0, size=n)
    variance = learning_curve(lambda: LinearRegression(alpha=0.0), X, y_noisy)
    gap_small = variance["train_score"][0] - variance["val_score"][0]
    gap_large = variance["train_score"][-1] - variance["val_score"][-1]
    assert gap_small > gap_large, (
        "the train/validation gap should narrow as the training set grows"
    )

    for key in ("size", "train_score", "val_score"):
        assert len(variance[key]) == 5
    assert variance["size"] == sorted(variance["size"])
