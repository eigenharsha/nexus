"""The test that makes the whole engine trustworthy. `standard` track.

A wrong gradient still trains — badly, and indistinguishably from a bad learning rate.
`gradcheck` localises it to one operation in under a second, which is the difference
between a fifteen-minute fix and a lost evening.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np

from .engine import Tensor

__all__ = ["gradcheck", "numerical_gradient"]


def numerical_gradient(f: Callable[..., Tensor], inputs: Sequence[Tensor],
                       eps: float = 1e-6) -> list[np.ndarray]:
    """TODO: central differences, `(f(x+h) - f(x-h)) / 2h`, one entry at a time.

    O(number of parameters) forward passes — which is exactly why nobody trains this
    way, and exactly why reverse-mode autodiff exists.
    """
    raise NotImplementedError("numerical_gradient")


def gradcheck(f: Callable[..., Tensor], inputs: Sequence[Tensor],
              eps: float = 1e-6, tol: float = 1e-6) -> float:
    """TODO: max relative error between analytic and numerical gradients.

    Return the error; raise AssertionError if it exceeds `tol`.
    Run it in float64. In float32 the numerical gradient's noise floor is ~1e-3 and
    the check tells you nothing.
    """
    raise NotImplementedError("gradcheck")
