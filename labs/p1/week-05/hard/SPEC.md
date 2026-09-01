# `hard` — LAB-P1-W05

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 3-5 h

## Constraint

A 50,000-item list must scroll at 60 fps on a mid-range laptop, and the page must remain usable
with the network offline after a first load.

## Acceptance criteria

- Offline caching via a service worker with an explicit cache-versioning strategy.
- Request cancellation proven: rapid typing produces exactly one rendered result set.
- A virtualized list rendering only the visible window; DOM node count stays bounded (assert it
  in the console) while scrolling 50,000 rows.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
