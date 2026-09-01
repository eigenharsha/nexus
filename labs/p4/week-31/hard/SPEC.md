# `hard` — LAB-P4-W31

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 6-8 h

## Constraint

Judge validated to the agreement threshold in `hard/targets.md`, a 15-attack red-team report,
and the eval suite kept inside a stated runtime and cost budget.

## Acceptance criteria

- Judge agreement with human labels above the stated threshold, reported as Cohen's kappa with
  its confidence interval.
- A red-team report: 15 attacks (direct injection, indirect injection through retrieved content,
  jailbreak, data exfiltration, denial of wallet, and more), each with the outcome and the
  mitigation, and a re-test after the mitigation.
- Eval suite runtime and cost inside the stated budget, with both reported per run.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
