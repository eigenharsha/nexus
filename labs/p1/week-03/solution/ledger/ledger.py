"""The ledger itself. It knows about the domain and about the `Storage` Protocol,
and about nothing else — no JSON, no files, no event log. That is what makes the
`hard` track possible without editing this file."""
from __future__ import annotations

from collections import defaultdict

from .errors import DuplicateTransaction, UnknownAccount
from .models import Account, Money, Transaction
from .storage import Storage


class Ledger:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    # -- accounts ---------------------------------------------------------
    def add_account(self, account: Account) -> None:
        self._storage.put_account(account)

    def account(self, account_id: str) -> Account:
        acc = self._storage.get_account(account_id)
        if acc is None:
            raise UnknownAccount(account_id)
        return acc

    def accounts(self) -> list[Account]:
        return sorted(self._storage.accounts(), key=lambda a: a.id)

    # -- transactions -----------------------------------------------------
    def post(self, txn: Transaction) -> None:
        """Record a transaction.

        Idempotent on id in the strict sense the spec asks for: posting the same id
        twice raises `DuplicateTransaction` and changes nothing. The validity checks
        run *before* the duplicate check so a malformed replay is reported as
        malformed rather than as a duplicate.
        """
        for account_id in sorted(txn.accounts()):
            if self._storage.get_account(account_id) is None:
                raise UnknownAccount(account_id)
        if self._storage.has_transaction(txn.id):
            raise DuplicateTransaction(txn.id)
        self._storage.put_transaction(txn)

    def transactions(self) -> list[Transaction]:
        return sorted(self._storage.transactions(), key=lambda t: (t.date, t.id))

    # -- reporting --------------------------------------------------------
    def balance(self, account_id: str) -> Money:
        acc = self.account(account_id)
        total = 0
        currency: str | None = None
        for txn in self._storage.transactions():
            for p in txn.postings:
                if p.account_id == acc.id:
                    total += p.amount.amount
                    currency = p.amount.currency
        return Money(total, currency or "GBP")

    def trial_balance(self) -> dict[str, Money]:
        """Every account's balance. The values always sum to zero — that is the
        whole point of double entry, and the property test proves it holds under
        any sequence of valid postings."""
        totals: dict[str, int] = defaultdict(int)
        currency = "GBP"
        for txn in self._storage.transactions():
            currency = txn.currency
            for p in txn.postings:
                totals[p.account_id] += p.amount.amount
        result = {a.id: Money(totals.get(a.id, 0), currency) for a in self._storage.accounts()}
        for account_id, amount in totals.items():
            result.setdefault(account_id, Money(amount, currency))
        return result
