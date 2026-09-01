"""Hash table: chaining vs open addressing (linear probe), load factor sweep."""
import time, random, gc, sys

class Chained:
    def __init__(self, cap=1024):
        self.cap=cap; self.n=0; self.buckets=[[] for _ in range(cap)]
    def _idx(self,k): return hash(k) & (self.cap-1)
    def put(self,k,v):
        b=self.buckets[self._idx(k)]
        for i,(kk,_) in enumerate(b):
            if kk==k: b[i]=(k,v); return
        b.append((k,v)); self.n+=1
    def get(self,k,default=None):
        for kk,vv in self.buckets[self._idx(k)]:
            if kk==k: return vv
        return default

TOMB=object()
class OpenAddr:
    def __init__(self, cap=1024):
        self.cap=cap; self.n=0; self.keys=[None]*cap; self.vals=[None]*cap
    def put(self,k,v):
        m=self.cap-1; i=hash(k)&m
        while self.keys[i] is not None and self.keys[i] is not TOMB:
            if self.keys[i]==k: self.vals[i]=v; return
            i=(i+1)&m
        self.keys[i]=k; self.vals[i]=v; self.n+=1
    def get(self,k,default=None):
        m=self.cap-1; i=hash(k)&m
        while self.keys[i] is not None:
            if self.keys[i] is not TOMB and self.keys[i]==k: return self.vals[i]
            i=(i+1)&m
        return default

CAP=1<<16
rng=random.Random(7)
universe=[f"key-{i}-{rng.random():.9f}" for i in range(CAP)]

def timeit(fn, reps=3):
    best=1e9
    for _ in range(reps):
        gc.collect(); t=time.perf_counter(); fn(); best=min(best, time.perf_counter()-t)
    return best

print("load_factor,chain_get_ns,open_get_ns,dict_get_ns,open_vs_chain")
for lf in (0.30,0.50,0.70,0.80,0.90,0.95):
    n=int(CAP*lf)
    keys=universe[:n]
    c=Chained(CAP); o=OpenAddr(CAP); d={}
    for i,k in enumerate(keys):
        c.put(k,i); o.put(k,i); d[k]=i
    probe=[keys[rng.randrange(n)] for _ in range(200_000)]
    def gc_(): 
        s=0
        for k in probe: s+=c.get(k)
    def go_():
        s=0
        for k in probe: s+=o.get(k)
    def gd_():
        s=0
        for k in probe: s+=d[k]
    a=timeit(gc_); b=timeit(go_); e=timeit(gd_)
    per=lambda t: t/200_000*1e9
    print(f"{lf:.2f},{per(a):.0f},{per(b):.0f},{per(e):.0f},{b/a:.2f}x", flush=True)
