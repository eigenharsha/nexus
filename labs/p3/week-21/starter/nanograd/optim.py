"""SGD with momentum, and Adam. `standard` track.

The tests check your update rule against the reference arithmetic step by step, so
"it trains" is not enough — the numbers have to match.

SGD (PyTorch's convention):   v = mu*v + g ;  theta -= lr*v
   The other common form uses (1-mu)*g, which differs by a factor of (1-mu) in the
   effective learning rate — a 10x difference at mu = 0.9.

Adam (Kingma & Ba 2015): include the bias correction. Without it the first ~1/(1-b2)
   steps are far too small, which on a short run is the entire run.
"""
from __future__ import annotations

from .engine import Tensor

__all__ = ["Adam", "Optimizer", "SGD"]


class Optimizer:
    def __init__(self, parameters: list[Tensor], lr: float) -> None:
        self.parameters = list(parameters)
        self.lr = lr

    def zero_grad(self) -> None:
        """TODO: actually zero them. Stale gradients make step k+1 the sum of steps
        1..k+1, which trains a model that slowly stops learning while the loss curve
        looks almost right."""
        raise NotImplementedError("Optimizer.zero_grad")

    def step(self) -> None:
        raise NotImplementedError


class SGD(Optimizer):
    def __init__(self, parameters: list[Tensor], lr: float = 0.1,
                 momentum: float = 0.0, weight_decay: float = 0.0) -> None:
        raise NotImplementedError("SGD")


class Adam(Optimizer):
    def __init__(self, parameters: list[Tensor], lr: float = 1e-3,
                 betas: tuple[float, float] = (0.9, 0.999), eps: float = 1e-8,
                 weight_decay: float = 0.0) -> None:
        raise NotImplementedError("Adam")
