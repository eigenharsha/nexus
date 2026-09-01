"""Two hash tables with the same interface and very different constants.

basic:    ChainedHashMap — fill in the four TODOs.
standard: OpenAddressingHashMap — write it from the spec.
hard:     IntHashMap.
"""
from __future__ import annotations

from collections.abc import Iterator, MutableMapping
from typing import Any, TypeVar

K = TypeVar("K")
V = TypeVar("V")

_MISSING = object()


class ChainedHashMap(MutableMapping[K, V]):
    """Separate chaining: each bucket holds a list of (key, value) pairs."""

    def __init__(self, initial_capacity: int = 8, max_load_factor: float = 0.75) -> None:
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be positive")
        self._capacity = initial_capacity
        self._max_load = max_load_factor
        self._buckets: list[list[tuple[K, V]] | None] = [None] * self._capacity
        self._size = 0
        self.resizes = 0        # the tests read this
        self.collisions = 0

    def _index(self, key: K) -> int:
        return hash(key) % self._capacity

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def load_factor(self) -> float:
        return self._size / self._capacity

    def _resize(self, new_capacity: int) -> None:
        # TODO 1: allocate a new bucket array and re-insert every live pair.
        # Increment self.resizes. Re-inserting through __setitem__ is fine and is
        # the readable version; just make sure you reset _size first or you will
        # double-count.
        raise NotImplementedError("ChainedHashMap._resize")

    def __setitem__(self, key: K, value: V) -> None:
        # TODO 2: find the bucket. If the key is already there, replace its value
        # and DO NOT change the size. Otherwise append, bump the size, and resize
        # when load_factor exceeds _max_load.
        raise NotImplementedError("ChainedHashMap.__setitem__")

    def __getitem__(self, key: K) -> V:
        # TODO 3: scan the bucket. Raise KeyError(key) if absent.
        raise NotImplementedError("ChainedHashMap.__getitem__")

    def __delitem__(self, key: K) -> None:
        # TODO 4: remove the pair from its bucket. Raise KeyError(key) if absent.
        raise NotImplementedError("ChainedHashMap.__delitem__")

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[K]:
        for bucket in self._buckets:
            if bucket:
                for k, _ in bucket:
                    yield k


class OpenAddressingHashMap(MutableMapping[K, V]):
    """`standard` — linear probing with tombstones.

    Read this before you start: a deleted slot must be marked as a TOMBSTONE, not as
    empty. If it is marked empty, a key that landed after a collision becomes
    unreachable the moment its predecessor is deleted. There is a test for exactly
    that, and a test for what happens when tombstones are never cleaned up.

    Expose `capacity`, `load_factor`, `resizes` and `probes` — the benchmark and the
    tests read all four.
    """

    def __init__(self, initial_capacity: int = 8, max_load_factor: float = 0.6) -> None:
        raise NotImplementedError("OpenAddressingHashMap")

    def __setitem__(self, key: K, value: V) -> None:
        raise NotImplementedError

    def __getitem__(self, key: K) -> V:
        raise NotImplementedError

    def __delitem__(self, key: K) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __iter__(self) -> Iterator[K]:
        raise NotImplementedError


class IntHashMap:
    """`hard` — specialised for non-negative int keys and a known final size.

    Give up: arbitrary keys, deletion, and growth. Get back: no rehashing, no tuple
    per entry, no generic hash dispatch. Say what you gave up in the write-up — a
    specialised structure that does not name its trade is just an undocumented bug.

    Needs: put/get/__len__/__contains__/__getitem__/__setitem__, and a RuntimeError
    when it is asked to exceed the capacity it was built with.
    """

    def __init__(self, expected_size: int) -> None:
        raise NotImplementedError("IntHashMap")

    def put(self, key: int, value: Any) -> None:
        raise NotImplementedError

    def get(self, key: int, default: Any = None) -> Any:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
