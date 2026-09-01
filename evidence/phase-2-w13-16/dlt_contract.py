"""Isolate each schema-contract mode in a clean pipeline (a failed package is retried otherwise)."""
import os, shutil, warnings
warnings.filterwarnings("ignore")
OUT=[]
def trial(mode_cols, mode_types, label, payload):
    work=f"/tmp/nexbench/dltc_{label}"
    shutil.rmtree(work, ignore_errors=True); os.makedirs(work)
    os.environ["DLT_DATA_DIR"]=work+"/state"
    os.chdir(work)
    import importlib, dlt, duckdb
    db=os.path.join(work,"warehouse.duckdb")
    p=dlt.pipeline(pipeline_name=f"t_{label}", destination=dlt.destinations.duckdb(db), dataset_name="shop")
    p.run([{"id":1,"customer":"ann","amount":10.0}], table_name="orders",
          write_disposition="merge", primary_key="id")
    OUT.append(f"### contract columns={mode_cols!r} data_type={mode_types!r}")
    try:
        p.run(payload, table_name="orders", write_disposition="merge", primary_key="id",
              schema_contract={"tables":"evolve","columns":mode_cols,"data_type":mode_types})
        OUT.append("  outcome: LOADED without error")
    except Exception as e:
        root=e
        while root.__cause__ is not None: root=root.__cause__
        OUT.append(f"  outcome: RAISED {type(e).__name__} -> root cause {type(root).__name__}")
        OUT.append(f"  message: {str(root)[:220]}")
    con=duckdb.connect(db, read_only=True)
    c=[x for x in con.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='shop' AND table_name='orders' ORDER BY ordinal_position").fetchall() if not x[0].startswith("_dlt")]
    names=[x[0] for x in c]
    OUT.append("  columns now: " + ", ".join(names))
    sel=", ".join(f'"{n}"' for n in names)
    for row in con.execute(f"SELECT {sel} FROM shop.orders ORDER BY id").fetchall():
        OUT.append("    " + " | ".join(f"{n}={v!r}" for n,v in zip(names,row)))
    con.close()

NEW_COL=[{"id":2,"customer":"bob","amount":20.0,"loyalty_tier":"gold"}]
for cm in ("evolve","freeze","discard_value","discard_row"):
    trial(cm,"evolve",f"col_{cm}", NEW_COL)

open("/tmp/nexbench/out/w15m4_contracts.txt","w").write("\n".join(OUT)+"\n")
print("\n".join(OUT))
