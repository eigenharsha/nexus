"""hard track — the invariants, proven over arbitrary sequences rather than examples.

The claim these tests make is stronger than anything in test_ledger.py: for *any*
sequence of valid postings the trial balance sums to zero and each account's balance
equals the sum of its own postings. That is the sentence to put in your README.
"""
from __future__ import annotations

from datetime import date

import pytest

hypothesis = pytest.importorskip("hypothesis", reason="hypothesis is required for the hard track")
from hypothesis import HealthCheck, given, settings  # noqa: E402
from hypothesis import strategies as st  # noqa: E402
from hypothesis.stateful import RuleBasedStateMachine, invariant, rule  # noqa: E402

import ledger as L  # noqa: E402

ACCOUNTS = ["cash", "sales", "rent", "bank", "vat"]


def a_book() -> L.Ledger:
    book = L.Ledger(L.MemoryStorage())
    for i, name in enumerate(ACCOUNTS):
        kind = list(L.AccountKind)[i % len(L.AccountKind)]
        book.add_account(L.Account(name, name.title(), kind))
    return book


postings_strategy = st.lists(
    st.tuples(st.sampled_from(ACCOUNTS), st.integers(min_value=-10**6, max_value=10**6).filter(bool)),
    min_size=1, max_size=6,
)


@pytest.mark.hard
@settings(max_examples=200, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(batches=st.lists(postings_strategy, min_size=0, max_size=20))
def test_trial_balance_always_sums_to_zero(batches: list[list[tuple[str, int]]]) -> None:
    book = a_book()
    for n, legs in enumerate(batches):
        # Make the batch balance by adding the closing leg. If that leg would be zero
        # the transaction is already balanced with the legs we have.
        residual = sum(amount for _, amount in legs)
        postings = [L.Posting(acc, L.Money(amt, "GBP")) for acc, amt in legs]
        if residual != 0:
            postings.append(L.Posting("bank", L.Money(-residual, "GBP")))
        if len(postings) < 2:
            continue
        book.post(L.Transaction(f"t{n}", date(2026, 1, 1), "generated", tuple(postings)))

    tb = book.trial_balance()
    assert sum(m.amount for m in tb.values()) == 0


@pytest.mark.hard
@settings(max_examples=200, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(batches=st.lists(postings_strategy, min_size=1, max_size=15))
def test_balance_equals_sum_of_own_postings(batches: list[list[tuple[str, int]]]) -> None:
    book = a_book()
    expected: dict[str, int] = dict.fromkeys(ACCOUNTS, 0)
    for n, legs in enumerate(batches):
        residual = sum(amount for _, amount in legs)
        pairs = list(legs)
        if residual != 0:
            pairs.append(("bank", -residual))
        if len(pairs) < 2:
            continue
        book.post(L.Transaction(
            f"t{n}", date(2026, 1, 1), "generated",
            tuple(L.Posting(a, L.Money(v, "GBP")) for a, v in pairs),
        ))
        for acc, amount in pairs:
            expected[acc] += amount

    for acc in ACCOUNTS:
        assert book.balance(acc).amount == expected[acc], acc


class LedgerMachine(RuleBasedStateMachine):
    """Interleave posts, reloads and balance queries across all three backends and
    assert they never disagree."""

    def __init__(self) -> None:
        super().__init__()
        import tempfile
        from pathlib import Path

        from ledger.event_log import EventLogStorage

        self._dir = Path(tempfile.mkdtemp())
        self._json = self._dir / "b.json"
        self._log = self._dir / "b.jsonl"
        self._EventLog = EventLogStorage
        self.books = [
            L.Ledger(L.MemoryStorage()),
            L.Ledger(L.JsonFileStorage(self._json)),
            L.Ledger(EventLogStorage(self._log)),
        ]
        for book in self.books:
            for i, name in enumerate(ACCOUNTS):
                book.add_account(L.Account(name, name.title(), list(L.AccountKind)[i % 5]))
        self.n = 0

    @rule(src=st.sampled_from(ACCOUNTS), dst=st.sampled_from(ACCOUNTS),
          amount=st.integers(min_value=1, max_value=100000))
    def post(self, src: str, dst: str, amount: int) -> None:
        if src == dst:
            return
        self.n += 1
        txn = L.Transaction(
            f"t{self.n}", date(2026, 1, 1), "move",
            (L.Posting(src, L.Money(amount, "GBP")), L.Posting(dst, L.Money(-amount, "GBP"))),
        )
        for book in self.books:
            book.post(txn)

    @rule()
    def reload_persistent_backends(self) -> None:
        self.books[1] = L.Ledger(L.JsonFileStorage(self._json))
        self.books[2] = L.Ledger(self._EventLog(self._log))

    @invariant()
    def backends_agree_and_balance(self) -> None:
        views = [{k: v.amount for k, v in b.trial_balance().items()} for b in self.books]
        assert views[0] == views[1] == views[2]
        assert sum(views[0].values()) == 0


TestLedgerMachine = pytest.mark.hard(
    LedgerMachine.TestCase  # type: ignore[attr-defined]
)
