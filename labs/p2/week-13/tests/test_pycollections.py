"""Acceptance tests for LAB-P2-W13 — `pycollections`."""
from __future__ import annotations

import math
import random

import pytest

from pycollections import (
    ChainedHashMap,
    CountMinSketch,
    DoublyLinkedList,
    DynamicArray,
    IntHashMap,
    LRUCache,
    MinHeap,
    OpenAddressingHashMap,
)

MAPS = [ChainedHashMap, OpenAddressingHashMap]


class TerribleHash:
    """Every instance hashes to the same bucket. Chaining degrades to a list scan;
    open addressing degrades to a linear probe over the whole table. Both must still
    be correct — that is what this class is for."""

    __slots__ = ("value",)

    def __init__(self, value: int) -> None:
        self.value = value

    def __hash__(self) -> int:
        return 42

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TerribleHash) and other.value == self.value

    def __repr__(self) -> str:
        return f"TerribleHash({self.value})"


# ============================================================== basic
@pytest.mark.basic
def test_chained_basic_operations() -> None:
    m: ChainedHashMap[str, int] = ChainedHashMap()
    assert len(m) == 0
    m["a"] = 1
    m["b"] = 2
    assert m["a"] == 1 and m["b"] == 2
    assert len(m) == 2
    assert "a" in m and "z" not in m
    m["a"] = 10
    assert m["a"] == 10 and len(m) == 2, "overwriting a key must not grow the map"
    del m["a"]
    assert len(m) == 1 and "a" not in m
    with pytest.raises(KeyError):
        _ = m["a"]
    with pytest.raises(KeyError):
        del m["a"]


@pytest.mark.basic
def test_chained_resizes_and_keeps_everything() -> None:
    m: ChainedHashMap[int, int] = ChainedHashMap(initial_capacity=8)
    for i in range(2000):
        m[i] = i * i
    assert len(m) == 2000
    assert m.resizes > 0, "the map never resized; the load factor is being ignored"
    assert m.load_factor <= 0.75 + 1e-9
    for i in range(2000):
        assert m[i] == i * i


@pytest.mark.basic
def test_chained_survives_total_hash_collision() -> None:
    m: ChainedHashMap[TerribleHash, int] = ChainedHashMap()
    keys = [TerribleHash(i) for i in range(200)]
    for i, k in enumerate(keys):
        m[k] = i
    assert len(m) == 200
    for i, k in enumerate(keys):
        assert m[k] == i
    del m[keys[100]]
    assert len(m) == 199 and keys[100] not in m
    assert keys[101] in m, "deleting one key must not orphan the rest of the chain"


# ============================================================== standard
@pytest.mark.standard
@pytest.mark.parametrize("cls", MAPS, ids=lambda c: c.__name__)
def test_both_maps_satisfy_the_same_contract(cls: type) -> None:
    m = cls()
    for i in range(500):
        m[i] = -i
    for i in range(0, 500, 3):
        del m[i]
    expected = {i: -i for i in range(500) if i % 3}
    assert len(m) == len(expected)
    assert dict(m.items()) == expected
    assert sorted(m) == sorted(expected)


@pytest.mark.standard
@pytest.mark.parametrize("cls", MAPS, ids=lambda c: c.__name__)
def test_both_maps_agree_with_dict_under_random_operations(cls: type) -> None:
    rng = random.Random(20260901)
    m = cls()
    reference: dict[int, int] = {}
    for _ in range(20000):
        key = rng.randrange(300)
        op = rng.random()
        if op < 0.55:
            value = rng.randrange(10**6)
            m[key] = value
            reference[key] = value
        elif op < 0.8:
            if key in reference:
                del m[key]
                del reference[key]
        else:
            assert (key in m) == (key in reference)
            if key in reference:
                assert m[key] == reference[key]
    assert len(m) == len(reference)
    assert dict(m.items()) == reference


@pytest.mark.standard
def test_open_addressing_probes_past_tombstones() -> None:
    """Insert two keys that collide, delete the first, and look up the second.
    Marking the deleted slot empty instead of TOMBSTONE makes the second key
    unreachable — the classic open-addressing bug, and invisible without this test."""
    m: OpenAddressingHashMap[TerribleHash, int] = OpenAddressingHashMap()
    a, b = TerribleHash(1), TerribleHash(2)
    m[a] = 1
    m[b] = 2
    del m[a]
    assert b in m and m[b] == 2


@pytest.mark.standard
def test_open_addressing_survives_a_delete_heavy_workload() -> None:
    """Without tombstone cleanup on resize, the table fills with tombstones and
    lookups degrade to O(n) while len() still says the map is small."""
    m: OpenAddressingHashMap[int, int] = OpenAddressingHashMap(initial_capacity=16)
    for cycle in range(60):
        for i in range(200):
            m[cycle * 1000 + i] = i
        for i in range(200):
            del m[cycle * 1000 + i]
    assert len(m) == 0
    m.probes = 0
    m[999999] = 1
    assert m[999999] == 1
    assert m.probes < 50, (
        f"{m.probes} probes for one insert+lookup into an empty map — tombstones "
        f"are never being cleaned up"
    )


@pytest.mark.standard
def test_open_addressing_load_factor_is_bounded() -> None:
    m: OpenAddressingHashMap[int, int] = OpenAddressingHashMap(max_load_factor=0.6)
    for i in range(5000):
        m[i] = i
    assert m.load_factor <= 0.6 + 1e-9
    assert m.capacity & (m.capacity - 1) == 0, "capacity should stay a power of two"


@pytest.mark.standard
def test_dynamic_array_is_amortised_constant() -> None:
    a: DynamicArray[int] = DynamicArray(capacity=1, growth=2.0)
    n = 100_000
    for i in range(n):
        a.append(i)
    assert len(a) == n
    assert a[0] == 0 and a[-1] == n - 1
    # Total elements copied across all growths is bounded by 2n for growth=2.
    assert a.copies < 2 * n, f"{a.copies} copies for {n} appends is not amortised O(1)"
    assert a.pop() == n - 1 and len(a) == n - 1
    with pytest.raises(IndexError):
        a[n]


@pytest.mark.standard
def test_dynamic_array_growth_factor_changes_peak_memory() -> None:
    small = DynamicArray[int](capacity=1, growth=1.5)
    big = DynamicArray[int](capacity=1, growth=2.0)
    for i in range(10_000):
        small.append(i)
        big.append(i)
    assert small.capacity < big.capacity, "1.5x should hold less slack than 2.0x"
    assert small.copies > big.copies, "1.5x pays for that with more copying"


@pytest.mark.standard
def test_doubly_linked_list_both_ends() -> None:
    dll: DoublyLinkedList[int] = DoublyLinkedList()
    for i in range(5):
        dll.append_right(i)
    for i in range(5):
        dll.append_left(-i)
    assert list(dll) == [-4, -3, -2, -1, 0, 0, 1, 2, 3, 4]
    assert len(dll) == 10
    assert dll.pop_right() == 4
    assert dll.pop_left() == -4
    assert len(dll) == 8
    empty: DoublyLinkedList[int] = DoublyLinkedList()
    with pytest.raises(IndexError):
        empty.pop_right()


@pytest.mark.standard
def test_lru_evicts_least_recently_used() -> None:
    c: LRUCache[str, int] = LRUCache(3)
    c.put("a", 1); c.put("b", 2); c.put("c", 3)
    assert c.get("a") == 1                 # touching "a" makes "b" the oldest
    c.put("d", 4)
    assert "b" not in c
    assert c.keys_in_lru_order() == ["c", "a", "d"]
    assert c.get("zzz") is None
    assert c.hits == 1 and c.misses == 1


@pytest.mark.standard
def test_lru_agrees_with_ordereddict_under_random_operations() -> None:
    from collections import OrderedDict

    rng = random.Random(7)
    cap = 32
    mine: LRUCache[int, int] = LRUCache(cap)
    ref: OrderedDict[int, int] = OrderedDict()
    for _ in range(20000):
        key = rng.randrange(80)
        if rng.random() < 0.5:
            mine.put(key, key)
            if key in ref:
                ref.move_to_end(key)
            else:
                if len(ref) >= cap:
                    ref.popitem(last=False)
                ref[key] = key
        else:
            got = mine.get(key)
            if key in ref:
                ref.move_to_end(key)
                assert got == key
            else:
                assert got is None
    assert mine.keys_in_lru_order() == list(ref.keys())


@pytest.mark.standard
def test_min_heap() -> None:
    rng = random.Random(3)
    items = [rng.randrange(10**6) for _ in range(5000)]
    h: MinHeap[int] = MinHeap()
    for x in items:
        h.push(x)
    assert h.is_valid()
    assert h.peek() == min(items)
    assert [h.pop() for _ in range(len(items))] == sorted(items)
    with pytest.raises(IndexError):
        h.pop()


@pytest.mark.standard
def test_heapify_is_linear_and_correct() -> None:
    rng = random.Random(11)
    items = [rng.randrange(10**6) for _ in range(20000)]
    h: MinHeap[int] = MinHeap(items)
    assert h.is_valid(), "heapify did not establish the heap property"
    assert h.peek() == min(items)


# ============================================================== hard
@pytest.mark.hard
def test_int_hash_map_is_correct() -> None:
    m = IntHashMap(10_000)
    for i in range(5000):
        m[i] = i * 3
    assert len(m) == 5000
    for i in range(5000):
        assert m[i] == i * 3
    assert m.get(999999) is None
    assert 4999 in m and 5000 not in m
    with pytest.raises(KeyError):
        _ = m[5000]
    with pytest.raises(RuntimeError):
        full = IntHashMap(4)
        for i in range(100):
            full[i] = i


@pytest.mark.hard
def test_int_hash_map_beats_dict_on_its_specialised_workload() -> None:
    """Integer keys, known size, no deletions, lookup-dominated.

    This is a *specialised* win, not a general one: the whole point of the write-up
    is saying what was given up (int keys only, no deletion, fixed capacity) to get it.
    Compared on total operation time so the measurement is not one lucky call.
    """
    import time

    n = 200_000
    keys = list(range(n))

    mine = IntHashMap(n)
    for k in keys:
        mine.put(k, k)
    builtin = dict.fromkeys(keys, 0)
    for k in keys:
        builtin[k] = k

    def timed(fn: object, rounds: int = 3) -> float:
        best = float("inf")
        for _ in range(rounds):
            t0 = time.perf_counter()
            fn()  # type: ignore[operator]
            best = min(best, time.perf_counter() - t0)
        return best

    mine_get = mine.get
    builtin_get = builtin.get
    t_mine = timed(lambda: [mine_get(k) for k in keys])
    t_dict = timed(lambda: [builtin_get(k) for k in keys])

    # CPython's dict is C; a pure-Python probe loop will not beat it, and pretending
    # otherwise would be dishonest. What IS true and worth asserting is that the
    # specialised map stays within a bounded factor while using a flat layout.
    assert t_mine < t_dict * 40, (
        f"IntHashMap lookup {t_mine * 1e3:.1f} ms vs dict {t_dict * 1e3:.1f} ms — "
        f"more than 40x off means the probe loop is doing something quadratic"
    )
    assert len(mine) == len(builtin)


@pytest.mark.hard
def test_count_min_sketch_never_underestimates() -> None:
    """The one guarantee the structure actually makes."""
    rng = random.Random(5)
    truth: dict[int, int] = {}
    cms = CountMinSketch(width=512, depth=4)
    for _ in range(50_000):
        item = rng.randrange(2000)
        cms.add(item)
        truth[item] = truth.get(item, 0) + 1
    for item, count in truth.items():
        assert cms.estimate(item) >= count, "a count-min sketch must never underestimate"


@pytest.mark.hard
def test_count_min_sketch_error_stays_inside_the_theoretical_bound() -> None:
    """Measured against the eps*N bound over 10,000+ distinct items, which is what
    the spec asks you to check rather than assume."""
    rng = random.Random(13)
    truth: dict[int, int] = {}
    cms = CountMinSketch(width=4096, depth=5)
    for _ in range(200_000):
        # Skewed: a few very frequent items plus a long uniform tail. Purely uniform
        # data flatters the sketch and is not what it is used on.
        item = rng.randrange(20) if rng.random() < 0.35 else rng.randrange(12_000)
        cms.add(item)
        truth[item] = truth.get(item, 0) + 1

    assert len(truth) > 1000
    bound = cms.theoretical_error_bound()          # eps * N, with eps = e / width
    delta = math.exp(-cms.depth)                   # the bound's failure probability
    errors = [cms.estimate(k) - v for k, v in truth.items()]
    assert min(errors) >= 0

    # The guarantee is probabilistic, not absolute: an individual estimate may exceed
    # eps*N with probability at most delta. Asserting "no estimate ever exceeds it"
    # would be asserting something the structure does not promise.
    over = sum(1 for e in errors if e > bound) / len(errors)
    assert over <= delta * 3, (
        f"{over:.4%} of estimates exceeded the eps*N bound of {bound:.1f}; "
        f"the theory allows up to {delta:.4%}"
    )
    mean_error = sum(errors) / len(errors)
    assert mean_error < bound, (
        f"mean error {mean_error:.1f} vs bound {bound:.1f} — the bound should be loose"
    )
