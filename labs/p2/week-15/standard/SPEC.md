# `standard` — LAB-P2-W15

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 7-8 h

## Acceptance criteria

- Extract from the REST API **and** an unstructured HTML source; normalize both into one schema.
- Incremental loading on a cursor field with `merge` write disposition; re-running the pipeline
  produces zero new rows (the test asserts an unchanged table hash).
- Schema evolution enabled and tested: the fixture adds a column mid-run and the pipeline absorbs it.
- Deduplication on a documented business key, with the tie-break rule written down.
- Data-quality checks: null rates, referential integrity, an amount-range check, and a row-count
  delta bound. A failed check fails the run loudly.
- A run report artifact per run: rows in, rows merged, rows rejected, checks passed, duration.
- Scheduled (cron or a scheduler of your choice) and safe to re-run at any point.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

This is the single most directly job-applicable artifact in Phase 2 for a working engineer.
The part that makes it credible in an interview is the run report: it is the evidence that you
have run a pipeline that someone depended on, rather than one that ran once on your laptop.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
