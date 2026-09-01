"""The ledger. `standard` track — you write this.

It may know about the domain models and the `Storage` Protocol. It must not know
about JSON, files, or any specific backend.
"""
from __future__ import annotations

from .models import Account, Money, Transaction
from .storage import Storage


class Ledger:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def add_account(self, account: Account) -> None:
        raise NotImplementedError("Ledger.add_account")

    def account(self, account_id: str) -> Account:
        raise NotImplementedError("Ledger.account")

    def accounts(self) -> list[Account]:
        raise NotImplementedError("Ledger.accounts")

    def post(self, txn: Transaction) -> None:
        """Record a transaction. Unknown account -> UnknownAccount.
        Already-posted id -> DuplicateTransaction, with no state change."""
        raise NotImplementedError("Ledger.post")

    def transactions(self) -> list[Transaction]:
        raise NotImplementedError("Ledger.transactions")

    def balance(self, account_id: str) -> Money:
        raise NotImplementedError("Ledger.balance")

    def trial_balance(self) -> dict[str, Money]:
        """Every account's balance. The values must always sum to zero."""
        raise NotImplementedError("Ledger.trial_balance")
