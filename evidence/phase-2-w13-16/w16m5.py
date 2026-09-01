"""Plotting 10M points honestly: scatter vs hexbin vs 2-D histogram."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np, time, os, gc, resource, sys
OUT="/tmp/nexbench/out"
def emit(n,l):
    open(os.path.join(OUT,n+".txt"),"w").write("\n".join(l)+"\n"); print("\n".join(l),flush=True)
rng=np.random.default_rng(0)
rows=["n_points,method,seconds,png_bytes,note"]
for n in (10_000, 100_000, 1_000_000, 10_000_000):
    x=rng.standard_normal(n); y=x*0.6+rng.standard_normal(n)*0.8
    for method in ("scatter","hexbin","hist2d"):
        if method=="scatter" and n>1_000_000:
            rows.append(f"{n},{method},SKIPPED,-,unusable: overplotting hides all structure")
            continue
        gc.collect()
        fig,ax=plt.subplots(figsize=(5,4),dpi=100)
        t=time.perf_counter()
        if method=="scatter": ax.scatter(x,y,s=1,alpha=0.1,linewidths=0)
        elif method=="hexbin": ax.hexbin(x,y,gridsize=100,bins="log")
        else: ax.hist2d(x,y,bins=200,norm=matplotlib.colors.LogNorm())
        p=f"/tmp/nexbench/plot_{n}_{method}.png"
        fig.savefig(p,dpi=100); el=time.perf_counter()-t
        plt.close(fig)
        rows.append(f"{n},{method},{el:.2f},{os.path.getsize(p)},-")
        print(rows[-1],flush=True)
    del x,y; gc.collect()
mb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6
rows.append(f"peak_process_RSS_MB,{mb:.0f},-,-,-")
emit("w16m5_plotting",rows)
