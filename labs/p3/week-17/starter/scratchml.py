"""`scratchml` — YOUR WORK GOES HERE.

basic:    single-feature linear regression by gradient descent (TODOs below).
standard: LinearRegression + LogisticRegression, scikit-learn-compatible, matching
          scikit-learn's coefficients on three datasets.
hard:     SoftmaxRegression with early stopping and a learning-curve tool.

Two conventions decide whether your coefficients MATCH scikit-learn or merely sit
near it. Get these wrong and you will spend an afternoon on a 3% discrepancy:

1. The intercept is NOT penalized. Fit it by centering, or exclude column 0 from
   the penalty term. There is a test that shifts the target by +500 and checks
   that only the intercept moves.

2. scikit-learn's logistic objective is `C * sum(log_loss) + 0.5 * ||w||^2`, a SUM.
   Divide by (C * n) and you get `mean(log_loss) + ||w||^2 / (2 * C * n)`. Same
   minimizer, comparable coefficients. `C` is the INVERSE of the regularization
   strength: bigger C means less regularization.

And two numerical traps, both of which the tests feed you deliberately:

  * `1/(1+exp(-z))` is `nan` at z = -800. Write sigmoid piecewise.
  * `softmax` without subtracting the row max is `nan` at z = 1000.
"""
from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]

__all__ = [
    "LinearRegression", "LogisticRegression", "SoftmaxRegression",
    "check_gradient", "learning_curve", "log_loss", "sigmoid", "softmax",
]


def sigmoid(z: Array) -> Array:
    """TODO (basic): numerically stable logistic function.

    Split on the sign of z so `exp` is never called on a positive argument.
    """
    raise NotImplementedError("sigmoid")


def log_loss(y: Array, z: Array) -> float:
    """TODO (standard): mean binary cross-entropy from the LOGITS, not from
    probabilities. `np.logaddexp(0, z) - y * z` is the whole function and it cannot
    take log(0)."""
    raise NotImplementedError("log_loss")


def softmax(z: Array) -> Array:
    """TODO (hard): row-wise softmax. Subtract the row max first."""
    raise NotImplementedError("softmax")


def check_gradient(
    f: Callable[[Array], float],
    grad: Callable[[Array], Array],
    x: Array,
    eps: float = 1e-5,
) -> float:
    """TODO (standard): max relative error between the analytic gradient and a
    central difference `(f(x+h) - f(x-h)) / 2h`.

    Why h = 1e-5: truncation error is O(h^2), round-off is O(machine_eps / h), and
    on float64 they cross near 1e-5. h = 1e-12 is worse, not better — and being able
    to say why is most of the point of writing this function.
    """
    raise NotImplementedError("check_gradient")


class LinearRegression:
    """Ordinary least squares, or ridge when alpha > 0.

    Objective, matching `sklearn.linear_model.Ridge`:

        ||y - Xw - b||^2 + alpha * ||w||^2       (a SUM of squares)

    Required attributes after `fit`: `coef_`, `intercept_`, `loss_history_`,
    `n_iter_`, `converged_`. Required methods: fit, predict, score (R^2).

    `solver` is one of "normal" (closed form), "gd", "sgd", "minibatch".
    Implement "normal" first — it is three lines and it becomes the oracle you check
    the iterative solvers against.
    """

    def __init__(self, *, alpha: float = 0.0, penalty: str = "l2",
                 solver: str = "normal", learning_rate: float | None = None,
                 max_iter: int = 20000, tol: float = 1e-12, batch_size: int = 64,
                 random_state: int = 0, fit_intercept: bool = True) -> None:
        raise NotImplementedError("LinearRegression")

    def fit(self, X: Array, y: Array) -> "LinearRegression":
        raise NotImplementedError

    def predict(self, X: Array) -> Array:
        raise NotImplementedError

    def score(self, X: Array, y: Array) -> float:
        raise NotImplementedError


class LogisticRegression:
    """Binary logistic regression with L2 regularization.

    Objective:  mean(log_loss) + ||w||^2 / (2 * C * n)

    Required after `fit`: `coef_`, `intercept_`, `classes_`, `loss_history_`,
    `n_iter_`, `converged_`.
    Required methods: fit, predict, predict_proba, decision_function, score.

    A hint you will want later: for an L-smooth convex objective, a step size of
    1/L is the largest one that cannot diverge. For logistic regression,
    L <= 0.25 * ||X||_2^2 / n + (regularization). Deriving the step instead of
    hand-tuning it is why the tests never see a nan loss.
    """

    def __init__(self, *, C: float = 1.0, solver: str = "gd",
                 learning_rate: float | None = None, max_iter: int = 20000,
                 tol: float = 1e-12, batch_size: int = 64, random_state: int = 0,
                 fit_intercept: bool = True) -> None:
        raise NotImplementedError("LogisticRegression")

    def fit(self, X: Array, y: Array) -> "LogisticRegression":
        raise NotImplementedError

    def predict_proba(self, X: Array) -> Array:
        raise NotImplementedError

    def predict(self, X: Array) -> Array:
        raise NotImplementedError

    def score(self, X: Array, y: Array) -> float:
        raise NotImplementedError


class SoftmaxRegression:
    """`hard` — multinomial logistic regression, early stopping, 1M rows in budget.

    The memory constraint is the design constraint: never build the full n x k
    one-hot target matrix. At 1M rows and 20 classes that is 160 MB of mostly zeros,
    and the gradient does not need it — `p[range(n), y] -= 1` on the batch is enough.
    Evaluate the training loss in chunks too, for the same reason.
    """

    def __init__(self, *, C: float = 1.0, solver: str = "minibatch",
                 learning_rate: float | None = None, max_iter: int = 500,
                 tol: float = 1e-9, batch_size: int = 256, random_state: int = 0,
                 early_stopping: bool = False, validation_fraction: float = 0.1,
                 patience: int = 10) -> None:
        raise NotImplementedError("SoftmaxRegression")

    def fit(self, X: Array, y: Array) -> "SoftmaxRegression":
        raise NotImplementedError

    def predict_proba(self, X: Array) -> Array:
        raise NotImplementedError

    def predict(self, X: Array) -> Array:
        raise NotImplementedError

    def score(self, X: Array, y: Array) -> float:
        raise NotImplementedError


def learning_curve(model_factory, X: Array, y: Array,  # noqa: ANN001
                   sizes: list[float] | None = None,
                   random_state: int = 0) -> dict[str, list[float]]:
    """`hard` — training and validation score against training-set size.

    Return {"size": [...], "train_score": [...], "val_score": [...]}.

    How to read the output, which is the deliverable:
      both curves low and converged      -> bias-limited; more data will not help
      wide gap, still closing            -> variance-limited; more data will help
      wide gap that stopped closing      -> regularize or drop features
    """
    raise NotImplementedError("learning_curve")
