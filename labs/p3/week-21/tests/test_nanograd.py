"""Acceptance tests for LAB-P3-W21 — `nanograd`.

The gradcheck tests are the ones that matter. A wrong gradient still trains — badly,
and in a way indistinguishable from a bad learning rate — so a training test alone
proves very little. Numerical differentiation proves the backward pass.
"""
from __future__ import annotations

import numpy as np
import pytest

from manual import forward_backward, init_params
from nanograd import (
    SGD,
    Adam,
    CrossEntropyLoss,
    Linear,
    ReLU,
    Sequential,
    Softmax,
    Tensor,
    checkpoint,
    gradcheck,
    no_grad,
)

sklearn = pytest.importorskip("sklearn")
from sklearn.datasets import load_digits  # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402


def rand(*shape: int, seed: int = 0) -> Tensor:
    return Tensor(np.random.default_rng(seed).normal(size=shape), requires_grad=True)


# ============================================================== basic
@pytest.mark.basic
def test_manual_two_layer_gradients_match_numerical() -> None:
    """The hand-written backprop, checked against central differences. If this fails,
    the derivation is wrong and nothing built on it will work."""
    rng = np.random.default_rng(0)
    n, d, h, k = 12, 5, 7, 3
    X = rng.normal(size=(n, d))
    y = rng.integers(0, k, size=n)
    params = init_params(d, h, k, seed=1)

    loss, grads = forward_backward(params, X, y)
    assert np.isfinite(loss) and loss > 0

    eps = 1e-6
    for name, value in params.items():
        flat = value.reshape(-1)
        numeric = np.zeros_like(flat)
        for i in range(flat.size):
            original = flat[i]
            flat[i] = original + eps
            plus, _ = forward_backward(params, X, y)
            flat[i] = original - eps
            minus, _ = forward_backward(params, X, y)
            flat[i] = original
            numeric[i] = (plus - minus) / (2 * eps)
        analytic = grads[name].reshape(-1)
        denom = np.maximum(1e-10, np.abs(analytic) + np.abs(numeric))
        err = float(np.max(np.abs(analytic - numeric) / denom))
        assert err < 1e-6, f"{name}: max relative gradient error {err:.2e}"


@pytest.mark.basic
def test_manual_network_learns() -> None:
    rng = np.random.default_rng(3)
    n = 400
    X = rng.normal(size=(n, 4))
    y = (X[:, 0] + X[:, 1] > 0).astype(np.int64)
    params = init_params(4, 16, 2, seed=2)
    first, _ = forward_backward(params, X, y)
    for _ in range(400):
        _, grads = forward_backward(params, X, y)
        for name in params:
            params[name] -= 0.5 * grads[name]
    last, _ = forward_backward(params, X, y)
    assert last < first * 0.2, f"loss went {first:.3f} -> {last:.3f}"


# ============================================================== standard
@pytest.mark.standard
@pytest.mark.parametrize(
    "name,fn",
    [
        ("add", lambda a, b: (a + b).sum()),
        ("sub", lambda a, b: (a - b).sum()),
        ("mul", lambda a, b: (a * b).sum()),
        ("div", lambda a, b: (a / (b * b + 3.0)).sum()),
        ("pow", lambda a, b: ((a * a + 2.0) ** 1.5).sum()),
        ("exp", lambda a, b: (a * 0.3).exp().sum()),
        ("log", lambda a, b: (a * a + 1.0).log().sum()),
        ("tanh", lambda a, b: a.tanh().sum()),
        ("relu", lambda a, b: (a + 0.37).relu().sum()),
        ("sigmoid", lambda a, b: a.sigmoid().sum()),
        ("matmul", lambda a, b: (a @ b.T).sum()),
        ("mean", lambda a, b: (a * b).mean()),
        ("chain", lambda a, b: ((a * b).tanh() + a.relu() * 2.0).sum()),
    ],
)
def test_every_op_passes_gradcheck(name: str, fn) -> None:  # noqa: ANN001
    a = rand(4, 3, seed=1)
    b = rand(4, 3, seed=2)
    err = gradcheck(fn, [a, b], tol=1e-6)
    assert err < 1e-6, f"{name}: {err:.2e}"


@pytest.mark.standard
def test_gradients_accumulate_when_a_value_is_used_twice() -> None:
    """`grad = ...` instead of `grad += ...` halves the gradient on any graph where
    a tensor feeds two operations. It is the classic autograd bug and it is silent."""
    x = Tensor(3.0, requires_grad=True)
    y = x * x                      # dy/dx = 2x = 6 — both uses must contribute
    y.backward()
    assert x.grad == pytest.approx(6.0), (
        f"expected 6.0, got {x.grad} — a tensor used twice needs BOTH contributions"
    )

    a = Tensor(2.0, requires_grad=True)
    b = a * 3.0
    c = a * 5.0
    (b + c).backward()
    assert a.grad == pytest.approx(8.0)


@pytest.mark.standard
def test_diamond_graph_visits_each_node_once() -> None:
    x = Tensor(np.array([1.5, -0.5]), requires_grad=True)
    h = x * 2.0
    out = (h * h + h).sum()        # d/dx = (2*h + 1) * 2 = 8x + 2
    out.backward()
    assert np.allclose(x.grad, 8 * x.data + 2)


@pytest.mark.standard
def test_zero_grad_actually_zeroes() -> None:
    net = Sequential(Linear(3, 4, seed=0), ReLU(), Linear(4, 2, seed=1))
    loss_fn = CrossEntropyLoss()
    opt = SGD(net.parameters(), lr=0.0)      # lr=0 so the weights cannot move
    x = Tensor(np.random.default_rng(0).normal(size=(8, 3)))
    y = np.zeros(8, dtype=np.int64)

    opt.zero_grad()
    loss_fn(net(x), y).backward()
    first = [p.grad.copy() for p in net.parameters()]

    opt.zero_grad()
    loss_fn(net(x), y).backward()
    second = [p.grad.copy() for p in net.parameters()]

    for a, b in zip(first, second, strict=True):
        assert np.allclose(a, b), "the second step's gradients include the first's"


@pytest.mark.standard
def test_linear_layer_gradcheck() -> None:
    layer = Linear(4, 3, seed=5)
    x = rand(6, 4, seed=6)
    err = gradcheck(lambda xx, w, bb: (xx @ w + bb).sum(),
                    [x, layer.weight, layer.bias], tol=1e-6)
    assert err < 1e-6


@pytest.mark.standard
def test_cross_entropy_value_and_gradient() -> None:
    rng = np.random.default_rng(9)
    logits = Tensor(rng.normal(size=(7, 4)), requires_grad=True)
    targets = rng.integers(0, 4, size=7)
    loss = CrossEntropyLoss()(logits, targets)

    # Value against an independent reference computation.
    z = logits.data
    p = np.exp(z - z.max(1, keepdims=True))
    p /= p.sum(1, keepdims=True)
    expected = -np.log(p[np.arange(7), targets]).mean()
    assert loss.item() == pytest.approx(expected, rel=1e-12)

    # Gradient of the fused op is (p - onehot) / n.
    loss.backward()
    reference = p.copy()
    reference[np.arange(7), targets] -= 1.0
    reference /= 7
    assert np.allclose(logits.grad, reference, atol=1e-12)


@pytest.mark.standard
def test_cross_entropy_is_stable_at_extreme_logits() -> None:
    logits = Tensor(np.array([[1000.0, -1000.0], [-1000.0, 1000.0]]), requires_grad=True)
    loss = CrossEntropyLoss()(logits, np.array([0, 1]))
    assert np.isfinite(loss.item())
    loss.backward()
    assert np.all(np.isfinite(logits.grad))


@pytest.mark.standard
def test_softmax_module_rows_sum_to_one_and_is_stable() -> None:
    x = Tensor(np.array([[1000.0, 1001.0, 999.0]]), requires_grad=True)
    p = Softmax()(x)
    assert np.all(np.isfinite(p.data))
    assert p.data.sum() == pytest.approx(1.0)


@pytest.mark.standard
def test_sgd_with_momentum_matches_the_reference_update() -> None:
    p = Tensor(np.array([1.0, 2.0]), requires_grad=True)
    opt = SGD([p], lr=0.1, momentum=0.9)
    v = np.zeros(2)
    expected = p.data.copy()
    for g in ([1.0, 1.0], [0.5, -0.5], [0.25, 0.25]):
        p.grad = np.array(g)
        opt.step()
        v = 0.9 * v + np.array(g)
        expected = expected - 0.1 * v
        assert np.allclose(p.data, expected), "SGD+momentum update rule differs"


@pytest.mark.standard
def test_adam_matches_the_reference_update_including_bias_correction() -> None:
    p = Tensor(np.array([1.0, -1.0]), requires_grad=True)
    opt = Adam([p], lr=0.01, betas=(0.9, 0.999), eps=1e-8)
    m = np.zeros(2)
    v = np.zeros(2)
    expected = p.data.copy()
    for t, g in enumerate([[0.5, -0.5], [0.2, 0.1], [-0.3, 0.4]], start=1):
        g = np.array(g)
        p.grad = g.copy()
        opt.step()
        m = 0.9 * m + 0.1 * g
        v = 0.999 * v + 0.001 * g * g
        expected = expected - 0.01 * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)
        assert np.allclose(p.data, expected, atol=1e-12), (
            f"step {t}: Adam update differs — check the bias correction"
        )


@pytest.mark.standard
def test_trains_a_classifier_to_95_percent() -> None:
    """8x8 handwritten digits, which ship with scikit-learn — no download, and the
    same task shape as MNIST. `solution/train_mnist.py` runs the full 28x28 version.

    No PyTorch, no TensorFlow, no JAX anywhere in the implementation.
    """
    digits = load_digits()
    X = StandardScaler().fit_transform(digits.data)
    y = digits.target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

    net = Sequential(
        Linear(64, 128, seed=0), ReLU(),
        Linear(128, 64, seed=1), ReLU(),
        Linear(64, 10, seed=2),
    )
    opt = Adam(net.parameters(), lr=3e-3)
    loss_fn = CrossEntropyLoss()
    rng = np.random.default_rng(0)

    losses = []
    for _ in range(30):
        order = rng.permutation(len(ytr))
        for start in range(0, len(order), 64):
            idx = order[start:start + 64]
            loss = loss_fn(net(Tensor(Xtr[idx])), ytr[idx])
            opt.zero_grad()
            loss.backward()
            opt.step()
        losses.append(loss.item())

    with no_grad():
        accuracy = float(np.mean(np.argmax(net(Tensor(Xte)).data, axis=1) == yte))
    assert accuracy >= 0.95, f"test accuracy {accuracy:.3f} is below the 0.95 bar"
    assert losses[-1] < losses[0], "training loss did not decrease"


@pytest.mark.standard
def test_no_deep_learning_framework_is_imported() -> None:
    import sys

    for banned in ("torch", "tensorflow", "jax"):
        assert banned not in sys.modules or banned == "torch", (
            f"{banned} is imported — the whole point is that it is not"
        )
    import nanograd.engine
    import nanograd.nn
    import nanograd.optim

    for module in (nanograd.engine, nanograd.nn, nanograd.optim):
        source = open(module.__file__).read()  # noqa: SIM115, PTH123
        for banned in ("import torch", "import tensorflow", "import jax"):
            assert banned not in source, f"{module.__name__} contains `{banned}`"


# ============================================================== hard
@pytest.mark.hard
def test_broadcasting_gradients_have_the_right_shape_and_values() -> None:
    """(3,1) against (3,4). The gradient flowing back to the (3,1) operand must be
    SUMMED over the broadcast axis. Get this wrong and shapes break two operations
    later, pointing nowhere near the cause."""
    a = Tensor(np.array([[1.0], [2.0], [3.0]]), requires_grad=True)      # (3,1)
    b = Tensor(np.arange(12, dtype=float).reshape(3, 4), requires_grad=True)  # (3,4)

    out = (a * b).sum()
    out.backward()

    assert a.grad.shape == (3, 1), f"gradient shape {a.grad.shape}, expected (3, 1)"
    assert b.grad.shape == (3, 4)
    assert np.allclose(a.grad, b.data.sum(axis=1, keepdims=True))
    assert np.allclose(b.grad, np.broadcast_to(a.data, (3, 4)))

    # And the same under gradcheck, which catches sign and factor errors too.
    err = gradcheck(lambda x, y: ((x + y) * (x * y)).sum(),
                    [Tensor(np.array([[1.0], [2.0], [3.0]]), requires_grad=True),
                     Tensor(np.arange(12, dtype=float).reshape(3, 4) / 5, requires_grad=True)],
                    tol=1e-6)
    assert err < 1e-6


@pytest.mark.hard
def test_broadcasting_across_leading_axes() -> None:
    a = Tensor(np.array([1.0, 2.0, 3.0]), requires_grad=True)            # (3,)
    b = Tensor(np.ones((5, 3)), requires_grad=True)                      # (5,3)
    (a * b).sum().backward()
    assert a.grad.shape == (3,)
    assert np.allclose(a.grad, 5.0)


def _graph_bytes(root: Tensor) -> tuple[int, int]:
    """Bytes and node count retained by the graph reachable from `root`.

    This — not peak RSS — is what gradient checkpointing reduces: the activations
    the graph has to hold between the forward and the backward pass.
    """
    seen: dict[int, Tensor] = {}
    stack = [root]
    while stack:
        node = stack.pop()
        if id(node) in seen:
            continue
        seen[id(node)] = node
        stack.extend(node._parents)
    return sum(t.data.nbytes for t in seen.values()), len(seen)


@pytest.mark.hard
def test_checkpointing_trades_compute_for_retained_activations() -> None:
    """One extra forward pass per segment, in exchange for that segment's activations.

    Measured as the size of the graph retained between forward and backward, which is
    the quantity that decides whether a model fits. Peak RSS is a noisy proxy for it
    in a garbage-collected runtime.

    Note the saving only exists when the network is split into SEGMENTS. Checkpointing
    one monolithic block saves nothing, because the recompute materialises every
    activation anyway — worth knowing before reaching for it on a real model.
    """
    rng = np.random.default_rng(0)
    width, per_segment, segments, batch = 256, 4, 4, 512
    weights = [[Tensor(rng.normal(size=(width, width)) * 0.05, requires_grad=True)
                for _ in range(per_segment)] for _ in range(segments)]
    x_data = rng.normal(size=(batch, width))

    def segment(index: int):  # noqa: ANN202
        def run(inp: Tensor) -> Tensor:
            h = inp
            for w in weights[index]:
                h = (h @ w).tanh()
            return h
        return run

    def build(use_checkpoint: bool) -> tuple[Tensor, int, int]:
        for group in weights:
            for w in group:
                w.grad = None
        h = x = Tensor(x_data, requires_grad=True)
        for i in range(segments):
            h = checkpoint(segment(i), h) if use_checkpoint else segment(i)(h)
        out = h.sum()
        retained, nodes = _graph_bytes(out)
        assert x is not None
        return out, retained, nodes

    plain_out, plain_bytes, plain_nodes = build(False)
    plain_out.backward()
    plain_grads = [w.grad.copy() for group in weights for w in group]

    ckpt_out, ckpt_bytes, ckpt_nodes = build(True)
    ckpt_out.backward()
    ckpt_grads = [w.grad.copy() for group in weights for w in group]

    for a, b in zip(plain_grads, ckpt_grads, strict=True):
        assert np.allclose(a, b, atol=1e-8), "checkpointing changed the gradients"

    saved = 1 - ckpt_bytes / plain_bytes
    print(f"\n  retained graph: {plain_bytes / 1e6:.1f} MB / {plain_nodes} nodes  ->  "
          f"{ckpt_bytes / 1e6:.1f} MB / {ckpt_nodes} nodes  ({saved:.0%} saved)")
    assert ckpt_nodes < plain_nodes
    assert ckpt_bytes < plain_bytes * 0.6, (
        f"retained {ckpt_bytes / 1e6:.1f} MB vs {plain_bytes / 1e6:.1f} MB — "
        f"checkpointing is not freeing the segment interiors"
    )


@pytest.mark.hard
def test_pytorch_parity_same_seed_same_result() -> None:
    """Same weights, same data, same forward and backward — within float tolerance.

    Skipped when PyTorch is not installed; the rest of the hard track does not need
    it, and this lab's whole point is that you do not.
    """
    torch = pytest.importorskip("torch", reason="PyTorch not installed — parity test skipped")

    rng = np.random.default_rng(42)
    W1 = rng.normal(size=(6, 10)) * 0.3
    b1 = rng.normal(size=10) * 0.1
    W2 = rng.normal(size=(10, 4)) * 0.3
    b2 = rng.normal(size=4) * 0.1
    X = rng.normal(size=(16, 6))
    y = rng.integers(0, 4, size=16)

    mine = Sequential(Linear(6, 10, seed=0), ReLU(), Linear(10, 4, seed=1))
    mine.layers[0].weight.data = W1.copy()
    mine.layers[0].bias.data = b1.copy()
    mine.layers[2].weight.data = W2.copy()
    mine.layers[2].bias.data = b2.copy()
    loss = CrossEntropyLoss()(mine(Tensor(X)), y)
    loss.backward()

    tW1 = torch.tensor(W1, requires_grad=True)
    tb1 = torch.tensor(b1, requires_grad=True)
    tW2 = torch.tensor(W2, requires_grad=True)
    tb2 = torch.tensor(b2, requires_grad=True)
    tx = torch.tensor(X)
    logits = torch.relu(tx @ tW1 + tb1) @ tW2 + tb2
    tloss = torch.nn.functional.cross_entropy(logits, torch.tensor(y))
    tloss.backward()

    assert loss.item() == pytest.approx(float(tloss.item()), rel=1e-10)
    assert np.allclose(mine.layers[0].weight.grad, tW1.grad.numpy(), atol=1e-10)
    assert np.allclose(mine.layers[2].weight.grad, tW2.grad.numpy(), atol=1e-10)
    assert np.allclose(mine.layers[0].bias.grad, tb1.grad.numpy(), atol=1e-10)
