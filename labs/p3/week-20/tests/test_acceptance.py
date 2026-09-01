"""Acceptance tests for LAB-P3-W20 — Credit-card fraud detection.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_train_baseline_imbalanced_dataset_produce_precision_recall() -> None:
    """
    Train a baseline on the imbalanced dataset and produce a precision-recall curve with the
    average precision reported.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_leakage_free_preprocessing_transformer_fit_inside_cv() -> None:
    """
    Leakage-free preprocessing: every transformer fit inside the CV fold. The Week-19
    harness should pass this pipeline.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_engineered_temporal_aggregate_features_time_since_account() -> None:
    """
    Engineered temporal and aggregate features: time since the account's previous
    transaction, rolling count and amount in 1 h / 24 h / 7 d windows, and amount relative
    to the account's own history — all computed **without** looking forward in time. The
    test plants a future-leaking feature and your pipeline must reject it.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_xgboost_scale_pos_weight_tuned_compared_against() -> None:
    """
    XGBoost with `scale_pos_weight`, tuned, compared against a logistic-regression baseline.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_pr_curve_threshold_optimization_against_explicit_cost() -> None:
    """
    PR-curve threshold optimization against the explicit cost matrix in
    `standard/costs.yaml`.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_probability_calibration_isotonic_platt_reliability_curve_before() -> None:
    """
    Probability calibration (isotonic or Platt), with the reliability curve before and
    after.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_slice_analysis_across_merchant_category_transaction_amount() -> None:
    """
    Slice analysis across merchant category and transaction amount bands.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_report_stating_expected_annual_savings_arithmetic_shown() -> None:
    """
    A report stating expected annual savings with the arithmetic shown.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_target_recall_fixed_fp_budget_reported_bootstrap() -> None:
    """
    Target recall at the fixed FP budget, reported with a bootstrap CI.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_sub_10_ms_p99_prediction_latency_including() -> None:
    """
    Sub-10 ms p99 per-prediction latency including feature computation — which means the
    rolling aggregates must be maintained incrementally, not recomputed.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_drift_monitoring_input_features_documented_alert_threshold() -> None:
    """
    Drift monitoring on the input features with a documented alert threshold.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_serialization_strategy_survives_dependency_upgrade_version_pinned() -> None:
    """
    A serialization strategy that survives a dependency upgrade: a version-pinned artifact
    plus a loading test that runs against the next minor version of the library.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

