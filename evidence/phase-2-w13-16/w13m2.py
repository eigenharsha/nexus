"""Prefix sums, two-pointer, sliding window, substring search."""
import time, gc, random, sys
def timeit(fn, reps=3):
    best=1e9
    for _ in range(reps):
        gc.collect(); t=time.perf_counter(); fn(); best=min(best,time.perf_counter()-t)
    return best

rng=random.Random(11)
print("== prefix sums vs naive range-sum ==")
print("n,q,naive_ms,prefix_build_ms,prefix_query_ms,speedup")
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
        p=[0]*(n+1)
        s=0
        for i,v in enumerate(a):
            s+=v; p[i+1]=s
        return p
    p=build()
    def query():
        t=0
        for i,j in qs: t+=p[j+1]-p[i]
        return t
    assert naive()==query()
    nv=timeit(naive); bd=timeit(build); qy=timeit(query)
    print(f"{n},{q},{nv*1e3:.1f},{bd*1e3:.1f},{qy*1e3:.3f},{nv/qy:.0f}x", flush=True)

print()
print("== substring search: naive vs KMP vs str.find ==")
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
# adversarial text: many partial matches
text = "a"*2_000_000 + "b"
pat  = "a"*200 + "b"
assert naive_find(text,pat)==kmp_find(text,pat)==text.find(pat)
nv=timeit(lambda: naive_find(text,pat),1)
km=timeit(lambda: kmp_find(text,pat),1)
bi=timeit(lambda: text.find(pat),3)
print(f"text_len,{len(text)},pattern_len,{len(pat)}")
print(f"naive_ms,{nv*1e3:.1f}")
print(f"kmp_ms,{km*1e3:.1f}")
print(f"str.find_ms,{bi*1e3:.3f}   (C two-way algorithm)")
print(f"naive/kmp,{nv/km:.2f}x  kmp/find,{km/bi:.0f}x")
