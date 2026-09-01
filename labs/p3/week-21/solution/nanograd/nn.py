"""Layers, losses and the module protocol. Thin on purpose — the engine does the work."""
from __future__ import annotations

from collections.abc import Iterator

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
    """y = x @ W + b.

    Kaiming/He initialisation: `std = sqrt(2 / fan_in)`. With ReLU, half the
    activations are zeroed, so the variance halves at every layer; the factor of 2
    is what keeps the signal from vanishing in a deep stack. Xavier (`1 / fan_in`)
    is the same argument for tanh, where nothing is zeroed.
    """

    def __init__(self, in_features: int, out_features: int, bias: bool = True,
                 seed: int | None = None) -> None:
        rng = np.random.default_rng(seed)
        std = np.sqrt(2.0 / in_features)
        self.weight = Tensor(rng.normal(0.0, std, (in_features, out_features)),
                             requires_grad=True)
        self.bias = Tensor(np.zeros(out_features), requires_grad=True) if bias else None

    def forward(self, x: Tensor) -> Tensor:
        out = x @ self.weight
        return out + self.bias if self.bias is not None else out

    def parameters(self) -> list[Tensor]:
        return [self.weight] + ([self.bias] if self.bias is not None else [])


class ReLU(Module):
    def forward(self, x: Tensor) -> Tensor:
        return x.relu()


class Tanh(Module):
    def forward(self, x: Tensor) -> Tensor:
        return x.tanh()


class Softmax(Module):
    """Row-wise softmax, stabilised by subtracting the row max.

    In a classifier you almost never want this: use `CrossEntropyLoss` on the raw
    logits instead, which is both more stable and a much simpler gradient. This
    exists because the spec asks for it and because seeing the fused version beside
    it is the lesson.
    """

    def forward(self, x: Tensor) -> Tensor:
        shifted = x - Tensor(x.data.max(axis=-1, keepdims=True))
        e = shifted.exp()
        return e / e.sum(axis=-1, keepdims=True)


class Sequential(Module):
    def __init__(self, *layers: Module) -> None:
        self.layers = list(layers)

    def forward(self, x: Tensor) -> Tensor:
        for layer in self.layers:
            x = layer(x)
        return x

    def parameters(self) -> list[Tensor]:
        return [p for layer in self.layers for p in layer.parameters()]

    def __iter__(self) -> Iterator[Module]:
        return iter(self.layers)


class CrossEntropyLoss:
    """Softmax and cross-entropy, FUSED.

    Computed separately, the forward pass takes `log(softmax(z))` — which is
    `log` of a number that can underflow to 0 — and the backward pass is a Jacobian
    product. Fused, the forward is `logsumexp(z) - z[y]` (never underflows) and the
    gradient is `(p - y) / n`, which is three lines. This is why every framework
    ships `cross_entropy(logits, targets)` and warns you off `softmax` + `nll`.
    """

    def __call__(self, logits: Tensor, targets: np.ndarray) -> Tensor:
        return self.forward(logits, targets)

    def forward(self, logits: Tensor, targets: np.ndarray) -> Tensor:
        idx = np.asarray(targets, dtype=np.int64).ravel()
        n = logits.shape[0]
        z = logits.data
        shifted = z - z.max(axis=1, keepdims=True)
        log_sum = np.log(np.exp(shifted).sum(axis=1, keepdims=True))
        log_probs = shifted - log_sum
        loss_value = -log_probs[np.arange(n), idx].mean()

        out = Tensor(loss_value, requires_grad=logits.requires_grad,
                     _parents=(logits,) if logits.requires_grad else (),
                     _op="cross_entropy")

        def _backward() -> None:
            assert out.grad is not None
            if logits.requires_grad:
                p = np.exp(log_probs)
                p[np.arange(n), idx] -= 1.0
                logits._accumulate(out.grad * p / n)

        out._backward = _backward
        return out
