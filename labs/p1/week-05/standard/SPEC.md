# `standard` — LAB-P1-W05

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 4-5 h

## Acceptance criteria

- Responsive layout, works from 360 px to 1920 px with no horizontal scroll.
- Search with a 250 ms debounce; the in-flight request is aborted when the query changes.
- Pagination with correct `aria-current` and keyboard access.
- Dark mode following `prefers-color-scheme`, with a manual override that persists.
- All four states, each with its own visual treatment and its own test.
- No framework. Vanilla ES2022 modules.
- Lighthouse >= 90 on all four categories, screenshot in the README.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

`AbortController` is the whole point of the search requirement: without it, a slow response
for "ab" arrives after the fast response for "abcd" and overwrites it. That race is the single
most common bug in hand-rolled search boxes.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
