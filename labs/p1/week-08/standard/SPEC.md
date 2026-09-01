# `standard` — LAB-P1-W08

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 7-8 h

## Acceptance criteria

- FastAPI + async SQLAlchemy 2.x.
- Payment verification and inventory decrement in **one** transaction with the correct isolation
  level, chosen deliberately and documented.
- Optimistic locking via a `version` column; a lost update raises and is retried a bounded number
  of times.
- Idempotency keys stored with the request hash; a replay returns the original response.
- Alembic migrations, including a downgrade that actually works.
- A concurrency test suite that runs 200 concurrent buyers against a stock of 12 and asserts
  exactly 12 orders, 12 payments and a final stock of 0 — run 20 times, zero flakes.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

`SELECT ... FOR UPDATE` is the easy answer and it is a defensible one. The point of the lab is
that you can say **why** you chose it over the optimistic version, with a throughput number
attached, rather than because it was the first result.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
