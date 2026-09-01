# `standard` — LAB-P1-W02

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 3-4 h

## Acceptance criteria

- `monitor.sh sample` appends one record to `metrics.tsv` and rotates it at a configured size.
- `monitor.sh report` renders `REPORT.md` from the metrics file: current values, 24 h min/max/mean.
- `monitor.sh publish` commits and pushes over SSH, and is a no-op when nothing changed.
- **Idempotent:** two `sample` runs inside the same interval produce exactly one record.
- **Locked:** concurrent invocations do not interleave writes (`flock`, or an atomic `mkdir` lock
  on macOS where `flock` is absent).
- **Logged:** every run writes a structured line to `monitor.log` with a timestamp and an outcome.
- `set -euo pipefail` and an `ERR` trap that reports the failing line.
- Installable as a cron entry (Linux) or a launchd plist (macOS) by `monitor.sh install`.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

The atomic-write pattern is the whole lab: write to `metrics.tsv.tmp`, `fsync` if you can,
then `mv` it into place. `mv` within one filesystem is atomic; `>>` is not. Everything else here
is quoting discipline.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
