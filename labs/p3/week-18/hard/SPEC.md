# `hard` — LAB-P3-W18

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 5-7 h

## Constraint

Beat the AUC target in `hard/targets.md` **within** the training-time budget stated there.
An unbounded hyperparameter search is not a solution.

## Acceptance criteria

- Meet the AUC target inside the training-time budget; report both.
- SHAP explanations for five individual customers, each with a one-paragraph reading a
  non-technical reader would follow.
- A model card: intended use, training data, metrics by slice, known limitations, and the
  conditions under which the model should be retired.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
