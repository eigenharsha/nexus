"""Count-min sketch — `hard` track.

Counts frequencies in sublinear space, at the cost of never underestimating and
sometimes overestimating. The theory says:

    with width w = ceil(e / eps) and depth d = ceil(ln(1 / delta)),
    the estimate exceeds the true count by more than eps * N
    with probability at most delta.

The lab asks you to check that empirically rather than believe it, because the bound
is loose in practice and knowing *how* loose is the useful part.
"""
from __future__ import annotations

import math
from typing import Any


class CountMinSketch:
    def __init__(self, width: int | None = None, depth: int | None = None,
                 epsilon: float = 0.001, delta: float = 0.001, seed: int = 1) -> None:
        if width is None:
            width = math.ceil(math.e / epsilon)
        if depth is None:
            depth = math.ceil(math.log(1 / delta))
        if width < 1 or depth < 1:
            raise ValueError("width and depth must be positive")
        self.width = width
        self.depth = depth
        self.total = 0
        self._table = [[0] * width for _ in range(depth)]
        # One salt per row. Reusing the same hash for every row makes the depth
        # decorative: all rows collide together and the error never averages out.
        self._salts = [hash((seed, row, 0x9E3779B9)) for row in range(depth)]

    def _slots(self, item: Any) -> list[int]:
        h = hash(item)
        return [(h ^ salt) % self.width for salt in self._salts]

    def add(self, item: Any, count: int = 1) -> None:
        if count < 0:
            raise ValueError("count-min sketch cannot handle negative counts")
        self.total += count
        for row, slot in enumerate(self._slots(item)):
            self._table[row][slot] += count

    def estimate(self, item: Any) -> int:
        return min(self._table[row][slot] for row, slot in enumerate(self._slots(item)))

    @property
    def bytes_used(self) -> int:
        """A rough figure for the write-up: 8 bytes per counter."""
        return self.width * self.depth * 8

    def theoretical_error_bound(self) -> float:
        """eps * N, where eps = e / w."""
        return (math.e / self.width) * self.total
