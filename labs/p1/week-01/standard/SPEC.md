# `standard` — LAB-P1-W01

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 5-6 h

## Acceptance criteria

- Implement, from an empty file: `sort_select`, `sort_merge`, `binary_search`,
  and `is_sorted` (used by the tests as an oracle).
- `sort_merge` is a genuine merge sort: O(n log n) comparisons, stable, and it must not recurse
  deeper than ~log2(n) frames.
- Every heap allocation is freed on **every** path, including the early-return error paths.
  `make verify` runs with `ASAN_OPTIONS=detect_leaks=1`; a leak is a test failure, not a warning.
- `binary_search` handles the classic boundary bugs: it must not overflow on `(lo+hi)/2` for
  large indices, and must terminate on every input including all-equal arrays.
- `bench.c` produces `bench/results.csv` with columns `algo,n,trial,nanoseconds`, for n from
  1,000 to 1,000,000, at least 3 trials per point.
- Zero warnings under `-Wall -Wextra -Wpedantic -std=c17`.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Two decisions worth writing down in your README:

1. **Where does merge sort's scratch buffer live?** Allocating inside the recursion is the
   obvious version and costs you an allocation per level per subarray. One buffer allocated once
   at the top is ~2x faster at n=1M. Measure both; that delta is your Layer-3 answer.
2. **`size_t` vs `int` for indices.** Mixed signedness in a binary search is where the CVEs come
   from. Pick one, and make `-Wextra` prove you were consistent.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
