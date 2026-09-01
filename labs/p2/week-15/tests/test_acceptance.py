"""Acceptance tests for LAB-P2-W15 — Incremental financial-records pipeline.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_dlt_pipeline_provided_rest_api_duckdb_full() -> None:
    """
    A `dlt` pipeline from the provided REST API into DuckDB, full refresh, with a row count
    check.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_extract_rest_api_unstructured_html_source_normalize() -> None:
    """
    Extract from the REST API **and** an unstructured HTML source; normalize both into one
    schema.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_incremental_loading_cursor_field_merge_write_disposition() -> None:
    """
    Incremental loading on a cursor field with `merge` write disposition; re-running the
    pipeline produces zero new rows (the test asserts an unchanged table hash).
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_schema_evolution_enabled_tested_fixture_adds_column() -> None:
    """
    Schema evolution enabled and tested: the fixture adds a column mid-run and the pipeline
    absorbs it.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_deduplication_documented_business_key_tie_break_rule() -> None:
    """
    Deduplication on a documented business key, with the tie-break rule written down.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_data_quality_checks_null_rates_referential_integrity() -> None:
    """
    Data-quality checks: null rates, referential integrity, an amount-range check, and a
    row-count delta bound. A failed check fails the run loudly.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_run_report_artifact_run_rows_rows_merged() -> None:
    """
    A run report artifact per run: rows in, rows merged, rows rejected, checks passed,
    duration.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_scheduled_cron_scheduler_choice_safe_re_run() -> None:
    """
    Scheduled (cron or a scheduler of your choice) and safe to re-run at any point.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_5m_rows_written_partitioned_parquet_documented_partition() -> None:
    """
    5M rows written as partitioned Parquet with a documented partition key.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_scd2_dimension_valid_valid_current_tested_across() -> None:
    """
    An SCD2 dimension with `valid_from` / `valid_to` / `is_current`, tested across three
    updates to the same business key.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_backfill_script_can_re_process_arbitrary_date() -> None:
    """
    A backfill script that can re-process an arbitrary date range without touching other
    partitions.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_written_proof_exactly_once_merge_semantics_mechanism() -> None:
    """
    A written proof of exactly-once merge semantics: the mechanism, and the test that
    demonstrates it under a mid-merge crash.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_cost_latency_analysis_seconds_million_rows_bytes() -> None:
    """
    Cost and latency analysis: seconds per million rows, bytes written, and the projected
    monthly cost.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

