# `standard` — LAB-P1-W03

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 5-6 h

## Acceptance criteria

- Full package: `models`, `errors`, `storage`, `ledger`.
- Validation lives in `__post_init__` / properties, not in the caller. Invalid objects cannot exist.
- Custom exception hierarchy rooted at `LedgerError`: `Unbalanced`, `CurrencyMismatch`,
  `UnknownAccount`, `DuplicateTransaction`, `StorageError`.
- A `Storage` **`Protocol`** with two implementations: `MemoryStorage` and `JsonFileStorage`.
  The core `Ledger` class depends only on the Protocol.
- `Ledger.post(txn)` is idempotent on transaction id: posting the same id twice raises
  `DuplicateTransaction` and leaves state unchanged.
- `Ledger.balance(account_id)` and `Ledger.trial_balance()` — the latter must sum to zero, always.
- `mypy --strict` clean. `ruff check` clean.
- Meaningful coverage above 90%: no test that only calls a getter.
- Installable: `uv pip install -e .` works from `pyproject.toml`.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Two design calls to defend in your README:

1. **Why `Protocol` and not an ABC?** Structural typing means `JsonFileStorage` never imports the
   core module, so the dependency arrow points one way only. An ABC would invert it.
2. **Where does the "balanced" invariant live?** In `Transaction.__post_init__`, not in
   `Ledger.post`. If it lives in the ledger, an unbalanced `Transaction` object can exist in
   memory and someone will eventually serialize one.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
