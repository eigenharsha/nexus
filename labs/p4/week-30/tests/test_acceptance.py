"""Acceptance tests for LAB-P4-W30 — Incident Auto-Remediation System.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_three_node_langgraph_plan_analyze_report_memory() -> None:
    """
    A three-node LangGraph (plan → analyze → report) with in-memory state, running end to
    end on a sample incident.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_planner_analyst_executor_agents_langgraph_typed_state() -> None:
    """
    Planner, analyst and executor agents on LangGraph with a **typed** state schema.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_postgres_checkpointing_so_state_survives_process_restart() -> None:
    """
    Postgres checkpointing so state survives a process restart.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_human_approval_interrupt_before_any_remediation_action() -> None:
    """
    A human-approval interrupt before **any** remediation action, with the proposed action
    and its blast radius shown to the approver.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_rag_over_runbook_corpus_reusing_week_27() -> None:
    """
    RAG over a runbook corpus (reusing the Week-27/28 pipeline).
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_mcp_served_sandboxed_terminal_access_reusing_week() -> None:
    """
    MCP-served sandboxed terminal access (reusing Week 29).
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_budget_guards_tokens_wall_time_tool_calls() -> None:
    """
    Budget guards on tokens, wall time and tool calls, each of which halts the run with a
    clear state.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_crash_resume_proven_test_kill_process_mid() -> None:
    """
    Crash-resume proven by test: kill the process mid-run, restart, and the graph continues
    from the last checkpoint without repeating a side effect.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_kill_storm_suite_20_randomly_timed_sigkills() -> None:
    """
    The kill-storm suite: 20 randomly-timed `SIGKILL`s during a run, with zero duplicated
    side effects and zero lost work, verified against a side-effect ledger.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_critic_agent_reviewing_planner_s_output_measured() -> None:
    """
    A critic agent reviewing the planner's output, with a measured quality improvement on a
    fixed task set — report the number, including if it is small.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_full_failure_injection_suite_green_tool_timeout() -> None:
    """
    A full failure-injection suite green: tool timeout, model returning malformed JSON,
    database unavailable, approval never granted, and budget exhausted mid-action.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

