# `standard` — LAB-P2-W11

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 6-7 h

## Acceptance criteria

- `Vector` and `Matrix` types with `+ - * @`, indexing, and shape validation.
- L1 / L2 / L-inf norms; cosine similarity.
- Gauss-Jordan inverse with partial pivoting; a singular matrix raises, not returns garbage.
- Power iteration for the dominant eigenvalue/eigenvector, with a convergence criterion you chose.
- PCA via SVD, validated against `sklearn.decomposition.PCA` on the same data (signs may differ —
  handle that in the test, not by fudging).
- Numerical gradient (central difference) with a documented step size and the error analysis for it.
- A reverse-mode autodiff engine in about 100 lines, supporting `+ * - / ** exp log tanh`.
- Every numeric result tested against NumPy to 1e-6.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Central differences with h = 1e-5 give you about 1e-10 truncation error and about 1e-11
round-off error on doubles — near the sweet spot. h = 1e-12 is worse, not better, and knowing why
is the point of the exercise.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
