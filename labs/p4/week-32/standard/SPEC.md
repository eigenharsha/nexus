# `standard` — LAB-P4-W32

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 8-10 h

## Acceptance criteria

- Full instrumentation of the Week-30 system: traces exported to a self-hosted Langfuse.
- Per-step token and cost attribution, so a trace answers "which node spent the money".
- Prompt versioning, with the version recorded on every trace.
- Scheduled evals (the Week-31 suite) running against production traffic samples.
- Dashboards: cost per run, p95 latency per step, error rate, token usage by model.
- Alerts on cost per run, error rate and latency, each with a threshold you justified.
- A cost-reduction experiment with before/after numbers on both cost **and** quality.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Attribute cost at the span, not at the run. "This incident cost £0.42" is not actionable;
"the critic agent is 61% of the cost and improves resolution quality by 3 points" is a decision.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
