"""Acceptance tests for LAB-P4-W29 — Agent from scratch + custom MCP server.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_react_loop_two_tools_max_iteration_guard() -> None:
    """
    A ReAct loop with two tools and a max-iteration guard, with the reasoning trace printed.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_agent_built_scratch_tool_registry_json_schema() -> None:
    """
    An agent built from scratch: a tool registry with JSON-schema tool definitions,
    conversation memory with a summarization strategy when the window fills, an explicit
    token budget, retries on malformed tool calls, and structured stop conditions (goal
    reached / budget exhausted / max iterations / explicit give-up).
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_custom_mcp_server_exposing_database_read_only() -> None:
    """
    A custom MCP server exposing a database (read-only, parameterized queries only) and
    sandboxed terminal access.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_sandbox_allowlist_commands_network_read_only_filesystem() -> None:
    """
    Sandbox: an allowlist of commands, no network, a read-only filesystem except one temp
    dir, a wall-clock timeout and an output size cap. Each of those is tested by trying to
    violate it.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_success_measured_over_30_task_benchmark_reported() -> None:
    """
    Success measured over a 30-task benchmark with a reported success rate and a failure
    taxonomy.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_full_test_suite_against_mocked_model_agent() -> None:
    """
    A full test suite against a **mocked model** — the agent's logic must be testable
    without calling anything.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_scale_30_tools_selection_accuracy_maintained_within() -> None:
    """
    Scale to 30 tools with selection accuracy maintained within a stated margin of the
    5-tool baseline; report the technique you used (retrieval over tool descriptions,
    hierarchical grouping, or something else) and the numbers before and after.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_adversarial_test_suite_against_sandbox_prompt_injection() -> None:
    """
    An adversarial test suite against the sandbox: prompt injection through tool output,
    path traversal, command chaining, resource exhaustion, and data exfiltration through an
    allowed command. Every attempt documented with its outcome and mitigation.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

