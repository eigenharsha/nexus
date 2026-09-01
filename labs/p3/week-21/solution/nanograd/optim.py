"""SGD with momentum, and Adam. Both match the update rules in their papers."""
from __future__ import annotations

import numpy as np

from .engine import Tensor

__all__ = ["Adam", "Optimizer", "SGD"]


class Optimizer:
    def __init__(self, parameters: list[Tensor], lr: float) -> None:
        self.parameters = list(parameters)
        self.lr = lr

    def zero_grad(self) -> None:
        """Actually zero them. Leaving stale gradients in place means step k+1 is
        computed from the sum of steps 1..k+1, which trains a model that slowly
        stops learning, and the loss curve looks *almost* right."""
        for p in self.parameters:
            p.grad = None

    def step(self) -> None:
        raise NotImplementedError


class SGD(Optimizer):
    """v = mu * v + g ; theta -= lr * v   (PyTorch's convention, not the
    (1 - mu) * g variant — they differ by a factor of (1 - mu) in the effective
    learning rate, which is a 10x difference at mu = 0.9)."""

    def __init__(self, parameters: list[Tensor], lr: float = 0.1,
                 momentum: float = 0.0, weight_decay: float = 0.0) -> None:
        super().__init__(parameters, lr)
        self.momentum = momentum
        self.weight_decay = weight_decay
        self._velocity: list[np.ndarray | None] = [None] * len(self.parameters)

    def step(self) -> None:
        for i, p in enumerate(self.parameters):
            if p.grad is None:
                continue
            g = p.grad
            if self.weight_decay:
                g = g + self.weight_decay * p.data
            if self.momentum:
                v = self._velocity[i]
                v = g.copy() if v is None else self.momentum * v + g
                self._velocity[i] = v
                g = v
            p.data -= self.lr * g


class Adam(Optimizer):
    """Kingma & Ba 2015, including the bias correction.

    Without the bias correction the first few steps are far too small, because m and
    v start at zero. It matters most in the first ~1/(1-beta2) = 1,000 steps, which
    on a short run is the entire run.
    """

    def __init__(self, parameters: list[Tensor], lr: float = 1e-3,
                 betas: tuple[float, float] = (0.9, 0.999), eps: float = 1e-8,
                 weight_decay: float = 0.0) -> None:
        super().__init__(parameters, lr)
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay
        self._m: list[np.ndarray] = [np.zeros_like(p.data) for p in self.parameters]
        self._v: list[np.ndarray] = [np.zeros_like(p.data) for p in self.parameters]
        self.t = 0

    def step(self) -> None:
        self.t += 1
        for i, p in enumerate(self.parameters):
            if p.grad is None:
                continue
            g = p.grad
            if self.weight_decay:
                g = g + self.weight_decay * p.data
            self._m[i] = self.beta1 * self._m[i] + (1 - self.beta1) * g
            self._v[i] = self.beta2 * self._v[i] + (1 - self.beta2) * (g * g)
            m_hat = self._m[i] / (1 - self.beta1 ** self.t)
            v_hat = self._v[i] / (1 - self.beta2 ** self.t)
            p.data -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)
