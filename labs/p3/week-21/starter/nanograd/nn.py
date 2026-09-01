"""Layers and losses. `standard` track. Thin on purpose — the engine does the work."""
from __future__ import annotations

import numpy as np

from .engine import Tensor

__all__ = ["CrossEntropyLoss", "Linear", "Module", "ReLU", "Sequential", "Softmax", "Tanh"]


class Module:
    def parameters(self) -> list[Tensor]:
        return []

    def zero_grad(self) -> None:
        for p in self.parameters():
            p.zero_grad()

    def __call__(self, x: Tensor) -> Tensor:
        return self.forward(x)

    def forward(self, x: Tensor) -> Tensor:
        raise NotImplementedError


class Linear(Module):
    """y = x @ W + b, He-initialised: std = sqrt(2 / fan_in).

    Signature must be `Linear(in_features, out_features, bias=True, seed=None)` and
    the weight must be `.weight` of shape (in, out) with bias `.bias` of shape (out,)
    — the parity test writes into them directly.
    """

    def __init__(self, in_features: int, out_features: int, bias: bool = True,
                 seed: int | None = None) -> None:
        raise NotImplementedError("Linear")


class ReLU(Module):
    def forward(self, x: Tensor) -> Tensor:
        raise NotImplementedError


class Tanh(Module):
    def forward(self, x: Tensor) -> Tensor:
        raise NotImplementedError


class Softmax(Module):
    """Row-wise softmax, stabilised by subtracting the row max.

    You almost never want this in a classifier — use CrossEntropyLoss on raw logits.
    It exists so you can see the fused version beside it.
    """

    def forward(self, x: Tensor) -> Tensor:
        raise NotImplementedError


class Sequential(Module):
    def __init__(self, *layers: Module) -> None:
        raise NotImplementedError


class CrossEntropyLoss:
    """Softmax and cross-entropy, FUSED.

    Forward:  logsumexp(z) - z[y]        (never underflows)
    Backward: (softmax(z) - onehot(y)) / n     (three lines)

    Computed separately, the forward takes log of a number that can underflow to 0 and
    the backward is a Jacobian product. This is why every framework ships
    `cross_entropy(logits, targets)` and warns you off softmax + nll.
    """

    def __call__(self, logits: Tensor, targets: np.ndarray) -> Tensor:
        return self.forward(logits, targets)

    def forward(self, logits: Tensor, targets: np.ndarray) -> Tensor:
        raise NotImplementedError("CrossEntropyLoss")
