"""Acceptance tests for LAB-P1-W07 — E-commerce schema & analytics suite.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_complete_partial_schema_basic_schema_partial_sql() -> None:
    """
    Complete the partial schema in `basic/schema_partial.sql` (missing keys, constraints,
    types).
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")

@pytest.mark.basic
def test_basic_write_15_provided_queries_tests_compare_result() -> None:
    """
    Write the 15 provided queries; the tests compare your result sets to expected fixtures.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_full_normalized_schema_users_products_inventory_carts() -> None:
    """
    Full normalized schema: users, products, inventory, carts, cart_items, orders,
    order_items, payments, refunds, reviews. Third normal form, with the denormalizations
    you chose documented and justified.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_foreign_key_declared_null_deliberate_check_constraints() -> None:
    """
    Every foreign key declared, every `NOT NULL` deliberate, `CHECK` constraints on money
    and quantity, and a partial unique index enforcing one active cart per user.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_seed_py_generates_1m_rows_realistic_skew() -> None:
    """
    `seed.py` generates 1M rows with realistic skew: an 80/20 product popularity
    distribution and a purchase-count distribution that is not uniform.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_20_analytical_queries_queries_explain_analyze_output() -> None:
    """
    20 analytical queries in `queries/`, each with its `EXPLAIN ANALYZE` output committed,
    including: cohort retention by signup month, top-N products per category (window
    function), refund rate by cohort, and a running 7-day revenue total.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_money_numeric_never_float_test_checks_column() -> None:
    """
    Money is `NUMERIC`, never `FLOAT`. The test checks the column types.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_hit_latency_target_hard_targets_md_10m() -> None:
    """
    Hit every latency target in `hard/targets.md` on a 10M-row seed.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_indexes_md_documents_index_query_serves_plan() -> None:
    """
    `INDEXES.md` documents every index with: the query it serves, the plan before and after,
    the measured write-cost (INSERT throughput with and without it), and the disk size.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_least_query_fixed_rewrite_rather_index_find() -> None:
    """
    At least one query must be fixed by a **rewrite** rather than an index — find it and say
    so.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

