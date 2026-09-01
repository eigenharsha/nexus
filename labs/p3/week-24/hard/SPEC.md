# `hard` — LAB-P3-W24

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 5-8 h

## Constraint

A zero-downtime rolling update under sustained load, **proven** with a request log showing zero
5xx, plus autoscaling on a custom queue-depth metric.

## Acceptance criteria

- Zero-downtime rolling update under sustained load, with the client-side request log committed
  as evidence: zero failed requests across the rollout.
- Custom-metric autoscaling on queue depth (via the Prometheus adapter), with the reason CPU is
  the wrong signal for this workload.
- p50/p95/p99 documented at three load levels, plus a cost-per-1M-predictions estimate compared
  against the Week-23 serverless number.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
