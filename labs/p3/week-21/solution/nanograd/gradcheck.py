"""The test that makes the whole engine trustworthy.

A wrong gradient trains anyway — badly, and in a way that looks like a bad learning
rate. `gradcheck` localises it to one operation in under a second.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np

from .engine import Tensor

__all__ = ["gradcheck", "numerical_gradient"]


def numerical_gradient(f: Callable[..., Tensor], inputs: Sequence[Tensor],
                       eps: float = 1e-6) -> list[np.ndarray]:
    """Central differences, one entry at a time.

    O(number of parameters) forward passes — which is exactly why nobody trains this
    way, and exactly why reverse-mode autodiff exists: one backward pass gives you
    every partial derivative at the cost of about two forward passes.
    """
    grads: list[np.ndarray] = []
    for t in inputs:
        g = np.zeros_like(t.data)
        flat = t.data.reshape(-1)
        for i in range(flat.size):
            original = flat[i]
            flat[i] = original + eps
            plus = f(*inputs).data.sum()
            flat[i] = original - eps
            minus = f(*inputs).data.sum()
            flat[i] = original
            g.reshape(-1)[i] = (plus - minus) / (2 * eps)
        grads.append(g)
    return grads


def gradcheck(f: Callable[..., Tensor], inputs: Sequence[Tensor],
              eps: float = 1e-6, tol: float = 1e-6) -> float:
    """Max relative error between analytic and numerical gradients.

    Returns the error so a caller can report it; raises if it exceeds `tol`.

    On float64, central differences with eps = 1e-6 give roughly 1e-9 accuracy.
    Do NOT run this in float32 — the numerical gradient's noise floor there is about
    1e-3 and the check tells you nothing.
    """
    for t in inputs:
        t.grad = None
        t.requires_grad = True

    out = f(*inputs)
    out.backward(np.ones_like(out.data))
    analytic = [t.grad if t.grad is not None else np.zeros_like(t.data) for t in inputs]

    numeric = numerical_gradient(f, inputs, eps=eps)

    worst = 0.0
    for a, n in zip(analytic, numeric, strict=True):
        denom = np.maximum(1e-10, np.abs(a) + np.abs(n))
        worst = max(worst, float(np.max(np.abs(a - n) / denom)))
    if worst > tol:
        raise AssertionError(f"gradcheck failed: max relative error {worst:.3e} > {tol:.1e}")
    return worst
