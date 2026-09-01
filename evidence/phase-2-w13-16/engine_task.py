"""One (engine, query) measurement in its own process, so peak RSS is honest.
Usage: engine_task.py <engine> <query>   -> prints  seconds,peak_rss_MB,result_rows
Engines: pandas | polars | polars_lazy | duckdb
Queries: groupby | filter_agg | join | sort_topk | read_only
"""
import sys, time, resource, os
PARQ="/tmp/nexbench/data/txns.parquet"
DIMS="/tmp/nexbench/data/merchants.parquet"
engine, query = sys.argv[1], sys.argv[2]
t0=time.perf_counter()
rows=0

if engine=="pandas":
    import pandas as pd
    if query=="read_only":
        df=pd.read_parquet(PARQ); rows=len(df)
    elif query=="groupby":
        df=pd.read_parquet(PARQ, columns=["category","region","amount"])
        r=(df.groupby(["category","region"], observed=True)["amount"]
             .agg(["sum","mean","count"]).reset_index()); rows=len(r)
    elif query=="filter_agg":
        df=pd.read_parquet(PARQ, columns=["category","amount","is_refund"])
        r=(df[(df.amount>150)&(~df.is_refund)].groupby("category")["amount"].sum()); rows=len(r)
    elif query=="join":
        df=pd.read_parquet(PARQ, columns=["merchant","amount"])
        d=pd.read_parquet(DIMS)
        r=(df.merge(d,on="merchant",how="left",validate="many_to_one")
             .groupby("mcc")["amount"].sum()); rows=len(r)
    elif query=="sort_topk":
        df=pd.read_parquet(PARQ, columns=["account_id","amount"])
        r=df.nlargest(100,"amount"); rows=len(r)

elif engine=="polars":
    import polars as pl
    if query=="read_only":
        df=pl.read_parquet(PARQ); rows=df.height
    elif query=="groupby":
        df=pl.read_parquet(PARQ, columns=["category","region","amount"])
        r=df.group_by(["category","region"]).agg(
            pl.col("amount").sum().alias("s"), pl.col("amount").mean().alias("m"),
            pl.len().alias("n")); rows=r.height
    elif query=="filter_agg":
        df=pl.read_parquet(PARQ, columns=["category","amount","is_refund"])
        r=(df.filter((pl.col("amount")>150)&(~pl.col("is_refund")))
             .group_by("category").agg(pl.col("amount").sum())); rows=r.height
    elif query=="join":
        df=pl.read_parquet(PARQ, columns=["merchant","amount"])
        d=pl.read_parquet(DIMS)
        r=df.join(d,on="merchant",how="left").group_by("mcc").agg(pl.col("amount").sum()); rows=r.height
    elif query=="sort_topk":
        df=pl.read_parquet(PARQ, columns=["account_id","amount"])
        r=df.top_k(100, by="amount"); rows=r.height

elif engine=="polars_lazy":
    import polars as pl
    lf=pl.scan_parquet(PARQ)
    if query=="read_only":
        rows=lf.select(pl.len()).collect().item()
    elif query=="groupby":
        r=(lf.group_by(["category","region"]).agg(
            pl.col("amount").sum().alias("s"), pl.col("amount").mean().alias("m"),
            pl.len().alias("n")).collect()); rows=r.height
    elif query=="filter_agg":
        r=(lf.filter((pl.col("amount")>150)&(~pl.col("is_refund")))
             .group_by("category").agg(pl.col("amount").sum()).collect()); rows=r.height
    elif query=="join":
        d=pl.scan_parquet(DIMS)
        r=lf.join(d,on="merchant",how="left").group_by("mcc").agg(pl.col("amount").sum()).collect(); rows=r.height
    elif query=="sort_topk":
        r=lf.top_k(100, by="amount").collect(); rows=r.height

elif engine=="duckdb":
    import duckdb
    con=duckdb.connect()
    Q={
     "read_only": f"SELECT count(*) FROM '{PARQ}'",
     "groupby":   f"SELECT category, region, sum(amount) s, avg(amount) m, count(*) n FROM '{PARQ}' GROUP BY 1,2",
     "filter_agg":f"SELECT category, sum(amount) FROM '{PARQ}' WHERE amount>150 AND NOT is_refund GROUP BY 1",
     "join":      f"SELECT d.mcc, sum(t.amount) FROM '{PARQ}' t LEFT JOIN '{DIMS}' d USING (merchant) GROUP BY 1",
     "sort_topk": f"SELECT account_id, amount FROM '{PARQ}' ORDER BY amount DESC LIMIT 100",
    }[query]
    rows=len(con.execute(Q).fetchall())

el=time.perf_counter()-t0
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# macOS reports bytes, Linux reports KB
mb = rss/1e6 if sys.platform=="darwin" else rss/1e3
print(f"{el:.3f},{mb:.1f},{rows}")
