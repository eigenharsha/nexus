# `standard` — LAB-P4-W28

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 8-10 h

## Acceptance criteria

- Hybrid retrieval: BM25 plus dense, fused with RRF, with the fusion constant tuned.
- HyDE query rewriting, ablated (it does not always help — report your number either way).
- Cross-encoder re-ranking of the top-k, with k chosen from the latency budget.
- A semantic cache with a similarity threshold chosen by measurement, reporting hit rate and the
  false-hit rate at that threshold.
- Grounded generation with citations, where every claim maps to a retrieved chunk and an
  unsupported claim is detectable.
- Every stage ablated on the Week-27 eval set, with a final table: quality, p95 latency, $/query.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Report the ablation that failed. A table where every row improves the metric is a table
nobody believes. HyDE in particular tends to help on vague queries and hurt on precise ones —
that split is a better finding than an average.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
