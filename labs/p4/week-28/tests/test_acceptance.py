"""Acceptance tests for LAB-P4-W28 — Production hybrid RAG.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_add_bm25_week_27_system_fuse_two() -> None:
    """
    Add BM25 to the Week-27 system and fuse the two rankings with reciprocal rank fusion;
    report the change in Recall@10.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_hybrid_retrieval_bm25_plus_dense_fused_rrf() -> None:
    """
    Hybrid retrieval: BM25 plus dense, fused with RRF, with the fusion constant tuned.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_hyde_query_rewriting_ablated_does_always_help() -> None:
    """
    HyDE query rewriting, ablated (it does not always help — report your number either way).
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_cross_encoder_re_ranking_top_k_k() -> None:
    """
    Cross-encoder re-ranking of the top-k, with k chosen from the latency budget.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_semantic_cache_similarity_threshold_chosen_measurement_reporting() -> None:
    """
    A semantic cache with a similarity threshold chosen by measurement, reporting hit rate
    and the false-hit rate at that threshold.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_grounded_generation_citations_where_claim_maps_retrieved() -> None:
    """
    Grounded generation with citations, where every claim maps to a retrieved chunk and an
    unsupported claim is detectable.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_stage_ablated_week_27_eval_set_final() -> None:
    """
    Every stage ablated on the Week-27 eval set, with a final table: quality, p95 latency,
    $/query.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_meet_quality_target_inside_stated_latency_cost() -> None:
    """
    Meet the quality target inside the stated latency and cost budgets, all three measured.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_incremental_re_indexing_changed_document_updates_place() -> None:
    """
    Incremental re-indexing: a changed document updates in place without a full rebuild,
    with the time for both reported.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_cache_correctness_after_update_proven_test_query() -> None:
    """
    Cache correctness after an update proven by test: a query cached before a document
    change must not return the stale answer.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

