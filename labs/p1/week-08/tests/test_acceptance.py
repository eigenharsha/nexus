"""Acceptance tests for LAB-P1-W08 — Concurrency-safe checkout service.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_transactional_checkout_endpoint_passes_provided_single_user() -> None:
    """
    A transactional checkout endpoint that passes the provided single-user tests: inventory
    decrement and order creation succeed or fail together.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_fastapi_async_sqlalchemy_2_x() -> None:
    """
    FastAPI + async SQLAlchemy 2.x.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_payment_verification_inventory_decrement_transaction_correct_isolation() -> None:
    """
    Payment verification and inventory decrement in **one** transaction with the correct
    isolation level, chosen deliberately and documented.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_optimistic_locking_version_column_lost_update_raises() -> None:
    """
    Optimistic locking via a `version` column; a lost update raises and is retried a bounded
    number of times.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_idempotency_keys_stored_request_hash_replay_returns() -> None:
    """
    Idempotency keys stored with the request hash; a replay returns the original response.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_alembic_migrations_including_downgrade_actually_works() -> None:
    """
    Alembic migrations, including a downgrade that actually works.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_concurrency_test_suite_runs_200_concurrent_buyers() -> None:
    """
    A concurrency test suite that runs 200 concurrent buyers against a stock of 12 and
    asserts exactly 12 orders, 12 payments and a final stock of 0 — run 20 times, zero
    flakes.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_meet_throughput_p95_targets_under_contention() -> None:
    """
    Meet the throughput and p95 targets under contention.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_concurrency_md_pessimistic_vs_optimistic_vs_serializable() -> None:
    """
    `CONCURRENCY.md`: pessimistic vs optimistic vs `SERIALIZABLE`, each with measured
    throughput, p95, and retry/abort rate from your own run.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_reproducible_deadlock_two_transactions_opposite_lock_order() -> None:
    """
    A reproducible deadlock (two transactions, opposite lock order) with the log evidence,
    and the fix — plus the ordering rule you adopted so it cannot recur.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

