"""Acceptance tests for LAB-P2-W14 — 15 medium problems + route planner.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_eight_guided_problems_hints_reference_solutions_available() -> None:
    """
    Eight guided problems with hints and reference solutions available after your attempt.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")

@pytest.mark.basic
def test_basic_pass_provided_tests_including_edge_cases_empty() -> None:
    """
    Each must pass the provided tests including the edge cases (empty input, single node,
    cycles).
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_fifteen_medium_problems_across_trees_graphs_dynamic() -> None:
    """
    Fifteen medium problems across trees, graphs and dynamic programming, all tests green.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_docstring_stating_time_space_complexity_sentence_why() -> None:
    """
    For each: a docstring stating time and space complexity, and one sentence on why.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_dijkstra_route_planner_cli_over_real_osm() -> None:
    """
    A Dijkstra route planner CLI over real OSM-derived data: `route --from A --to B` returns
    the path, the distance and the node-expansion count.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_planner_uses_own_binary_heap_week_13() -> None:
    """
    The planner uses your own binary heap (Week 13) or `heapq` — state which and why.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_geographic_heuristic_haversine_scaled_measured_node_expansion() -> None:
    """
    A* with a geographic heuristic (haversine, scaled); measured node-expansion ratio >= 3x
    on the provided query set, reported per query.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_written_proof_sketch_admissibility_heuristic_including_what() -> None:
    """
    A written proof sketch of admissibility for your heuristic, including what breaks it if
    the edge weights stop being distances.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

