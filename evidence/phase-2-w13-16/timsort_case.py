import sys, random, time, gc
n=2_000_000; case=sys.argv[1]
r=random.Random(17)
if case=="random":        data=[r.random() for _ in range(n)]
elif case=="sorted":      data=sorted(r.random() for _ in range(n))
elif case=="reversed":    data=sorted((r.random() for _ in range(n)),reverse=True)
elif case=="nearly":
    data=sorted(r.random() for _ in range(n))
    for _ in range(1000): data[r.randrange(n)]=r.random()
gc.collect()
t=time.perf_counter(); data.sort(); el=time.perf_counter()-t
print(f"{case:>14}: {el*1000:7.1f} ms")
