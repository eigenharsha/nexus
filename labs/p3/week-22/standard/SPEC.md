# `standard` — LAB-P3-W22

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 7-8 h

## Acceptance criteria

- A dataset audit first: class balance, duplicates, near-duplicates across the train/test split,
  corrupt files, and label spot-checks. Report what you found before you train anything.
- An augmentation policy chosen for this domain and justified — and one you rejected, with the
  reason (horizontal flip is fine for cells; it is not fine for text).
- A custom CNN baseline trained from scratch, then transfer learning from a pretrained backbone
  (ResNet-18 or EfficientNet-B0), with the frozen/unfrozen schedule documented.
- >= 90% test accuracy on the held-out split.
- Mixed precision (AMP) where a GPU is present, with the CPU path still correct.
- Checkpointing that resumes correctly mid-epoch.
- Per-class precision/recall/F1, a confusion matrix, and an error analysis of the 20 worst
  misclassifications with a written pattern.
- A model card.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

The dataset audit is not a formality. Near-duplicate leakage across a train/test split is the
single most common reason a medical-imaging model reports 97% and delivers 70%. Do the check
before you spend an evening training.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
