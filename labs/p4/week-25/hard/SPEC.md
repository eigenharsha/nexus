# `hard` — LAB-P4-W25

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 6-8 h

## Constraint

RoPE plus grouped-query attention plus FlashAttention (through
`F.scaled_dot_product_attention`), with tokens/sec and peak memory measured at three context
lengths.

## Acceptance criteria

- Rotary position embeddings replacing learned positional embeddings, with the equivalence check
  against a reference implementation.
- Grouped-query attention with a configurable group count; report the KV-cache memory saving.
- FlashAttention via `F.scaled_dot_product_attention`, with output parity against your own
  implementation to 1e-4.
- Tokens/sec and peak memory at three context lengths (512 / 2048 / 8192) for each variant, in
  one table.
- An attention-visualization tool rendering the per-head attention pattern for a given prompt.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
