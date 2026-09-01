# LAB-P2-W13 — `pycollections`: structures from scratch + benchmark harness

> Week 13 · Phase 2 · Systems & Data · time box: **10-12 h**
> Language: python · `make verify` grades you · no instructor required

> **Status: verified.** `starter/`, `solution/` and the test suite are complete and were
> actually run to produce the output in *Verify* below. `make contract` passes on all three
> tracks: green on `solution/`, red on `starter/`.

## The ticket

A service is burning 60% of its CPU in a hot loop doing `if key in some_list`. The fix is
obvious and someone will make it this afternoon.

What is not obvious — and what this team keeps getting wrong in design reviews — is when the
obvious fix is the wrong one: when the list of 8 items beats the dict, when open addressing beats
chaining and when it collapses, and why the "O(1)" structure got slower after we raised the load
factor. Build them from scratch, benchmark them honestly, and write down where Big-O stops
predicting the answer.

## What "done" looks like

- Both hash-table strategies implemented, tested identically, and benchmarked against each other.
- A complexity plot generated from measured data, not drawn from theory.
- A written report on where the constants win.

## Tracks

Pick the one that matches where you are. You can climb mid-lab; the tests for the lower track
keep passing.

| Track | You get | You write | Spec |
|---|---|---|---|
| `basic` | ~60% of the code, TODOs marked | the marked TODOs | [basic/SPEC.md](basic/SPEC.md) |
| `standard` | a spec and a test suite | the implementation | [standard/SPEC.md](standard/SPEC.md) |
| `hard` | the same spec plus a constraint the standard solution fails | a better implementation | [hard/SPEC.md](hard/SPEC.md) |

## Getting started

```bash
cd labs/p2/week-13
make help                    # what this lab can do
cat standard/SPEC.md         # the acceptance criteria
$EDITOR starter/             # your work goes here
make verify                  # TRACK=standard against starter/  -> red until you finish
make verify TRACK=basic      # the scaffolded track
make verify IMPL=solution    # proves the tests are honest
make contract                # asserts solution green AND starter red
```

You edit **`starter/`**. `basic/`, `standard/` and `hard/` hold the specs and any track-specific
scaffolding; `solution/` is the reference. Open `solution/` only after you have a failing
attempt of your own — reading it first converts a 6-hour skill into a 6-minute read.

## Verify — real output from this repo

```
$ make verify IMPL=solution TRACK=hard
==> LAB-P2-W13 · track=hard · impl=solution
.....................                                                    [100%]
21 passed in 0.56s

$ make verify        # starter/, standard track
FAILED tests/test_pycollections.py::test_lru_agrees_with_ordereddict_under_random_operations
FAILED tests/test_pycollections.py::test_min_heap - NotImplementedError: MinHeap
FAILED tests/test_pycollections.py::test_heapify_is_linear_and_correct - NotI...
17 failed, 4 deselected in 0.18s
make[1]: *** [_verify_impl] Error 1
make: *** [verify] Error 2

$ make contract TRACK=hard
==> contract check: LAB-P2-W13 track=hard
  PASS  solution/ is green
  PASS  starter/ is red (as it must be)
contract holds
```
21 tests green on `solution/` at the `hard` track, 17 failed on `starter/`, and the same
parametrised contract runs against both hash-table implementations.

## Measured — `make bench IMPL=solution`

Apple M2, macOS 15, CPython 3.12.9, minimum of 3 runs. Full output in `bench/results.csv`.

**Hash maps, nanoseconds per operation**

| n | chained insert | open insert | chained get | open get | dict get |
|---|---|---|---|---|---|
| 1,000 | 684 | 562 | 149 | 138 | 14 |
| 10,000 | 741 | 886 | 197 | 149 | 13 |
| 100,000 | 1,577 | 680 | 309 | 138 | 12 |
| 300,000 | 1,635 | 7,107 | 326 | 174 | 14 |

**Open addressing: what the load factor actually costs** (capacity fixed at 65,536,
random integer keys)

| load factor | ns/get | probes/get |
|---|---|---|
| 0.30 | 153 | 1.22 |
| 0.50 | 168 | 1.49 |
| 0.60 | 189 | 1.77 |
| 0.70 | 213 | 2.16 |
| 0.80 | 276 | 3.17 |
| 0.90 | 420 | 5.39 |

This is the graph the lab exists for. Between 0.3 and 0.7 the cost rises 39%; between 0.7 and
0.9 it rises another 97%. Linear probing's expected probe count is
`(1 + 1/(1-a)^2) / 2` — 1.5 at a = 0.5, 13 at a = 0.9 — and the measurement tracks it
until the cache stops cooperating. Every "O(1)" claim in this table is true and none of them
are the same speed.

**The benchmark trap worth knowing:** the first version of this harness used keys
`range(n)`. In CPython `hash(int) == int`, so consecutive integers land in consecutive slots
and probe **exactly once at every load factor** — a perfectly flat, completely wrong graph.
The numbers above use `random.sample`. If your load-factor curve is flat, this is why.

**heapify O(n) vs n pushes O(n log n)**

| n | n pushes (ms) | heapify (ms) | ratio |
|---|---|---|---|
| 10,000 | 1.1 | 0.6 | 1.9x |
| 100,000 | 9.9 | 5.5 | 1.8x |
| 500,000 | 51.5 | 32.6 | 1.6x |

The asymptotic gap is `log n`, so 17x at n = 10^5. The measured gap is 1.8x. The difference is
the constant: `push` does one sift-up of average length ~1.6 regardless of n, because most
pushes land near the bottom and stop immediately. The theory is about the worst case; the
average case is nearly flat. This is the clearest small example in the course of Big-O being
correct and useless at the same time.

**Where a list scan stops beating a set** (uniform hits, average case)

| size | `in` list (ns) | `in` set (ns) |
|---|---|---|
| 1 | 12 | 11 |
| 2 | 15 | 19 |
| 4 | 21 | 14 |
| 8 | 32 | 15 |
| 64 | 144 | 13 |

The crossover is at about **3 elements** — much lower than most people guess, because
CPython's set lookup is one C call and the list scan is a Python-level loop. In a compiled
language with contiguous small structs, the same crossover is typically 8–16.

**Dynamic array growth factor** (n = 200,000)

| growth | final capacity | slack | elements copied | ms |
|---|---|---|---|---|
| 1.125 | 208,621 | 1.04x | 1,669,250 | 38.4 |
| 1.5 | 207,382 | 1.04x | 414,776 | 18.8 |
| 2.0 | 262,144 | 1.31x | 262,143 | 16.9 |
| 4.0 | 262,144 | 1.31x | 87,381 | 13.8 |

Total copies for growth factor g is `n / (g - 1)`: 8n at 1.125, 2n at 1.5, n at 2.0. Doubling
buys 2.3x fewer copies than 1.5 and pays 31% peak slack for it. CPython's list uses ~1.125
and eats the copying, because for a list of 12 elements — which most lists are — the slack
matters more than the copies.

**Count-min sketch: measured error vs the eps·N bound** (200,000 events, ~12,000 distinct keys)

| width | depth | bytes | mean error | p99 error | eps·N bound |
|---|---|---|---|---|---|
| 512 | 4 | 16 KB | 377.4 | 3,751 | 1,061.8 |
| 2,048 | 4 | 64 KB | 82.0 | 76 | 265.5 |
| 4,096 | 5 | 160 KB | 32.8 | 34 | 132.7 |
| 16,384 | 5 | 640 KB | 0.0 | 0 | 33.2 |

The bound holds, and it is loose by roughly 3-4x at the mean — which is the useful finding:
sizing a sketch off the theoretical bound gives you 3x more memory than you need, and sizing
it off a measurement on your own data does not. Note the test asserts the *probabilistic*
form (at most `delta = e^-depth` of estimates may exceed the bound), because that is what the
structure actually promises.


## Ship it

Repo plus a written "what I learned about constants vs Big-O" report with the plots.

A lab never ends at "it printed the right thing".

## Rubric

See [RUBRIC.md](RUBRIC.md). Grade yourself before you look at `solution/`.

## If you get stuck

1. Twenty minutes stuck, then read the *Common mistakes* table in the week's module pages.
2. Then re-read Layer 1 of the module this lab tests.
3. Then `solution/`, one function at a time — and delete-and-rewrite the function you read.
