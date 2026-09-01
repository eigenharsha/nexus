# `hard` — LAB-P2-W10

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 5-7 h

## Constraint

1,000 concurrent clients on a single event loop, with back-pressure, surviving 5% packet loss
injected with `tc netem`. A thread-per-client server will not get there.

## Acceptance criteria

- 1,000 concurrent connections sustained; report memory per connection and p99 message latency.
- Back-pressure: a client that stops reading must not grow the server's memory without bound —
  the server drops or disconnects it according to a documented policy.
- Heartbeats with a documented timeout, detecting the half-open case within it.
- Survives `tc netem loss 5%` (Linux) with no message loss at the application layer.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
