"""Acceptance tests for LAB-P1-W03 — `ledger`.

Tracks are cumulative: `make verify TRACK=hard` runs basic + standard + hard.
`make verify` puts starter/ or solution/ first on sys.path, so these import `ledger`
and never care which one they are grading.
"""
from __future__ import annotations

import inspect
import json
from datetime import date
from pathlib import Path

import pytest

import ledger as L

GBP = "GBP"


def money(n: int, cur: str = GBP) -> L.Money:
    return L.Money(n, cur)


def simple_txn(txn_id: str = "t1", amount: int = 1000) -> L.Transaction:
    return L.Transaction(
        txn_id,
        date(2026, 1, 5),
        "sale",
        (L.Posting("cash", money(amount)), L.Posting("sales", money(-amount))),
    )


def fresh_book() -> L.Ledger:
    book = L.Ledger(L.MemoryStorage())
    book.add_account(L.Account("cash", "Cash", L.AccountKind.ASSET))
    book.add_account(L.Account("sales", "Sales", L.AccountKind.INCOME))
    book.add_account(L.Account("rent", "Rent", L.AccountKind.EXPENSE))
    return book


# ============================================================== basic
@pytest.mark.basic
def test_account_kinds_have_normal_signs() -> None:
    assert L.AccountKind.ASSET.normal_sign == 1
    assert L.AccountKind.EXPENSE.normal_sign == 1
    assert L.AccountKind.LIABILITY.normal_sign == -1
    assert L.AccountKind.EQUITY.normal_sign == -1
    assert L.AccountKind.INCOME.normal_sign == -1


@pytest.mark.basic
def test_money_is_exact_integer_minor_units() -> None:
    assert money(1050).amount == 1050
    assert str(money(1050)) == "10.50 GBP"
    assert str(money(-5)) == "-0.05 GBP"
    assert money(10) + money(20) == money(30)
    assert money(10) - money(20) == money(-10)


@pytest.mark.basic
def test_money_rejects_floats_and_bad_currency() -> None:
    with pytest.raises(TypeError):
        L.Money(10.5, GBP)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        L.Money(True, GBP)  # bool is an int subclass; it is still not an amount
    for bad in ("gbp", "GB", "GBPP", ""):
        with pytest.raises(ValueError):
            L.Money(1, bad)


@pytest.mark.basic
def test_money_arithmetic_across_currencies_raises() -> None:
    with pytest.raises(L.CurrencyMismatch) as exc:
        money(100, "GBP") + money(100, "USD")
    assert {exc.value.left, exc.value.right} == {"GBP", "USD"}


@pytest.mark.basic
def test_account_requires_id_and_name() -> None:
    L.Account("cash", "Cash", L.AccountKind.ASSET)
    for bad_id, bad_name in ((" ", "Cash"), ("cash", "  "), ("", "Cash")):
        with pytest.raises(ValueError):
            L.Account(bad_id, bad_name, L.AccountKind.ASSET)


@pytest.mark.basic
def test_transaction_must_balance() -> None:
    good = simple_txn()
    assert good.currency == GBP
    assert good.accounts() == frozenset({"cash", "sales"})

    with pytest.raises(L.Unbalanced) as exc:
        L.Transaction(
            "bad", date(2026, 1, 5), "oops",
            (L.Posting("cash", money(1000)), L.Posting("sales", money(-999))),
        )
    assert exc.value.residual == 1


@pytest.mark.basic
def test_transaction_needs_two_postings_and_one_currency() -> None:
    with pytest.raises(ValueError):
        L.Transaction("x", date(2026, 1, 5), "one leg", (L.Posting("cash", money(1)),))
    with pytest.raises(L.CurrencyMismatch):
        L.Transaction(
            "x", date(2026, 1, 5), "mixed",
            (L.Posting("cash", money(100, "GBP")), L.Posting("sales", money(-100, "USD"))),
        )


@pytest.mark.basic
def test_domain_objects_are_immutable() -> None:
    m = money(1)
    with pytest.raises((AttributeError, TypeError)):
        m.amount = 2  # type: ignore[misc]


# ============================================================== standard
@pytest.mark.standard
def test_storage_is_a_protocol_not_an_abc() -> None:
    assert getattr(L.Storage, "_is_protocol", False), "Storage must be a typing.Protocol"
    assert isinstance(L.MemoryStorage(), L.Storage)


@pytest.mark.standard
def test_error_hierarchy_is_rooted() -> None:
    for exc in (L.Unbalanced, L.CurrencyMismatch, L.UnknownAccount,
                L.DuplicateTransaction, L.StorageError):
        assert issubclass(exc, L.LedgerError), f"{exc.__name__} must inherit LedgerError"


@pytest.mark.standard
def test_post_and_balance() -> None:
    book = fresh_book()
    book.post(simple_txn("t1", 1000))
    book.post(simple_txn("t2", 250))
    assert book.balance("cash") == money(1250)
    assert book.balance("sales") == money(-1250)


@pytest.mark.standard
def test_unknown_account_is_rejected_before_anything_is_written() -> None:
    book = fresh_book()
    txn = L.Transaction(
        "t1", date(2026, 1, 5), "typo",
        (L.Posting("cash", money(100)), L.Posting("saels", money(-100))),
    )
    with pytest.raises(L.UnknownAccount) as exc:
        book.post(txn)
    assert exc.value.account_id == "saels"
    assert book.transactions() == []


@pytest.mark.standard
def test_duplicate_transaction_id_raises_and_changes_nothing() -> None:
    book = fresh_book()
    book.post(simple_txn("t1", 1000))
    before = book.balance("cash")
    with pytest.raises(L.DuplicateTransaction):
        book.post(simple_txn("t1", 9999))
    assert book.balance("cash") == before
    assert len(book.transactions()) == 1


@pytest.mark.standard
def test_trial_balance_sums_to_zero() -> None:
    book = fresh_book()
    book.post(simple_txn("t1", 1000))
    book.post(L.Transaction(
        "t2", date(2026, 2, 1), "rent",
        (L.Posting("rent", money(400)), L.Posting("cash", money(-400))),
    ))
    tb = book.trial_balance()
    assert sum(m.amount for m in tb.values()) == 0
    assert tb["cash"] == money(600)
    assert tb["rent"] == money(400)


@pytest.mark.standard
def test_json_file_storage_round_trips(tmp_path: Path) -> None:
    path = tmp_path / "book.json"
    book = L.Ledger(L.JsonFileStorage(path))
    book.add_account(L.Account("cash", "Cash", L.AccountKind.ASSET))
    book.add_account(L.Account("sales", "Sales", L.AccountKind.INCOME))
    book.post(simple_txn("t1", 1234))

    reopened = L.Ledger(L.JsonFileStorage(path))
    assert reopened.balance("cash") == money(1234)
    assert {a.id for a in reopened.accounts()} == {"cash", "sales"}
    assert json.loads(path.read_text())["transactions"][0]["id"] == "t1"


@pytest.mark.standard
def test_json_file_storage_writes_atomically(tmp_path: Path) -> None:
    """A temp file plus os.replace, not a truncating write into the live path."""
    src = inspect.getsource(type(L.JsonFileStorage(tmp_path / "b.json")))
    assert "replace" in src, (
        "JsonFileStorage must write to a temp file and os.replace it into position; "
        "a partial write into the real path loses the ledger"
    )


@pytest.mark.standard
def test_both_backends_agree(tmp_path: Path) -> None:
    backends = [L.MemoryStorage(), L.JsonFileStorage(tmp_path / "b.json")]
    results = []
    for storage in backends:
        book = L.Ledger(storage)
        for acc in ("cash", "sales", "rent"):
            book.add_account(L.Account(acc, acc.title(), L.AccountKind.ASSET))
        for i in range(10):
            book.post(simple_txn(f"t{i}", 100 + i))
        results.append({k: v.amount for k, v in book.trial_balance().items()})
    assert results[0] == results[1]


@pytest.mark.standard
def test_ledger_core_does_not_know_about_any_backend() -> None:
    """The dependency arrow points one way. This is what makes the hard track possible."""
    src = inspect.getsource(L.ledger)
    for forbidden in ("json", "open(", "Path", "MemoryStorage", "JsonFileStorage"):
        assert forbidden not in src, (
            f"ledger/ledger.py mentions {forbidden!r} — the core must depend only on "
            f"the Storage Protocol"
        )


# ============================================================== hard
@pytest.mark.hard
def test_event_log_backend_exists_and_replays(tmp_path: Path) -> None:
    from ledger.event_log import EventLogStorage

    path = tmp_path / "events.jsonl"
    book = L.Ledger(EventLogStorage(path))
    book.add_account(L.Account("cash", "Cash", L.AccountKind.ASSET))
    book.add_account(L.Account("sales", "Sales", L.AccountKind.INCOME))
    book.post(simple_txn("t1", 500))
    book.post(simple_txn("t2", 700))

    assert path.read_text().count("\n") == 4  # 2 accounts + 2 transactions, append-only

    replayed = L.Ledger(EventLogStorage(path))
    assert replayed.balance("cash") == money(1200)
    assert len(replayed.transactions()) == 2


@pytest.mark.hard
def test_event_log_survives_a_torn_final_line(tmp_path: Path) -> None:
    from ledger.event_log import EventLogStorage

    path = tmp_path / "events.jsonl"
    book = L.Ledger(EventLogStorage(path))
    book.add_account(L.Account("cash", "Cash", L.AccountKind.ASSET))
    book.add_account(L.Account("sales", "Sales", L.AccountKind.INCOME))
    book.post(simple_txn("t1", 500))

    with path.open("a") as fh:
        fh.write('{"event": "transa')  # killed mid-append

    recovered = L.Ledger(EventLogStorage(path))
    assert recovered.balance("cash") == money(500)


@pytest.mark.hard
def test_open_closed_core_never_mentions_the_event_log() -> None:
    """Adding a backend must not require editing core. Proven from the import graph."""
    for module in (L.ledger, L.models, L.errors):
        src = inspect.getsource(module)
        assert "EventLog" not in src and "event_log" not in src, (
            f"{module.__name__} references the event-log backend — the hard track "
            f"requires the core to be closed for modification"
        )
    import ledger.event_log as ev
    ev_src = inspect.getsource(ev)
    assert "from .ledger import" not in ev_src and "from ledger.ledger import" not in ev_src, (
        "the backend must not import the core either"
    )


@pytest.mark.hard
def test_all_three_backends_agree(tmp_path: Path) -> None:
    from ledger.event_log import EventLogStorage

    backends = [
        L.MemoryStorage(),
        L.JsonFileStorage(tmp_path / "b.json"),
        EventLogStorage(tmp_path / "b.jsonl"),
    ]
    results = []
    for storage in backends:
        book = L.Ledger(storage)
        for acc in ("cash", "sales", "rent"):
            book.add_account(L.Account(acc, acc.title(), L.AccountKind.ASSET))
        for i in range(25):
            book.post(simple_txn(f"t{i}", 10 * (i + 1)))
        results.append({k: v.amount for k, v in book.trial_balance().items()})
    assert results[0] == results[1] == results[2]
