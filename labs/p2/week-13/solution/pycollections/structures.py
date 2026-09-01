"""The rest of the structures. Small enough to read in one sitting, which is the point."""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Generic, TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class DynamicArray(Generic[T]):
    """Amortised O(1) append.

    The growth factor is the interesting knob. 2.0 is what everyone writes; CPython's
    list uses roughly 1.125 (`new = old + old >> 3 + 6`). Larger factors mean fewer
    copies and more peak memory, and — the part people miss — a factor of 2 can never
    reuse the memory it just freed, because the sum of all previous blocks is always
    smaller than the next one. Factors below the golden ratio (~1.618) can.
    """

    def __init__(self, capacity: int = 8, growth: float = 2.0) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        if growth <= 1.0:
            raise ValueError("growth factor must exceed 1.0")
        self._growth = growth
        self._store: list[Any] = [None] * capacity
        self._size = 0
        self.copies = 0          # total elements copied by all resizes; the amortised cost

    @property
    def capacity(self) -> int:
        return len(self._store)

    def append(self, value: T) -> None:
        if self._size == len(self._store):
            new_cap = max(len(self._store) + 1, int(len(self._store) * self._growth))
            new_store: list[Any] = [None] * new_cap
            for i in range(self._size):
                new_store[i] = self._store[i]
            self.copies += self._size
            self._store = new_store
        self._store[self._size] = value
        self._size += 1

    def pop(self) -> T:
        if self._size == 0:
            raise IndexError("pop from an empty DynamicArray")
        self._size -= 1
        value = self._store[self._size]
        self._store[self._size] = None
        return value  # type: ignore[no-any-return]

    def __getitem__(self, i: int) -> T:
        if i < 0:
            i += self._size
        if not 0 <= i < self._size:
            raise IndexError(i)
        return self._store[i]  # type: ignore[no-any-return]

    def __setitem__(self, i: int, value: T) -> None:
        if i < 0:
            i += self._size
        if not 0 <= i < self._size:
            raise IndexError(i)
        self._store[i] = value

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        for i in range(self._size):
            yield self._store[i]


class _Node(Generic[T]):
    __slots__ = ("value", "prev", "next")

    def __init__(self, value: T) -> None:
        self.value = value
        self.prev: _Node[T] | None = None
        self.next: _Node[T] | None = None


class DoublyLinkedList(Generic[T]):
    """O(1) at both ends. A sentinel head/tail pair removes every None check from
    the hot path, which is why the code has no `if self._head is None` in it."""

    def __init__(self) -> None:
        self._head: _Node[T] = _Node(None)  # type: ignore[arg-type]
        self._tail: _Node[T] = _Node(None)  # type: ignore[arg-type]
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0

    def append_right(self, value: T) -> _Node[T]:
        node = _Node(value)
        prev = self._tail.prev
        assert prev is not None
        prev.next = node
        node.prev = prev
        node.next = self._tail
        self._tail.prev = node
        self._size += 1
        return node

    def append_left(self, value: T) -> _Node[T]:
        node = _Node(value)
        nxt = self._head.next
        assert nxt is not None
        self._head.next = node
        node.prev = self._head
        node.next = nxt
        nxt.prev = node
        self._size += 1
        return node

    def unlink(self, node: _Node[T]) -> T:
        assert node.prev is not None and node.next is not None
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None
        self._size -= 1
        return node.value

    def pop_right(self) -> T:
        if self._size == 0:
            raise IndexError("pop from an empty list")
        node = self._tail.prev
        assert node is not None
        return self.unlink(node)

    def pop_left(self) -> T:
        if self._size == 0:
            raise IndexError("pop from an empty list")
        node = self._head.next
        assert node is not None
        return self.unlink(node)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        node = self._head.next
        while node is not None and node is not self._tail:
            yield node.value
            node = node.next


class LRUCache(Generic[K, V]):
    """dict for O(1) lookup, doubly-linked list for O(1) recency. Neither structure
    can do this alone, which is why this is the canonical interview question."""

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._map: dict[K, _Node[tuple[K, V]]] = {}
        self._order: DoublyLinkedList[tuple[K, V]] = DoublyLinkedList()
        self.hits = 0
        self.misses = 0

    def get(self, key: K, default: V | None = None) -> V | None:
        node = self._map.get(key)
        if node is None:
            self.misses += 1
            return default
        self.hits += 1
        k, v = self._order.unlink(node)
        self._map[key] = self._order.append_right((k, v))
        return v

    def put(self, key: K, value: V) -> None:
        node = self._map.get(key)
        if node is not None:
            self._order.unlink(node)
        elif len(self._map) >= self.capacity:
            evicted_key, _ = self._order.pop_left()
            del self._map[evicted_key]
        self._map[key] = self._order.append_right((key, value))

    def __contains__(self, key: object) -> bool:
        return key in self._map

    def __len__(self) -> int:
        return len(self._map)

    def keys_in_lru_order(self) -> list[K]:
        """Least recently used first."""
        return [k for k, _ in self._order]


class MinHeap(Generic[T]):
    """Binary min-heap in an array.

    `heapify` is O(n), not O(n log n): sifting down from n/2 to 0, most nodes are
    near the bottom and move at most one or two levels. The sum telescopes to 2n.
    Pushing n items one at a time really is O(n log n) — the benchmark shows the gap.
    """

    def __init__(self, items: list[T] | None = None) -> None:
        self._data: list[T] = list(items or [])
        if self._data:
            self.heapify()

    def heapify(self) -> None:
        for i in range(len(self._data) // 2 - 1, -1, -1):
            self._sift_down(i)

    def _sift_up(self, i: int) -> None:
        data = self._data
        while i > 0:
            parent = (i - 1) // 2
            if data[i] < data[parent]:
                data[i], data[parent] = data[parent], data[i]
                i = parent
            else:
                return

    def _sift_down(self, i: int) -> None:
        data = self._data
        n = len(data)
        while True:
            left, right, smallest = 2 * i + 1, 2 * i + 2, i
            if left < n and data[left] < data[smallest]:
                smallest = left
            if right < n and data[right] < data[smallest]:
                smallest = right
            if smallest == i:
                return
            data[i], data[smallest] = data[smallest], data[i]
            i = smallest

    def push(self, item: T) -> None:
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> T:
        if not self._data:
            raise IndexError("pop from an empty heap")
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return top

    def peek(self) -> T:
        if not self._data:
            raise IndexError("peek at an empty heap")
        return self._data[0]

    def __len__(self) -> int:
        return len(self._data)

    def is_valid(self) -> bool:
        """The heap property, checked directly. Used by the tests."""
        n = len(self._data)
        return all(
            not (child < n and self._data[child] < self._data[i])
            for i in range(n)
            for child in (2 * i + 1, 2 * i + 2)
        )
