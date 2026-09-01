"""top-K over a 10M stream: full sort vs heapq.nlargest vs bounded heap; memory."""
import time, gc, heapq, random, sys, tracemalloc
def timeit(fn, reps=1):
    best=1e9
    for _ in range(reps):
        gc.collect(); t=time.perf_counter(); r=fn(); best=min(best,time.perf_counter()-t)
    return best, r

N=10_000_000; K=100
rng=random.Random(5)
def stream():
    r=random.Random(5)
    for _ in range(N): yield r.random()

def full_sort():
    xs=list(stream())
    xs.sort()
    return xs[-K:]
def nlargest():
    return heapq.nlargest(K, stream())
def bounded():
    h=[]
    for v in stream():
        if len(h)<K: heapq.heappush(h,v)
        elif v>h[0]: heapq.heapreplace(h,v)
    return sorted(h)

tracemalloc.start()
t1,r1=timeit(full_sort); _,peak1=tracemalloc.get_traced_memory(); tracemalloc.reset_peak()
t2,r2=timeit(nlargest); _,peak2=tracemalloc.get_traced_memory(); tracemalloc.reset_peak()
t3,r3=timeit(bounded); _,peak3=tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"N,{N},K,{K}")
print(f"full_sort_s,{t1:.2f},peak_MB,{peak1/1e6:.1f}")
print(f"heapq.nlargest_s,{t2:.2f},peak_MB,{peak2/1e6:.3f}")
print(f"bounded_heap_s,{t3:.2f},peak_MB,{peak3/1e6:.3f}")
print("agree:", sorted(r1)==sorted(r2)==sorted(r3))
