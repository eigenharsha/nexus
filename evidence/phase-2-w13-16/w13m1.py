import time, sys, random, gc

def bench(fn, reps=3):
    ts=[]
    for _ in range(reps):
        gc.collect()
        t=time.perf_counter(); fn(); ts.append(time.perf_counter()-t)
    return min(ts)

class Node:
    __slots__=('val','nxt')
    def __init__(self,v): self.val=v; self.nxt=None

def build_list(n, shuffled):
    nodes=[Node(i) for i in range(n)]
    order=list(range(n))
    if shuffled: random.Random(42).shuffle(order)
    for a,b in zip(order, order[1:]):
        nodes[a].nxt=nodes[b]
    nodes[order[-1]].nxt=None
    return nodes[order[0]]

def sum_list(head):
    s=0; c=head
    while c is not None:
        s+=c.val; c=c.nxt
    return s

def sum_pylist(lst):
    s=0
    for v in lst: s+=v
    return s

print("n,pylist_ms,linked_seq_ms,linked_shuf_ms,shuf_vs_list")
for n in (1000, 10_000, 100_000, 1_000_000):
    lst=list(range(n))
    h1=build_list(n, False)
    h2=build_list(n, True)
    a=bench(lambda: sum_pylist(lst))
    b=bench(lambda: sum_list(h1))
    c=bench(lambda: sum_list(h2))
    print(f"{n},{a*1e3:.3f},{b*1e3:.3f},{c*1e3:.3f},{c/a:.1f}x", flush=True)
    del h1,h2,lst; gc.collect()
