# `standard` — LAB-P2-W12

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 5-6 h

## Acceptance criteria

- A CLI tool: `abtest analyze results.csv --primary conversion --guardrail latency_p95`.
- Sample-size calculator: given baseline rate, MDE and power, output required n per arm.
- **SRM check** (sample ratio mismatch) via chi-square; if it fails, refuse to report and say why.
- Primary and guardrail metrics reported together, with effect size (both absolute and relative)
  and a bootstrap CI (10,000 resamples).
- A written decision block: ship / do not ship / inconclusive, with the reason.
- Plus a from-scratch multinomial naive Bayes classifier with Laplace smoothing, evaluated on a
  text dataset with a confusion matrix.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

The four errors in their analysis are: peeking (they checked daily and stopped at
significance), no SRM check, a guardrail metric that regressed and was not reported, and a
relative effect quoted from an absolute difference on a small base. Your tool should make three
of those four impossible and loudly report the fourth.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
