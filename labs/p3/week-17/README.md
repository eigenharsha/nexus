# LAB-P3-W17 — `scratchml`: regression & classification from NumPy

> Week 17 · Phase 3 · Machine Learning · time box: **10-12 h**
> Language: python · `make verify` grades you · no instructor required

> **Status: verified.** `starter/`, `solution/` and the test suite are complete and were
> actually run to produce the output in *Verify* below. `make contract` passes on all three
> tracks: green on `solution/`, red on `starter/`.

## The ticket

Two of our production models are "linear regression" and nobody can tell you what the
regularization parameter is doing, why the loss diverged after last month's feature change, or
whether the features were standardized before or after the train/test split. (It was after. That
is why the offline numbers were wrong.)

Rebuild both from NumPy so the answers live in code you wrote, and prove them equal to
scikit-learn on three datasets.

## What "done" looks like

- Coefficients match scikit-learn within tolerance on three datasets.
- The analytic gradient passes a numerical gradient check.
- You can explain, from your own code, exactly what `C` and `alpha` do.

## Tracks

Pick the one that matches where you are. You can climb mid-lab; the tests for the lower track
keep passing.

| Track | You get | You write | Spec |
|---|---|---|---|
| `basic` | ~60% of the code, TODOs marked | the marked TODOs | [basic/SPEC.md](basic/SPEC.md) |
| `standard` | a spec and a test suite | the implementation | [standard/SPEC.md](standard/SPEC.md) |
| `hard` | the same spec plus a constraint the standard solution fails | a better implementation | [hard/SPEC.md](hard/SPEC.md) |

## Getting started

```bash
cd labs/p3/week-17
make help                    # what this lab can do
cat standard/SPEC.md         # the acceptance criteria
$EDITOR starter/             # your work goes here
make verify                  # TRACK=standard against starter/  -> red until you finish
make verify TRACK=basic      # the scaffolded track
make verify IMPL=solution    # proves the tests are honest
make contract                # asserts solution green AND starter red
```

You edit **`starter/`**. `basic/`, `standard/` and `hard/` hold the specs and any track-specific
scaffolding; `solution/` is the reference. Open `solution/` only after you have a failing
attempt of your own — reading it first converts a 6-hour skill into a 6-minute read.

## Verify — real output from this repo

```
$ make verify IMPL=solution TRACK=hard
==> LAB-P3-W17 · track=hard · impl=solution
........................                                                 [100%]
24 passed in 6.92s

$ make verify        # starter/, standard track
FAILED tests/test_scratchml.py::test_no_python_loop_over_samples_in_fit - Not...
FAILED tests/test_scratchml.py::test_fit_rejects_mismatched_shapes - NotImple...
FAILED tests/test_scratchml.py::test_r2_matches_sklearn_on_a_real_dataset - N...
20 failed, 4 deselected in 1.10s
make[1]: *** [_verify_impl] Error 1
make: *** [verify] Error 2

$ make contract TRACK=hard
==> contract check: LAB-P3-W17 track=hard
  PASS  solution/ is green
  PASS  starter/ is red (as it must be)
contract holds
```
24 tests green on `solution/` at the `hard` track. The claims that matter:

| Comparison | Measured |
|---|---|
| OLS coefficients vs `sklearn.LinearRegression` | max diff **8.5e-14** |
| Ridge coefficients vs `sklearn.Ridge` (alpha = 0.5, 3, 25) | max diff **4.3e-14** |
| Logistic coefficients vs `sklearn.LogisticRegression` (synthetic) | max diff **2.3e-4** |
| Logistic predicted probabilities, 3 datasets | max diff **< 5e-3** |
| Analytic vs central-difference gradient | relative error **1.1e-10** |
| Softmax label agreement with sklearn, 4 classes | **100.0%** |

## Measured — `make bench IMPL=solution`

**Iterations vs agreement** (breast_cancer, 569 x 30, standardized, C = 1.0):

| max_iter | iterations run | wall (s) | max abs coef diff | max abs prob diff |
|---|---|---|---|---|
| 100 | 100 | 0.00 | 7.7e-01 | 3.7e-01 |
| 1,000 | 1,000 | 0.04 | 2.2e-01 | 6.2e-02 |
| 10,000 | 10,000 | 0.39 | 1.5e-02 | 3.7e-03 |
| 50,000 | 18,902 (converged) | 0.70 | 1.6e-02 | 3.7e-03 |
| 200,000 | 18,902 (converged) | 0.70 | 1.6e-02 | 3.7e-03 |

Read the last three rows carefully, because this is the thing that makes people think they
have a bug when they do not. Gradient descent converges — the objective stops moving at
18,902 iterations and running 10x longer changes nothing — and the coefficients still differ
from L-BFGS by 1.6e-2.

They are not wrong. The test evaluates **both** parameter vectors under our objective:

```
loss(ours)        = 0.066360186
loss(scikit-learn)= 0.066362418
```

Ours is *lower*. The remaining coefficient difference is the flatness of the optimum on a
nearly-separable dataset: a large move in parameter space costs almost nothing in loss. That
is why the standard-track test asserts the objective comparison as well as a tolerance — a
tolerance alone would either be too tight to pass or too loose to mean anything.

**Optimizers on the same problem** (n = 20,000, d = 20, standardized):

| solver | iterations | wall (s) | R² | gap to closed form |
|---|---|---|---|---|
| closed form | 1 | — | 0.999241 | — |
| full-batch GD | 15 | 0.01 | 0.999241 | 0 |
| mini-batch (256) | 200 | 0.40 | 0.999241 | 3.5e-08 |
| SGD | 30 | 1.88 | 0.999241 | 3.1e-08 |

Full-batch GD converges in 15 iterations here because the step size is derived from the
Lipschitz constant (`lr = 1/L`, `L = 2·‖X‖₂²`) rather than hand-tuned. That is also why no
test in this lab ever sees a `nan` loss — the "my loss diverged after the feature change"
symptom in the ticket is almost always a learning rate that was tuned for the old feature
scaling.

**Softmax convergence** (2,000 rows, 8 features, 4 classes):

| solver | epochs | wall (s) | label agreement with sklearn | accuracy |
|---|---|---|---|---|
| mini-batch | 400 | 0.15 | 92.0% | 0.5225 |
| mini-batch | 2,000 | 0.79 | 93.6% | 0.5330 |
| full-batch GD | 20,000 | 5.38 | 100.0% | 0.5350 |

scikit-learn's accuracy on the same data is 0.5350. Mini-batch at 400 epochs is 36x faster and
agrees on 92% of labels; whether that gap matters is a product question, not a maths question,
and this table is how you'd answer it.


## Ship it

Repo plus a blog-style derivation write-up: the loss, the gradient, and the three lines of
algebra between them. Excellent interview and LinkedIn artifact.

A lab never ends at "it printed the right thing".

## Rubric

See [RUBRIC.md](RUBRIC.md). Grade yourself before you look at `solution/`.

## If you get stuck

1. Twenty minutes stuck, then read the *Common mistakes* table in the week's module pages.
2. Then re-read Layer 1 of the module this lab tests.
3. Then `solution/`, one function at a time — and delete-and-rewrite the function you read.
