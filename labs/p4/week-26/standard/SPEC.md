# `standard` — LAB-P4-W26

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 8-10 h

## Acceptance criteria

- Build a dataset of 500+ examples for a real structured-extraction task, with a documented
  construction process and a held-out split that was never trained on.
- QLoRA fine-tune of a 3B model: 4-bit base, LoRA adapters on the attention and MLP projections,
  with the rank, alpha and target modules chosen and justified.
- >99% schema-valid output on the held-out set, measured by actually parsing and validating
  against the schema — not by eyeballing.
- Merge the adapter and serve via vLLM behind an OpenAI-compatible endpoint.
- Integrate into the Week-6 service, replacing the rule-based path behind a feature flag.
- A documented CPU/Colab fallback path so this lab is completable with no local GPU.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

The memory arithmetic is the part to get right before you start: a 3B model in 4-bit is about
1.7 GB of weights, plus optimizer state for the adapters only (a few hundred MB), plus activations
that scale with batch x sequence length. Work out your batch size on paper first; discovering it
by OOM takes twenty minutes per attempt.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
