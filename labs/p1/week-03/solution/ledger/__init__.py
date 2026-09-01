"""`ledger` — a small, exact, double-entry bookkeeping library.

    >>> from datetime import date
    >>> from ledger import Account, AccountKind, Ledger, MemoryStorage, Money, Posting, Transaction
    >>> book = Ledger(MemoryStorage())
    >>> book.add_account(Account("cash", "Cash", AccountKind.ASSET))
    >>> book.add_account(Account("sales", "Sales", AccountKind.INCOME))
    >>> book.post(Transaction("t1", date(2026, 1, 5), "coffee", (
    ...     Posting("cash", Money(350, "GBP")),
    ...     Posting("sales", Money(-350, "GBP")),
    ... )))
    >>> str(book.balance("cash"))
    '3.50 GBP'
"""
from __future__ import annotations

from .errors import (
    CurrencyMismatch,
    DuplicateTransaction,
    LedgerError,
    StorageError,
    Unbalanced,
    UnknownAccount,
)
from .ledger import Ledger
from .models import Account, AccountKind, Money, Posting, Transaction
from .storage import JsonFileStorage, MemoryStorage, Storage

__version__ = "0.1.0"

__all__ = [
    "Account",
    "AccountKind",
    "CurrencyMismatch",
    "DuplicateTransaction",
    "JsonFileStorage",
    "Ledger",
    "LedgerError",
    "MemoryStorage",
    "Money",
    "Posting",
    "Storage",
    "StorageError",
    "Transaction",
    "Unbalanced",
    "UnknownAccount",
    "__version__",
]
