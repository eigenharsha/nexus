# `standard` — LAB-P1-W06

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 6-7 h

## Acceptance criteria

- FastAPI with Pydantic v2 models on every request and response.
- File upload endpoint with size limit (2 MB), content-type allowlist, and extension/`magic`
  agreement — reject a `.pdf` that is actually a zip.
- API-key auth on write endpoints; 401 vs 403 used correctly.
- Rate limiting per key with a `Retry-After` header.
- Structured error responses: one shape for every error, with a machine-readable `code`.
- Fully async I/O — no blocking call in a coroutine (the test asserts the event loop is never
  blocked for more than 50 ms).
- 25+ tests including auth failures, oversize uploads, malformed JSON and rate-limit behaviour.
- `/docs` renders and every endpoint has a description and an example.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Keep this service. It is upgraded with a fine-tuned model in Week 26 and instrumented with
OpenTelemetry in Week 32. The interfaces you choose now are the ones you will live with.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
