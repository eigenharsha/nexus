"""Acceptance tests for LAB-P3-W19 — Evaluation harness.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_compute_plot_standard_metric_set_accuracy_precision() -> None:
    """
    Compute and plot the standard metric set (accuracy, precision, recall, F1, ROC-AUC, PR-
    AUC, confusion matrix) for a provided model and dataset.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_reusable_library_importable_tested_notebook() -> None:
    """
    A reusable library, importable and tested, not a notebook.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_cv_strategy_selector_given_dataset_s_shape() -> None:
    """
    A CV strategy selector: given a dataset's shape (grouped? time-ordered? imbalanced?), it
    picks and justifies stratified / grouped / time-series CV, and refuses to run plain
    k-fold on grouped data.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_leakage_audit_checks_target_leakage_correlation_train() -> None:
    """
    Leakage audit checks: target leakage by correlation, train/test row duplication,
    preprocessing fit before split (detected by a fitted-transformer fingerprint), group
    spillover across folds, and a time-travel check on datetime features.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_metric_suite_bootstrap_confidence_intervals_10_000() -> None:
    """
    A metric suite with bootstrap confidence intervals (10,000 resamples) on every metric.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_slice_analysis_metrics_category_categorical_feature_worst() -> None:
    """
    Slice analysis: metrics per category for every categorical feature, with the worst slice
    flagged.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_calibration_report_threshold_optimizer_against_supplied_cost() -> None:
    """
    A calibration report and a threshold optimizer against a supplied cost matrix.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_auto_generated_html_evaluation_report() -> None:
    """
    An auto-generated HTML evaluation report.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_validated_three_datasets() -> None:
    """
    Validated on three datasets.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_nested_cross_validation_unbiased_performance_estimation_under() -> None:
    """
    Nested cross-validation for unbiased performance estimation under hyperparameter search;
    report the optimism gap versus flat CV on the same data.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_adversarial_validation_train_classifier_distinguish_train_test() -> None:
    """
    Adversarial validation: train a classifier to distinguish train from test; an AUC above
    a stated threshold is reported as a distribution-shift warning.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_automated_leakage_detection_catching_five_planted_leaks() -> None:
    """
    Automated leakage detection catching **all five** planted leaks in `standard/leaks/`.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_whole_harness_runs_inside_stated_runtime_budget() -> None:
    """
    The whole harness runs inside the stated runtime budget.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

