"""`hard` — count-min sketch.

Counts frequencies in sublinear space. Never underestimates; sometimes overestimates.

    width w = ceil(e / eps), depth d = ceil(ln(1 / delta))
    P[estimate - true > eps * N] <= delta

The lab asks you to measure that rather than believe it. Note the bound is
*probabilistic*: some estimates are allowed to exceed it, at a rate of at most delta.

One trap: use a different hash per row. If every row uses the same hash, all d rows
collide identically, the depth does nothing, and your error will be d times worse
than the theory says for reasons that take an afternoon to find.
"""
from __future__ import annotations

from typing import Any


class CountMinSketch:
    def __init__(self, width: int | None = None, depth: int | None = None,
                 epsilon: float = 0.001, delta: float = 0.001, seed: int = 1) -> None:
        raise NotImplementedError("CountMinSketch")

    def add(self, item: Any, count: int = 1) -> None:
        raise NotImplementedError

    def estimate(self, item: Any) -> int:
        raise NotImplementedError

    @property
    def bytes_used(self) -> int:
        raise NotImplementedError

    def theoretical_error_bound(self) -> float:
        """eps * N, where eps = e / width."""
        raise NotImplementedError
