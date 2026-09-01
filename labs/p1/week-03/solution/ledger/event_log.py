"""`hard` track — a third storage backend, added without touching core.

Append-only: one JSON line per write, state rebuilt by replaying the file on load.
Note what this module imports: models, errors, and the JSON helpers. It does **not**
import `ledger.ledger`, and `ledger.ledger` does not import it. That is the Open/Closed
principle as a fact about the import graph rather than as a claim in a README.
"""
from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

from .errors import StorageError
from .models import Account, Transaction
from .storage import account_from_dict, account_to_dict, txn_from_dict, txn_to_dict


class EventLogStorage:
    """Append-only event log with replay-on-load."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._accounts: dict[str, Account] = {}
        self._txns: dict[str, Transaction] = {}
        self._replay()

    def _replay(self) -> None:
        if not self.path.exists():
            return
        try:
            lines = self.path.read_text().splitlines()
        except OSError as exc:
            raise StorageError(f"cannot read {self.path}: {exc}") from exc
        for lineno, line in enumerate(lines, 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                # A torn final line is the expected failure of an append-only log
                # that was killed mid-write. Anything earlier is real corruption.
                if lineno == len(lines):
                    break
                raise StorageError(f"{self.path}:{lineno}: corrupt event: {exc}") from exc
            kind = event.get("event")
            if kind == "account":
                acc = account_from_dict(event["data"])
                self._accounts[acc.id] = acc
            elif kind == "transaction":
                txn = txn_from_dict(event["data"])
                self._txns[txn.id] = txn
            else:
                raise StorageError(f"{self.path}:{lineno}: unknown event kind {kind!r}")

    def _append(self, kind: str, data: dict[str, object]) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps({"event": kind, "data": data}, sort_keys=True) + "\n")
        except OSError as exc:
            raise StorageError(f"cannot append to {self.path}: {exc}") from exc

    def put_account(self, account: Account) -> None:
        self._accounts[account.id] = account
        self._append("account", dict(account_to_dict(account)))

    def get_account(self, account_id: str) -> Account | None:
        return self._accounts.get(account_id)

    def accounts(self) -> Iterator[Account]:
        return iter(list(self._accounts.values()))

    def put_transaction(self, txn: Transaction) -> None:
        self._txns[txn.id] = txn
        self._append("transaction", txn_to_dict(txn))

    def has_transaction(self, txn_id: str) -> bool:
        return txn_id in self._txns

    def transactions(self) -> Iterator[Transaction]:
        return iter(list(self._txns.values()))
