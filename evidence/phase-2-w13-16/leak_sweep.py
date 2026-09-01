"""Where does imputation leakage ACTUALLY bite? Sweep n, imputer, and scaling."""
import numpy as np, os, warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score
OUT="/tmp/nexbench/out"

def make(n, p, seed, miss_depends_on_y=True):
    rng=np.random.default_rng(seed)
    X=rng.standard_normal((n,p))
    sig=X[:,0]*1.2 - X[:,1]*0.8 + X[:,2]*0.6
    y=(sig + rng.standard_normal(n)*1.0 > 0).astype(int)
    Xm=X.copy()
    for j in range(p):
        base=0.35 if j<p//4 else 0.15
        pm = base + (0.25*y if miss_depends_on_y else 0.0)
        Xm[rng.random(n) < pm, j]=np.nan
    return Xm, y

def run(imputer_factory, n, p, seed):
    Xm,y=make(n,p,seed)
    # LEAKY: fit imputer + scaler on everything
    imp=imputer_factory(); Xf=imp.fit_transform(Xm)
    sc=StandardScaler().fit(Xf); Xf=sc.transform(Xf)
    a,b,ya,yb=train_test_split(Xf,y,test_size=0.3,random_state=seed,stratify=y)
    m=LogisticRegression(max_iter=3000).fit(a,ya)
    leaky=roc_auc_score(yb,m.predict_proba(b)[:,1])
    # CORRECT
    a,b,ya,yb=train_test_split(Xm,y,test_size=0.3,random_state=seed,stratify=y)
    pipe=Pipeline([("i",imputer_factory()),("s",StandardScaler()),
                   ("c",LogisticRegression(max_iter=3000))]).fit(a,ya)
    ok=roc_auc_score(yb,pipe.predict_proba(b)[:,1])
    return leaky, ok

rows=["imputer,n_samples,n_features,leaky_AUC,correct_AUC,inflation,runs"]
for name,fac,ns,p,reps in (
    ("mean",       lambda: SimpleImputer(strategy="mean"), (100,300,1000,5000), 40, 30),
    ("knn_k5",     lambda: KNNImputer(n_neighbors=5),      (100,300,1000),      20, 12),
    ("iterative",  lambda: IterativeImputer(max_iter=5, random_state=0), (100,300), 15, 8),
):
    for n in ns:
        L=[];O=[]
        for s in range(reps):
            l,o=run(fac,n,p,s); L.append(l); O.append(o)
        rows.append(f"{name},{n},{p},{np.mean(L):.4f},{np.mean(O):.4f},"
                    f"{np.mean(L)-np.mean(O):+.4f},{reps}")
        print(rows[-1], flush=True)
open(os.path.join(OUT,"w16m3_leak_sweep.txt"),"w").write("\n".join(rows)+"\n")
