import numpy as np, pandas as pd
print("=== MCAR/MAR/MNAR ===")
rng = np.random.default_rng(0)
n = 1000
age = rng.integers(22, 65, n)
income = 20000 + age * 900 + rng.normal(0, 8000, n)
mcar = income.copy(); mcar[rng.random(n) < 0.10] = np.nan
mar = income.copy(); mar[rng.random(n) < (0.30 - age * 0.004)] = np.nan
mnar = income.copy(); mnar[rng.random(n) < (income / income.max() * 0.5)] = np.nan
for name, arr in (("true", income), ("MCAR", mcar), ("MAR", mar), ("MNAR", mnar)):
    print(f"{name:5s} mean of observed: {np.nanmean(arr):9,.0f}")

print("\n=== outliers ===")
x = np.array([12, 15, 14, 13, 16, 15, 14, 250])
q1, q3 = np.percentile(x, [25, 75]); iqr = q3 - q1
print("IQR:", x[(x < q1 - 1.5*iqr) | (x > q3 + 1.5*iqr)])
z = (x - x.mean()) / x.std()
print("zscore>3:", x[np.abs(z) > 3], " max|z| =", round(float(np.abs(z).max()),3))
med = np.median(x); mad = np.median(np.abs(x - med))
print("modified z:", x[np.abs(0.6745 * (x - med) / mad) > 3.5])

print("\n=== imputer ===")
from sklearn.impute import SimpleImputer, MissingIndicator
X = np.array([[1.0, 10.0], [np.nan, 20.0], [3.0, np.nan], [4.0, 40.0]])
print(SimpleImputer(strategy="mean").fit_transform(X))
print(MissingIndicator().fit_transform(X))

print("\n=== isna on the messy frame ===")
df = pd.DataFrame({
    "name":   ["Ann Patel", "BOB SMITH ", "ann patel", "Cy Jones", "Dee Roy"],
    "age":    [34, 28, 34, np.nan, 199],
    "income": [55000, np.nan, 55000, 41000, np.nan],
    "city":   ["Leeds", "leeds", "LEEDS", "York", None],
    "joined": ["2024-01-15", "15/02/2024", "2024-01-15", "2024-03-01", "not a date"],
})
print(df.isna().sum())
print(df.dtypes)
