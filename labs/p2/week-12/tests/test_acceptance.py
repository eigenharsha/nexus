"""Acceptance tests for LAB-P2-W12 — A/B test analyzer + Bayes classifier.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_compute_means_standard_errors_95_ci_two() -> None:
    """
    Compute means, standard errors, a 95% CI and a two-sample t-test on the provided data.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")

@pytest.mark.basic
def test_basic_state_conclusion_sentence_non_statistician_would_read() -> None:
    """
    State the conclusion in a sentence that a non-statistician would read correctly.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_cli_tool_abtest_analyze_results_csv_primary() -> None:
    """
    A CLI tool: `abtest analyze results.csv --primary conversion --guardrail latency_p95`.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_sample_size_calculator_given_baseline_rate_mde() -> None:
    """
    Sample-size calculator: given baseline rate, MDE and power, output required n per arm.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_srm_check_sample_ratio_mismatch_chi_square() -> None:
    """
    **SRM check** (sample ratio mismatch) via chi-square; if it fails, refuse to report and
    say why.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_primary_guardrail_metrics_reported_together_effect_size() -> None:
    """
    Primary and guardrail metrics reported together, with effect size (both absolute and
    relative) and a bootstrap CI (10,000 resamples).
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_written_decision_block_ship_do_ship_inconclusive() -> None:
    """
    A written decision block: ship / do not ship / inconclusive, with the reason.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_plus_scratch_multinomial_naive_bayes_classifier_laplace() -> None:
    """
    Plus a from-scratch multinomial naive Bayes classifier with Laplace smoothing, evaluated
    on a text dataset with a confusion matrix.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_sequential_testing_alpha_spending_correction_demonstrate_simulated() -> None:
    """
    Sequential testing with an alpha-spending correction; demonstrate on simulated data that
    naive peeking inflates the false-positive rate to a measured value, and that yours does
    not.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_cuped_variance_reduction_using_pre_period_covariate() -> None:
    """
    CUPED variance reduction using a pre-period covariate; report the measured variance
    reduction and the resulting reduction in required n.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

