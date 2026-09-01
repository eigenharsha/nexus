"""Reverse-mode automatic differentiation. `standard` track — the core of the lab.

Three ideas, and that really is all of it:

1. Every operation records the tensors it consumed and a closure that knows how to
   push a gradient back through it.
2. `backward()` walks the graph in reverse topological order, so a tensor's gradient
   is complete before it is used to compute its parents'.
3. Gradients ACCUMULATE. Write `+=`, never `=`. A tensor used twice must receive both
   contributions; `=` silently halves the gradient on any diamond-shaped graph and
   there is a test for exactly that.

Two traps that will each cost you an afternoon:

  * The topological sort needs a VISITED SET. Recursing without one on a diamond
    graph is exponential, and worse, doubles gradients.
  * Broadcasting must be reversed. When (3,1) + (3,4) broadcasts, the gradient going
    back to the (3,1) operand has to be SUMMED over the broadcast axis. Get it wrong
    and shapes break two operations later, pointing nowhere near the cause.
"""
from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

__all__ = ["Tensor", "checkpoint", "no_grad"]

_GRAD_ENABLED = True


class no_grad:  # noqa: N801
    """TODO: context manager that stops the graph being built (used for evaluation)."""

    def __enter__(self) -> "no_grad":
        raise NotImplementedError("no_grad")

    def __exit__(self, *exc: object) -> None:
        raise NotImplementedError


def _unbroadcast(grad: NDArray[np.float64], shape: tuple[int, ...]) -> NDArray[np.float64]:
    """TODO: reverse NumPy broadcasting — sum `grad` down to `shape`.

    Two steps, both required:
      * sum away leading axes that broadcasting added
      * sum (keepdims=True) any axis where the original size was 1
    """
    raise NotImplementedError("_unbroadcast")


class Tensor:
    """Required surface (the tests use all of it):

    attributes:  data, grad, requires_grad, shape, ndim
    operators:   + - * / ** @ , and the reflected forms
    unary:       exp, log, tanh, relu, sigmoid
    reductions:  sum(axis, keepdims), mean(axis, keepdims)
    shape:       reshape, .T
    graph:       backward(gradient=None), zero_grad(), detach(), item()

    `backward()` on a non-scalar without an explicit gradient should raise.
    """

    def __init__(self, data: object, requires_grad: bool = False,
                 _parents: tuple["Tensor", ...] = (), _op: str = "") -> None:
        self.data: NDArray[np.float64] = np.asarray(data, dtype=np.float64)
        self.requires_grad = requires_grad and _GRAD_ENABLED
        self.grad: NDArray[np.float64] | None = None
        self._backward: Callable[[], None] = lambda: None
        self._parents = _parents
        self._op = _op

    def _accumulate(self, g: NDArray[np.float64]) -> None:
        """TODO: += , never = ."""
        raise NotImplementedError("Tensor._accumulate")

    def __add__(self, other: object) -> "Tensor":
        raise NotImplementedError("Tensor.__add__")

    def __mul__(self, other: object) -> "Tensor":
        raise NotImplementedError("Tensor.__mul__")

    def __matmul__(self, other: "Tensor") -> "Tensor":
        raise NotImplementedError("Tensor.__matmul__")

    def sum(self, axis: int | tuple[int, ...] | None = None,
            keepdims: bool = False) -> "Tensor":
        raise NotImplementedError("Tensor.sum")

    def relu(self) -> "Tensor":
        raise NotImplementedError("Tensor.relu")

    def backward(self, gradient: object = None) -> None:
        """TODO: reverse-mode differentiation from this tensor.

        Build the topological order with an explicit visited set, seed this tensor's
        gradient, then call each node's `_backward` in reverse order.
        """
        raise NotImplementedError("Tensor.backward")


def checkpoint(fn: Callable[..., Tensor], *inputs: Tensor) -> Tensor:
    """`hard` — trade compute for retained activations.

    Run `fn` under `no_grad` so none of its intermediates are kept. On the backward
    pass, recompute the block with grad enabled and differentiate it then. Costs one
    extra forward pass of `fn`; saves every activation inside it.

    Only worth it when the model is split into SEGMENTS. Checkpointing one monolithic
    block saves nothing, because the recompute materialises everything anyway.
    """
    raise NotImplementedError("checkpoint")
