"""Train nanograd on the full 28x28 MNIST. The ship-it deliverable for LAB-P3-W21.

    python solution/train_mnist.py                 # downloads MNIST once via OpenML
    python solution/train_mnist.py --digits        # 8x8 fallback, no network needed

MNIST is ~11 MB and is cached by scikit-learn under ~/scikit_learn_data. If you are
offline, `--digits` runs the same code on the bundled 8x8 digits and the acceptance
test uses that path — the network and the training loop are identical.
"""
from __future__ import annotations

import argparse
import time

import numpy as np

from nanograd import Adam, CrossEntropyLoss, Linear, ReLU, Sequential, Tensor, no_grad


def load(use_digits: bool) -> tuple[np.ndarray, np.ndarray, int]:
    from sklearn.datasets import fetch_openml, load_digits

    if use_digits:
        d = load_digits()
        return d.data.astype(np.float64), d.target.astype(np.int64), 64
    mnist = fetch_openml("mnist_784", version=1, as_frame=False, parser="liac-arff")
    return mnist.data.astype(np.float64), mnist.target.astype(np.int64), 784


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--digits", action="store_true", help="use the bundled 8x8 set")
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--batch-size", type=int, default=128)
    ap.add_argument("--lr", type=float, default=1e-3)
    args = ap.parse_args()

    X, y, n_features = load(args.digits)
    X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)

    rng = np.random.default_rng(0)
    perm = rng.permutation(len(y))
    split = int(len(y) * 0.85)
    tr, te = perm[:split], perm[split:]
    Xtr, ytr, Xte, yte = X[tr], y[tr], X[te], y[te]

    net = Sequential(
        Linear(n_features, 256, seed=0), ReLU(),
        Linear(256, 128, seed=1), ReLU(),
        Linear(128, 10, seed=2),
    )
    opt = Adam(net.parameters(), lr=args.lr)
    loss_fn = CrossEntropyLoss()

    print(f"train {len(ytr)}  test {len(yte)}  features {n_features}")
    print(f"{'epoch':>6} {'train loss':>11} {'test acc':>9} {'wall (s)':>9}")
    began = time.time()
    for epoch in range(1, args.epochs + 1):
        order = rng.permutation(len(ytr))
        running = 0.0
        batches = 0
        for start in range(0, len(order), args.batch_size):
            idx = order[start:start + args.batch_size]
            loss = loss_fn(net(Tensor(Xtr[idx])), ytr[idx])
            opt.zero_grad()
            loss.backward()
            opt.step()
            running += loss.item()
            batches += 1
        with no_grad():
            acc = float(np.mean(np.argmax(net(Tensor(Xte)).data, axis=1) == yte))
        print(f"{epoch:>6} {running / batches:>11.4f} {acc:>9.4f} {time.time() - began:>9.1f}")

    print(f"\nfinal test accuracy: {acc:.4f}")


if __name__ == "__main__":
    main()
