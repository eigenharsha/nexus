"""Storage backends.

`Storage` is a `Protocol`, not an ABC, and that is a deliberate choice worth defending:
structural typing means a backend never has to import anything from the core, so the
dependency arrow points one way only. An ABC would invert it — every backend would
`from ledger.storage import Storage`, and adding a backend would mean touching core.

The proof that this was the right call is the `hard` track: `EventLogStorage` lives in
its own module, imports nothing from `ledger.ledger`, and requires zero changes to it.
"""
from __future__ import annotations

import json
from collections.abc import Iterator
from datetime import date as _date
from pathlib import Path
from typing import Protocol, runtime_checkable

from .errors import StorageError
from .models import Account, AccountKind, Money, Posting, Transaction


@runtime_checkable
class Storage(Protocol):
    """What the ledger needs from a place to put things. Nothing more."""

    def put_account(self, account: Account) -> None: ...
    def get_account(self, account_id: str) -> Account | None: ...
    def accounts(self) -> Iterator[Account]: ...
    def put_transaction(self, txn: Transaction) -> None: ...
    def has_transaction(self, txn_id: str) -> bool: ...
    def transactions(self) -> Iterator[Transaction]: ...


class MemoryStorage:
    """Everything in dicts. Fast, and the one to use in tests."""

    def __init__(self) -> None:
        self._accounts: dict[str, Account] = {}
        self._txns: dict[str, Transaction] = {}

    def put_account(self, account: Account) -> None:
        self._accounts[account.id] = account

    def get_account(self, account_id: str) -> Account | None:
        return self._accounts.get(account_id)

    def accounts(self) -> Iterator[Account]:
        return iter(list(self._accounts.values()))

    def put_transaction(self, txn: Transaction) -> None:
        self._txns[txn.id] = txn

    def has_transaction(self, txn_id: str) -> bool:
        return txn_id in self._txns

    def transactions(self) -> Iterator[Transaction]:
        return iter(list(self._txns.values()))


# --------------------------------------------------------------------------- json
def account_to_dict(a: Account) -> dict[str, str]:
    return {"id": a.id, "name": a.name, "kind": a.kind.value}


def account_from_dict(d: dict[str, str]) -> Account:
    return Account(id=d["id"], name=d["name"], kind=AccountKind(d["kind"]))


def txn_to_dict(t: Transaction) -> dict[str, object]:
    return {
        "id": t.id,
        "date": t.date.isoformat(),
        "description": t.description,
        "postings": [
            {"account_id": p.account_id, "amount": p.amount.amount, "currency": p.amount.currency}
            for p in t.postings
        ],
    }


def txn_from_dict(d: dict[str, object]) -> Transaction:
    raw_postings = d["postings"]
    assert isinstance(raw_postings, list)
    postings = tuple(
        Posting(account_id=str(p["account_id"]), amount=Money(int(p["amount"]), str(p["currency"])))
        for p in raw_postings
    )
    return Transaction(
        id=str(d["id"]),
        date=_date.fromisoformat(str(d["date"])),
        description=str(d["description"]),
        postings=postings,
    )


class JsonFileStorage:
    """A single JSON document on disk, rewritten atomically on every write.

    Atomically: write to a sibling temp file, then `os.replace`. A partial `write()`
    into the real path is how you lose a ledger, and it happens the first time the
    process is killed during a flush.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._accounts: dict[str, Account] = {}
        self._txns: dict[str, Transaction] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            raw = json.loads(self.path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            raise StorageError(f"cannot read {self.path}: {exc}") from exc
        for a in raw.get("accounts", []):
            acc = account_from_dict(a)
            self._accounts[acc.id] = acc
        for t in raw.get("transactions", []):
            txn = txn_from_dict(t)
            self._txns[txn.id] = txn

    def _flush(self) -> None:
        payload = {
            "accounts": [account_to_dict(a) for a in self._accounts.values()],
            "transactions": [txn_to_dict(t) for t in self._txns.values()],
        }
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp.write_text(json.dumps(payload, indent=2, sort_keys=True))
            tmp.replace(self.path)
        except OSError as exc:
            raise StorageError(f"cannot write {self.path}: {exc}") from exc

    def put_account(self, account: Account) -> None:
        self._accounts[account.id] = account
        self._flush()

    def get_account(self, account_id: str) -> Account | None:
        return self._accounts.get(account_id)

    def accounts(self) -> Iterator[Account]:
        return iter(list(self._accounts.values()))

    def put_transaction(self, txn: Transaction) -> None:
        self._txns[txn.id] = txn
        self._flush()

    def has_transaction(self, txn_id: str) -> bool:
        return txn_id in self._txns

    def transactions(self) -> Iterator[Transaction]:
        return iter(list(self._txns.values()))
