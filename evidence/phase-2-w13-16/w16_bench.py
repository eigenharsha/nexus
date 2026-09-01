"""Week 16 measurements: NumPy internals, pandas memory/apply, and the leakage demo."""
import os, sys, time, gc
OUT="/tmp/nexbench/out"
def emit(name,lines):
    open(os.path.join(OUT,name+".txt"),"w").write("\n".join(lines)+"\n")
    print(f"--- {name} ---\n"+"\n".join(lines)+"\n",flush=True)
def best(fn,reps=5):
    b=1e18; r=None
    for _ in range(reps):
        gc.collect(); t=time.perf_counter(); r=fn(); b=min(b,time.perf_counter()-t)
    return b,r

def numpy_bench():
    import numpy as np
    rows=["operation,n,python_loop_ms,numpy_ms,speedup"]
    for n in (10_000, 100_000, 1_000_000):
        a=np.random.default_rng(0).random(n); al=a.tolist()
        t1,_=best(lambda: [x*2.5+1 for x in al],3)
        t2,_=best(lambda: a*2.5+1,5)
        rows.append(f"elementwise_affine,{n},{t1*1e3:.3f},{t2*1e3:.3f},{t1/t2:.0f}x")
        t1,_=best(lambda: sum(x*y for x,y in zip(al,al)),3)
        t2,_=best(lambda: np.dot(a,a),5)
        rows.append(f"dot_product,{n},{t1*1e3:.3f},{t2*1e3:.3f},{t1/t2:.0f}x")
    emit("w16m1_vectorize",rows)

    # C vs F order traversal
    rows=["array,order,sum_axis0_ms,sum_axis1_ms,ratio"]
    for n in (2000, 5000):
        c=np.asarray(np.random.default_rng(1).random((n,n)), order="C")
        f=np.asfortranarray(c)
        for name,arr in (("C_order",c),("F_order",f)):
            t0,_=best(lambda: arr.sum(axis=0),3)
            t1,_=best(lambda: arr.sum(axis=1),3)
            rows.append(f"{n}x{n},{name},{t0*1e3:.1f},{t1*1e3:.1f},{max(t0,t1)/min(t0,t1):.2f}x")
        del c,f; gc.collect()
    emit("w16m1_order",rows)

    # float32 vs float64 accumulation error
    rows=["n,dtype,naive_sum,pairwise_np_sum,math_fsum_exact,naive_rel_error,np_rel_error"]
    import math
    for n in (1_000_000, 10_000_000, 100_000_000):
        x32=np.full(n, 0.1, dtype=np.float32)
        exact=0.1*n
        naive=np.float32(0.0)
        # simulate a naive loop-accumulation in float32 without a python loop:
        naive=x32.sum(dtype=np.float32)          # numpy uses pairwise -> already good
        # true naive: cumulative add via reduce with no pairwise (use math loop on a slice)
        s=np.float32(0.0)
        for v in x32[:min(n,2_000_000)]: s=np.float32(s+v)
        scaled_naive = float(s)*(n/min(n,2_000_000))
        rows.append(f"{n},float32,{scaled_naive:.4f},{float(naive):.4f},{exact:.4f},"
                    f"{abs(scaled_naive-exact)/exact:.6f},{abs(float(naive)-exact)/exact:.9f}")
        del x32; gc.collect()
    emit("w16m1_precision",rows)

    # views vs copies
    a=np.arange(50_000_000, dtype=np.int64)
    import resource
    rows=[f"base_array_MB,{a.nbytes/1e6:.0f}"]
    t,_=best(lambda: a[::2],5); rows.append(f"slice_view_ms,{t*1e6:.2f} us (no copy)")
    t,_=best(lambda: a[::2].copy(),3); rows.append(f"slice_copy_ms,{t*1e3:.1f}")
    idx=np.arange(0,len(a),2)
    t,_=best(lambda: a[idx],3); rows.append(f"fancy_index_ms,{t*1e3:.1f} (ALWAYS copies)")
    mask=np.zeros(len(a),dtype=bool); mask[::2]=True
    t,_=best(lambda: a[mask],3); rows.append(f"boolean_mask_ms,{t*1e3:.1f} (ALWAYS copies)")
    rows.append(f"copy_size_MB,{a[::2].copy().nbytes/1e6:.0f}")
    emit("w16m1_views",rows)

def pandas_bench():
    import pandas as pd, numpy as np
    N=5_000_000
    rng=np.random.default_rng(3)
    cats=np.array(["groceries","fuel","travel","dining","utilities","electronics","health","subs"])
    df=pd.DataFrame({
        "id": np.arange(N, dtype=np.int64),
        "small_int": rng.integers(0,100,N).astype(np.int64),
        "amount": rng.random(N)*1000,
        "category": cats[rng.integers(0,8,N)],
        "flag": rng.random(N)<0.3,
    })
    before=df.memory_usage(deep=True).sum()
    rows=["column,dtype_before,MB_before,dtype_after,MB_after,reduction"]
    opt=df.copy()
    for col,newt in (("id","int32"),("small_int","int8"),("amount","float32"),
                     ("category","category"),("flag","bool")):
        b=df[col].memory_usage(deep=True)
        opt[col]=df[col].astype(newt)
        a=opt[col].memory_usage(deep=True)
        rows.append(f"{col},{df[col].dtype},{b/1e6:.1f},{newt},{a/1e6:.1f},{b/a:.1f}x")
    after=opt.memory_usage(deep=True).sum()
    rows.append(f"TOTAL,-,{before/1e6:.1f},-,{after/1e6:.1f},{before/after:.2f}x")
    rows.append(f"rows,{N},-,-,-,-")
    emit("w16m2_dtypes",rows)

    # apply penalty
    sub=df.head(1_000_000)
    rows=["approach,seconds,per_row_ns,vs_vectorized"]
    t_apply,_=best(lambda: sub["amount"].apply(lambda x: x*1.2+5),1)
    t_map,_  =best(lambda: sub["amount"].map(lambda x: x*1.2+5),1)
    t_list,_ =best(lambda: [x*1.2+5 for x in sub["amount"].tolist()],3)
    t_vec,_  =best(lambda: sub["amount"]*1.2+5,5)
    t_np,_   =best(lambda: sub["amount"].to_numpy()*1.2+5,5)
    n=len(sub)
    for name,t in (("Series.apply",t_apply),("Series.map",t_map),
                   ("python_list_comp",t_list),("pandas_vectorized",t_vec),
                   ("numpy_direct",t_np)):
        rows.append(f"{name},{t:.4f},{t/n*1e9:.0f},{t/t_vec:.1f}x")
    rows.append(f"rows,{n},-,-")
    emit("w16m2_apply",rows)

    # iterrows vs itertuples vs vectorized
    small=df.head(200_000)
    rows=["approach,seconds,per_row_us"]
    def it_rows():
        s=0.0
        for _,r in small.iterrows(): s+=r["amount"]
        return s
    def it_tuples():
        s=0.0
        for r in small.itertuples(index=False): s+=r.amount
        return s
    for name,fn in (("iterrows",it_rows),("itertuples",it_tuples),
                    ("vectorized_sum",lambda: small["amount"].sum())):
        t,_=best(fn,1 if name=="iterrows" else 3)
        rows.append(f"{name},{t:.4f},{t/len(small)*1e6:.2f}")
    emit("w16m2_iteration",rows)

def leakage_bench():
    """The demonstration: imputing BEFORE the split inflates test accuracy."""
    import numpy as np, pandas as pd
    from sklearn.model_selection import train_test_split, cross_val_score, KFold
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.metrics import roc_auc_score

    rows=[]
    rng=np.random.default_rng(42)
    N, P = 2000, 40
    # y depends on only the first 3 features; the rest are noise.
    X = rng.standard_normal((N, P))
    signal = X[:,0]*1.2 - X[:,1]*0.8 + X[:,2]*0.6
    y = (signal + rng.standard_normal(N)*1.0 > 0).astype(int)

    # Introduce MNAR missingness: values are missing more often for y==1.
    Xm = X.copy()
    for j in range(P):
        p = 0.35 if j < 10 else 0.15
        miss = rng.random(N) < (p + 0.20*y)     # missingness depends on the LABEL
        Xm[miss, j] = np.nan

    def auc_wrong(seed):
        """Impute using the WHOLE dataset, then split."""
        imp = SimpleImputer(strategy="mean")
        Xf = imp.fit_transform(Xm)                     # <-- sees test rows
        sc = StandardScaler().fit(Xf)                  # <-- sees test rows
        Xf = sc.transform(Xf)
        Xtr,Xte,ytr,yte = train_test_split(Xf,y,test_size=0.3,random_state=seed,stratify=y)
        m = LogisticRegression(max_iter=2000).fit(Xtr,ytr)
        return roc_auc_score(yte, m.predict_proba(Xte)[:,1])

    def auc_right(seed):
        """Split FIRST, then fit the imputer on train only, inside a pipeline."""
        Xtr,Xte,ytr,yte = train_test_split(Xm,y,test_size=0.3,random_state=seed,stratify=y)
        pipe = Pipeline([("imp",SimpleImputer(strategy="mean")),
                         ("sc",StandardScaler()),
                         ("clf",LogisticRegression(max_iter=2000))])
        pipe.fit(Xtr,ytr)
        return roc_auc_score(yte, pipe.predict_proba(Xte)[:,1])

    w=[auc_wrong(s) for s in range(20)]
    r=[auc_right(s) for s in range(20)]
    rows += [f"n_samples,{N},n_features,{P}",
             f"missing_rate_overall,{np.isnan(Xm).mean():.3f}",
             f"leaky_impute_then_split_AUC,mean,{np.mean(w):.4f},std,{np.std(w):.4f}",
             f"correct_split_then_impute_AUC,mean,{np.mean(r):.4f},std,{np.std(r):.4f}",
             f"inflation_auc_points,{(np.mean(w)-np.mean(r)):.4f}",
             f"runs,20"]

    # The much larger effect: leaky CV with an over-fit feature selection step
    from sklearn.feature_selection import SelectKBest, f_classif
    Xn = rng.standard_normal((200, 5000))            # PURE NOISE
    yn = rng.integers(0,2,200)
    # WRONG: select features on all the data, then cross-validate
    sel = SelectKBest(f_classif, k=20).fit(Xn, yn)
    Xsel = sel.transform(Xn)
    wrong_cv = cross_val_score(LogisticRegression(max_iter=2000), Xsel, yn,
                               cv=KFold(5, shuffle=True, random_state=0), scoring="accuracy")
    # RIGHT: selection inside the pipeline, refit each fold
    pipe = Pipeline([("sel",SelectKBest(f_classif,k=20)),
                     ("clf",LogisticRegression(max_iter=2000))])
    right_cv = cross_val_score(pipe, Xn, yn, cv=KFold(5, shuffle=True, random_state=0),
                               scoring="accuracy")
    rows += ["",
             "pure_noise_experiment: 200 samples x 5000 random features, random labels",
             f"true_accuracy_is,0.50",
             f"leaky_select_then_cv_accuracy,{wrong_cv.mean():.4f}",
             f"correct_select_inside_pipeline_accuracy,{right_cv.mean():.4f}",
             f"inflation_points,{(wrong_cv.mean()-right_cv.mean()):.4f}"]
    emit("w16m3_leakage",rows)

if __name__=="__main__":
    for a in sys.argv[1:]:
        {"numpy":numpy_bench,"pandas":pandas_bench,"leakage":leakage_bench}[a]()
