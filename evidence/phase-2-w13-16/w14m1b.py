"""Degenerate BST: sorted insert vs shuffled insert, measured depth and lookup time."""
import time, gc, random, sys
sys.setrecursionlimit(100000)
class BST:
    __slots__=('root',)
    class N:
        __slots__=('k','l','r')
        def __init__(s,k): s.k=k; s.l=None; s.r=None
    def __init__(self): self.root=None
    def insert(self,k):
        if self.root is None: self.root=BST.N(k); return
        n=self.root
        while True:
            if k<n.k:
                if n.l is None: n.l=BST.N(k); return
                n=n.l
            else:
                if n.r is None: n.r=BST.N(k); return
                n=n.r
    def find(self,k):
        n=self.root; steps=0
        while n is not None:
            steps+=1
            if k==n.k: return steps
            n = n.l if k<n.k else n.r
        return steps
    def depth(self):
        # iterative to avoid recursion limits on degenerate trees
        best=0; stack=[(self.root,1)]
        while stack:
            n,d=stack.pop()
            if n is None: continue
            best=max(best,d)
            stack.append((n.l,d+1)); stack.append((n.r,d+1))
        return best

N=100_000
keys=list(range(N))
rng=random.Random(1)
shuf=keys[:]; rng.shuffle(shuf)
probes=[rng.randrange(N) for _ in range(20_000)]
for name,order in (("sorted_insert",keys),("shuffled_insert",shuf)):
    t=BST()
    t0=time.perf_counter()
    for k in order: t.insert(k)
    build=time.perf_counter()-t0
    d=t.depth()
    gc.collect()
    t0=time.perf_counter()
    steps=sum(t.find(k) for k in probes)
    look=time.perf_counter()-t0
    print(f"{name},n,{N},depth,{d},build_s,{build:.2f},lookup_ms,{look*1e3:.1f},avg_steps,{steps/len(probes):.1f}", flush=True)
