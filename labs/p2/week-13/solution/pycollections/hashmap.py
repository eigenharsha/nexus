"""Two hash tables with the same interface and very different behaviour.

The point of implementing both is the benchmark, not the code. Chaining and open
addressing have identical Big-O and completely different constants, and which one
wins depends on the load factor and on your cache — which is exactly the thing
Big-O is defined to ignore.
"""
from __future__ import annotations

from collections.abc import Iterator, MutableMapping
from typing import Any, TypeVar

K = TypeVar("K")
V = TypeVar("V")

_MISSING = object()


class ChainedHashMap(MutableMapping[K, V]):
    """Separate chaining: each bucket holds a list of (key, value) pairs.

    Simple, tolerant of a high load factor, and two pointer dereferences per lookup
    (bucket array, then the list) — which is the reason it loses to open addressing
    at low load factor and wins at high.
    """

    def __init__(self, initial_capacity: int = 8, max_load_factor: float = 0.75) -> None:
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be positive")
        if not 0 < max_load_factor <= 4:
            raise ValueError("max_load_factor must be in (0, 4]")
        self._capacity = initial_capacity
        self._max_load = max_load_factor
        self._buckets: list[list[tuple[K, V]] | None] = [None] * self._capacity
        self._size = 0
        self.resizes = 0
        self.collisions = 0

    # -- internals --------------------------------------------------------
    def _index(self, key: K) -> int:
        return hash(key) & (self._capacity - 1) if self._is_pow2() else hash(key) % self._capacity

    def _is_pow2(self) -> bool:
        return self._capacity & (self._capacity - 1) == 0

    def _resize(self, new_capacity: int) -> None:
        old = self._buckets
        self._capacity = new_capacity
        self._buckets = [None] * new_capacity
        self._size = 0
        self.resizes += 1
        for bucket in old:
            if bucket:
                for k, v in bucket:
                    self[k] = v

    @property
    def load_factor(self) -> float:
        return self._size / self._capacity

    @property
    def capacity(self) -> int:
        return self._capacity

    # -- MutableMapping ---------------------------------------------------
    def __setitem__(self, key: K, value: V) -> None:
        i = self._index(key)
        bucket = self._buckets[i]
        if bucket is None:
            self._buckets[i] = [(key, value)]
        else:
            for pos, (k, _) in enumerate(bucket):
                if k == key:
                    bucket[pos] = (key, value)
                    return
            self.collisions += 1
            bucket.append((key, value))
        self._size += 1
        if self.load_factor > self._max_load:
            self._resize(self._capacity * 2)

    def __getitem__(self, key: K) -> V:
        bucket = self._buckets[self._index(key)]
        if bucket is not None:
            for k, v in bucket:
                if k == key:
                    return v
        raise KeyError(key)

    def __delitem__(self, key: K) -> None:
        i = self._index(key)
        bucket = self._buckets[i]
        if bucket is not None:
            for pos, (k, _) in enumerate(bucket):
                if k == key:
                    del bucket[pos]
                    if not bucket:
                        self._buckets[i] = None
                    self._size -= 1
                    return
        raise KeyError(key)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[K]:
        for bucket in self._buckets:
            if bucket:
                for k, _ in bucket:
                    yield k

    def __repr__(self) -> str:
        return f"{type(self).__name__}({dict(self)!r})"


class _Tombstone:
    """A deleted slot. Not empty — probing must continue past it, or a key that
    landed after a collision becomes unreachable the moment its predecessor is
    deleted. That bug is invisible until a delete-heavy workload finds it."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "<deleted>"


TOMBSTONE = _Tombstone()


class OpenAddressingHashMap(MutableMapping[K, V]):
    """Linear probing with tombstones.

    One flat array, so a lookup touches one cache line in the common case. That is
    the whole advantage, and it evaporates above a load factor of roughly 0.7 as
    probe sequences lengthen.

    Tombstones are counted separately from live entries. A table where half the slots
    are tombstones probes like a full table even though `len()` says it is empty, so
    the resize trigger must consider `size + tombstones`, not `size`.
    """

    def __init__(self, initial_capacity: int = 8, max_load_factor: float = 0.6) -> None:
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be positive")
        if not 0 < max_load_factor < 1:
            raise ValueError("open addressing needs a max_load_factor strictly below 1")
        self._capacity = 1 << max(3, (initial_capacity - 1).bit_length())
        self._max_load = max_load_factor
        self._keys: list[Any] = [_MISSING] * self._capacity
        self._values: list[Any] = [None] * self._capacity
        self._size = 0
        self._tombstones = 0
        self.resizes = 0
        self.probes = 0

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def load_factor(self) -> float:
        return (self._size + self._tombstones) / self._capacity

    def _probe(self, key: K) -> tuple[int, bool]:
        """Return (slot, found). If not found, slot is where the key would go."""
        mask = self._capacity - 1
        i = hash(key) & mask
        first_free = -1
        while True:
            self.probes += 1
            k = self._keys[i]
            if k is _MISSING:
                return (first_free if first_free >= 0 else i), False
            if k is TOMBSTONE:
                if first_free < 0:
                    first_free = i
            elif k == key:
                return i, True
            i = (i + 1) & mask

    def _resize(self, new_capacity: int) -> None:
        old_keys, old_values = self._keys, self._values
        self._capacity = new_capacity
        self._keys = [_MISSING] * new_capacity
        self._values = [None] * new_capacity
        self._size = 0
        self._tombstones = 0          # rehashing is also how tombstones get cleaned up
        self.resizes += 1
        for k, v in zip(old_keys, old_values, strict=True):
            if k is not _MISSING and k is not TOMBSTONE:
                self[k] = v

    def __setitem__(self, key: K, value: V) -> None:
        slot, found = self._probe(key)
        if found:
            self._values[slot] = value
            return
        if self._keys[slot] is TOMBSTONE:
            self._tombstones -= 1
        self._keys[slot] = key
        self._values[slot] = value
        self._size += 1
        if self.load_factor > self._max_load:
            # Grow on live entries, not on slots used: a table that is mostly
            # tombstones should be rehashed at the same size, not doubled forever.
            target = self._capacity * 2 if self._size / self._capacity > self._max_load / 2 \
                else self._capacity
            self._resize(target)

    def __getitem__(self, key: K) -> V:
        slot, found = self._probe(key)
        if not found:
            raise KeyError(key)
        return self._values[slot]  # type: ignore[no-any-return]

    def __delitem__(self, key: K) -> None:
        slot, found = self._probe(key)
        if not found:
            raise KeyError(key)
        self._keys[slot] = TOMBSTONE
        self._values[slot] = None
        self._size -= 1
        self._tombstones += 1

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[K]:
        for k in self._keys:
            if k is not _MISSING and k is not TOMBSTONE:
                yield k

    def __repr__(self) -> str:
        return f"{type(self).__name__}({dict(self)!r})"


class IntHashMap:
    """`hard` track — specialised for int keys and a known final size.

    What it gives up, and you must say so in the write-up:
      * int keys only
      * no deletion
      * the capacity is fixed at construction; exceeding it raises

    What it buys: no rehashing, no per-entry tuple, no generic `hash()` dispatch,
    and identity comparison on the fast path.
    """

    __slots__ = ("_keys", "_values", "_mask", "_size", "_capacity")

    def __init__(self, expected_size: int) -> None:
        if expected_size < 1:
            raise ValueError("expected_size must be positive")
        capacity = 1 << max(3, (int(expected_size / 0.5) - 1).bit_length())
        self._capacity = capacity
        self._mask = capacity - 1
        self._keys: list[int] = [-1] * capacity   # -1 is the empty sentinel
        self._values: list[Any] = [None] * capacity
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def put(self, key: int, value: Any) -> None:
        if key < 0:
            raise ValueError("IntHashMap holds non-negative int keys only")
        keys = self._keys
        i = key & self._mask
        while True:
            k = keys[i]
            if k == -1:
                if self._size + 1 > self._capacity * 0.7:
                    raise RuntimeError("IntHashMap is full; construct it with a larger size")
                keys[i] = key
                self._values[i] = value
                self._size += 1
                return
            if k == key:
                self._values[i] = value
                return
            i = (i + 1) & self._mask

    def get(self, key: int, default: Any = None) -> Any:
        keys = self._keys
        i = key & self._mask
        while True:
            k = keys[i]
            if k == -1:
                return default
            if k == key:
                return self._values[i]
            i = (i + 1) & self._mask

    def __contains__(self, key: int) -> bool:
        return self.get(key, _MISSING) is not _MISSING

    def __getitem__(self, key: int) -> Any:
        v = self.get(key, _MISSING)
        if v is _MISSING:
            raise KeyError(key)
        return v

    def __setitem__(self, key: int, value: Any) -> None:
        self.put(key, value)
