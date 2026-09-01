"""`nanograd` — YOUR WORK GOES HERE.

basic:    manual.py — a 2-layer net with hand-written backprop.
standard: engine.py, nn.py, optim.py, gradcheck.py — the autograd engine and the
          network built on it, trained to >=95% test accuracy.
hard:     broadcasting, checkpoint(), and the PyTorch parity test.

No PyTorch, no TensorFlow, no JAX. There is a test that greps your source for them.
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
