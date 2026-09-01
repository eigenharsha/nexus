# `hard` — LAB-P3-W21

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 5-8 h

## Constraint

A tensor-based engine with broadcasting, matching PyTorch to within tolerance on the same seed,
plus gradient checkpointing with the memory saving **measured**.

## Acceptance criteria

- Tensor-valued autograd with NumPy broadcasting, including correct gradient reduction when a
  broadcast axis is summed over — the test broadcasts (3,1) against (3,4) and checks the shape and
  the values of the resulting gradient.
- A PyTorch parity test: same seed, same data, same architecture, results within tolerance.
- A speed comparison against PyTorch CPU on the same workload, with the ratio and an honest
  explanation of where the difference comes from.
- Gradient checkpointing with the measured peak-memory saving on a deep network.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
