# `hard` — LAB-P3-W22

**For:** `standard` is green and you want the interview story. This track adds a constraint
that a straightforward `standard` solution **fails**.

**Time box:** 5-7 h

## Constraint

>= 93% accuracy under the CPU inference-latency budget in `hard/targets.md`, with an ONNX
export and a measured latency/size table.

## Acceptance criteria

- >= 93% test accuracy under the stated CPU latency budget.
- ONNX export with output parity against the PyTorch model to 1e-4.
- A latency/size table: PyTorch eager, TorchScript, ONNX Runtime, and a quantized variant —
  p50/p95 latency and file size for each, measured on CPU.
- Grad-CAM explanations for five predictions, including at least one the model got wrong.

## Acceptance

```bash
make verify TRACK=hard
make bench
```

## The deliverable that matters

A short write-up with **numbers**: what the standard approach measured, what yours measures, and
the sentence explaining why. No number, no credit — that is the rule for every `hard` track in
this course.
