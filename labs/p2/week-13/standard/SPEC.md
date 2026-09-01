# `standard` — LAB-P2-W13

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 6-7 h

## Acceptance criteria

- `ChainedHashMap` **and** `OpenAddressingHashMap` (linear probing with tombstones), both
  satisfying the same test suite via a shared parametrised fixture.
- Correct resize behaviour: growth at a documented load factor, and — for open addressing —
  tombstone cleanup, tested by a delete-heavy workload that would otherwise degrade to O(n).
- `DynamicArray` with amortised O(1) append and a documented growth factor.
- `DoublyLinkedList` with O(1) `append_left` / `pop_right`.
- `LRUCache` built from the dict + doubly-linked-list combination, O(1) `get` and `put`.
- `MinHeap` with `push`, `pop`, `peek`, and `heapify` in O(n).
- A benchmark harness producing `bench/results.csv` and complexity plots for each structure.
- Every structure has a property-based test asserting it agrees with the stdlib equivalent under
  an arbitrary sequence of operations.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Two things the benchmark will show you that the textbook does not:

1. Open addressing wins on lookup at low load factor because it touches one cache line, not two.
   Above about 0.7 it falls off a cliff. Find your cliff and put the number in the report.
2. `DynamicArray` with growth factor 1.5 uses less peak memory than 2.0 and is not measurably
   slower. CPython uses roughly 1.125. Measure all three.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
