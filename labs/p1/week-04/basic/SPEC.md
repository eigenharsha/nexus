# `basic` — LAB-P1-W04

**For:** you have not done this before. About 60% of the code is written; the gaps are marked
`TODO`. Every TODO has a one-line hint above it.

**Time box:** 1-2 h

## What you must make true

- `download_all(urls, dest)` uses `asyncio.gather` to fetch a list of URLs concurrently.
- Prints a progress counter `[k/n]` as each completes.
- Returns the list of destination paths in the same order as the input URLs.
- One failure must not lose the other results (`return_exceptions=True` and report them).

## Acceptance

```bash
make verify TRACK=basic
```

Green means every `TODO` in the files listed above is filled in correctly.

## Hints are not cheating here

The point of `basic` is to see the shape of a correct solution while typing it. If you finish in
under half the time box, do `standard` from an empty file — that is where the learning is.
