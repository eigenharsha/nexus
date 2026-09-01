"""The exception hierarchy. This one is given to you — it is the shape, not the work."""
from __future__ import annotations


class LedgerError(Exception):
    """Base class for every error raised by `ledger`."""


class Unbalanced(LedgerError):
    def __init__(self, residual: int, currency: str) -> None:
        super().__init__(
            f"postings do not sum to zero: residual {residual} minor units of {currency}"
        )
        self.residual = residual
        self.currency = currency


class CurrencyMismatch(LedgerError):
    def __init__(self, left: str, right: str) -> None:
        super().__init__(f"cannot combine {left} and {right}")
        self.left = left
        self.right = right


class UnknownAccount(LedgerError):
    def __init__(self, account_id: str) -> None:
        super().__init__(f"unknown account: {account_id!r}")
        self.account_id = account_id


class DuplicateTransaction(LedgerError):
    def __init__(self, txn_id: str) -> None:
        super().__init__(f"transaction already posted: {txn_id!r}")
        self.txn_id = txn_id


class StorageError(LedgerError):
    """A storage backend failed to read or write."""
