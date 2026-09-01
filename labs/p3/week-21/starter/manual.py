"""`basic` track — a 2-layer network with hand-written backprop, no engine.

Write this once by hand and the autograd engine stops being magic: `backward()` is
literally this file, generated at runtime.

Forward:
    z1 = X @ W1 + b1
    a1 = relu(z1)
    z2 = a1 @ W2 + b2
    L  = mean cross-entropy(z2, y)

Backward — derive it on paper first, it takes fifteen minutes:
    dz2 = (softmax(z2) - onehot(y)) / n
    dW2 = a1.T @ dz2          db2 = dz2.sum(0)
    da1 = dz2 @ W2.T          dz1 = da1 * (z1 > 0)
    dW1 = X.T @ dz1           db1 = dz1.sum(0)

The test differentiates your loss numerically and compares. It will find a wrong sign,
a missing transpose, and a forgotten /n.
"""
from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]

__all__ = ["forward_backward", "init_params"]


def init_params(n_in: int, n_hidden: int, n_out: int, seed: int = 0) -> dict[str, Array]:
    """He initialisation: std = sqrt(2 / fan_in). With ReLU half the activations are
    zeroed, so the variance halves per layer; the 2 is what stops the signal dying."""
    rng = np.random.default_rng(seed)
    return {
        "W1": rng.normal(0, np.sqrt(2.0 / n_in), (n_in, n_hidden)),
        "b1": np.zeros(n_hidden),
        "W2": rng.normal(0, np.sqrt(2.0 / n_hidden), (n_hidden, n_out)),
        "b2": np.zeros(n_out),
    }


def forward_backward(params: dict[str, Array], X: Array,
                     y: NDArray[np.int64]) -> tuple[float, dict[str, Array]]:
    """Return (mean cross-entropy loss, gradients keyed exactly like `params`).

    TODO: implement the forward and backward passes above.

    Compute the loss from log-probabilities via the shifted logits
    (`z - z.max(axis=1, keepdims=True)`); taking `log(softmax(z))` directly will
    take `log(0)` on the first badly-scaled input you hand it.
    """
    raise NotImplementedError("forward_backward")
