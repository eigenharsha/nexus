import numpy as np, pyarrow as pa, pyarrow.parquet as pq, os, time
rng = np.random.default_rng(42)
N = 10_000_000
t0=time.perf_counter()
merchants = np.array([f"m{i:04d}" for i in range(2000)])
cats = np.array(["groceries","fuel","travel","dining","utilities","electronics","health","subscriptions"])
regions = np.array(["APAC","EMEA","NA","LATAM"])
tbl = pa.table({
    "txn_id": pa.array(np.arange(N, dtype=np.int64)),
    "account_id": pa.array(rng.integers(0, 250_000, N, dtype=np.int32)),
    "merchant": pa.array(merchants[rng.integers(0, len(merchants), N)]),
    "category": pa.array(cats[rng.integers(0, len(cats), N)]),
    "region": pa.array(regions[rng.integers(0, len(regions), N)]),
    "amount": pa.array(np.round(rng.gamma(2.0, 40.0, N), 2)),
    "ts": pa.array((np.datetime64("2024-01-01") + (rng.integers(0, 365*24*60, N)*60).astype("timedelta64[s]")).astype("datetime64[ms]")),
    "is_refund": pa.array(rng.random(N) < 0.03),
})
os.makedirs("/tmp/nexbench/data", exist_ok=True)
pq.write_table(tbl, "/tmp/nexbench/data/txns.parquet", compression="snappy")
print("parquet written", time.perf_counter()-t0, flush=True)
import csv
t1=time.perf_counter()
import pandas as pd
df = tbl.to_pandas()
df.to_csv("/tmp/nexbench/data/txns.csv", index=False)
print("csv written", time.perf_counter()-t1, flush=True)
for f in ("txns.parquet","txns.csv"):
    p=f"/tmp/nexbench/data/{f}"
    print(f, os.path.getsize(p)/1e6, "MB", flush=True)
