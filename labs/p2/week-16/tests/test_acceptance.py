"""Acceptance tests for LAB-P2-W16 — Automated EDA dashboard.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_guided_notebook_producing_eight_required_plots_provided() -> None:
    """
    A guided notebook producing the eight required plots on the provided dataset.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_cli_eda_report_data_parquet_target_churned() -> None:
    """
    A CLI: `eda report data.parquet --target churned --out report.html`.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_report_sections_schema_dtypes_missingness_count_pattern() -> None:
    """
    Report sections: schema and dtypes, missingness (count, %, pattern), per-column
    distributions, outliers by IQR and by z-score with the disagreement flagged, correlation
    matrix (Pearson and Spearman), and target relationships per feature.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_leakage_warnings_feature_near_perfect_correlation_target() -> None:
    """
    **Leakage warnings**: a feature with near-perfect correlation to the target, a feature
    that is constant within target groups, an ID-like column with high cardinality, a
    datetime feature that post-dates the target, and duplicated rows across a train/test
    split if one is supplied.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_written_summary_section_generated_findings_plain_sentences() -> None:
    """
    A written summary section generated from the findings, in plain sentences.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_tested_three_structurally_different_datasets_wide_tall() -> None:
    """
    Tested on three structurally different datasets (wide, tall, mixed-type).
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_10m_rows_within_memory_budget_hard_targets() -> None:
    """
    10M rows within the memory budget in `hard/targets.md`, in under 60 s. Streaming or
    columnar chunking — a `pd.read_csv` of the whole file will not fit.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_drift_comparison_between_two_datasets_psi_ks() -> None:
    """
    Drift comparison between two datasets: PSI and KS per numeric feature, chi-square per
    categorical, with a documented threshold for "this has drifted".
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_runtime_reported_section_so_slow_part_visible() -> None:
    """
    Runtime reported per section so the slow part is visible.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

