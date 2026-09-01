import numpy as np, pyarrow as pa, pyarrow.parquet as pq
rng=np.random.default_rng(1)
merchants=np.array([f"m{i:04d}" for i in range(2000)])
mccs=np.array(["5411","5541","4722","5812","4900","5732","8011","5968"])
t=pa.table({"merchant":pa.array(merchants),
            "mcc":pa.array(mccs[rng.integers(0,len(mccs),len(merchants))]),
            "merchant_name":pa.array([f"Merchant {i}" for i in range(2000)])})
pq.write_table(t,"/tmp/nexbench/data/merchants.parquet")
print("dims written", t.num_rows)
