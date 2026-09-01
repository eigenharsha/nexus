"""The transforms that DO leak catastrophically: target encoding, feature selection,
resampling, and duplicate rows across the split."""
import numpy as np, os, warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.ensemble import RandomForestClassifier
OUT="/tmp/nexbench/out"
rows=[]

# 1. TARGET ENCODING a high-cardinality categorical, fitted on ALL data
def target_encode_leak(n=2000, card=500, reps=20):
    L=[];O=[]
    for s in range(reps):
        rng=np.random.default_rng(s)
        cat=rng.integers(0,card,n)          # PURE NOISE: category is unrelated to y
        y=rng.integers(0,2,n)
        # LEAKY: encode using the whole dataset's target means
        means=np.zeros(card)
        for c in range(card):
            m=cat==c
            means[c]=y[m].mean() if m.any() else y.mean()
        Xall=means[cat].reshape(-1,1)
        a,b,ya,yb=train_test_split(Xall,y,test_size=0.3,random_state=s,stratify=y)
        m1=LogisticRegression(max_iter=2000).fit(a,ya)
        L.append(roc_auc_score(yb,m1.predict_proba(b)[:,1]))
        # CORRECT: encode using TRAIN target means only
        ia,ib=train_test_split(np.arange(n),test_size=0.3,random_state=s,stratify=y)
        gm=y[ia].mean(); tm=np.full(card,gm)
        for c in range(card):
            m=(cat[ia]==c)
            if m.any(): tm[c]=y[ia][m].mean()
        m2=LogisticRegression(max_iter=2000).fit(tm[cat[ia]].reshape(-1,1),y[ia])
        O.append(roc_auc_score(y[ib],m2.predict_proba(tm[cat[ib]].reshape(-1,1))[:,1]))
    return np.mean(L),np.mean(O)
l,o=target_encode_leak()
rows += ["experiment_1: target encoding a 500-level categorical that is PURE NOISE",
         "  true AUC is 0.500 (the feature carries no information)",
         f"  leaky_encode_on_all_data_AUC,{l:.4f}",
         f"  correct_encode_on_train_only_AUC,{o:.4f}",
         f"  inflation_auc,{l-o:+.4f}"]

# 2. FEATURE SELECTION before CV, sweeping the feature count
rows += ["", "experiment_2: SelectKBest(k=20) on pure noise, before vs inside CV",
         "  true accuracy is 0.500",
         "  n_features,leaky_cv_acc,correct_cv_acc,inflation"]
for p in (200, 1000, 5000, 20000):
    L=[];O=[]
    for s in range(5):
        rng=np.random.default_rng(s)
        X=rng.standard_normal((200,p)); y=rng.integers(0,2,200)
        sel=SelectKBest(f_classif,k=20).fit(X,y)
        L.append(cross_val_score(LogisticRegression(max_iter=2000), sel.transform(X), y,
                 cv=KFold(5,shuffle=True,random_state=0)).mean())
        O.append(cross_val_score(Pipeline([("s",SelectKBest(f_classif,k=20)),
                 ("c",LogisticRegression(max_iter=2000))]), X, y,
                 cv=KFold(5,shuffle=True,random_state=0)).mean())
    rows.append(f"  {p},{np.mean(L):.4f},{np.mean(O):.4f},{np.mean(L)-np.mean(O):+.4f}")
    print(rows[-1],flush=True)

# 3. DUPLICATE ROWS spanning the split (the leak nobody looks for)
rows += ["", "experiment_3: 30% duplicated rows, split randomly (duplicates land on both sides)",
         "  n_dup_pct,leaky_random_split_AUC,correct_group_split_AUC,inflation"]
for dup in (0.0, 0.10, 0.30, 0.50):
    L=[];O=[]
    for s in range(10):
        rng=np.random.default_rng(s)
        n=1500
        X=rng.standard_normal((n,10)); y=(X[:,0]+rng.standard_normal(n)*1.5>0).astype(int)
        k=int(n*dup)
        idx=rng.integers(0,n,k)
        Xd=np.vstack([X,X[idx]]); yd=np.concatenate([y,y[idx]])
        gid=np.concatenate([np.arange(n),idx])          # true identity of each row
        a,b,ya,yb=train_test_split(Xd,yd,test_size=0.3,random_state=s,stratify=yd)
        m=RandomForestClassifier(n_estimators=100,random_state=0).fit(a,ya)
        L.append(roc_auc_score(yb,m.predict_proba(b)[:,1]))
        from sklearn.model_selection import GroupShuffleSplit
        tr,te=next(GroupShuffleSplit(n_splits=1,test_size=0.3,random_state=s).split(Xd,yd,gid))
        m2=RandomForestClassifier(n_estimators=100,random_state=0).fit(Xd[tr],yd[tr])
        O.append(roc_auc_score(yd[te],m2.predict_proba(Xd[te])[:,1]))
    rows.append(f"  {dup:.0%},{np.mean(L):.4f},{np.mean(O):.4f},{np.mean(L)-np.mean(O):+.4f}")
    print(rows[-1],flush=True)

open(os.path.join(OUT,"w16m3_leak_target.txt"),"w").write("\n".join(rows)+"\n")
print("\n".join(rows[:6]))
