import numpy as np
rng = np.random.default_rng(0)
n = 1000
age = rng.integers(22, 65, n)
income = 20000 + age * 900 + rng.normal(0, 8000, n)
mcar = income.copy(); mcar[rng.random(n) < 0.10] = np.nan
mar  = income.copy(); mar[rng.random(n) < np.clip(1.2 - age * 0.025, 0, 1)] = np.nan
pct  = (income - income.min()) / (income.max() - income.min())
mnar = income.copy(); mnar[rng.random(n) < pct**2] = np.nan
for name, arr in (("true", income), ("MCAR", mcar), ("MAR", mar), ("MNAR", mnar)):
    miss = np.isnan(arr).mean()
    print(f"{name:5s} mean of observed: {np.nanmean(arr):9,.0f}   ({miss:.0%} missing)")
