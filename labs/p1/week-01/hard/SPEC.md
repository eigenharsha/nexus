# `hard` — LAB-P1-W01

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 6-8 h

## Constraint

Sort a file of **50,000,000** 32-bit integers using no more than **64 MB** of resident memory.
The `standard` solution allocates the whole array and dies. You need an external merge sort:
read a bounded chunk, sort it, spill it to a run file, then k-way merge the runs with a heap.

## Acceptance criteria

- `sort_external(const char *in_path, const char *out_path, size_t mem_budget_bytes)`
  produces a fully sorted output file.
- Peak RSS stays under the stated budget. `make bench` measures it (`getrusage`) and the test
  fails if it is exceeded — the test runs a 5M-element file with a 4 MB budget so it finishes in
  CI time; the 50M/64MB run is yours to do and report.
- Temporary run files are cleaned up even if the merge fails halfway.
- Report wall time and peak RSS for the full 50M run in your README.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
