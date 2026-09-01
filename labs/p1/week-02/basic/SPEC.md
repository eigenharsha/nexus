# `basic` — LAB-P1-W02

**For:** you have not done this before. About 60% of the code is written; the gaps are marked
`TODO`. Every TODO has a one-line hint above it.

**Time box:** 1-2 h

## What you must make true

- `monitor.sh` samples CPU load and memory once and prints a formatted report to stdout.
- Works on both macOS and Linux (the memory command differs; detect, do not assume).
- Exits 0 on success and non-zero with a message on stderr if a required tool is missing.
- Passes `shellcheck` with no warnings.

## Acceptance

```bash
make verify TRACK=basic
```

Green means every `TODO` in the files listed above is filled in correctly.

## Hints are not cheating here

The point of `basic` is to see the shape of a correct solution while typing it. If you finish in
under half the time box, do `standard` from an empty file — that is where the learning is.
