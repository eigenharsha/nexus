# `standard` — LAB-P4-W31

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 8-10 h

## Acceptance criteria

- A 100+ case eval suite combining deterministic assertions, a validated LLM judge, and RAG
  metrics (faithfulness, answer relevance, context precision).
- Running in GitHub Actions on every prompt or code change, failing the build on a regression
  against a committed baseline.
- A results comment posted on the PR showing per-category pass rates and the diff versus baseline.
- A Llama Guard (or equivalent) input layer, plus output checks for PII and groundedness.
- Measured false-positive and true-positive rates for every guardrail, on a labelled set.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Validate the judge before you trust it. Label 50 cases by hand, measure the judge's agreement
with your labels (Cohen's kappa, not raw accuracy), and report it. An unvalidated LLM judge is a
random number generator with good manners.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
