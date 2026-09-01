# `standard` — LAB-P4-W25

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 8-10 h

## Acceptance criteria

- Train your own byte-level BPE tokenizer on a corpus: merge training, encode, decode, special
  tokens, and exact round-trip on arbitrary UTF-8 including emoji and unpaired surrogates.
- A full causal Transformer: scaled dot-product attention with the causal mask, multi-head
  attention, an MLP block, layer norm placed deliberately (pre-norm, and say why), residual
  connections, a block, a stack, and an LM head with weight tying.
- Every component unit-tested against the `torch.nn` equivalent given identical weights, to 1e-5.
- Trained on a small corpus to a stated loss, with generated samples committed.
- KV-cached generation producing **token-identical** output to the uncached path, with the
  speedup measured at three sequence lengths.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

The KV-cache identity test is the one worth writing first. Cached and uncached generation
diverging at token 40 is the classic symptom of an off-by-one in the position index, and it is
invisible until you diff the two sequences.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
