# `hard` — LAB-P4-W26

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 6-8 h

## Constraint

Beat the base model **plus constrained decoding** on both accuracy and cost — which is a real
bar, because constrained decoding gets schema validity to 100% for free.

## Acceptance criteria

- Beat base + constrained decoding on accuracy *and* cost, with both measured.
- A LoRA rank sweep (at least r = 4, 8, 16, 32) with quality and training cost for each.
- A quantization Pareto plot: quality vs latency vs memory across at least three quantization
  settings.
- A written serve-vs-API cost analysis at three volume levels, including the GPU hours.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
