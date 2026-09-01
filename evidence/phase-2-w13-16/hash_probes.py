"""Deterministic probe counting for chaining vs open addressing.
Probe counts do not depend on machine load, so these numbers reproduce exactly."""
import random, os
OUT="/tmp/nexbench/out"
CAP=1<<16
rng=random.Random(7)
universe=[f"user-{i:06d}-{rng.randrange(10**9):09d}" for i in range(CAP)]
rows=["load_factor,entries,chain_avg_probes,chain_max_probes,open_avg_probes,open_max_probes,theory_chain_1+a/2,theory_open_(1+1/(1-a)^2)/2"]
for lf in (0.30,0.50,0.70,0.80,0.90,0.95,0.99):
    n=int(CAP*lf); keys=universe[:n]
    # chaining
    buckets=[[] for _ in range(CAP)]
    for i,k in enumerate(keys): buckets[hash(k)&(CAP-1)].append((k,i))
    # open addressing (linear probe)
    slots=[None]*CAP
    for i,k in enumerate(keys):
        j=hash(k)&(CAP-1)
        while slots[j] is not None: j=(j+1)&(CAP-1)
        slots[j]=k
    probe=[keys[rng.randrange(n)] for _ in range(50_000)]
    ct=cm=0
    for k in probe:
        b=buckets[hash(k)&(CAP-1)]; p=0
        for kk,_ in b:
            p+=1
            if kk==k: break
        ct+=p; cm=max(cm,p)
    ot=om=0
    for k in probe:
        j=hash(k)&(CAP-1); p=1
        while slots[j]!=k: j=(j+1)&(CAP-1); p+=1
        ot+=p; om=max(om,p)
    a=lf
    th_c=1+a/2
    th_o=(1+1/(1-a)**2)/2
    rows.append(f"{lf:.2f},{n},{ct/len(probe):.2f},{cm},{ot/len(probe):.2f},{om},{th_c:.2f},{th_o:.1f}")
open(os.path.join(OUT,"w13m4_probes.txt"),"w").write("\n".join(rows)+"\n")
print("\n".join(rows))
