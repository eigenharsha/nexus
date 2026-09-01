# `standard` — LAB-P4-W30

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 9-11 h

## Acceptance criteria

- Planner, analyst and executor agents on LangGraph with a **typed** state schema.
- Postgres checkpointing so state survives a process restart.
- A human-approval interrupt before **any** remediation action, with the proposed action and its
  blast radius shown to the approver.
- RAG over a runbook corpus (reusing the Week-27/28 pipeline).
- MCP-served sandboxed terminal access (reusing Week 29).
- Budget guards on tokens, wall time and tool calls, each of which halts the run with a clear state.
- Crash-resume proven by test: kill the process mid-run, restart, and the graph continues from
  the last checkpoint without repeating a side effect.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Idempotency keys on every side-effecting action are what make resume safe. Checkpointing tells
you where you were; it does not tell you whether the command you were running actually ran. The
executor has to record intent before acting and check for the result on resume.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
