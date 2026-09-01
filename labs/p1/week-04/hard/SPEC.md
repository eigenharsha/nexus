# `hard` — LAB-P1-W04

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 5-8 h

## Constraint

10,000 URLs, a hard **500 requests/minute** ceiling, and a **300 MB** RSS ceiling.
Naive `asyncio.gather` over 10,000 coroutines allocates all 10,000 up front and blows the memory
budget before it sends a byte.

## Acceptance criteria

- A token-bucket rate limiter holds the observed request rate at or under the limit, measured
  over any 60-second sliding window (the test asserts this from the server-side access log).
- Work is streamed, not materialised: the test caps memory and fails if peak RSS exceeds it.
- Response bodies are streamed to disk in chunks — never `await resp.read()` on a large file.
- A throughput/latency report: total wall time, achieved req/min, p50/p95/p99 per-file latency.
- Proof of no corruption and no double-write: every file's sha256 matches and every path was
  opened for writing exactly once (the fixture records opens).

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
