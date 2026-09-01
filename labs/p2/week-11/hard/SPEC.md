# `hard` — LAB-P2-W11

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 5-7 h

## Constraint

A tiled matmul at least **10x** faster than the naive triple loop at n=512, and the autodiff
engine must train a real 2-layer network end to end.

## Acceptance criteria

- Tiled/blocked matmul >= 10x the naive version at n=512; report the tile size you chose and the
  measured numbers for at least three tile sizes.
- The autodiff engine trains a 2-layer network on a toy classification set to a stated accuracy.
- A benchmark report with the numbers and the cache explanation for the tile size.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
