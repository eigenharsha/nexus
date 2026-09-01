"""Acceptance tests for LAB-P4-W32 — Full observability & cost control.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_opentelemetry_spans_around_llm_call_exported_local() -> None:
    """
    OpenTelemetry spans around every LLM call, exported to a local collector, with a
    screenshot of one full trace.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_full_instrumentation_week_30_system_traces_exported() -> None:
    """
    Full instrumentation of the Week-30 system: traces exported to a self-hosted Langfuse.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_step_token_cost_attribution_so_trace_answers() -> None:
    """
    Per-step token and cost attribution, so a trace answers "which node spent the money".
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_prompt_versioning_version_recorded_trace() -> None:
    """
    Prompt versioning, with the version recorded on every trace.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_scheduled_evals_week_31_suite_running_against() -> None:
    """
    Scheduled evals (the Week-31 suite) running against production traffic samples.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_dashboards_cost_run_p95_latency_step_error() -> None:
    """
    Dashboards: cost per run, p95 latency per step, error rate, token usage by model.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_alerts_cost_run_error_rate_latency_threshold() -> None:
    """
    Alerts on cost per run, error rate and latency, each with a threshold you justified.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_cost_reduction_experiment_before_after_numbers_both() -> None:
    """
    A cost-reduction experiment with before/after numbers on both cost **and** quality.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_50_cost_reduction_quality_regression_both_measured() -> None:
    """
    >= 50% cost reduction with no quality regression, both measured against the Week-31 eval
    suite.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_documented_game_day_injected_failure_alert_fired() -> None:
    """
    A documented game-day: an injected failure, the alert that fired, the time to detection
    and the time to resolution.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_tail_based_sampling_under_load_keeping_slow() -> None:
    """
    Tail-based sampling under load, keeping the slow and failed traces while dropping the
    rest, with the retained fraction and the storage saving reported.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_published_tco_analysis_infrastructure_model_storage_engineering() -> None:
    """
    A published TCO analysis: infrastructure, model, storage and engineering time, per 1,000
    incidents handled.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

