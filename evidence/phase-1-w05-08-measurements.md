# Nexus W5-W8 measurement log
Host: Apple Silicon (11 cores, 18 GB), macOS, load average ~16-25 during runs.
PostgreSQL 16.14 in Docker (shared_buffers=256MB, max_connections=300), Python 3.13, pydantic 2.10.4,
FastAPI 0.115.6, SQLAlchemy 2.0.36, psycopg 3.2.3, Chrome-headless-shell 134, Node 24.19.

## W5 HTTP (curl 8.x, MDN/Wikipedia)
DNS 6.8-24.6 ms; TCP connect +8.5-11.2 ms; TLS +18.6-26 ms; TTFB 45.2 ms; total 71.8 ms / 221,912 B
6 requests fresh connection each: 780 ms (685 ms in an earlier run) | 6 over one keep-alive conn: 204 ms (125 ms) => 3.8-5.5x
12 parallel page fetches: h2 66-93 ms, h1.1 55-103 ms (no measurable multiplexing win at ~20 ms RTT); h2 sequential 109 ms

## W5 DOM (Chrome headless shell 134, 50,000 rows)
innerHTML += per row: 123.6 ms for 1,000 rows (O(n^2)); extrapolated 50k ~309 s
appendChild per row 50k: build 15.2 ms, +layout 230.7 ms
LAYOUT THRASH read offsetHeight each iteration, 5,000 rows: 2,406.3 ms
DocumentFragment 50k: build 36.9 ms, +layout 264.2 ms
one innerHTML assignment 50k: build 17.7 ms, +layout 252.8 ms
virtualized 30 of 50,000: build 0.1 ms, +layout 0.3 ms  => 843x vs full render

## W5 CSS layout (5,000 items)
flexbox wrap 80.2 ms | grid 20.5 ms | float 18.2 ms
relayout after 1 child resize: flex 2.8 ms, grid 3.3 ms, contain:strict 2.3 ms
inline style write to 5,000 children + forced layout: 12.3 ms

## W5 JS event loop (node 24.19)
order: 1 sync start, 2 async body, 3 sync end, 4 queueMicrotask, 5 promise.then, 6 after await, 7 setTimeout 0
puzzle2: A-sync -> MAIN -> P1 -> A-after-await -> P2 -> T1 -> T1-micro -> T2
sequential awaits (100+120+90) 315 ms | Promise.all 122 ms | allSettled 102 ms | race 93 ms | AbortController fires at 51 ms

## W6 FastAPI (uvicorn 0.34, 1 worker, ab -k, 50 ms I/O)
/ping no I/O c=50: 3,536 rps, p50 9 ms
async def + await asyncio.sleep(50ms) c=50: 470 rps p50 58 ms p95 263 ms
async def + blocking time.sleep(50ms) c=50: 16.9 rps p50 2,873 ms  => 27.8x collapse
def (threadpool) c=50: 538 rps p50 68 ms p95 112 ms
c=100: async 1,224 rps / sync-def 587 rps ; c=200: async 2,565 rps p50 59 ms / sync-def 655 rps p50 279 ms (3.9x)

## W6 Pydantic 2.10.4 / pydantic-core 2.27.2 (20k iters x 12 interleaved reps, min)
model_validate(dict) 2.70 us (369,901/s) | model_validate_json 2.74 us (364,803/s)
json.loads + model_validate 5.10 us (196,035/s) | json.loads alone 1.93 us
model_construct 2.46 us | model_dump 1.48 us | model_dump_json 1.29 us | failing payload (3 errors) 2.73 us
100k payloads = 270 ms single core. 3 errors reported in one pass.

## W6 auth
argon2id default (t=3,m=64MiB,p=4) hash 65.5 ms median, verify 51.4 ms
bcrypt cost=10 79.3 ms | cost=12 245.6 ms | cost=14 1,237.7 ms | cost=12 verify 261.1 ms
JWT HS256 sign 10.5 us (95,613/s), verify 13.2 us (75,550/s), token 149 chars
bcrypt 72-byte truncation confirmed: checkpw("A"*72+"different", hash("A"*72)) == True

## W7 dataset: 200k customers, 20k products, 1M orders, 3M order_items (orders heap 69 MB, total 90 MB)
### load
100k single-row INSERT autocommit: 83,773 ms (1,194 rows/s)
same 100k in ONE transaction: 23,227 ms (4,306 rows/s) = 3.6x
COPY 100k: 295-508 ms (196,000-339,000 rows/s) = 165-284x vs autocommit
### joins
nested loop (55 rows): 9.5 ms | parallel hash join (200k x 40k): 1,148 ms cold / merge join forced 742 ms
EXISTS: 210 ms and IN: 171 ms produce the IDENTICAL plan (Parallel Hash Semi Join); count(DISTINCT)+JOIN 237 ms
fan-out bug: 5,002 orders -> 15,000 rows after joining order_items; SUM 507,507,500 -> 1,522,492,500 (3.0x inflation)
### analytics
top-3-per-category window function: 330 ms ; equivalent correlated subquery CANCELLED after 5 min 07 s
cohort retention matrix on 749,741 orders/150,000 customers: 2,328 ms; m1 63-67%, m2 47-50%, m3 38-39%, m6 17-18%
running total + 3-month MA: 85.7 ms | dedup ROW_NUMBER 9,997 -> 1,999: 3.8 ms
ROWS vs RANGE on (1,1,2,3,3,4): ROWS gives 1,2,3,5,6,7 ; RANGE gives 2,2,4,8,8,10
sort avoidance: ORDER BY placed_at with composite index 0.139 ms (no Sort node) vs ORDER BY total_cents 0.084 ms with quicksort 25 kB
### MVCC / vacuum
200k rows x 200-byte payload = 48 MB; after 5 full-table UPDATEs = 284 MB, 999,959 dead tuples
VACUUM: still 284 MB (space reusable, file not shrunk); VACUUM FULL: 47 MB

## W8 indexing (1M-row orders)
point lookup customer_id: parallel seq scan 64.9-86.8 ms warm (8,772 buffers) -> index scan 0.033-0.046 ms = ~1,970x
index build 629 ms, index size 11 MB on a 69 MB heap
composite (customer_id, placed_at DESC): 0.512 ms; same index, query on placed_at only -> seq scan 116.6 ms (no leftmost prefix)
index-only scan (Heap Fetches: 0) 505 rows: 0.439 ms
partial index WHERE deleted_at IS NULL: 6,704 kB vs full 6,840 kB; query 106.2 ms -> 94.4 ms index-only
expression index on lower(email): 193.9 ms seq scan -> 1.878 ms
98% of rows: seq scan 116.1 ms vs forced index-only scan 375.6 ms => seq scan 3.2x faster
write amplification: 50k INSERTs 788.9 ms with 0 indexes -> 1,591.8 ms with 5 indexes (2.02x); index bytes 13 MB > heap 8.2 MB

## W8 concurrency (200 buyers, 10 units, psycopg threads)
naive read-modify-write RC: sold 200, oversell 190, 6,614 ms, 30.2 tps
pessimistic FOR UPDATE:     sold 10, 5,882 ms, 34.0 tps, p95 2,374 ms
atomic conditional UPDATE:  sold 10, 6,495 ms, 30.8 tps, p95 2,259 ms
optimistic version+retry:   sold 10, 9,227 ms, 21.7 tps, p95 5,563 ms, 515 retries
SERIALIZABLE + retry:       sold 10, 4,434 ms, 45.1 tps, p95 1,404 ms, 944 retries

## W8 sustained throughput (50 workers, 2,000 txns)
                       1 hot row      10 rows        100 rows
RC atomic UPDATE       170.2 tps      759.5 tps      1,019.5 tps
RC SELECT FOR UPDATE   108.4 tps      543.9 tps        683.5 tps
SERIALIZABLE + retry    60.7 tps       67.2 tps        190.4 tps
retries (SSI)           27,261         27,124          7,482
=> SERIALIZABLE is 2.8x / 11.3x / 5.4x slower than RC atomic at these contention levels

## W8 anomalies (two psql sessions, verbatim transcripts captured)
non-repeatable read RC: 10 then 7 inside one transaction
repeatable read: 10 then 10; write -> ERROR: could not serialize access due to concurrent update
lost update RC: both read 10, both write 9, final 9 (two sales, one unit gone)
FOR UPDATE: B blocks, re-reads 9 after A commits, final 8
phantom RC: 9,372 -> 9,373 ; RR: 9,373 -> 9,373
write skew RR: both doctors go off call (alice f, bob f)
SERIALIZABLE: B fails on COMMIT - "could not serialize access due to read/write dependencies among transactions,
  Reason code: Canceled on identification as a pivot, during commit attempt."
deadlock: "Process 741 waits for ShareLock on transaction 200858; blocked by process 740..." detected after deadlock_timeout (1 s)

## W8 SQLAlchemy 2.0.36 (500 customers, 2,502 orders)
lazy load N+1:            501 queries, 1,321.5 ms
selectinload:               2 queries,    61.6 ms  (21x)
joinedload:                 1 query,      44.2 ms  (30x)
aggregate pushed to SQL:    1 query,      11.2 ms  (118x)
bulk insert 100k: ORM add_all 5,448 ms (18,357/s) | ORM insert() dicts 2,255 ms (44,338/s)
                  Core executemany 2,513 ms (39,799/s) | psycopg COPY 518 ms (193,123/s)
pool: size=2 timeout=1s -> 8/40 ok, 32 TimeoutError; size=5 -> 20/40 ok; size=5+10 overflow 1,150 ms; size=20+10 700 ms

## W8 cache
no cache, 40 sequential: 2,510 ms (62.8 ms/query, 15.9 rps)
cache-aside 4 keys:        692 ms, 90% hit rate, 57.8 rps
stampede 40 cold threads: 40 DB calls, 1,784 ms
single-flight coalescing:  1 DB call,    85 ms (21x faster, 40x fewer DB calls)
