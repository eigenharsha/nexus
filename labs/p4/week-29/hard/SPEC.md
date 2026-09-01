# `hard` — LAB-P4-W29

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 6-8 h

## Constraint

Thirty tools with tool-selection accuracy maintained, plus adversarial testing of the sandbox
with a written report of every escape attempt and its mitigation.

## Acceptance criteria

- Scale to 30 tools with selection accuracy maintained within a stated margin of the 5-tool
  baseline; report the technique you used (retrieval over tool descriptions, hierarchical
  grouping, or something else) and the numbers before and after.
- An adversarial test suite against the sandbox: prompt injection through tool output, path
  traversal, command chaining, resource exhaustion, and data exfiltration through an allowed
  command. Every attempt documented with its outcome and mitigation.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
