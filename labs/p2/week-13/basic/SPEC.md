# `basic` — LAB-P2-W13

**For:** you have not done this before. About 60% of the code is written; the gaps are marked
`TODO`. Every TODO has a one-line hint above it.

**Time box:** 2 h

## What you must make true

- `ChainedHashMap` with `get`, `put`, `delete`, `__len__`, `__contains__`, and resizing,
  passing the provided tests.
- Collisions handled by chaining. The tests include a key class with a deliberately terrible
  `__hash__` so every key collides.

## Acceptance

```bash
make verify TRACK=basic
```

Green means every `TODO` in the files listed above is filled in correctly.

## Hints are not cheating here

The point of `basic` is to see the shape of a correct solution while typing it. If you finish in
under half the time box, do `standard` from an empty file — that is where the learning is.
