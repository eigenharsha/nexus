"""W13-M2 extras + W14 M2-M5 benchmarks. stdlib only, serial."""
import time,gc,random,heapq,sys,os,unicodedata,tracemalloc
from collections import deque
OUT="/tmp/nexbench/out"
def emit(name,lines):
    open(os.path.join(OUT,name+".txt"),"w").write("\n".join(lines)+"\n")
    print(f"--- {name} ---\n"+"\n".join(lines)+"\n",flush=True)
def best_of(fn,reps=5):
    b=1e18
    for _ in range(reps):
        gc.collect(); t=time.perf_counter(); fn(); b=min(b,time.perf_counter()-t)
    return b

def w13m2_extra():
    # sliding window maximum: naive vs monotonic deque
    rng=random.Random(21); rows=["n,k,naive_ms,monotonic_deque_ms,speedup"]
    for n,k in ((100_000,1000),(1_000_000,1000)):
        a=[rng.randrange(1_000_000) for _ in range(n)]
        def naive():
            return [max(a[i:i+k]) for i in range(n-k+1)]
        def mono():
            dq=deque(); out=[]
            for i,v in enumerate(a):
                while dq and a[dq[-1]]<=v: dq.pop()
                dq.append(i)
                if dq[0]<=i-k: dq.popleft()
                if i>=k-1: out.append(a[dq[0]])
            return out
        if n<=100_000: assert naive()==mono()
        nv=best_of(naive,1 if n>100_000 else 3); mo=best_of(mono,3)
        rows.append(f"{n},{k},{nv*1e3:.1f},{mo*1e3:.1f},{nv/mo:.0f}x")
        del a; gc.collect()
    emit("w13m2_window",rows)
    # unicode normalisation cost + length surprises
    s="café"; s2="café"
    rows=[f"cafe_precomposed_len,{len(s)}", f"cafe_decomposed_len,{len(s2)}",
          f"equal_as_python_strings,{s==s2}",
          f"equal_after_NFC,{unicodedata.normalize('NFC',s)==unicodedata.normalize('NFC',s2)}",
          f"family_emoji,{len('👨‍👩‍👧‍👦')} python chars",
          f"utf8_bytes_of_family_emoji,{len('👨‍👩‍👧‍👦'.encode())}"]
    corpus="".join(random.Random(3).choice("abcdéèêñ漢字") for _ in range(2_000_000))
    t=best_of(lambda: unicodedata.normalize("NFC",corpus),3)
    t2=best_of(lambda: corpus.lower(),3)
    rows += [f"corpus_chars,{len(corpus)}",
             f"NFC_normalize_ms,{t*1e3:.1f}",
             f"lower_ms,{t2*1e3:.1f}",
             f"normalize_over_lower,{t/t2:.1f}x"]
    emit("w13m2_unicode",rows)

def w14m2():
    """Bounded priority queue: top-K nearest neighbours over 1M vectors, brute force."""
    import array, math
    D=64; N=1_000_000; K=10
    rng=random.Random(4)
    # flat array of floats: N*D. Use array('f') for compactness.
    vecs=array.array('f',(rng.gauss(0,1) for _ in range(N*D)))
    q=array.array('f',(rng.gauss(0,1) for _ in range(D)))
    def scan_full_sort():
        scores=[]
        for i in range(N):
            b=i*D; s=0.0
            for j in range(D): s+=vecs[b+j]*q[j]
            scores.append((s,i))
        scores.sort(reverse=True)
        return scores[:K]
    def scan_bounded_heap():
        h=[]; push=heapq.heappush; rep=heapq.heapreplace
        for i in range(N):
            b=i*D; s=0.0
            for j in range(D): s+=vecs[b+j]*q[j]
            if len(h)<K: push(h,(s,i))
            elif s>h[0][0]: rep(h,(s,i))
        return sorted(h,reverse=True)
    rows=[f"vectors,{N}",f"dim,{D}",f"K,{K}"]
    for name,fn in (("full_sort_all_scores",scan_full_sort),("bounded_min_heap",scan_bounded_heap)):
        gc.collect(); tracemalloc.start()
        t=time.perf_counter(); r=fn(); el=time.perf_counter()-t
        _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
        rows.append(f"{name},seconds,{el:.2f},peak_python_heap_MB,{peak/1e6:.2f}")
        gc.collect()
    emit("w14m2_topk_vectors",rows)
    del vecs; gc.collect()
    # heap ops microbench
    rows=["operation,n,total_ms,per_op_ns"]
    for n in (100_000,1_000_000):
        data=[rng.random() for _ in range(n)]
        def build_heapify():
            h=data[:]; heapq.heapify(h); return h
        def build_pushes():
            h=[]
            for v in data: heapq.heappush(h,v)
            return h
        a=best_of(build_heapify,3); b=best_of(build_pushes,3)
        rows.append(f"heapify_bottom_up,{n},{a*1e3:.1f},{a/n*1e9:.0f}")
        rows.append(f"n_successive_pushes,{n},{b*1e3:.1f},{b/n*1e9:.0f}")
        rows.append(f"heapify_speedup,{n},{b/a:.2f}x,-")
        del data; gc.collect()
    emit("w14m2_heap_build",rows)

def w14m3():
    """Graph representation memory + BFS + toposort/cycle detection."""
    import sys
    rng=random.Random(6)
    rows=["nodes,edges,adj_list_MB,adj_matrix_bitset_MB,dense_matrix_MB,list_over_matrix"]
    for n,m in ((10_000,100_000),(100_000,1_000_000)):
        adj={i:[] for i in range(n)}
        for _ in range(m):
            u=rng.randrange(n); v=rng.randrange(n); adj[u].append(v)
        def deep(o,seen=None):
            seen=seen if seen is not None else set()
            if id(o) in seen: return 0
            seen.add(id(o)); s=sys.getsizeof(o)
            if isinstance(o,dict):
                for k,v in o.items(): s+=deep(k,seen)+deep(v,seen)
            elif isinstance(o,list):
                for i in o: s+=deep(i,seen)
            return s
        lst_mb=deep(adj)/1e6
        bitset_mb=(n*n)/8/1e6
        dense_mb=(n*n)/1e6   # 1 byte per cell
        rows.append(f"{n},{m},{lst_mb:.1f},{bitset_mb:.1f},{dense_mb:.1f},{bitset_mb/lst_mb:.2f}x")
        del adj; gc.collect()
    emit("w14m3_graph_memory",rows)

    # BFS on a 1M-edge graph
    n,m=100_000,1_000_000
    adj=[[] for _ in range(n)]
    for _ in range(m):
        u=rng.randrange(n); v=rng.randrange(n); adj[u].append(v); adj[v].append(u)
    def bfs(src):
        dist=[-1]*n; dist[src]=0; q=deque([src])
        while q:
            u=q.popleft()
            du=dist[u]+1
            for v in adj[u]:
                if dist[v]<0: dist[v]=du; q.append(v)
        return sum(1 for d in dist if d>=0)
    t=best_of(lambda: bfs(0),3)
    reach=bfs(0)
    emit("w14m3_bfs",[f"nodes,{n}",f"undirected_edges,{m}",f"bfs_ms,{t*1e3:.1f}",
                      f"reached,{reach}",f"ns_per_edge,{t/(2*m)*1e9:.0f}"])
    del adj; gc.collect()

    # toposort with cycle detection on a DAG + injected cycle
    def toposort(graph, nnodes):
        indeg=[0]*nnodes
        for u in range(nnodes):
            for v in graph[u]: indeg[v]+=1
        q=deque(i for i in range(nnodes) if indeg[i]==0); order=[]
        while q:
            u=q.popleft(); order.append(u)
            for v in graph[u]:
                indeg[v]-=1
                if indeg[v]==0: q.append(v)
        return order if len(order)==nnodes else None
    N=200_000
    dag=[[] for _ in range(N)]
    for u in range(N):
        for _ in range(3):
            v=rng.randrange(u+1,N) if u+1<N else None
            if v is not None: dag[u].append(v)
    t=best_of(lambda: toposort(dag,N),3)
    ok=toposort(dag,N) is not None
    dag[N-1].append(0)   # inject a back edge -> cycle
    t2=best_of(lambda: toposort(dag,N),3)
    bad=toposort(dag,N) is None
    emit("w14m3_toposort",[f"nodes,{N}",f"edges,{sum(len(x) for x in dag)}",
                           f"toposort_dag_ms,{t*1e3:.1f},valid_order,{ok}",
                           f"toposort_with_cycle_ms,{t2*1e3:.1f},detected,{bad}"])
    del dag; gc.collect()

def w14m4():
    """Dijkstra vs A* on a grid with obstacles: node expansions + runtime."""
    import math
    W=H=1200
    rng=random.Random(8)
    blocked=bytearray(W*H)
    for _ in range(int(W*H*0.20)):
        blocked[rng.randrange(W*H)]=1
    src=(0,0); dst=(W-1,H-1)
    blocked[0]=0; blocked[W*H-1]=0
    def nbrs(i):
        x,y=i%W,i//W
        if x>0: yield i-1
        if x<W-1: yield i+1
        if y>0: yield i-W
        if y<H-1: yield i+W
    def dijkstra():
        dist=[math.inf]*(W*H); s=src[1]*W+src[0]; t=dst[1]*W+dst[0]
        dist[s]=0; pq=[(0,s)]; exp=0
        while pq:
            d,u=heapq.heappop(pq)
            if d>dist[u]: continue
            exp+=1
            if u==t: return d,exp
            for v in nbrs(u):
                if blocked[v]: continue
                nd=d+1
                if nd<dist[v]: dist[v]=nd; heapq.heappush(pq,(nd,v))
        return None,exp
    def astar():
        dist=[math.inf]*(W*H); s=src[1]*W+src[0]; t=dst[1]*W+dst[0]
        tx,ty=dst
        def h(i): return abs(i%W-tx)+abs(i//W-ty)
        dist[s]=0; pq=[(h(s),0,s)]; exp=0
        while pq:
            f,d,u=heapq.heappop(pq)
            if d>dist[u]: continue
            exp+=1
            if u==t: return d,exp
            for v in nbrs(u):
                if blocked[v]: continue
                nd=d+1
                if nd<dist[v]: dist[v]=nd; heapq.heappush(pq,(nd+h(v),nd,v))
        return None,exp
    gc.collect(); t0=time.perf_counter(); d1,e1=dijkstra(); t1=time.perf_counter()-t0
    gc.collect(); t0=time.perf_counter(); d2,e2=astar();   t2=time.perf_counter()-t0
    emit("w14m4_astar",[f"grid,{W}x{H}",f"cells,{W*H}",f"blocked_pct,20",
                        f"dijkstra,path_cost,{d1},expansions,{e1},seconds,{t1:.2f}",
                        f"astar_manhattan,path_cost,{d2},expansions,{e2},seconds,{t2:.2f}",
                        f"expansion_reduction,{e1/e2:.2f}x",
                        f"speedup,{t1/t2:.2f}x",
                        f"same_cost,{d1==d2}"])

def w14m5():
    """DP: fib call counts; edit distance timing + space optimisation."""
    sys.setrecursionlimit(20000)
    calls={"naive":0,"memo":0}
    def fib_naive(n):
        calls["naive"]+=1
        return n if n<2 else fib_naive(n-1)+fib_naive(n-2)
    def fib_memo(n,seen={}):
        calls["memo"]+=1
        if n<2: return n
        if n in seen: return seen[n]
        seen[n]=fib_memo(n-1,seen)+fib_memo(n-2,seen)
        return seen[n]
    rows=["n,naive_calls,memo_calls,tab_steps,naive_seconds"]
    for n in (10,20,30,35):
        calls["naive"]=0; calls["memo"]=0
        t=time.perf_counter(); fib_naive(n); el=time.perf_counter()-t
        fib_memo(n,{})
        rows.append(f"{n},{calls['naive']},{calls['memo']},{n+1},{el:.4f}")
    emit("w14m5_fib",rows)

    def ed_full(a,b):
        n,m=len(a),len(b)
        dp=[[0]*(m+1) for _ in range(n+1)]
        for i in range(n+1): dp[i][0]=i
        for j in range(m+1): dp[0][j]=j
        for i in range(1,n+1):
            ai=a[i-1]; row=dp[i]; prev=dp[i-1]
            for j in range(1,m+1):
                row[j]=min(prev[j]+1,row[j-1]+1,prev[j-1]+(ai!=b[j-1]))
        return dp[n][m]
    def ed_two_rows(a,b):
        n,m=len(a),len(b)
        if m>n: a,b=b,a; n,m=m,n
        prev=list(range(m+1))
        for i in range(1,n+1):
            cur=[i]+[0]*m; ai=a[i-1]
            for j in range(1,m+1):
                cur[j]=min(prev[j]+1,cur[j-1]+1,prev[j-1]+(ai!=b[j-1]))
            prev=cur
        return prev[m]
    rng=random.Random(2)
    rows=["len_a,len_b,full_matrix_ms,two_row_ms,full_matrix_MB,two_row_MB,answers_match"]
    for L in (500,2000,4000):
        a="".join(rng.choice("acgt") for _ in range(L))
        b="".join(rng.choice("acgt") for _ in range(L))
        gc.collect(); tracemalloc.start()
        t=time.perf_counter(); r1=ed_full(a,b); t1=time.perf_counter()-t
        _,p1=tracemalloc.get_traced_memory(); tracemalloc.reset_peak()
        t=time.perf_counter(); r2=ed_two_rows(a,b); t2=time.perf_counter()-t
        _,p2=tracemalloc.get_traced_memory(); tracemalloc.stop()
        rows.append(f"{L},{L},{t1*1e3:.1f},{t2*1e3:.1f},{p1/1e6:.2f},{p2/1e6:.4f},{r1==r2}")
    emit("w14m5_editdistance",rows)

if __name__=="__main__":
    which=sys.argv[1] if len(sys.argv)>1 else "all"
    fns={"w13m2x":w13m2_extra,"w14m2":w14m2,"w14m3":w14m3,"w14m4":w14m4,"w14m5":w14m5}
    for k,f in fns.items():
        if which in ("all",k):
            print(f"### {k}",flush=True); f()
