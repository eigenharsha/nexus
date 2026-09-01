"""Reverse-mode automatic differentiation over NumPy arrays.

Reference implementation for LAB-P3-W21.

The whole engine is three ideas:

1. Every operation records the tensors it consumed and a closure that knows how to
   push a gradient back through it.
2. `backward()` walks the graph in reverse topological order, so a tensor's gradient
   is complete before it is used to compute its parents'.
3. Gradients ACCUMULATE (`+=`). A tensor used twice gets both contributions. Writing
   `=` instead of `+=` is the single most common bug in a hand-written autograd, it
   silently halves gradients on any diamond-shaped graph, and there is a test for it.

Broadcasting is the part people underestimate. When `(3,1) + (3,4)` broadcasts, the
gradient flowing back to the `(3,1)` operand must be SUMMED over the broadcast axis,
or shapes stop matching two operations later and the error message points nowhere near
the cause.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable

import numpy as np
from numpy.typing import NDArray

__all__ = ["Tensor", "checkpoint", "no_grad"]

_GRAD_ENABLED = True


class no_grad:  # noqa: N801 - deliberately mirrors torch.no_grad
    """Context manager that stops the graph being built. Used for evaluation."""

    def __enter__(self) -> "no_grad":
        global _GRAD_ENABLED
        self._previous = _GRAD_ENABLED
        _GRAD_ENABLED = False
        return self

    def __exit__(self, *exc: object) -> None:
        global _GRAD_ENABLED
        _GRAD_ENABLED = self._previous


def _unbroadcast(grad: NDArray[np.float64], shape: tuple[int, ...]) -> NDArray[np.float64]:
    """Reverse NumPy broadcasting: sum `grad` down to `shape`.

    Two steps, and both are needed:
      * sum away leading axes that broadcasting added
      * sum (keeping the axis) any axis where the original size was 1
    """
    while grad.ndim > len(shape):
        grad = grad.sum(axis=0)
    for axis, size in enumerate(shape):
        if size == 1 and grad.shape[axis] != 1:
            grad = grad.sum(axis=axis, keepdims=True)
    return grad.reshape(shape)


class Tensor:
    __slots__ = ("data", "grad", "requires_grad", "_backward", "_parents", "_op")

    def __init__(
        self,
        data: object,
        requires_grad: bool = False,
        _parents: tuple["Tensor", ...] = (),
        _op: str = "",
    ) -> None:
        self.data: NDArray[np.float64] = np.asarray(data, dtype=np.float64)
        self.requires_grad = requires_grad and _GRAD_ENABLED
        self.grad: NDArray[np.float64] | None = None
        self._backward: Callable[[], None] = lambda: None
        self._parents = _parents
        self._op = _op

    # -- construction -----------------------------------------------------
    @property
    def shape(self) -> tuple[int, ...]:
        return self.data.shape

    @property
    def ndim(self) -> int:
        return self.data.ndim

    def __repr__(self) -> str:
        return f"Tensor(shape={self.shape}, op={self._op or 'leaf'}, requires_grad={self.requires_grad})"

    def _child(self, data: object, parents: tuple["Tensor", ...], op: str) -> "Tensor":
        needs = _GRAD_ENABLED and any(p.requires_grad for p in parents)
        return Tensor(data, requires_grad=needs, _parents=parents if needs else (), _op=op)

    def _accumulate(self, g: NDArray[np.float64]) -> None:
        # += , never = . A tensor consumed by two operations receives two gradients
        # and must end up with their sum.
        if self.grad is None:
            self.grad = g.astype(np.float64).copy()
        else:
            self.grad += g

    # -- elementwise ------------------------------------------------------
    def __add__(self, other: object) -> "Tensor":
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = self._child(self.data + other.data, (self, other), "+")

        def _backward() -> None:
            assert out.grad is not None
            if self.requires_grad:
                self._accumulate(_unbroadcast(out.grad, self.shape))
            if other.requires_grad:
                other._accumulate(_unbroadcast(out.grad, other.shape))

        out._backward = _backward
        return out

    def __mul__(self, other: object) -> "Tensor":
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = self._child(self.data * other.data, (self, other), "*")

        def _backward() -> None:
            assert out.grad is not None
            if self.requires_grad:
                self._accumulate(_unbroadcast(out.grad * other.data, self.shape))
            if other.requires_grad:
                other._accumulate(_unbroadcast(out.grad * self.data, other.shape))

        out._backward = _backward
        return out

    def __pow__(self, exponent: float) -> "Tensor":
        if not isinstance(exponent, int | float):
            raise TypeError("only int/float exponents are supported")
        out = self._child(self.data ** exponent, (self,), f"**{exponent}")

        def _backward() -> None:
            assert out.grad is not None
            if self.requires_grad:
                self._accumulate(out.grad * exponent * self.data ** (exponent - 1))

        out._backward = _backward
        return out

    def __neg__(self) -> "Tensor":
        return self * -1.0

    def __sub__(self, other: object) -> "Tensor":
        other = other if isinstance(other, Tensor) else Tensor(other)
        return self + (-other)

    def __truediv__(self, other: object) -> "Tensor":
        other = other if isinstance(other, Tensor) else Tensor(other)
        return self * other ** -1.0

    def __radd__(self, other: object) -> "Tensor":
        return self + other

    def __rmul__(self, other: object) -> "Tensor":
        return self * other

    def __rsub__(self, other: object) -> "Tensor":
        return (-self) + other

    def __rtruediv__(self, other: object) -> "Tensor":
        return (self ** -1.0) * other

    # -- unary ------------------------------------------------------------
    def exp(self) -> "Tensor":
        value = np.exp(self.data)
        out = self._child(value, (self,), "exp")

        def _backward() -> None:
            assert out.grad is not None
            if self.requires_grad:
                self._accumulate(out.grad * value)

        out._backward = _backward
        return out

    def log(self) -> "Tensor":
        out = self._child(np.log(self.data), (self,), "log")

        def _backward() -> None:
            assert out.grad is not None
            if self.requires_grad:
                self._accumulate(out.grad / self.data)

        out._backward = _backward
        return out

    def tanh(self) -> "Tensor":
        value = np.tanh(self.data)
        out = self._child(value, (self,), "tanh")

        def _backward() -> None:
            assert out.grad is not None
            if self.requires_grad:
                self._accumulate(out.grad * (1.0 - value ** 2))

        out._backward = _backward
        return out

    def relu(self) -> "Tensor":
        mask = self.data > 0
        out = self._child(np.where(mask, self.data, 0.0), (self,), "relu")

        def _backward() -> None:
            assert out.grad is not None
            if self.requires_grad:
                # The subgradient at exactly 0 is a choice. 0 is the conventional one
                # and it is what PyTorch does.
                self._accumulate(out.grad * mask)

        out._backward = _backward
        return out

    def sigmoid(self) -> "Tensor":
        value = np.where(
            self.data >= 0,
            1.0 / (1.0 + np.exp(-np.abs(self.data))),
            np.exp(-np.abs(self.data)) / (1.0 + np.exp(-np.abs(self.data))),
        )
        out = self._child(value, (self,), "sigmoid")

        def _backward() -> None:
            assert out.grad is not None
            if self.requires_grad:
                self._accumulate(out.grad * value * (1.0 - value))

        out._backward = _backward
        return out

    # -- shape / reduction ------------------------------------------------
    def __matmul__(self, other: "Tensor") -> "Tensor":
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = self._child(self.data @ other.data, (self, other), "@")

        def _backward() -> None:
            assert out.grad is not None
            if self.requires_grad:
                self._accumulate(out.grad @ other.data.T)
            if other.requires_grad:
                other._accumulate(self.data.T @ out.grad)

        out._backward = _backward
        return out

    def sum(self, axis: int | tuple[int, ...] | None = None, keepdims: bool = False) -> "Tensor":
        out = self._child(self.data.sum(axis=axis, keepdims=keepdims), (self,), "sum")

        def _backward() -> None:
            assert out.grad is not None
            if self.requires_grad:
                g = out.grad
                if axis is not None and not keepdims:
                    g = np.expand_dims(g, axis)
                self._accumulate(np.broadcast_to(g, self.shape).copy())

        out._backward = _backward
        return out

    def mean(self, axis: int | tuple[int, ...] | None = None, keepdims: bool = False) -> "Tensor":
        count = self.data.size if axis is None else self.data.shape[axis]  # type: ignore[index]
        return self.sum(axis=axis, keepdims=keepdims) * (1.0 / count)

    def reshape(self, *shape: int) -> "Tensor":
        original = self.shape
        out = self._child(self.data.reshape(shape), (self,), "reshape")

        def _backward() -> None:
            assert out.grad is not None
            if self.requires_grad:
                self._accumulate(out.grad.reshape(original))

        out._backward = _backward
        return out

    @property
    def T(self) -> "Tensor":  # noqa: N802
        out = self._child(self.data.T, (self,), "T")

        def _backward() -> None:
            assert out.grad is not None
            if self.requires_grad:
                self._accumulate(out.grad.T)

        out._backward = _backward
        return out

    # -- the reverse pass -------------------------------------------------
    def backward(self, gradient: object = None) -> None:
        """Reverse-mode differentiation from this tensor.

        Topological order with an explicit visited set. Recursing without one on a
        diamond-shaped graph visits shared nodes more than once, which is both
        exponential in the worst case and — worse — produces doubled gradients.
        """
        topo: list[Tensor] = []
        visited: set[int] = set()
        stack: list[tuple[Tensor, bool]] = [(self, False)]
        while stack:
            node, expanded = stack.pop()
            if expanded:
                topo.append(node)
                continue
            if id(node) in visited:
                continue
            visited.add(id(node))
            stack.append((node, True))
            for parent in node._parents:
                if id(parent) not in visited:
                    stack.append((parent, False))

        if gradient is None:
            if self.data.size != 1:
                raise RuntimeError(
                    "backward() on a non-scalar needs an explicit gradient argument"
                )
            gradient = np.ones_like(self.data)
        self.grad = np.asarray(gradient, dtype=np.float64).reshape(self.shape).copy()

        for node in reversed(topo):
            node._backward()

    def zero_grad(self) -> None:
        self.grad = None

    def detach(self) -> "Tensor":
        return Tensor(self.data.copy(), requires_grad=False)

    def item(self) -> float:
        return float(self.data.reshape(()))


def checkpoint(fn: Callable[..., Tensor], *inputs: Tensor) -> Tensor:
    """`hard` track — trade compute for memory.

    Run `fn` without building a graph, so none of its intermediates are retained.
    On the backward pass, recompute the block with grad enabled and differentiate it
    then. Costs one extra forward pass of `fn`; saves every activation inside it.
    """
    with no_grad():
        value = fn(*inputs)

    out = Tensor(value.data, requires_grad=any(i.requires_grad for i in inputs),
                 _parents=tuple(i for i in inputs if i.requires_grad), _op="checkpoint")

    def _backward() -> None:
        assert out.grad is not None
        clones = [Tensor(i.data, requires_grad=i.requires_grad) for i in inputs]
        recomputed = fn(*clones)
        recomputed.backward(out.grad)
        for original, clone in zip(inputs, clones, strict=True):
            if original.requires_grad and clone.grad is not None:
                original._accumulate(clone.grad)

    out._backward = _backward
    return out


def stack_parameters(tensors: Iterable[Tensor]) -> list[Tensor]:
    return [t for t in tensors if t.requires_grad]
