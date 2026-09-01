"""Verified crash-and-resume: a paginated extractor with a persisted watermark."""
import json, os, sqlite3, shutil, time, random, sys

WORK="/tmp/nexbench/resume"; shutil.rmtree(WORK, ignore_errors=True); os.makedirs(WORK)
TOTAL=100_000; PAGE=1_000

class FakeAPI:
    """Cursor-paginated source. 100,000 records, 1,000 per page."""
    def __init__(self): self.calls=0
    def fetch(self, cursor=None, limit=PAGE):
        self.calls+=1
        start=0 if cursor is None else int(cursor)
        rows=[{"id":i,"updated_at":f"2026-01-01T00:{i//60%60:02d}:{i%60:02d}Z","value":i*3}
              for i in range(start, min(start+limit, TOTAL))]
        nxt=str(start+limit) if start+limit < TOTAL else None
        return {"data":rows,"next_cursor":nxt}

class Store:
    def __init__(self, path):
        self.con=sqlite3.connect(path)
        self.con.execute("CREATE TABLE IF NOT EXISTS records(id INTEGER PRIMARY KEY, updated_at TEXT, value INTEGER)")
        self.con.execute("CREATE TABLE IF NOT EXISTS _state(k TEXT PRIMARY KEY, v TEXT)")
        self.con.commit()
    def load_page(self, rows, cursor):
        # ONE transaction: rows and the cursor commit together, or neither does.
        with self.con:
            self.con.executemany("INSERT OR REPLACE INTO records VALUES (?,?,?)",
                                 [(r["id"],r["updated_at"],r["value"]) for r in rows])
            self.con.execute("INSERT OR REPLACE INTO _state VALUES ('cursor',?)",
                             (cursor if cursor is not None else "DONE",))
    def cursor(self):
        r=self.con.execute("SELECT v FROM _state WHERE k='cursor'").fetchone()
        return None if r is None else (None if r[0]=="DONE" else r[0])
    def count(self):
        return self.con.execute("SELECT count(*) FROM records").fetchone()[0]
    def checksum(self):
        return self.con.execute("SELECT sum(value), count(*), min(id), max(id) FROM records").fetchone()

def extract(store, api, crash_after_records=None):
    cursor=store.cursor()
    pulled=0
    while True:
        resp=api.fetch(cursor)
        rows=resp["data"]
        if not rows: break
        store.load_page(rows, resp["next_cursor"])
        pulled+=len(rows)
        cursor=resp["next_cursor"]
        if crash_after_records and store.count()>=crash_after_records:
            raise RuntimeError(f"simulated crash after {store.count()} records")
        if cursor is None: break
    return pulled

OUT=[]
db=os.path.join(WORK,"a.db")
api=FakeAPI(); store=Store(db)
try:
    extract(store, api, crash_after_records=43_000)
except RuntimeError as e:
    OUT.append(f"crash: {e}")
OUT.append(f"after crash: rows={store.count()} saved_cursor={store.cursor()} api_calls={api.calls}")
n=extract(store, api)
OUT.append(f"after resume: rows={store.count()} pulled_on_resume={n} total_api_calls={api.calls}")
OUT.append(f"checksum(sum,count,min,max)={store.checksum()}")

# clean single run, for comparison
db2=os.path.join(WORK,"b.db"); api2=FakeAPI(); store2=Store(db2)
extract(store2, api2)
OUT.append(f"clean run:    rows={store2.count()} api_calls={api2.calls}")
OUT.append(f"checksum(sum,count,min,max)={store2.checksum()}")
OUT.append(f"IDENTICAL RESULT: {store.checksum()==store2.checksum()}")

# run the resumed one AGAIN (idempotency check)
n3=extract(store, api)
OUT.append(f"re-run of a completed pipeline: pulled={n3} rows={store.count()} checksum_unchanged={store.checksum()==store2.checksum()}")
open("/tmp/nexbench/out/w15m2_resume.txt","w").write("\n".join(OUT)+"\n")
print("\n".join(OUT))
