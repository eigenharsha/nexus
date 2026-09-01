"""Acceptance tests for LAB-P4-W31 — Eval CI pipeline + guardrail layer.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_twenty_eval_cases_assertions_running_locally_pytest() -> None:
    """
    Twenty eval cases with assertions running locally via `pytest`, with a summary report.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_100_case_eval_suite_combining_deterministic_assertions() -> None:
    """
    A 100+ case eval suite combining deterministic assertions, a validated LLM judge, and
    RAG metrics (faithfulness, answer relevance, context precision).
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_running_github_actions_prompt_code_change_failing() -> None:
    """
    Running in GitHub Actions on every prompt or code change, failing the build on a
    regression against a committed baseline.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_results_comment_posted_pr_showing_category_pass() -> None:
    """
    A results comment posted on the PR showing per-category pass rates and the diff versus
    baseline.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_llama_guard_equivalent_input_layer_plus_output() -> None:
    """
    A Llama Guard (or equivalent) input layer, plus output checks for PII and groundedness.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_measured_false_positive_true_positive_rates_guardrail() -> None:
    """
    Measured false-positive and true-positive rates for every guardrail, on a labelled set.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_judge_agreement_human_labels_above_stated_threshold() -> None:
    """
    Judge agreement with human labels above the stated threshold, reported as Cohen's kappa
    with its confidence interval.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_red_team_report_15_attacks_direct_injection() -> None:
    """
    A red-team report: 15 attacks (direct injection, indirect injection through retrieved
    content, jailbreak, data exfiltration, denial of wallet, and more), each with the
    outcome and the mitigation, and a re-test after the mitigation.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_eval_suite_runtime_cost_inside_stated_budget() -> None:
    """
    Eval suite runtime and cost inside the stated budget, with both reported per run.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

