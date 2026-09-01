# `standard` — LAB-P1-W04

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 5-6 h

## Acceptance criteria

- A `Downloader` class with explicit configuration: `concurrency`, `max_retries`,
  `backoff_base`, `timeout`, `chunk_size`.
- **Bounded concurrency** via a semaphore — never more than `concurrency` sockets open, asserted
  by the test fixture, which counts concurrent connections and fails the run if the bound is broken.
- **Retries with exponential backoff and jitter** on connection errors, timeouts, 5xx and 429.
  Never retries a 404.
- **Checksum verification**: given an expected sha256, a mismatch is a failure, and the partial
  file is deleted rather than left on disk.
- **Resumable**: a `.part` file plus an HTTP `Range` request continues an interrupted transfer;
  a completed file is skipped without a network call.
- **Graceful cancellation**: `KeyboardInterrupt` / `CancelledError` cancels in-flight tasks,
  awaits their cleanup, and leaves no `.part` file in an unrecoverable state.
- **Structured logs**: one JSON line per attempt with url, attempt number, status, bytes, duration.
- Tests run against a **local flaky-server fixture** with a seeded failure policy — deterministic
  flakiness, so a failing test is reproducible.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

The fixture is the interesting part of this lab. A test that hits the real internet is not a
test. `tests/flaky_server.py` is an asyncio HTTP server that, driven by a seed, will: return 503
for the first N attempts of a given path, truncate the body at a byte offset, stall past your
timeout, or honour a `Range` header — all deterministically. Read it before you write the client;
it *is* the spec for the failure modes you must handle.

Design call to defend: a semaphore bounds **concurrency**, not **rate**. 8 concurrent requests
that each take 10 ms is 800 req/s, which blows a 500-req/min budget by 96x. You need both.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
