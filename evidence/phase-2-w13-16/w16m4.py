"""EDA: drift tests, correlation vs mutual information, and profiling cost."""
import numpy as np, pandas as pd, os, time, gc, warnings
warnings.filterwarnings("ignore")
from scipy import stats
OUT="/tmp/nexbench/out"
def emit(n,l):
    open(os.path.join(OUT,n+".txt"),"w").write("\n".join(l)+"\n"); print(f"--- {n} ---\n"+"\n".join(l)+"\n",flush=True)

# 1. KS test power: how big a shift can it detect, at what sample size?
rows=["shift_sd,n_per_sample,ks_detect_rate_at_p0.01,mean_ks_stat,mean_p"]
for shift in (0.0, 0.05, 0.1, 0.25, 0.5):
    for n in (1000, 10_000, 100_000):
        det=0; stats_=[]; ps=[]
        for s in range(200):
            rng=np.random.default_rng(s)
            a=rng.standard_normal(n); b=rng.standard_normal(n)+shift
            st,p=stats.ks_2samp(a,b)
            stats_.append(st); ps.append(p); det += p<0.01
        rows.append(f"{shift},{n},{det/200:.3f},{np.mean(stats_):.4f},{np.mean(ps):.4f}")
        print(rows[-1],flush=True)
emit("w16m4_ks_power",rows)

# 2. The false-positive problem: KS on large samples flags trivial differences
rows=["n_per_sample,identical_dist_flag_rate_p0.01,shift_0.01sd_flag_rate,shift_0.05sd_flag_rate"]
for n in (1_000, 10_000, 100_000, 1_000_000):
    f0=f1=f5=0
    for s in range(100):
        rng=np.random.default_rng(s)
        a=rng.standard_normal(n)
        f0 += stats.ks_2samp(a, rng.standard_normal(n))[1] < 0.01
        f1 += stats.ks_2samp(a, rng.standard_normal(n)+0.01)[1] < 0.01
        f5 += stats.ks_2samp(a, rng.standard_normal(n)+0.05)[1] < 0.01
    rows.append(f"{n},{f0/100:.2f},{f1/100:.2f},{f5/100:.2f}")
    print(rows[-1],flush=True)
emit("w16m4_ks_falsepos",rows)

# 3. Correlation vs mutual information on a non-linear relationship
from sklearn.feature_selection import mutual_info_regression
rows=["relationship,pearson_r,spearman_rho,mutual_info"]
rng=np.random.default_rng(0); n=5000
x=rng.uniform(-3,3,n)
for name,y in (("linear", 2*x+rng.normal(0,1,n)),
               ("quadratic", x**2+rng.normal(0,1,n)),
               ("sine", np.sin(3*x)+rng.normal(0,0.3,n)),
               ("none", rng.normal(0,1,n))):
    r=stats.pearsonr(x,y)[0]; rho=stats.spearmanr(x,y)[0]
    mi=mutual_info_regression(x.reshape(-1,1), y, random_state=0)[0]
    rows.append(f"{name},{r:+.4f},{rho:+.4f},{mi:.4f}")
    print(rows[-1],flush=True)
emit("w16m4_corr_mi",rows)

# 4. Cost of a profile report vs targeted checks
rows=[]
N=1_000_000
rng=np.random.default_rng(1)
df=pd.DataFrame({f"c{i}": rng.standard_normal(N) for i in range(20)})
df["cat"]=rng.choice(list("abcdefgh"),N)
def targeted():
    return {"rows":len(df), "nulls":df.isna().sum().to_dict(),
            "desc":df.describe().to_dict(), "nunique":df.nunique().to_dict(),
            "corr":df.select_dtypes("number").corr().to_numpy()}
t=time.perf_counter(); targeted(); t1=time.perf_counter()-t
rows.append(f"rows,{N},cols,{df.shape[1]}")
rows.append(f"targeted_checks_seconds,{t1:.2f}")
# correlation alone
t=time.perf_counter(); df.select_dtypes("number").corr(); t2=time.perf_counter()-t
rows.append(f"pearson_corr_matrix_seconds,{t2:.2f}")
t=time.perf_counter(); df.select_dtypes("number").corr(method="spearman"); t3=time.perf_counter()-t
rows.append(f"spearman_corr_matrix_seconds,{t3:.2f},ratio_vs_pearson,{t3/t2:.0f}x")
t=time.perf_counter(); df.nunique(); t4=time.perf_counter()-t
rows.append(f"nunique_all_columns_seconds,{t4:.2f}")
emit("w16m4_cost",rows)
