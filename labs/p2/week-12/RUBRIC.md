# Rubric — LAB-P2-W12

Score yourself **before** you open `solution/`. Four dimensions, 0–3 each, 12 points total.
`make verify` decides Correctness for you; the other three you grade honestly.

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **Correctness** | `make verify` fails | happy path only | edge cases handled | adversarial inputs handled |
| **Code quality** | it works | readable | tested and typed | a reviewer would approve unchanged |
| **Performance** | never measured | measured once | meets the stated budget | beats the budget, with evidence |
| **Explanation** | none | a README exists | reasoning documented | trade-offs defended in writing |

## What each score actually means here

**Correctness**
- 1 — `make verify TRACK=basic` green.
- 2 — `make verify TRACK=standard` green, including the edge cases listed in `standard/SPEC.md`.
- 3 — `make verify TRACK=hard` green under the stated constraint.

**Code quality**
- 2 requires: no function longer than ~40 lines, names that need no comment, and every error
  path either handled or explicitly documented as impossible.
- 3 requires: someone else could extend it without asking you a question.

**Performance**
- You cannot score above 1 without a number in your README. "It felt fast" is a 0.
- The budget for this lab is in `hard/SPEC.md` under *Constraint*.

**Explanation**
- 3 means you wrote down the option you rejected and why. That paragraph is the single
  highest-value thing in your portfolio repo, and it is the one everybody skips.

## Interview translation

A 12/12 on this lab is roughly one strong 45-minute answer. Write the three sentences you would
say if an interviewer asked *"walk me through something you built"* and keep them in the README.
