# `basic` — LAB-P1-W01

**For:** you have not done this before. About 60% of the code is written; the gaps are marked
`TODO`. Every TODO has a one-line hint above it.

**Time box:** 2 h

## What you must make true

- Fill in the two `TODO` bodies in `starter/sorts.c`: `sort_select` and `binary_search`.
- `sort_select(int *a, size_t n)` sorts ascending, in place.
- `binary_search(const int *a, size_t n, int key)` returns the index of `key`, or `-1` if absent.
  On duplicates it may return any matching index.
- Both must be correct for `n == 0` and `n == 1`. That is where the provided tests will catch you.

## Acceptance

```bash
make verify TRACK=basic
```

Green means every `TODO` in the files listed above is filled in correctly.

## Hints are not cheating here

The point of `basic` is to see the shape of a correct solution while typing it. If you finish in
under half the time box, do `standard` from an empty file — that is where the learning is.
