# `standard` — LAB-P2-W09

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 6-7 h

## Acceptance criteria

- The full chip set: `Inc16`, `ALU`, `Bit`, `Register`, `RAM8`, `RAM64`, `RAM512`, `RAM4K`,
  `RAM16K`, `PC`.
- Every `.cmp` comparison file matches with zero diffs.
- A gate-count report: total NAND gates per chip, computed by expansion, with the ALU total.
- No chip uses a primitive that is not built from `Nand` somewhere down the tree.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

The ALU's six control bits are the elegant part: `zx nx zy ny f no`. Before you write any HDL,
fill in the truth table by hand for the 18 documented functions. If you can derive `x-y` from the
bits without looking it up, the HDL takes twenty minutes.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
