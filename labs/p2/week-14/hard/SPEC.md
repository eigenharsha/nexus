# `hard` — LAB-P2-W14

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 4-6 h

## Constraint

A* with a custom heuristic must expand at least **3x fewer nodes** than Dijkstra on the same
query set, and you must sketch why your heuristic is admissible.

## Acceptance criteria

- A* with a geographic heuristic (haversine, scaled); measured node-expansion ratio >= 3x on the
  provided query set, reported per query.
- A written proof sketch of admissibility for your heuristic, including what breaks it if the
  edge weights stop being distances.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
