# `hard` — LAB-P4-W30

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 6-9 h

## Constraint

Survive **20 randomly-timed process kills** with no duplicated side effects and no lost work.

## Acceptance criteria

- The kill-storm suite: 20 randomly-timed `SIGKILL`s during a run, with zero duplicated side
  effects and zero lost work, verified against a side-effect ledger.
- A critic agent reviewing the planner's output, with a measured quality improvement on a fixed
  task set — report the number, including if it is small.
- A full failure-injection suite green: tool timeout, model returning malformed JSON, database
  unavailable, approval never granted, and budget exhausted mid-action.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
