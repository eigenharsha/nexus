# `standard` — LAB-P4-W29

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 8-10 h

## Acceptance criteria

- An agent built from scratch: a tool registry with JSON-schema tool definitions, conversation
  memory with a summarization strategy when the window fills, an explicit token budget, retries
  on malformed tool calls, and structured stop conditions (goal reached / budget exhausted /
  max iterations / explicit give-up).
- A custom MCP server exposing a database (read-only, parameterized queries only) and sandboxed
  terminal access.
- Sandbox: an allowlist of commands, no network, a read-only filesystem except one temp dir, a
  wall-clock timeout and an output size cap. Each of those is tested by trying to violate it.
- Success measured over a 30-task benchmark with a reported success rate and a failure taxonomy.
- A full test suite against a **mocked model** — the agent's logic must be testable without
  calling anything.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Testing against a mocked model is what makes this repo credible. An agent you can only test by
running it against a live API is an agent nobody can review. Record a set of model responses and
replay them; the loop, the budget and the stop conditions are all deterministic then.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
