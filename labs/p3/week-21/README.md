# LAB-P3-W21 — `nanograd`: autograd + neural net from scratch

> Week 21 · Phase 3 · Machine Learning · time box: **12-15 h**
> Language: python · `make verify` grades you · no instructor required

> **Status: verified.** `starter/`, `solution/` and the test suite are complete and were
> actually run to produce the output in *Verify* below. `make contract` passes on all three
> tracks: green on `solution/`, red on `starter/`.

## The ticket

Next week you start using PyTorch. From then on, every bug you hit lives somewhere between
your loss function and a C++ kernel you will never read, and "the loss is nan" will be a
four-hour afternoon unless you already know what is underneath.

Build the engine first. Reverse-mode autograd, the layers, the optimizers, trained to 95% on
MNIST, with a gradient check that proves every backward pass. After this, nothing in Phase 4 is
magic.

## What "done" looks like

- Every backward pass passes a numerical gradient check to 1e-6 relative error.
- A network trained end to end with your own optimizer, no framework.
- You can draw the computation graph for a two-layer MLP from memory.

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
cd labs/p3/week-21
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
==> LAB-P3-W21 · track=hard · impl=solution
.............................s                                           [100%]
=============================== warnings summary ===============================
tests/test_nanograd.py::test_trains_a_classifier_to_95_percent

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
SKIPPED [1] tests/test_nanograd.py:413: PyTorch not installed — parity test skipped
29 passed, 1 skipped, 1 warning in 1.58s

$ make verify        # starter/, standard track
FAILED tests/test_nanograd.py::test_sgd_with_momentum_matches_the_reference_update
FAILED tests/test_nanograd.py::test_adam_matches_the_reference_update_including_bias_correction
FAILED tests/test_nanograd.py::test_trains_a_classifier_to_95_percent - NotIm...
25 failed, 1 passed, 4 deselected, 1 warning in 0.86s
make[1]: *** [_verify_impl] Error 1
make: *** [verify] Error 2

$ make contract TRACK=hard
==> contract check: LAB-P3-W21 track=hard
  PASS  solution/ is green
  PASS  starter/ is red (as it must be)
contract holds
```
29 tests green on `solution/` at the `hard` track; one skipped (PyTorch parity, which
needs `torch` installed — `./bootstrap.sh` installs it in week 21). 25 failed on `starter/`.

## What the gradcheck actually covers

`make verify TRACK=standard` runs `gradcheck` — analytic gradient against a central
difference, max relative error — over thirteen expressions:

```
add  sub  mul  div  pow  exp  log  tanh  relu  sigmoid  matmul  mean  chain
```

Every one is below **1e-6** relative error. That is what makes the rest of the lab
trustworthy: a wrong gradient still trains, badly, and looks exactly like a bad learning
rate. `gradcheck` turns a lost evening into a named failing test.

Three failure modes get their own test, because each one is silent:

| Bug | Test |
|---|---|
| `grad = ...` instead of `grad += ...` | `test_gradients_accumulate_when_a_value_is_used_twice` |
| Topological sort without a visited set (doubled gradients on a diamond) | `test_diamond_graph_visits_each_node_once` |
| `zero_grad()` that does not zero | `test_zero_grad_actually_zeroes` |

The optimizer tests check the update rule arithmetic step by step against the reference
recurrences, so "it trains" is not enough — SGD's momentum convention and Adam's bias
correction both have to be right.

## Measured — training MNIST on pure NumPy

`python solution/train_mnist.py` — 59,500 train / 10,500 test, 784-256-128-10 with ReLU,
Adam at lr 1e-3, batch 128, on an Apple M2 CPU:

```
 epoch  train loss  test acc  wall (s)
     1      0.2588    0.9561       1.8
     2      0.0908    0.9645       2.7
     5      0.0287    0.9688       5.4
    10      0.0199    0.9694       9.4
    14      0.0094    0.9756      12.6
    20      0.0093    0.9729      17.4

final test accuracy: 0.9729
```

**95.6% after one epoch and 1.8 seconds**, 97.3% at twenty epochs and 17.4 seconds — with
no framework, on a laptop CPU. Worth sitting with: the reason deep learning needs GPUs is
not MNIST-sized models, it is the 10,000x more parameters and 1,000x more data that came
after. The mechanism you just wrote is the same one.

The acceptance test uses scikit-learn's bundled 8x8 digits instead (no download, runs in
1.6 s, same code path) and asserts >= 95%; it measures 97.3% there too.

## Measured — gradient checkpointing

`make verify TRACK=hard` reports the retained graph, which is the quantity checkpointing
actually reduces — 16 layers of 256x256 at batch 512, split into 4 segments of 4:

```
retained graph: 43.0 MB / 50 nodes  ->  5.2 MB / 6 nodes  (88% saved)
```

Gradients are identical to 1e-8 either way; the cost is one extra forward pass per segment.

The finding worth writing down: **checkpointing one monolithic block saves nothing.** The
recompute materialises every activation anyway. The saving comes from segmentation, and the
number of segments is the knob — `sqrt(depth)` segments is the classic choice, giving
O(sqrt(n)) memory for one extra forward pass.


## Ship it

Repo plus a "how backprop actually works" explainer built from your own diagrams. One of the
two strongest portfolio pieces in the course.

A lab never ends at "it printed the right thing".

## Rubric

See [RUBRIC.md](RUBRIC.md). Grade yourself before you look at `solution/`.

## If you get stuck

1. Twenty minutes stuck, then read the *Common mistakes* table in the week's module pages.
2. Then re-read Layer 1 of the module this lab tests.
3. Then `solution/`, one function at a time — and delete-and-rewrite the function you read.
