from __future__ import annotations
import gc, math, time
from typing import Callable, Sequence

def measure(fn: Callable[[int], None], n: int, reps: int = 5) -> float:
    best = math.inf
    for _ in range(reps):
        gc.collect()
        t0 = time.perf_counter()
        fn(n)
        best = min(best, time.perf_counter() - t0)
    return best

def fit_exponent(sizes: Sequence[int], times: Sequence[float]) -> tuple[float, float]:
    xs = [math.log(n) for n in sizes]; ys = [math.log(t) for t in times]
    k = len(xs); mx, my = sum(xs)/k, sum(ys)/k
    num = sum((x-mx)*(y-my) for x,y in zip(xs,ys)); den = sum((x-mx)**2 for x in xs)
    slope = num/den
    return slope, my - slope*mx

def classify(slope: float) -> str:
    for bound, name in ((0.15,"O(1) or O(log n)"),(0.75,"sub-linear"),(1.15,"O(n)"),
                        (1.45,"O(n log n)"),(2.30,"O(n^2)"),(3.30,"O(n^3)")):
        if slope < bound: return name
    return f"worse than cubic (exponent {slope:.2f})"

def profile(name, fn, sizes):
    times = [measure(fn, n) for n in sizes]
    slope,_ = fit_exponent(sizes, times)
    print(f"{name:<28} exponent={slope:5.2f}  ->  {classify(slope)}")
    for n,t in zip(sizes,times):
        print(f"    n={n:>8,}  {t*1e3:9.3f} ms")

if __name__ == "__main__":
    SIZES = (1_000, 4_000, 16_000, 64_000)
    def linear_scan(n):
        data = list(range(n)); _ = sum(data)
    def quadratic_membership(n):
        a = list(range(n)); b = list(range(n))
        _ = sum(1 for x in a if x in b)
    def linear_membership(n):
        a = list(range(n)); b = set(range(n))
        _ = sum(1 for x in a if x in b)
    def sort_it(n):
        import random
        data = [random.random() for _ in range(n)]; data.sort()
    profile("linear scan", linear_scan, SIZES)
    profile("membership in list", quadratic_membership, SIZES)
    profile("membership in set", linear_membership, SIZES)
    profile("list.sort (Timsort)", sort_it, SIZES)
