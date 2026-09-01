# `standard` — LAB-P3-W21

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 7-9 h

## Acceptance criteria

- A reverse-mode autograd engine: a `Value` (or `Tensor`) type recording a computation graph,
  with `backward()` performing a topological-order reverse pass.
- Supported ops with correct gradients: `+ - * / **`, `exp`, `log`, `tanh`, `relu`, `sum`,
  `mean`, matmul.
- Gradient accumulation done right: a value used twice must receive both contributions. The
  classic bug is `grad = ...` instead of `grad += ...`; there is a test for exactly that.
- Modules: `Linear`, `ReLU`, `Softmax`, `CrossEntropyLoss`, `Sequential`, each with `parameters()`.
- Optimizers: `SGD` (with momentum) and `Adam`, both matching a reference update rule.
- `zero_grad()` that actually zeroes, tested by running two steps and checking the second step's
  gradients do not include the first's.
- A `gradcheck(f, inputs)` utility using central differences, with relative error below 1e-6 on
  every op — this is the test that makes the whole thing trustworthy.
- Trained on MNIST to >= 95% test accuracy, with the training curve committed.
- No PyTorch, no TensorFlow, no JAX anywhere in the implementation.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Two things that will cost you an afternoon if nobody tells you:

1. **The topological sort must be over the graph reachable from the output**, and each node
   visited once. Recursing without a visited set on a diamond-shaped graph gives you exponential
   time and, worse, doubled gradients.
2. **Softmax + cross-entropy should be fused.** Computing them separately is numerically unstable
   and the gradient is a mess; fused, the gradient is `(p - y)` and it is three lines.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
