"""Hash-collision DoS: what happens when every key lands in one bucket."""
import time, gc, os
OUT="/tmp/nexbench/out"
CAP=1<<14
class Evil:
    __slots__=("v",)
    def __init__(self,v): self.v=v
    def __hash__(self): return 0                 # every key hashes to bucket 0
    def __eq__(self,o): return isinstance(o,Evil) and self.v==o.v
rows=[]
for n in (1000, 2000, 4000, 8000):
    good={i:i for i in range(n)}
    evil={Evil(i):i for i in range(n)}
    gk=list(range(n)); ek=[Evil(i) for i in range(n)]
    gc.collect(); t=time.perf_counter()
    for k in gk: good[k]
    tg=time.perf_counter()-t
    gc.collect(); t=time.perf_counter()
    for k in ek: evil[k]
    te=time.perf_counter()-t
    rows.append(f"{n},{tg*1e3:.2f},{te*1e3:.2f},{te/tg:.0f}x")
out=["n_keys,normal_dict_lookup_all_ms,all_colliding_lookup_all_ms,slowdown"]+rows
open(os.path.join(OUT,"w13m4_dos.txt"),"w").write("\n".join(out)+"\n")
print("\n".join(out))
