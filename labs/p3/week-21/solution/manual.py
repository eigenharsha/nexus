"""`basic` track — a 2-layer network with hand-written backprop, no engine.

Write this once by hand and the autograd engine stops being magic: `backward()` is
this file, generated.

Forward:   z1 = X @ W1 + b1 ; a1 = relu(z1) ; z2 = a1 @ W2 + b2 ; L = CE(z2, y)
Backward:  dz2 = (softmax(z2) - onehot(y)) / n
           dW2 = a1.T @ dz2         db2 = dz2.sum(0)
           da1 = dz2 @ W2.T         dz1 = da1 * (z1 > 0)
           dW1 = X.T @ dz1          db1 = dz1.sum(0)

Every line of that is one application of the chain rule. Derive it on paper before
you read it here; it takes fifteen minutes and it is the fifteen minutes the whole
week is built on.
"""
from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]

__all__ = ["forward_backward", "init_params"]


def init_params(n_in: int, n_hidden: int, n_out: int, seed: int = 0) -> dict[str, Array]:
    rng = np.random.default_rng(seed)
    return {
        "W1": rng.normal(0, np.sqrt(2.0 / n_in), (n_in, n_hidden)),
        "b1": np.zeros(n_hidden),
        "W2": rng.normal(0, np.sqrt(2.0 / n_hidden), (n_hidden, n_out)),
        "b2": np.zeros(n_out),
    }


def forward_backward(params: dict[str, Array], X: Array,
                     y: NDArray[np.int64]) -> tuple[float, dict[str, Array]]:
    """Returns (mean cross-entropy loss, gradients keyed like `params`)."""
    n = X.shape[0]
    W1, b1, W2, b2 = params["W1"], params["b1"], params["W2"], params["b2"]

    z1 = X @ W1 + b1
    a1 = np.maximum(z1, 0.0)
    z2 = a1 @ W2 + b2

    shifted = z2 - z2.max(axis=1, keepdims=True)      # stability, not decoration
    log_probs = shifted - np.log(np.exp(shifted).sum(axis=1, keepdims=True))
    loss = float(-log_probs[np.arange(n), y].mean())

    dz2 = np.exp(log_probs)
    dz2[np.arange(n), y] -= 1.0
    dz2 /= n

    grads = {
        "W2": a1.T @ dz2,
        "b2": dz2.sum(axis=0),
    }
    da1 = dz2 @ W2.T
    dz1 = da1 * (z1 > 0)
    grads["W1"] = X.T @ dz1
    grads["b1"] = dz1.sum(axis=0)
    return loss, grads
