"""deque vs list-as-queue; LRU cache throughput; array-backed vs pointer deque."""
import time, gc, random
from collections import deque, OrderedDict

def timeit(fn, reps=3):
    best=1e9
    for _ in range(reps):
        gc.collect(); t=time.perf_counter(); fn(); best=min(best,time.perf_counter()-t)
    return best

print("== queue: list.pop(0) vs deque.popleft ==")
print("n,list_ms,deque_ms,ratio")
for n in (1_000, 10_000, 50_000, 100_000):
    def L():
        q=list(range(n))
        while q: q.pop(0)
    def D():
        q=deque(range(n))
        while q: q.popleft()
    a=timeit(L); b=timeit(D)
    print(f"{n},{a*1e3:.2f},{b*1e3:.2f},{a/b:.0f}x", flush=True)

print()
print("== LRU: hand-rolled (dict+DLL) vs OrderedDict vs functools.lru_cache ==")
class LRU:
    __slots__=('cap','map','head','tail')
    class N:
        __slots__=('k','v','p','n')
        def __init__(s,k,v): s.k=k; s.v=v; s.p=None; s.n=None
    def __init__(self,cap):
        self.cap=cap; self.map={}
        self.head=LRU.N(None,None); self.tail=LRU.N(None,None)
        self.head.n=self.tail; self.tail.p=self.head
    def _unlink(self,x): x.p.n=x.n; x.n.p=x.p
    def _push(self,x):
        x.p=self.head; x.n=self.head.n; self.head.n.p=x; self.head.n=x
    def get(self,k,default=None):
        x=self.map.get(k)
        if x is None: return default
        self._unlink(x); self._push(x); return x.v
    def put(self,k,v):
        x=self.map.get(k)
        if x is not None:
            x.v=v; self._unlink(x); self._push(x); return
        if len(self.map)>=self.cap:
            old=self.tail.p; self._unlink(old); del self.map[old.k]
        x=LRU.N(k,v); self.map[k]=x; self._push(x)

CAP=10_000
rng=random.Random(3)
# zipf-ish access pattern: 80% of hits on 20% of keys
ops=[]
for _ in range(500_000):
    r=rng.random()
    k = rng.randrange(0, 2_000) if r<0.8 else rng.randrange(0, 40_000)
    ops.append(k)

def run_lru():
    c=LRU(CAP); h=0
    for k in ops:
        v=c.get(k)
        if v is None: c.put(k,k*2)
        else: h+=1
    return h
def run_od():
    c=OrderedDict(); h=0
    for k in ops:
        if k in c:
            c.move_to_end(k); h+=1
        else:
            c[k]=k*2
            if len(c)>CAP: c.popitem(last=False)
    return h
h1=run_lru(); h2=run_od()
a=timeit(run_lru); b=timeit(run_od)
print(f"ops,{len(ops)}")
print(f"hand_rolled_ms,{a*1e3:.1f},hit_rate,{h1/len(ops):.3f},per_op_ns,{a/len(ops)*1e9:.0f}")
print(f"ordereddict_ms,{b*1e3:.1f},hit_rate,{h2/len(ops):.3f},per_op_ns,{b/len(ops)*1e9:.0f}")
