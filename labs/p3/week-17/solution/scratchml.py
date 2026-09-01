"""`scratchml` — linear and logistic regression from NumPy, matching scikit-learn.

Reference implementation for LAB-P3-W17.

Two conventions decide whether your coefficients match scikit-learn's or merely sit
near them, and both are worth writing down because they cost people an afternoon:

1. **The intercept is not penalized.** Penalizing it makes the model sensitive to a
   constant shift of the target, which is never what you want, and scikit-learn does
   not do it. Fit the intercept by centering, or exclude column 0 from the penalty.

2. **`C` is the inverse of lambda, and scikit-learn's logistic objective is a SUM,
   not a mean.** It minimizes `C * sum(log_loss) + 0.5 * ||w||^2`. Divide through by
   `C * n` and you get `mean(log_loss) + ||w||^2 / (2 * C * n)`, which is the form
   implemented here. Same minimizer, and now `coef_` is directly comparable.

Numerical stability is the other half. `1/(1+exp(-z))` returns `nan` for z = -800;
`np.logaddexp` does not. The test suite feeds inputs at +/-800 for exactly this reason.
"""
from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]

__all__ = [
    "LinearRegression",
    "LogisticRegression",
    "SoftmaxRegression",
    "check_gradient",
    "learning_curve",
    "log_loss",
    "sigmoid",
    "softmax",
]


# --------------------------------------------------------------------------- math
def sigmoid(z: Array) -> Array:
    """Numerically stable logistic function.

    The naive form overflows `exp` for large negative z and returns `inf`, then `nan`.
    The piecewise form below never evaluates `exp` on a positive argument.
    """
    out = np.empty_like(z, dtype=np.float64)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1.0 + ez)
    return out


def log_loss(y: Array, z: Array) -> float:
    """Mean binary cross-entropy computed from the LOGITS.

    Computing probabilities first and then taking their log loses precision and can
    take log(0). `log(1 + exp(-|z|))` via `logaddexp` cannot.
    """
    return float(np.mean(np.logaddexp(0.0, z) - y * z))


def softmax(z: Array) -> Array:
    """Row-wise softmax. Subtracting the row max is not an optimisation; without it
    `exp(1000)` is `inf` and every probability becomes `nan`."""
    shifted = z - z.max(axis=1, keepdims=True)
    e = np.exp(shifted)
    return e / e.sum(axis=1, keepdims=True)


# ----------------------------------------------------------------------- gradients
def check_gradient(
    f: Callable[[Array], float],
    grad: Callable[[Array], Array],
    x: Array,
    eps: float = 1e-5,
) -> float:
    """Max relative error between an analytic gradient and a central difference.

    Central differences have O(h^2) truncation error and O(eps_machine / h) round-off.
    On float64 the two cross at h ~ 1e-5, giving ~1e-10 total. h = 1e-12 is *worse*,
    not better: round-off dominates and you get noise. That trade is the point of the
    exercise, not the number.
    """
    x = np.asarray(x, dtype=np.float64)
    analytic = np.asarray(grad(x), dtype=np.float64).ravel()
    numeric = np.zeros_like(analytic)
    flat = x.ravel().copy()
    for i in range(flat.size):
        original = flat[i]
        flat[i] = original + eps
        plus = f(flat.reshape(x.shape))
        flat[i] = original - eps
        minus = f(flat.reshape(x.shape))
        flat[i] = original
        numeric[i] = (plus - minus) / (2 * eps)
    denom = np.maximum(1e-12, np.abs(analytic) + np.abs(numeric))
    return float(np.max(np.abs(analytic - numeric) / denom))


# ------------------------------------------------------------------------- shared
class _GradientModel:
    """Everything the two models share: the optimizer, the stopping rule, and the
    automatic step size."""

    def __init__(
        self,
        *,
        solver: str = "gd",
        learning_rate: float | None = None,
        max_iter: int = 5000,
        tol: float = 1e-9,
        batch_size: int = 64,
        random_state: int = 0,
        fit_intercept: bool = True,
    ) -> None:
        if solver not in ("gd", "sgd", "minibatch"):
            raise ValueError("solver must be 'gd', 'sgd' or 'minibatch'")
        self.solver = solver
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.tol = tol
        self.batch_size = batch_size
        self.random_state = random_state
        self.fit_intercept = fit_intercept
        self.loss_history_: list[float] = []
        self.n_iter_: int = 0
        self.converged_: bool = False

    def _design(self, X: Array) -> Array:
        X = np.asarray(X, dtype=np.float64)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if self.fit_intercept:
            return np.hstack([np.ones((X.shape[0], 1)), X])
        return X

    def _split(self, theta: Array) -> tuple[Array, float]:
        if self.fit_intercept:
            return theta[1:], float(theta[0])
        return theta, 0.0

    def _descend(
        self,
        X: Array,
        y: Array,
        loss_fn: Callable[[Array, Array, Array], float],
        grad_fn: Callable[[Array, Array, Array], Array],
        lipschitz: float,
    ) -> Array:
        n, d = X.shape
        theta = np.zeros(d)
        # A step of 1/L is the largest one guaranteed not to diverge for an
        # L-smooth convex objective. Hand-tuned learning rates are how people end
        # up with the "my loss went to nan" bug this lab's ticket describes.
        lr = self.learning_rate if self.learning_rate is not None else 1.0 / lipschitz
        rng = np.random.default_rng(self.random_state)
        self.loss_history_ = []
        previous = np.inf

        for it in range(1, self.max_iter + 1):
            if self.solver == "gd":
                theta = theta - lr * grad_fn(theta, X, y)
            else:
                size = 1 if self.solver == "sgd" else min(self.batch_size, n)
                order = rng.permutation(n)
                for start in range(0, n, size):
                    idx = order[start:start + size]
                    theta = theta - lr * grad_fn(theta, X[idx], y[idx])

            current = loss_fn(theta, X, y)
            self.loss_history_.append(current)
            self.n_iter_ = it
            if abs(previous - current) < self.tol * max(1.0, abs(previous)):
                self.converged_ = True
                break
            previous = current
        return theta


# ---------------------------------------------------------------------- regression
class LinearRegression(_GradientModel):
    """Ordinary least squares, or ridge when `alpha > 0`.

    Objective (matching `sklearn.linear_model.Ridge`):

        ||y - Xw - b||^2 + alpha * ||w||^2        (a SUM of squares, not a mean)

    `solver="normal"` solves it in closed form. `solver="gd"` minimises the same
    objective by gradient descent so the two can be compared — and they should agree
    to about 1e-6, which is the single most useful sanity check in the lab.
    """

    def __init__(
        self,
        *,
        alpha: float = 0.0,
        penalty: str = "l2",
        solver: str = "normal",
        learning_rate: float | None = None,
        max_iter: int = 20000,
        tol: float = 1e-12,
        batch_size: int = 64,
        random_state: int = 0,
        fit_intercept: bool = True,
    ) -> None:
        if solver != "normal":
            super().__init__(solver=solver, learning_rate=learning_rate, max_iter=max_iter,
                             tol=tol, batch_size=batch_size, random_state=random_state,
                             fit_intercept=fit_intercept)
        else:
            super().__init__(solver="gd", learning_rate=learning_rate, max_iter=max_iter,
                             tol=tol, batch_size=batch_size, random_state=random_state,
                             fit_intercept=fit_intercept)
        if penalty not in ("l1", "l2", None):
            raise ValueError("penalty must be 'l1', 'l2' or None")
        self.alpha = float(alpha)
        self.penalty = penalty
        self._closed_form = solver == "normal"
        self.coef_: Array = np.empty(0)
        self.intercept_: float = 0.0

    # -- objective ---------------------------------------------------------
    def _penalty(self, theta: Array) -> float:
        w = theta[1:] if self.fit_intercept else theta
        if self.alpha == 0 or self.penalty is None:
            return 0.0
        return self.alpha * (float(np.sum(w ** 2)) if self.penalty == "l2"
                             else float(np.sum(np.abs(w))))

    def _loss(self, theta: Array, X: Array, y: Array) -> float:
        resid = X @ theta - y
        return float(resid @ resid) + self._penalty(theta)

    def _grad(self, theta: Array, X: Array, y: Array) -> Array:
        resid = X @ theta - y
        g = 2.0 * (X.T @ resid)
        if self.alpha and self.penalty:
            reg = np.zeros_like(theta)
            w_slice = slice(1, None) if self.fit_intercept else slice(None)
            reg[w_slice] = (2.0 * self.alpha * theta[w_slice] if self.penalty == "l2"
                            else self.alpha * np.sign(theta[w_slice]))
            g = g + reg
        return g

    # -- api ---------------------------------------------------------------
    def fit(self, X: Array, y: Array) -> "LinearRegression":
        Xd = self._design(X)
        y = np.asarray(y, dtype=np.float64).ravel()
        if Xd.shape[0] != y.shape[0]:
            raise ValueError(f"X has {Xd.shape[0]} rows but y has {y.shape[0]}")

        if self._closed_form:
            reg = np.eye(Xd.shape[1]) * self.alpha
            if self.fit_intercept:
                reg[0, 0] = 0.0            # never penalize the intercept
            theta = np.linalg.solve(Xd.T @ Xd + reg, Xd.T @ y)
            self.loss_history_ = [self._loss(theta, Xd, y)]
            self.n_iter_ = 1
            self.converged_ = True
        else:
            # L for a sum-of-squares objective is 2 * largest eigenvalue of X^T X.
            lipschitz = 2.0 * float(np.linalg.norm(Xd, 2) ** 2) + 2.0 * self.alpha
            theta = self._descend(Xd, y, self._loss, self._grad, lipschitz)

        self.coef_, self.intercept_ = self._split(theta)
        return self

    def predict(self, X: Array) -> Array:
        return self._design(X) @ np.concatenate(
            ([self.intercept_], self.coef_) if self.fit_intercept else (self.coef_,)
        )

    def score(self, X: Array, y: Array) -> float:
        """R^2, the same definition scikit-learn uses."""
        y = np.asarray(y, dtype=np.float64).ravel()
        resid = y - self.predict(X)
        total = y - y.mean()
        return float(1.0 - (resid @ resid) / (total @ total))


class LogisticRegression(_GradientModel):
    """Binary logistic regression with L2 regularization.

    Objective, in the form that makes `coef_` comparable to scikit-learn's:

        mean(log_loss) + ||w||^2 / (2 * C * n)

    which is `C * sum(log_loss) + 0.5 * ||w||^2` divided by `C * n`.
    """

    def __init__(
        self,
        *,
        C: float = 1.0,
        solver: str = "gd",
        learning_rate: float | None = None,
        max_iter: int = 20000,
        tol: float = 1e-12,
        batch_size: int = 64,
        random_state: int = 0,
        fit_intercept: bool = True,
    ) -> None:
        super().__init__(solver=solver, learning_rate=learning_rate, max_iter=max_iter,
                         tol=tol, batch_size=batch_size, random_state=random_state,
                         fit_intercept=fit_intercept)
        if C <= 0:
            raise ValueError("C must be positive")
        self.C = float(C)
        self.coef_: Array = np.empty(0)
        self.intercept_: float = 0.0
        self.classes_: Array = np.array([0, 1])
        self._n: int = 0

    def _reg_scale(self) -> float:
        return 1.0 / (self.C * max(1, self._n))

    def _loss(self, theta: Array, X: Array, y: Array) -> float:
        z = X @ theta
        w = theta[1:] if self.fit_intercept else theta
        return log_loss(y, z) + 0.5 * self._reg_scale() * float(w @ w)

    def _grad(self, theta: Array, X: Array, y: Array) -> Array:
        m = X.shape[0]
        p = sigmoid(X @ theta)
        g = X.T @ (p - y) / m
        reg = np.zeros_like(theta)
        w_slice = slice(1, None) if self.fit_intercept else slice(None)
        reg[w_slice] = self._reg_scale() * theta[w_slice]
        return g + reg

    def fit(self, X: Array, y: Array) -> "LogisticRegression":
        Xd = self._design(X)
        y = np.asarray(y, dtype=np.float64).ravel()
        self.classes_ = np.unique(y)
        if self.classes_.size != 2:
            raise ValueError(f"binary logistic regression needs 2 classes, got {self.classes_.size}")
        y01 = (y == self.classes_[1]).astype(np.float64)
        self._n = Xd.shape[0]
        # Hessian of the mean log-loss is bounded by 0.25 * X^T X / n.
        lipschitz = 0.25 * float(np.linalg.norm(Xd, 2) ** 2) / self._n + self._reg_scale()
        theta = self._descend(Xd, y01, self._loss, self._grad, lipschitz)
        self.coef_, self.intercept_ = self._split(theta)
        return self

    def decision_function(self, X: Array) -> Array:
        return self._design(X) @ np.concatenate(
            ([self.intercept_], self.coef_) if self.fit_intercept else (self.coef_,)
        )

    def predict_proba(self, X: Array) -> Array:
        p1 = sigmoid(self.decision_function(X))
        return np.column_stack([1.0 - p1, p1])

    def predict(self, X: Array) -> Array:
        return self.classes_[(self.decision_function(X) > 0).astype(int)]

    def score(self, X: Array, y: Array) -> float:
        return float(np.mean(self.predict(X) == np.asarray(y).ravel()))


class SoftmaxRegression(_GradientModel):
    """`hard` track — multinomial logistic regression with optional early stopping.

    Deliberately never materialises the full one-hot target matrix for the whole
    dataset when using mini-batches: at 1M rows and 20 classes that is 160 MB of
    float64 to hold a matrix that is 95% zeros.
    """

    def __init__(
        self,
        *,
        C: float = 1.0,
        solver: str = "minibatch",
        learning_rate: float | None = None,
        max_iter: int = 500,
        tol: float = 1e-9,
        batch_size: int = 256,
        random_state: int = 0,
        early_stopping: bool = False,
        validation_fraction: float = 0.1,
        patience: int = 10,
    ) -> None:
        super().__init__(solver=solver, learning_rate=learning_rate, max_iter=max_iter,
                         tol=tol, batch_size=batch_size, random_state=random_state)
        self.C = float(C)
        self.early_stopping = early_stopping
        self.validation_fraction = validation_fraction
        self.patience = patience
        self.coef_: Array = np.empty(0)
        self.intercept_: Array = np.empty(0)
        self.classes_: Array = np.empty(0)
        self.val_loss_history_: list[float] = []
        self.best_iter_: int = 0

    def _loss_theta(self, W: Array, X: Array, y_idx: NDArray[np.int64],
                    chunk: int = 2048) -> float:
        """Evaluated in chunks. A full-dataset `softmax(X @ W)` is n x k floats — at
        1M rows and 20 classes that is 160 MB just to report a training loss."""
        n = X.shape[0]
        total = 0.0
        for start in range(0, n, chunk):
            stop = min(start + chunk, n)
            p = softmax(X[start:stop] @ W)
            rows = np.arange(stop - start)
            total += -float(np.sum(np.log(np.clip(p[rows, y_idx[start:stop]], 1e-300, None))))
        return total / max(1, n) + 0.5 * float(np.sum(W[1:] ** 2)) / (self.C * n)

    def _grad_theta(self, W: Array, X: Array, y_idx: NDArray[np.int64]) -> Array:
        n = X.shape[0]
        p = softmax(X @ W)
        # One-hot only for the current batch, never for the whole dataset.
        p[np.arange(n), y_idx] -= 1.0
        g = X.T @ p / n
        reg = np.zeros_like(W)
        reg[1:] = W[1:] / (self.C * n)
        return g + reg

    def fit(self, X: Array, y: Array) -> "SoftmaxRegression":
        Xd = self._design(X)
        y = np.asarray(y).ravel()
        self.classes_ = np.unique(y)
        lookup = {c: i for i, c in enumerate(self.classes_)}
        y_idx = np.array([lookup[v] for v in y], dtype=np.int64)

        rng = np.random.default_rng(self.random_state)
        if self.early_stopping:
            n_val = max(1, int(len(y_idx) * self.validation_fraction))
            perm = rng.permutation(len(y_idx))
            val, train = perm[:n_val], perm[n_val:]
            Xtr, ytr, Xva, yva = Xd[train], y_idx[train], Xd[val], y_idx[val]
        else:
            Xtr, ytr, Xva, yva = Xd, y_idx, Xd[:0], y_idx[:0]

        n, d = Xtr.shape
        k = self.classes_.size
        W = np.zeros((d, k))
        lipschitz = (0.5 * float(np.linalg.norm(Xtr, 2) ** 2) / n) + 1.0 / (self.C * n)
        lr = self.learning_rate if self.learning_rate is not None else 1.0 / lipschitz

        best_val, best_W, since_best = np.inf, W.copy(), 0
        self.loss_history_, self.val_loss_history_ = [], []
        size = min(self.batch_size, n) if self.solver != "gd" else n

        for it in range(1, self.max_iter + 1):
            order = rng.permutation(n)
            for start in range(0, n, size):
                idx = order[start:start + size]
                W = W - lr * self._grad_theta(W, Xtr[idx], ytr[idx])
            train_loss = self._loss_theta(W, Xtr, ytr)
            self.loss_history_.append(train_loss)
            self.n_iter_ = it

            if self.early_stopping:
                v = self._loss_theta(W, Xva, yva)
                self.val_loss_history_.append(v)
                if v < best_val - 1e-9:
                    best_val, best_W, since_best = v, W.copy(), 0
                    self.best_iter_ = it
                else:
                    since_best += 1
                    if since_best >= self.patience:
                        W = best_W
                        self.converged_ = True
                        break
            elif len(self.loss_history_) > 1 and \
                    abs(self.loss_history_[-2] - train_loss) < self.tol:
                self.converged_ = True
                break

        self.intercept_ = W[0]
        self.coef_ = W[1:].T
        self._W = W
        return self

    def predict_proba(self, X: Array) -> Array:
        return softmax(self._design(X) @ self._W)

    def predict(self, X: Array) -> Array:
        return self.classes_[np.argmax(self.predict_proba(X), axis=1)]

    def score(self, X: Array, y: Array) -> float:
        return float(np.mean(self.predict(X) == np.asarray(y).ravel()))


# -------------------------------------------------------------------- diagnostics
def learning_curve(
    model_factory: Callable[[], object],
    X: Array,
    y: Array,
    sizes: list[float] | None = None,
    random_state: int = 0,
) -> dict[str, list[float]]:
    """Training and validation score against training-set size.

    How to read it, which is the actual deliverable:
      * both curves low and converged  -> bias-limited. A bigger model, or better
        features. More data will not help.
      * a wide gap that is still closing -> variance-limited. More data will help.
      * a wide gap that has stopped closing -> regularize, or drop features.
    """
    sizes = sizes or [0.1, 0.25, 0.5, 0.75, 1.0]
    X = np.asarray(X, dtype=np.float64)
    y = np.asarray(y).ravel()
    rng = np.random.default_rng(random_state)
    perm = rng.permutation(len(y))
    split = int(len(y) * 0.8)
    tr, va = perm[:split], perm[split:]

    out: dict[str, list[float]] = {"size": [], "train_score": [], "val_score": []}
    for frac in sizes:
        k = max(2, int(len(tr) * frac))
        idx = tr[:k]
        model = model_factory()
        model.fit(X[idx], y[idx])  # type: ignore[attr-defined]
        out["size"].append(float(k))
        out["train_score"].append(model.score(X[idx], y[idx]))  # type: ignore[attr-defined]
        out["val_score"].append(model.score(X[va], y[va]))      # type: ignore[attr-defined]
    return out
