import sys, random, time
print("=== W13-M1 growth_factor.py ===")
def total_copies(n, factor, start=1):
    cap, size, copies = start, 0, 0
    while size < n:
        if size == cap:
            cap = max(cap + 1, int(cap * factor)); copies += size
        size += 1
    return copies
for f in (1.0000001, 1.125, 1.25, 1.5, 2.0, 4.0):
    c = total_copies(1_000_000, f)
    print(f"factor {f:>9}:  {c:>12,} copies  ({c/1_000_000:.2f} per append)")

print("\n=== W13-M2 sys.getsizeof growth ===")
xs=[]; prev=None
for i in range(20):
    size=sys.getsizeof(xs)
    if size!=prev:
        print(f"len={len(xs):3d}  {size} bytes"); prev=size
    xs.append(i)

print("\n=== W13-M1 count_ops.py ===")
def slow(xs):
    ops=0
    for a in xs:
        for b in xs: ops+=1
    return ops
def fast(xs):
    ops=0
    for a in xs: ops+=1
    return ops+1
for n in (10,100,1000):
    d=list(range(n)); print(f"n={n:5d}  slow={slow(d):9d} ops   fast={fast(d):6d} ops")

print("\n=== W13-M5 Timsort adaptivity ===")
n=2_000_000
cases=[]
cases.append(("random",[random.random() for _ in range(n)]))
cases.append(("sorted",sorted(random.random() for _ in range(n))))
cases.append(("reversed",sorted((random.random() for _ in range(n)),reverse=True)))
ns=sorted(random.random() for _ in range(n))
for _ in range(1000):
    ns[random.randrange(n)]=random.random()
cases.append(("nearly sorted",ns))
for name,data in cases:
    t=time.perf_counter(); data.sort(); el=time.perf_counter()-t
    print(f"{name:>14}: {el*1000:7.1f} ms")
