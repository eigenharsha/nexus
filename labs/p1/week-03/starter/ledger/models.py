"""The domain types.

basic track: fill in the four TODOs below. About 60% is written for you.

The one rule that matters: money is an integer count of minor units (pence, cents),
never a float. `0.1 + 0.2 != 0.3` and a ledger that is wrong by 1e-17 is still wrong.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date as _date
from enum import Enum

from .errors import CurrencyMismatch

_CURRENCY_RE = re.compile(r"^[A-Z]{3}$")


class AccountKind(Enum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    INCOME = "income"
    EXPENSE = "expense"

    @property
    def normal_sign(self) -> int:
        """+1 if a debit increases this account, -1 if a credit does."""
        # TODO 1: assets and expenses increase on the debit side; the other three
        # increase on the credit side.
        raise NotImplementedError("AccountKind.normal_sign")


@dataclass(frozen=True, slots=True, order=True)
class Money:
    amount: int
    currency: str

    def __post_init__(self) -> None:
        # TODO 2: reject a non-int amount (bool is an int in Python — reject it too)
        # and reject a currency that is not three uppercase letters.
        raise NotImplementedError("Money.__post_init__")

    def _check(self, other: Money) -> None:
        if self.currency != other.currency:
            raise CurrencyMismatch(self.currency, other.currency)

    def __add__(self, other: Money) -> Money:
        self._check(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: Money) -> Money:
        self._check(other)
        return Money(self.amount - other.amount, self.currency)

    def __neg__(self) -> Money:
        return Money(-self.amount, self.currency)

    def __str__(self) -> str:
        sign = "-" if self.amount < 0 else ""
        whole, frac = divmod(abs(self.amount), 100)
        return f"{sign}{whole}.{frac:02d} {self.currency}"

    @classmethod
    def zero(cls, currency: str) -> Money:
        return cls(0, currency)


@dataclass(frozen=True, slots=True)
class Account:
    id: str
    name: str
    kind: AccountKind

    def __post_init__(self) -> None:
        # TODO 3: an empty or whitespace-only id or name is not an account.
        raise NotImplementedError("Account.__post_init__")


@dataclass(frozen=True, slots=True)
class Posting:
    """One leg of a transaction. Positive is a debit, negative is a credit."""

    account_id: str
    amount: Money

    def __post_init__(self) -> None:
        if not self.account_id.strip():
            raise ValueError("posting account_id must not be empty")
        if self.amount.amount == 0:
            raise ValueError("a zero-amount posting carries no information; omit it")


@dataclass(frozen=True, slots=True)
class Transaction:
    id: str
    date: _date
    description: str
    postings: tuple[Posting, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        # TODO 4: enforce the invariants, in this order:
        #   - a non-empty id
        #   - at least two postings
        #   - exactly one currency across all postings (else CurrencyMismatch)
        #   - the postings' amounts sum to zero (else Unbalanced(residual, currency))
        raise NotImplementedError("Transaction.__post_init__")

    @property
    def currency(self) -> str:
        return self.postings[0].amount.currency

    def accounts(self) -> frozenset[str]:
        return frozenset(p.account_id for p in self.postings)
