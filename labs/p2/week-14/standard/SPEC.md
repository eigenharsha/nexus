# `standard` — LAB-P2-W14

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 7-8 h

## Acceptance criteria

- Fifteen medium problems across trees, graphs and dynamic programming, all tests green.
- For each: a docstring stating time and space complexity, and one sentence on why.
- A Dijkstra route planner CLI over real OSM-derived data: `route --from A --to B` returns the
  path, the distance and the node-expansion count.
- The planner uses your own binary heap (Week 13) or `heapq` — state which and why.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

The journal is the deliverable, not the solutions. For each problem write down the idea you
tried first and why it failed. Interviewers ask "what did you try?" far more often than they ask
for an optimal solution, and the honest answer is the one that gets you hired.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
