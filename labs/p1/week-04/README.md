# LAB-P1-W04 — Async Concurrent Downloader

> Week 4 · Phase 1 · Foundations · time box: **8-10 h**
> Language: python · `make verify` grades you · no instructor required

> **Status: verified.** `starter/`, `solution/` and the test suite are complete and were
> actually run to produce the output in *Verify* below. `make contract` passes on all three
> tracks: green on `solution/`, red on `starter/`.

## The ticket

The nightly ingest pulls about 4,000 files from a partner's CDN. It is a `for` loop around
`requests.get` and it now takes just over six hours, which means it is still running when the
morning reports fire.

Two constraints from the partner, both real: they rate-limit us at 500 requests per minute, and
their edge returns a 503 roughly 2% of the time — plus, about once a night, a truncated body with
a 200 status. The current job has no retries and no checksum, so we have silently ingested
truncated files at least twice.

Rewrite it. Concurrent, bounded, resumable, and provably not corrupting anything when it is
interrupted.

## What "done" looks like

- Throughput limited by the partner's rate limit, not by our code.
- A killed job resumes without re-downloading completed files and without corrupting partial ones.
- A truncated response is detected and retried, not written.
- Ctrl-C exits within a second, cleanly, with no orphaned tasks and no half-written files.

## Tracks

Pick the one that matches where you are. You can climb mid-lab; the tests for the lower track
keep passing.

| Track | You get | You write | Spec |
|---|---|---|---|
| `basic` | ~60% of the code, TODOs marked | the marked TODOs | [basic/SPEC.md](basic/SPEC.md) |
| `standard` | a spec and a test suite | the implementation | [standard/SPEC.md](standard/SPEC.md) |
| `hard` | the same spec plus a constraint the standard solution fails | a better implementation | [hard/SPEC.md](hard/SPEC.md) |

## Getting started

```bash
cd labs/p1/week-04
make help                    # what this lab can do
cat standard/SPEC.md         # the acceptance criteria
$EDITOR starter/             # your work goes here
make verify                  # TRACK=standard against starter/  -> red until you finish
make verify TRACK=basic      # the scaffolded track
make verify IMPL=solution    # proves the tests are honest
make contract                # asserts solution green AND starter red
```

You edit **`starter/`**. `basic/`, `standard/` and `hard/` hold the specs and any track-specific
scaffolding; `solution/` is the reference. Open `solution/` only after you have a failing
attempt of your own — reading it first converts a 6-hour skill into a 6-minute read.

## Verify — real output from this repo

```
$ make verify IMPL=solution TRACK=hard
==> LAB-P1-W04 · track=hard · impl=solution
...................                                                      [100%]
19 passed in 5.50s

$ make verify        # starter/, standard track
FAILED tests/test_downloader.py::test_completed_file_is_skipped_with_no_network_call
FAILED tests/test_downloader.py::test_cancellation_is_graceful - NotImplement...
FAILED tests/test_downloader.py::test_structured_logs_are_json_shaped - NotIm...
FAILED tests/test_downloader.py::test_one_failure_does_not_lose_the_others - ...
14 failed, 5 deselected in 0.85s
make[1]: *** [_verify_impl] Error 1
make: *** [verify] Error 2

$ make contract TRACK=hard
==> contract check: LAB-P1-W04 track=hard
  PASS  solution/ is green
  PASS  starter/ is red (as it must be)
contract holds
```
19 tests green on `solution/` at the `hard` track — every one of them against
`tests/flaky_server.py`, not against the internet.

## The fixture is the interesting half

`tests/flaky_server.py` is a ~200-line asyncio HTTP server that produces, on demand and
reproducibly, every failure the ticket describes:

| Failure | How it is produced | Which test |
|---|---|---|
| 503, first N attempts | `fail_first=3` | `test_retries_5xx_with_backoff_then_succeeds` |
| 429 with `Retry-After` | `status_when_failing=429` | `test_retries_429` |
| 404 (must never be retried) | `status=404` | `test_404_is_not_retried` |
| Truncated body, 200 status | `truncate_at=9000` | `test_truncated_body_is_detected_and_retried` |
| Stall past your timeout | `stall_seconds=0.15` | `test_cancellation_is_graceful` |
| `Range: bytes=N-` resume | always honoured, 206 + `Content-Range` | `test_resumes_from_a_partial_file_with_range` |

It also records what the client did, which is how three of the tests check things you cannot
observe from the client side at all:

- **peak concurrency** — the server counts live connections, so `concurrency=4` is verified
  against the socket count rather than against your semaphore;
- **the request timeline** — `peak_rate_per_minute()` computes the highest count in any
  sliding window, which is what makes the rate-limit test honest;
- **request counts per path** — so "a completed file costs zero network calls" is a fact,
  not a claim.

## Measured — sequential vs threads vs async

`make bench IMPL=solution` on an Apple M2, Python 3.12.9, 60 files x 32 KB with a 20 ms
server-side stall each (the workload is latency-bound, which is the shape of the real job):

| strategy | wall (s) | files/s | speedup |
|---|---|---|---|
| sequential | 1.45 | 41.4 | 1.0x |
| threads x8 | 0.20 | 302.2 | 7.3x |
| threads x32 | 0.07 | 887.8 | 21.5x |
| asyncio x8 | 0.22 | 277.9 | 6.7x |
| asyncio x32 | 0.09 | 704.2 | 17.0x |

The honest reading, which is the paragraph that belongs in your write-up:

**Threads are not slower than asyncio here, and at this scale they are marginally faster.**
For 60 connections, an OS thread costs about 8 KB of kernel stack plus a scheduler entry, and
the GIL is released during socket I/O, so there is nothing for async to win. The advantage
shows up at a scale this benchmark deliberately does not reach: at 10,000 concurrent
connections, 10,000 threads is roughly 80 MB of stacks and a context-switch storm, while
10,000 coroutines is roughly 10 MB of Python objects on one thread. Anyone whose benchmark
shows async beating threads by 5x on 60 requests measured something else.

What actually mattered for the six-hour job in the ticket was neither: it was going from
concurrency 1 to concurrency 8. The first 7x is free; everything after it is engineering.


## Ship it

Repo plus a benchmark README comparing sequential, threaded and async on the identical
workload against the same local fixture — with the wall-clock numbers and the explanation of why
threads do not lose by as much as people expect.

A lab never ends at "it printed the right thing".

## Rubric

See [RUBRIC.md](RUBRIC.md). Grade yourself before you look at `solution/`.

## If you get stuck

1. Twenty minutes stuck, then read the *Common mistakes* table in the week's module pages.
2. Then re-read Layer 1 of the module this lab tests.
3. Then `solution/`, one function at a time — and delete-and-rewrite the function you read.
