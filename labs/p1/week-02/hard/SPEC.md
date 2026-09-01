# `hard` — LAB-P1-W02

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 3-5 h

## Constraint

The script must survive `SIGTERM` and `SIGKILL` delivered at an arbitrary point during a write,
100 times in a row, without ever producing a metrics file that the report step cannot parse.
The test harness does exactly that.

## Acceptance criteria

- Alert thresholds in a config file; crossing one writes an `ALERT` line and exits 1.
- `trap` handlers clean up the lock and any temp file on `SIGTERM` / `SIGINT` / `EXIT`.
- Log rotation at a size bound, keeping N generations.
- The kill-storm test (`tests/kill_storm.bats`) passes: 100 randomly-timed kills, zero corrupt files.
- Commit history is `git bisect`-friendly: one commit per sample, message contains the metric summary.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
