"""The benchmark harness for LAB-P2-W13.

    make bench IMPL=solution

Writes bench/results.csv and prints the tables. Everything reported is the MINIMUM of
`repeats` runs — the minimum is the closest thing available to "this machine with
nothing else on it"; means and medians measure your background processes.

What to look for, because these are the findings the write-up is about:

  1. Open addressing beats chaining on lookup at low load factor, and the gap closes
     or reverses as the load factor climbs.
  2. `MinHeap(items)` (heapify, O(n)) beats n pushes (O(n log n)) by a factor that
     grows with n.
  3. A linear scan of a small list beats a hash lookup below some crossover size.
     Find yours. It is bigger than most people guess.
"""
from __future__ import annotations

import csv
import random
import sys
import time
from pathlib import Path

from pycollections import (
    ChainedHashMap,
    CountMinSketch,
    DynamicArray,
    IntHashMap,
    MinHeap,
    OpenAddressingHashMap,
)

REPEATS = 3


def best(fn, repeats: int = REPEATS) -> float:  # noqa: ANN001
    lo = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        lo = min(lo, time.perf_counter() - t0)
    return lo


def bench_maps(rows: list[dict[str, object]]) -> None:
    print("\n== hash maps: build + lookup, ns/op ==")
    print(f"  {'n':>8}  {'chained ins':>12} {'open ins':>12} {'chained get':>12} "
          f"{'open get':>12} {'dict get':>10}")
    for n in (1_000, 10_000, 100_000, 300_000):
        keys = list(range(n))
        random.Random(1).shuffle(keys)

        def build(cls):  # noqa: ANN001, ANN202
            m = cls()
            for k in keys:
                m[k] = k
            return m

        t_ci = best(lambda: build(ChainedHashMap)) / n * 1e9
        t_oi = best(lambda: build(OpenAddressingHashMap)) / n * 1e9

        cm = build(ChainedHashMap)
        om = build(OpenAddressingHashMap)
        dm = dict.fromkeys(keys, 0)
        t_cg = best(lambda: [cm[k] for k in keys]) / n * 1e9
        t_og = best(lambda: [om[k] for k in keys]) / n * 1e9
        t_dg = best(lambda: [dm[k] for k in keys]) / n * 1e9

        print(f"  {n:>8}  {t_ci:>12.0f} {t_oi:>12.0f} {t_cg:>12.0f} {t_og:>12.0f} {t_dg:>10.0f}")
        for algo, ns in (("chained_insert", t_ci), ("open_insert", t_oi),
                         ("chained_get", t_cg), ("open_get", t_og), ("dict_get", t_dg)):
            rows.append({"group": "hashmap", "algo": algo, "n": n, "ns_per_op": round(ns, 1)})


def bench_load_factor(rows: list[dict[str, object]]) -> None:
    print("\n== open addressing: lookup cost vs load factor (capacity fixed at 65,536) ==")
    print(f"  {'target':>7} {'actual':>7}  {'ns/get':>8}  {'probes/get':>11}")
    # Random keys, not range(n): hash(int) is the identity in CPython, so
    # consecutive integers land in consecutive slots and probe exactly once at any
    # load factor. Benchmarking a hash table with integer keys 0..n-1 measures a
    # perfect hash, which is the single most common way to get this graph wrong.
    capacity = 1 << 16
    rng = random.Random(4242)
    for lf in (0.3, 0.5, 0.6, 0.7, 0.8, 0.9):
        n = int(capacity * lf)
        keys = rng.sample(range(10**9), n)
        m: OpenAddressingHashMap[int, int] = OpenAddressingHashMap(
            initial_capacity=capacity, max_load_factor=0.999
        )
        for k in keys:
            m[k] = k
        m.probes = 0
        t = best(lambda: [m[k] for k in keys]) / n * 1e9
        probes = m.probes / (n * REPEATS)
        print(f"  {lf:>7.1f} {m.load_factor:>7.2f}  {t:>8.0f}  {probes:>11.2f}")
        rows.append({"group": "load_factor", "algo": "open_get", "n": lf,
                     "ns_per_op": round(t, 1), "probes": round(probes, 2)})


def bench_heap(rows: list[dict[str, object]]) -> None:
    print("\n== heapify O(n) vs n pushes O(n log n) ==")
    print(f"  {'n':>8}  {'pushes (ms)':>12} {'heapify (ms)':>13} {'ratio':>7}")
    for n in (10_000, 100_000, 500_000):
        items = [random.Random(n).randrange(10**9) for _ in range(n)]

        def push_all() -> None:
            h: MinHeap[int] = MinHeap()
            for x in items:
                h.push(x)

        t_push = best(lambda: push_all(), 2) * 1e3
        t_heapify = best(lambda: MinHeap(items), 2) * 1e3
        print(f"  {n:>8}  {t_push:>12.1f} {t_heapify:>13.1f} {t_push / t_heapify:>6.1f}x")
        rows.append({"group": "heap", "algo": "push_n", "n": n, "ms": round(t_push, 2)})
        rows.append({"group": "heap", "algo": "heapify", "n": n, "ms": round(t_heapify, 2)})


def bench_small_container_crossover(rows: list[dict[str, object]]) -> None:
    print("\n== where does a list scan stop beating a set? (uniform hits, average case) ==")
    print(f"  {'size':>6}  {'list in (ns)':>13} {'set in (ns)':>12}  winner")
    rng = random.Random(77)
    for size in (1, 2, 3, 4, 8, 16, 32, 64):
        data = list(range(size))
        as_set = set(data)
        probes = [rng.randrange(size) for _ in range(1000)]
        t_list = best(lambda: [p in data for p in probes]) / 1000 * 1e9
        t_set = best(lambda: [p in as_set for p in probes]) / 1000 * 1e9
        winner = "list" if t_list < t_set else "set"
        print(f"  {size:>6}  {t_list:>13.0f} {t_set:>12.0f}  {winner}")
        rows.append({"group": "crossover", "algo": "list_in", "n": size, "ns_per_op": round(t_list, 1)})
        rows.append({"group": "crossover", "algo": "set_in", "n": size, "ns_per_op": round(t_set, 1)})


def bench_dynamic_array(rows: list[dict[str, object]]) -> None:
    print("\n== dynamic array growth factor: copies and slack (n=200,000) ==")
    print(f"  {'growth':>7}  {'capacity':>9} {'slack':>7} {'copies':>10} {'ms':>8}")
    n = 200_000
    for growth in (1.125, 1.5, 2.0, 4.0):
        def fill() -> DynamicArray[int]:
            a: DynamicArray[int] = DynamicArray(capacity=1, growth=growth)
            for i in range(n):
                a.append(i)
            return a

        t = best(lambda: fill(), 2) * 1e3
        a = fill()
        slack = a.capacity / n
        print(f"  {growth:>7.3f}  {a.capacity:>9} {slack:>6.2f}x {a.copies:>10} {t:>8.1f}")
        rows.append({"group": "dynarray", "algo": f"growth_{growth}", "n": n,
                     "ms": round(t, 2), "capacity": a.capacity, "copies": a.copies})


def bench_int_map(rows: list[dict[str, object]]) -> None:
    print("\n== IntHashMap vs dict, integer keys, known size, no deletes ==")
    n = 200_000
    keys = list(range(n))
    m = IntHashMap(n)
    for k in keys:
        m.put(k, k)
    d = dict.fromkeys(keys, 0)
    mg, dg = m.get, d.get
    t_mine = best(lambda: [mg(k) for k in keys]) / n * 1e9
    t_dict = best(lambda: [dg(k) for k in keys]) / n * 1e9
    print(f"  IntHashMap.get {t_mine:>8.0f} ns/op")
    print(f"  dict.get       {t_dict:>8.0f} ns/op   ({t_mine / t_dict:.1f}x)")
    print("  (CPython's dict is C. A pure-Python probe loop does not beat it, and the")
    print("   honest write-up says so — the win is layout and predictability, not speed.)")
    rows.append({"group": "intmap", "algo": "IntHashMap_get", "n": n, "ns_per_op": round(t_mine, 1)})
    rows.append({"group": "intmap", "algo": "dict_get", "n": n, "ns_per_op": round(t_dict, 1)})


def bench_sketch(rows: list[dict[str, object]]) -> None:
    print("\n== count-min sketch: measured error vs the eps*N bound ==")
    print(f"  {'width':>7} {'depth':>6} {'bytes':>8} {'mean err':>9} {'p99 err':>8} {'bound':>9}")
    rng = random.Random(99)
    stream = [rng.randrange(20) if rng.random() < 0.35 else rng.randrange(12_000)
              for _ in range(200_000)]
    truth: dict[int, int] = {}
    for x in stream:
        truth[x] = truth.get(x, 0) + 1

    for width, depth in ((512, 4), (2048, 4), (4096, 5), (16384, 5)):
        cms = CountMinSketch(width=width, depth=depth)
        for x in stream:
            cms.add(x)
        errs = sorted(cms.estimate(k) - v for k, v in truth.items())
        mean = sum(errs) / len(errs)
        p99 = errs[int(len(errs) * 0.99)]
        print(f"  {width:>7} {depth:>6} {cms.bytes_used:>8} {mean:>9.1f} {p99:>8} "
              f"{cms.theoretical_error_bound():>9.1f}")
        rows.append({"group": "sketch", "algo": f"w{width}_d{depth}", "n": len(truth),
                     "mean_error": round(mean, 2), "p99_error": p99,
                     "bound": round(cms.theoretical_error_bound(), 1),
                     "bytes": cms.bytes_used})


def main() -> None:
    out = Path("bench")
    out.mkdir(exist_ok=True)
    rows: list[dict[str, object]] = []
    bench_maps(rows)
    bench_load_factor(rows)
    bench_heap(rows)
    bench_small_container_crossover(rows)
    bench_dynamic_array(rows)
    bench_int_map(rows)
    bench_sketch(rows)

    fields: list[str] = []
    for r in rows:
        for k in r:
            if k not in fields:
                fields.append(k)
    with (out / "results.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nwrote {out / 'results.csv'} ({len(rows)} rows)")
    print(f"python {sys.version.split()[0]}")


if __name__ == "__main__":
    main()
