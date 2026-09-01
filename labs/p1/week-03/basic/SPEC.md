# `basic` — LAB-P1-W03

**For:** you have not done this before. About 60% of the code is written; the gaps are marked
`TODO`. Every TODO has a one-line hint above it.

**Time box:** 2 h

## What you must make true

- Implement `Account` and `Transaction` in `starter/ledger/models.py` against the provided tests.
- `Account(id: str, name: str, kind: AccountKind)`; `kind` is an enum of `ASSET`, `LIABILITY`,
  `EQUITY`, `INCOME`, `EXPENSE`.
- `Money` wraps an integer number of minor units plus a 3-letter currency code. Arithmetic across
  currencies raises `CurrencyMismatch`.
- `Transaction` holds a date, a description and at least two `Posting`s; it raises `Unbalanced`
  if the postings do not sum to zero.

## Acceptance

```bash
make verify TRACK=basic
```

Green means every `TODO` in the files listed above is filled in correctly.

## Hints are not cheating here

The point of `basic` is to see the shape of a correct solution while typing it. If you finish in
under half the time box, do `standard` from an empty file — that is where the learning is.
