"""`nanograd` — reverse-mode autograd and a neural network, from scratch.

    >>> import numpy as np
    >>> from nanograd import Tensor, Linear, ReLU, Sequential, CrossEntropyLoss, Adam
    >>> net = Sequential(Linear(4, 8, seed=0), ReLU(), Linear(8, 3, seed=1))
    >>> loss_fn, opt = CrossEntropyLoss(), Adam(net.parameters(), lr=0.05)
    >>> x, y = Tensor(np.random.default_rng(0).normal(size=(16, 4))), np.zeros(16, int)
    >>> loss = loss_fn(net(x), y); opt.zero_grad(); loss.backward(); opt.step()
"""
from __future__ import annotations

from .engine import Tensor, checkpoint, no_grad
from .gradcheck import gradcheck, numerical_gradient
from .nn import CrossEntropyLoss, Linear, Module, ReLU, Sequential, Softmax, Tanh
from .optim import SGD, Adam, Optimizer

__all__ = [
    "SGD", "Adam", "CrossEntropyLoss", "Linear", "Module", "Optimizer", "ReLU",
    "Sequential", "Softmax", "Tanh", "Tensor", "checkpoint", "gradcheck",
    "no_grad", "numerical_gradient",
]
