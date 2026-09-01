# `standard` — LAB-P2-W16

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 6-7 h

## Acceptance criteria

- A CLI: `eda report data.parquet --target churned --out report.html`.
- Report sections: schema and dtypes, missingness (count, %, pattern), per-column distributions,
  outliers by IQR and by z-score with the disagreement flagged, correlation matrix (Pearson and
  Spearman), and target relationships per feature.
- **Leakage warnings**: a feature with near-perfect correlation to the target, a feature that is
  constant within target groups, an ID-like column with high cardinality, a datetime feature that
  post-dates the target, and duplicated rows across a train/test split if one is supplied.
- A written summary section generated from the findings, in plain sentences.
- Tested on three structurally different datasets (wide, tall, mixed-type).

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

The leakage checks are the product. Everything else in this tool exists in five libraries
already; the reason to build it is that none of them will tell you your `account_closed_date`
column is the target in disguise.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
