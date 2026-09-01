"""dlt 1.4.1 + duckdb 1.1.3: force three upstream schema changes and record what happens."""
import os, shutil, json, warnings
warnings.filterwarnings("ignore")
os.environ["DLT_DATA_DIR"]="/tmp/nexbench/dltdata"
WORK="/tmp/nexbench/dltwork"
shutil.rmtree(WORK, ignore_errors=True); os.makedirs(WORK, exist_ok=True)
shutil.rmtree("/tmp/nexbench/dltdata", ignore_errors=True)
os.chdir(WORK)
import dlt, duckdb

DB=os.path.join(WORK,"warehouse.duckdb")

def cols(con, table):
    try:
        r=con.execute(f"SELECT column_name, data_type FROM information_schema.columns "
                      f"WHERE table_schema='shop' AND table_name='{table}' ORDER BY ordinal_position").fetchall()
        return [(a,b) for a,b in r if not a.startswith("_dlt")]
    except Exception as e:
        return [("ERR",str(e))]

def run(name, data, write_disposition="merge", primary_key="id"):
    p = dlt.pipeline(pipeline_name="shop", destination=dlt.destinations.duckdb(DB), dataset_name="shop")
    info = p.run(data, table_name="orders", write_disposition=write_disposition, primary_key=primary_key)
    return p

OUT=[]
def snap(label):
    con=duckdb.connect(DB, read_only=True)
    c=cols(con,"orders")
    rows=con.execute("SELECT * FROM shop.orders ORDER BY id").fetchall()
    names=[x[0] for x in c]
    OUT.append(f"### {label}")
    OUT.append("columns: " + ", ".join(f"{n}:{t}" for n,t in c))
    con2=duckdb.connect(DB, read_only=True)
    sel=", ".join(f'"{n}"' for n,_ in c)
    r=con2.execute(f"SELECT {sel} FROM shop.orders ORDER BY id").fetchall()
    for row in r:
        OUT.append("  " + " | ".join(f"{n}={v!r}" for (n,_),v in zip(c,row)))
    con.close(); con2.close()

# RUN 1 — baseline
run("v1", [
    {"id":1,"customer":"ann","amount":10.0},
    {"id":2,"customer":"bob","amount":20.0},
])
snap("RUN 1 — baseline: id, customer, amount")

# RUN 2 — NEW FIELD appears upstream
run("v2", [
    {"id":2,"customer":"bob","amount":20.0,"currency":"EUR"},
    {"id":3,"customer":"cy","amount":30.0,"currency":"USD"},
])
snap("RUN 2 — NEW FIELD 'currency' appears upstream")

# RUN 3 — TYPE CHANGE: amount arrives as a string
run("v3", [
    {"id":4,"customer":"dee","amount":"40.50","currency":"GBP"},
])
snap("RUN 3 — TYPE CHANGE: amount arrives as text '40.50'")

# RUN 4 — FIELD REMOVED upstream
run("v4", [
    {"id":5,"customer":"ed"},
])
snap("RUN 4 — FIELDS REMOVED: amount and currency absent")

# RUN 5 — schema contract: freeze
OUT.append("### RUN 5 — schema_contract='freeze', then a new field arrives")
try:
    p = dlt.pipeline(pipeline_name="shop", destination=dlt.destinations.duckdb(DB), dataset_name="shop")
    p.run([{"id":6,"customer":"fay","amount":60.0,"loyalty_tier":"gold"}],
          table_name="orders", write_disposition="merge", primary_key="id",
          schema_contract={"tables":"evolve","columns":"freeze","data_type":"freeze"})
    OUT.append("  NO ERROR RAISED (unexpected)")
except Exception as e:
    OUT.append(f"  RAISED: {type(e).__name__}")
    OUT.append(f"  message: {str(e)[:300]}")
snap("after freeze attempt")

# RUN 6 — discard
OUT.append("### RUN 6 — schema_contract columns='discard_value'")
try:
    p = dlt.pipeline(pipeline_name="shop", destination=dlt.destinations.duckdb(DB), dataset_name="shop")
    p.run([{"id":7,"customer":"gus","amount":70.0,"loyalty_tier":"silver"}],
          table_name="orders", write_disposition="merge", primary_key="id",
          schema_contract={"tables":"evolve","columns":"discard_value","data_type":"evolve"})
    OUT.append("  loaded, extra column dropped")
except Exception as e:
    OUT.append(f"  RAISED: {type(e).__name__}: {str(e)[:200]}")
snap("after discard_value")

# nested JSON -> child table
OUT.append("### NESTED JSON -> child tables")
p = dlt.pipeline(pipeline_name="nested", destination=dlt.destinations.duckdb(DB), dataset_name="nested")
p.run([{"id":1,"customer":"ann","items":[{"sku":"A1","qty":2},{"sku":"B2","qty":1}]},
       {"id":2,"customer":"bob","items":[{"sku":"C3","qty":5}]}],
      table_name="orders", write_disposition="replace")
con=duckdb.connect(DB, read_only=True)
tabs=con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='nested' ORDER BY 1").fetchall()
OUT.append("tables created: " + ", ".join(t[0] for t in tabs))
for t, in tabs:
    if t.startswith("_dlt"): continue
    c=[x for x in con.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema='nested' AND table_name='{t}' ORDER BY ordinal_position").fetchall()]
    OUT.append(f"  {t}: " + ", ".join(x[0] for x in c))
    r=con.execute(f'SELECT * FROM nested."{t}" LIMIT 4').fetchall()
    for row in r: OUT.append(f"    {row}")
con.close()

open("/tmp/nexbench/out/w15m4_dlt.txt","w").write("\n".join(OUT)+"\n")
print("\n".join(OUT))
