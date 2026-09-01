"""Week 13-14 DSA benchmark suite. Runs SERIALLY. stdlib only.
Each section frees its structures before the next one builds."""
import time, gc, random, heapq, bisect, sys, os, tracemalloc
from collections import deque, OrderedDict

OUT = "/tmp/nexbench/out"
def emit(name, lines):
    p=os.path.join(OUT, name+".txt")
    with open(p,"w") as f: f.write("\n".join(lines)+"\n")
    print(f"--- {name} ---"); print("\n".join(lines)); print(flush=True)

def best_of(fn, reps=5):
    b=1e18
    for _ in range(reps):
        gc.collect()
        t=time.perf_counter(); fn(); b=min(b, time.perf_counter()-t)
    return b

# ============ W13-M1: array vs linked list traversal (cache locality) ============
def w13m1():
    class Node:
        __slots__=('val','nxt')
        def __init__(s,v): s.val=v; s.nxt=None
    def build(n, shuffled):
        nodes=[Node(i) for i in range(n)]
        order=list(range(n))
        if shuffled: random.Random(42).shuffle(order)
        for a,b in zip(order, order[1:]): nodes[a].nxt=nodes[b]
        nodes[order[-1]].nxt=None
        head=nodes[order[0]]
        return head, nodes
    def sum_linked(h):
        s=0; c=h
        while c is not None: s+=c.val; c=c.nxt
        return s
    def sum_arr(a):
        s=0
        for v in a: s+=v
        return s
    rows=["n,list_ms,linked_sequential_ms,linked_shuffled_ms,shuffled_over_list"]
    for n in (1_000, 10_000, 100_000, 1_000_000):
        gc.disable()                      # isolate from GC noise; each case measured alone
        a=list(range(n)); t_list=best_of(lambda: sum_arr(a)); del a
        gc.enable(); gc.collect(); gc.disable()
        h,keep=build(n,False); t_seq=best_of(lambda: sum_linked(h)); del h,keep
        gc.enable(); gc.collect(); gc.disable()
        h,keep=build(n,True);  t_shf=best_of(lambda: sum_linked(h)); del h,keep
        gc.enable(); gc.collect()
        rows.append(f"{n},{t_list*1e3:.3f},{t_seq*1e3:.3f},{t_shf*1e3:.3f},{t_shf/t_list:.1f}x")
    emit("w13m1_locality", rows)

# ============ W13-M2: prefix sums + substring search ============
def w13m2():
    rng=random.Random(11)
    rows=["n,queries,naive_ms,build_ms,prefix_query_ms,query_speedup"]
    for n in (100_000, 1_000_000):
        a=[rng.randrange(1,100) for _ in range(n)]
        q=2000
        qs=[]
        for _ in range(q):
            i=rng.randrange(0,n); j=rng.randrange(i,n); qs.append((i,j))
        def naive():
            t=0
            for i,j in qs: t+=sum(a[i:j+1])
            return t
        def build():
            p=[0]*(n+1); s=0
            for i,v in enumerate(a): s+=v; p[i+1]=s
            return p
        p=build()
        def query():
            t=0
            for i,j in qs: t+=p[j+1]-p[i]
            return t
        assert naive()==query()
        nv=best_of(naive,3); bd=best_of(build,3); qy=best_of(query,5)
        rows.append(f"{n},{q},{nv*1e3:.1f},{bd*1e3:.1f},{qy*1e3:.3f},{nv/qy:.0f}x")
        del a,p,qs; gc.collect()
    emit("w13m2_prefix", rows)

    def naive_find(t,p):
        n,m=len(t),len(p)
        for i in range(n-m+1):
            if t[i:i+m]==p: return i
        return -1
    def kmp_table(p):
        f=[0]*len(p); k=0
        for i in range(1,len(p)):
            while k and p[i]!=p[k]: k=f[k-1]
            if p[i]==p[k]: k+=1
            f[i]=k
        return f
    def kmp_find(t,p):
        if not p: return 0
        f=kmp_table(p); k=0
        for i,ch in enumerate(t):
            while k and ch!=p[k]: k=f[k-1]
            if ch==p[k]:
                k+=1
                if k==len(p): return i-k+1
        return -1
    text="a"*2_000_000+"b"; pat="a"*200+"b"
    assert naive_find(text,pat)==kmp_find(text,pat)==text.find(pat)
    nv=best_of(lambda: naive_find(text,pat),2)
    km=best_of(lambda: kmp_find(text,pat),2)
    bi=best_of(lambda: text.find(pat),5)
    rows=[f"text_chars,{len(text)}", f"pattern_chars,{len(pat)}",
          f"naive_python_ms,{nv*1e3:.1f}",
          f"kmp_python_ms,{km*1e3:.1f}",
          f"str_find_C_ms,{bi*1e3:.3f}",
          f"naive_over_kmp,{nv/km:.2f}x",
          f"kmp_over_str_find,{km/bi:.0f}x"]
    emit("w13m2_substring", rows)

# ============ W13-M3: queue + LRU ============
def w13m3():
    rows=["n,list_pop0_ms,deque_popleft_ms,ratio"]
    for n in (1_000, 10_000, 50_000, 100_000):
        def L():
            q=list(range(n))
            while q: q.pop(0)
        def D():
            q=deque(range(n))
            while q: q.popleft()
        a=best_of(L,3); b=best_of(D,3)
        rows.append(f"{n},{a*1e3:.2f},{b*1e3:.2f},{a/b:.0f}x")
    emit("w13m3_queue", rows)

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
    CAP=10_000; rng=random.Random(3)
    ops=[(rng.randrange(0,2_000) if rng.random()<0.8 else rng.randrange(0,40_000)) for _ in range(500_000)]
    def run_lru():
        c=LRU(CAP); h=0
        for k in ops:
            if c.get(k) is None: c.put(k,k*2)
            else: h+=1
        return h
    def run_od():
        c=OrderedDict(); h=0
        for k in ops:
            if k in c: c.move_to_end(k); h+=1
            else:
                c[k]=k*2
                if len(c)>CAP: c.popitem(last=False)
        return h
    h1=run_lru(); h2=run_od()
    a=best_of(run_lru,3); b=best_of(run_od,3)
    rows=[f"operations,{len(ops)}", f"capacity,{CAP}",
          f"hand_rolled_dict_dll_ms,{a*1e3:.1f},per_op_ns,{a/len(ops)*1e9:.0f},hit_rate,{h1/len(ops):.3f}",
          f"ordereddict_ms,{b*1e3:.1f},per_op_ns,{b/len(ops)*1e9:.0f},hit_rate,{h2/len(ops):.3f}",
          f"ordereddict_speedup,{a/b:.2f}x"]
    emit("w13m3_lru", rows)

# ============ W13-M4: hash table load factor sweep ============
def w13m4():
    class Chained:
        def __init__(self, cap): self.cap=cap; self.buckets=[[] for _ in range(cap)]
        def put(self,k,v):
            b=self.buckets[hash(k)&(self.cap-1)]
            for i,(kk,_) in enumerate(b):
                if kk==k: b[i]=(k,v); return
            b.append((k,v))
        def get(self,k):
            for kk,vv in self.buckets[hash(k)&(self.cap-1)]:
                if kk==k: return vv
            return None
    TOMB=object()
    class OpenAddr:
        def __init__(self,cap): self.cap=cap; self.keys=[None]*cap; self.vals=[None]*cap
        def put(self,k,v):
            m=self.cap-1; i=hash(k)&m
            while self.keys[i] is not None and self.keys[i] is not TOMB:
                if self.keys[i]==k: self.vals[i]=v; return
                i=(i+1)&m
            self.keys[i]=k; self.vals[i]=v
        def get(self,k):
            m=self.cap-1; i=hash(k)&m
            while self.keys[i] is not None:
                if self.keys[i] is not TOMB and self.keys[i]==k: return self.vals[i]
                i=(i+1)&m
            return None
    CAP=1<<16; rng=random.Random(7)
    universe=[f"user-{i:06d}-{rng.randrange(10**9):09d}" for i in range(CAP)]
    NPROBE=200_000
    rows=["load_factor,entries,chaining_ns_per_get,open_addr_ns_per_get,builtin_dict_ns_per_get,open_over_chain"]
    for lf in (0.30,0.50,0.70,0.80,0.90,0.95):
        n=int(CAP*lf); keys=universe[:n]
        probe=[keys[rng.randrange(n)] for _ in range(NPROBE)]
        gc.disable()
        c=Chained(CAP)
        for i,k in enumerate(keys): c.put(k,i)
        def gc_():
            g=c.get
            for k in probe: g(k)
        tc=best_of(gc_,5); del c
        gc.enable(); gc.collect(); gc.disable()
        o=OpenAddr(CAP)
        for i,k in enumerate(keys): o.put(k,i)
        def go_():
            g=o.get
            for k in probe: g(k)
        to=best_of(go_,5); del o
        gc.enable(); gc.collect(); gc.disable()
        d={k:i for i,k in enumerate(keys)}
        def gd_():
            for k in probe: d[k]
        td=best_of(gd_,5); del d
        gc.enable(); gc.collect()
        per=lambda t: t/NPROBE*1e9
        rows.append(f"{lf:.2f},{n},{per(tc):.0f},{per(to):.0f},{per(td):.0f},{to/tc:.2f}x")
    emit("w13m4_hashtable", rows)

# ============ W13-M5: top-K over a 10M stream ============
def w13m5():
    N=10_000_000; K=100
    def stream():
        r=random.Random(5)
        for _ in range(N): yield r.random()
    def full_sort():
        xs=list(stream()); xs.sort(); return xs[-K:]
    def nlargest(): return heapq.nlargest(K, stream())
    def bounded():
        h=[]
        push=heapq.heappush; rep=heapq.heapreplace
        for v in stream():
            if len(h)<K: push(h,v)
            elif v>h[0]: rep(h,v)
        return sorted(h)
    rows=[f"stream_elements,{N}", f"K,{K}"]
    for name,fn in (("full_sort_list",full_sort),("heapq_nlargest",nlargest),("bounded_min_heap",bounded)):
        gc.collect(); tracemalloc.start()
        t=time.perf_counter(); r=fn(); el=time.perf_counter()-t
        cur,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
        rows.append(f"{name},seconds,{el:.2f},peak_python_heap_MB,{peak/1e6:.3f}")
        gc.collect()
    emit("w13m5_topk", rows)

# ============ W14-M1: trie vs sorted array ; degenerate BST ============
def w14m1():
    def deep_size(obj, seen=None):
        seen = seen if seen is not None else set()
        if id(obj) in seen: return 0
        seen.add(id(obj)); size=sys.getsizeof(obj)
        if isinstance(obj,dict):
            for k,v in obj.items(): size+=deep_size(k,seen)+deep_size(v,seen)
        elif isinstance(obj,(list,tuple,set,frozenset)):
            for i in obj: size+=deep_size(i,seen)
        elif hasattr(obj,'__slots__'):
            for s in obj.__slots__:
                if hasattr(obj,s): size+=deep_size(getattr(obj,s),seen)
        return size
    words=[w.strip().lower() for w in open("/usr/share/dict/words")]
    words=sorted({w for w in words if w.isascii() and w.isalpha()})[:100_000]
    class TN:
        __slots__=('kids','end')
        def __init__(s): s.kids={}; s.end=False
    root=TN()
    for w in words:
        n=root
        for ch in w:
            nx=n.kids.get(ch)
            if nx is None: nx=TN(); n.kids[ch]=nx
            n=nx
        n.end=True
    def trie_complete(prefix, limit=10):
        n=root
        for ch in prefix:
            n=n.kids.get(ch)
            if n is None: return []
        out=[]; stack=[(n,prefix)]
        while stack and len(out)<limit:
            node,pre=stack.pop()
            if node.end: out.append(pre)
            for ch in sorted(node.kids, reverse=True): stack.append((node.kids[ch],pre+ch))
        return out[:limit]
    def arr_complete(prefix, limit=10):
        i=bisect.bisect_left(words,prefix); out=[]
        while i<len(words) and words[i].startswith(prefix) and len(out)<limit:
            out.append(words[i]); i+=1
        return out
    rng=random.Random(9)
    prefixes=[rng.choice(words)[:rng.randrange(1,4)] for _ in range(20_000)]
    a=best_of(lambda: [trie_complete(p) for p in prefixes],3)
    b=best_of(lambda: [arr_complete(p) for p in prefixes],3)
    rows=[f"vocabulary_words,{len(words)}", f"autocomplete_queries,{len(prefixes)}",
          f"trie_total_ms,{a*1e3:.1f},per_query_us,{a/len(prefixes)*1e6:.1f}",
          f"sorted_array_bisect_total_ms,{b*1e3:.1f},per_query_us,{b/len(prefixes)*1e6:.1f}",
          f"trie_resident_MB,{deep_size(root)/1e6:.1f}",
          f"sorted_list_resident_MB,{deep_size(words)/1e6:.1f}"]
    emit("w14m1_trie", rows)
    del root; gc.collect()

    class BST:
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
                n=n.l if k<n.k else n.r
            return steps
        def depth(self):
            best=0; st=[(self.root,1)]
            while st:
                n,d=st.pop()
                if n is None: continue
                if d>best: best=d
                st.append((n.l,d+1)); st.append((n.r,d+1))
            return best
    N=100_000; keys=list(range(N)); rng=random.Random(1)
    shuf=keys[:]; rng.shuffle(shuf)
    probes=[rng.randrange(N) for _ in range(5_000)]
    rows=["insert_order,n,tree_depth,build_s,lookup_ms_5000_probes,avg_comparisons"]
    for name,order in (("sorted_ascending",keys),("random_shuffled",shuf)):
        t=BST(); gc.disable()
        t0=time.perf_counter()
        for k in order: t.insert(k)
        build=time.perf_counter()-t0
        d=t.depth()
        t0=time.perf_counter(); steps=sum(t.find(k) for k in probes); look=time.perf_counter()-t0
        gc.enable()
        rows.append(f"{name},{N},{d},{build:.2f},{look*1e3:.1f},{steps/len(probes):.1f}")
        del t; gc.collect()
    emit("w14m1_bst", rows)

if __name__=="__main__":
    which=sys.argv[1] if len(sys.argv)>1 else "all"
    fns={"w13m1":w13m1,"w13m2":w13m2,"w13m3":w13m3,"w13m4":w13m4,"w13m5":w13m5,"w14m1":w14m1}
    for k,f in fns.items():
        if which in ("all",k):
            print(f"### running {k}", flush=True); f()
