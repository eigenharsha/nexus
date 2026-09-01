"""The domain types.

The invariant that matters — a transaction's postings sum to zero — is enforced in
`Transaction.__post_init__`, not in `Ledger.post`. If it lived in the ledger, an
unbalanced `Transaction` object could exist in memory, and sooner or later somebody
would serialise one and hand it to another system.

Money is an integer count of minor units (pence, cents) plus an ISO-4217 code.
Never a float: 0.1 + 0.2 != 0.3, and a ledger that is wrong by 1e-17 is still wrong.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date as _date
from enum import Enum

from .errors import CurrencyMismatch, Unbalanced

_CURRENCY_RE = re.compile(r"^[A-Z]{3}$")


class AccountKind(Enum):
    """The five account types of double-entry bookkeeping.

    `normal_sign` is +1 if a debit increases the account and -1 if a credit does.
    It is what makes `trial_balance` readable rather than a wall of signs.
    """

    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    INCOME = "income"
    EXPENSE = "expense"

    @property
    def normal_sign(self) -> int:
        return 1 if self in (AccountKind.ASSET, AccountKind.EXPENSE) else -1


@dataclass(frozen=True, slots=True, order=True)
class Money:
    """An exact amount. `amount` is minor units: Money(1050, "GBP") is £10.50."""

    amount: int
    currency: str

    def __post_init__(self) -> None:
        if not isinstance(self.amount, int) or isinstance(self.amount, bool):
            raise TypeError(
                f"amount must be an int of minor units, got {type(self.amount).__name__}"
            )
        if not _CURRENCY_RE.match(self.currency):
            raise ValueError(f"currency must be a 3-letter ISO-4217 code, got {self.currency!r}")

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
        if not self.id.strip():
            raise ValueError("account id must not be empty")
        if not self.name.strip():
            raise ValueError("account name must not be empty")


@dataclass(frozen=True, slots=True)
class Posting:
    """One leg of a transaction. A positive amount is a debit, negative is a credit."""

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
        if not self.id.strip():
            raise ValueError("transaction id must not be empty")
        if len(self.postings) < 2:
            raise ValueError("a transaction needs at least two postings")

        currencies = {p.amount.currency for p in self.postings}
        if len(currencies) > 1:
            a, b = sorted(currencies)[:2]
            raise CurrencyMismatch(a, b)

        currency = next(iter(currencies))
        residual = sum(p.amount.amount for p in self.postings)
        if residual != 0:
            raise Unbalanced(residual, currency)

    @property
    def currency(self) -> str:
        return self.postings[0].amount.currency

    def accounts(self) -> frozenset[str]:
        return frozenset(p.account_id for p in self.postings)
