"""`standard` track. Every one of these is small; the value is in the benchmark
you run afterwards, not in the line count."""
from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class DynamicArray(Generic[T]):
    """Amortised O(1) append.

    Expose `capacity` and `copies` (total elements copied by all resizes) — the tests
    use `copies` to check the amortisation and the benchmark uses it to compare
    growth factors. Growth of 2.0 can never reuse the memory it just freed; 1.5 can.
    """

    def __init__(self, capacity: int = 8, growth: float = 2.0) -> None:
        raise NotImplementedError("DynamicArray")

    def append(self, value: T) -> None:
        raise NotImplementedError

    def pop(self) -> T:
        raise NotImplementedError

    def __getitem__(self, i: int) -> T:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


class DoublyLinkedList(Generic[T]):
    """O(1) at both ends. A sentinel head/tail pair removes every None check from
    the hot path — write it that way and compare.

    Needs: append_left, append_right, pop_left, pop_right, unlink(node), __len__,
    __iter__. `unlink` has to be public because the LRU cache needs it.
    """

    def __init__(self) -> None:
        raise NotImplementedError("DoublyLinkedList")


class LRUCache(Generic[K, V]):
    """dict for O(1) lookup + doubly-linked list for O(1) recency.

    Needs: get, put, __contains__, __len__, keys_in_lru_order() (least recent first),
    and `hits` / `misses` counters.
    """

    def __init__(self, capacity: int) -> None:
        raise NotImplementedError("LRUCache")


class MinHeap(Generic[T]):
    """Binary min-heap in an array.

    `MinHeap(items)` must heapify in O(n) — sift down from n//2 to 0 — not push
    n times. The benchmark measures the difference; if your ratio is 1.0 you
    implemented push-n-times.

    Needs: push, pop, peek, heapify, __len__, is_valid().
    """

    def __init__(self, items: list[T] | None = None) -> None:
        raise NotImplementedError("MinHeap")
