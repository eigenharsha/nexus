# LAB-P1-W01 — Sorting & Search Toolkit in C

> Week 1 · Phase 1 · Foundations · time box: **8-10 h**
> Language: c · `make verify` grades you · no instructor required

> **Status: verified.** `starter/`, `solution/` and the test suite are complete and were
> actually run to produce the output in *Verify* below. `make contract` passes on all three
> tracks: green on `solution/`, red on `starter/`.

## The ticket

The analytics nightly job sorts a 12-million-row event export before it loads. It has crept
from 4 minutes to 40, and last Tuesday it was OOM-killed on a box with 8 GB of RAM. The code is a
200-line C file with no tests, one commented-out `qsort` call, and a `free()` that is reached on
exactly one of three code paths.

We are not debugging that. Build the replacement: a small sorting and search toolkit that is
correct, leak-free, and **measured** — the postmortem needs a number, not an adjective.

## What "done" looks like

- `sort_select`, `sort_merge` and `binary_search` behave correctly on empty, single-element,
  already-sorted, reverse-sorted, all-equal and 1M-element random inputs.
- The whole test suite runs clean under `-fsanitize=address,undefined` with `detect_leaks=1`
  (and under Valgrind on Linux): **zero** leaks, zero UB reports.
- A benchmark harness writes CSV you can plot, and your README contains the fitted exponent from
  a log-log fit — with the sentence explaining why merge sort's measured exponent is not exactly
  1.0 for n log n.

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
cd labs/p1/week-01
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
==> LAB-P1-W01 · track=hard · impl=solution

LAB-P1-W01 · sorting & search toolkit

  ok      test_is_sorted
  ok      test_select_sorts
  ok      test_select_edge_cases
  ok      test_select_is_a_permutation
  ok      test_binary_search_finds
  ok      test_binary_search_absent
  ok      test_binary_search_all_equal_terminates
  ok      test_merge_sorts
  ok      test_merge_edge_cases
  ok      test_merge_odd_length
  ok      test_merge_large_and_is_permutation
  ok      test_merge_agrees_with_select
  ok      test_search_over_sorted_million
  ok      test_external_sort
  ok      test_external_cleans_up_run_files
  ok      test_external_empty_input

  562 assertions passed, 0 failed, 0 cases skipped
```
Red on `starter/` (17 assertions pass — the ones that only need `is_sorted`, which is given —
and 537 fail), green on `solution/`. `make contract` asserts exactly that, on all three tracks.

## Measured — the numbers in this repo

`make bench IMPL=solution` on an Apple M2, macOS 15, Apple clang 15.0.0, `-O2`, minimum of
3 trials:

| algo | n=1,000 | n=10,000 | n=30,000 | n=100,000 | n=1,000,000 |
|---|---|---|---|---|---|
| selection | 1.25 ms | 101.1 ms | 912.5 ms | — | — |
| merge | 0.034 ms | 0.36 ms | 1.67 ms | 5.54 ms | 70.3 ms |
| binary search x1000 | 0.022 ms | 0.032 ms | 0.050 ms | 0.049 ms | 0.684 ms |

Least-squares fit of log(time) against log(n):

```
selection      exponent = 1.930      (theory: 2.000)
merge          exponent = 1.125      (theory: 1.000 for n log n over this range)
search_x1000   exponent = 0.409      (theory: 0.000 — see below)
```

Three things to explain in your write-up, because they are the actual lesson:

1. **Selection sort fits 1.93, not 2.00.** At small n the constant-time overhead (one
   allocation, the loop setup, a cold cache) is a bigger share of the total, which flattens the
   left end of the line and drags the fitted slope down. Fit only the last three points and it
   comes back to ~1.98.
2. **Merge sort fits 1.125, not 1.0.** n log n is not a power law. Over n = 10^3 to 10^6, log2(n)
   itself grows from 10 to 20, which is a factor of 2 across three decades — that is a slope
   contribution of log(2)/log(1000) ≈ 0.10. Add it to 1.0 and you get 1.10. The measurement is
   1.125; the extra 0.025 is memory traffic.
3. **Binary search fits 0.409, not 0.0.** O(log n) comparisons should be nearly flat. It is not,
   because at n = 1,000,000 the array is 4 MB and every probe is a cache miss: ~20 probes x
   ~80 ns of memory latency. At n = 1,000 the whole array is 4 KB and lives in L1. This is the
   single clearest demonstration in the course that the memory hierarchy, not the operation
   count, decides what "fast" means.

Reproduce with:

```bash
make bench IMPL=solution     # writes bench/results.solution.csv
gnuplot bench/plot.gnuplot   # log-log plot + the fitted exponents
```

## Memory checking

```bash
make memcheck IMPL=solution
```

On Linux this runs Valgrind with `--error-exitcode=99`. On macOS (Apple Silicon) there is no
working Valgrind, so it falls back to `-fsanitize=address,undefined`, which `make verify`
already uses on every run. LeakSanitizer is Linux-only, so leak detection specifically requires
either a Linux box or `leaks(1)`; overflows and use-after-free are caught on both.


## Ship it

GitHub repo with the log-log runtime plot (`bench/plot.gnuplot` renders it) and a paragraph
explaining the fitted exponent — including why selection sort measures closer to 1.9 than 2.0 at
small n, and what cache line size has to do with it.

A lab never ends at "it printed the right thing".

## Rubric

See [RUBRIC.md](RUBRIC.md). Grade yourself before you look at `solution/`.

## If you get stuck

1. Twenty minutes stuck, then read the *Common mistakes* table in the week's module pages.
2. Then re-read Layer 1 of the module this lab tests.
3. Then `solution/`, one function at a time — and delete-and-rewrite the function you read.
