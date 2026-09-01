"""top-K over a 10M stream. Time measured WITHOUT tracemalloc (it is ~30x overhead
on an allocation-heavy loop). Memory measured in a separate process via ru_maxrss."""
import time, gc, heapq, random, sys, os, resource
N=10_000_000; K=100
def stream():
    r=random.Random(5)
    for _ in range(N): yield r.random()
def full_sort():
    xs=list(stream()); xs.sort(); return xs[-K:]
def nlargest(): return heapq.nlargest(K, stream())
def bounded():
    h=[]; push=heapq.heappush; rep=heapq.heapreplace
    for v in stream():
        if len(h)<K: push(h,v)
        elif v>h[0]: rep(h,v)
    return sorted(h)
FNS={"full_sort_list":full_sort,"heapq_nlargest":nlargest,"bounded_min_heap":bounded}
if __name__=="__main__":
    name=sys.argv[1]
    gc.collect()
    base=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    t=time.perf_counter(); r=FNS[name](); el=time.perf_counter()-t
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    mb = peak/1e6 if sys.platform=="darwin" else peak/1e3
    print(f"{name},seconds,{el:.2f},process_peak_RSS_MB,{mb:.1f},checksum,{sum(r):.6f}")
