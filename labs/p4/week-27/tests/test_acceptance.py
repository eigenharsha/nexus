"""Acceptance tests for LAB-P4-W27 — 1,000-PDF retrieval system on pgvector/HNSW.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_ingest_50_provided_pdfs_parse_chunk_embed() -> None:
    """
    Ingest 50 provided PDFs: parse, chunk, embed, store in pgvector, and query, returning
    the top 5 chunks with their source document and page.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_ingest_1_000_real_pdfs_robust_parsing() -> None:
    """
    Ingest 1,000 real PDFs with robust parsing: multi-column layouts, tables, scanned pages
    (report what fraction failed and why — a parser that silently returns empty text is the
    failure mode here).
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_chunking_strategy_chosen_justified_least_three_alternatives() -> None:
    """
    A chunking strategy chosen and justified, with at least three alternatives evaluated
    (fixed-size, recursive, semantic) on the eval set.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_embedding_model_chosen_measurement_least_two_compared() -> None:
    """
    An embedding model chosen by measurement, with at least two compared.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_pgvector_hnsw_index_m_ef_construction_tuned() -> None:
    """
    pgvector with an HNSW index, `m` and `ef_construction` tuned, and `ef_search` swept at
    query time.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_metadata_filtering_document_type_date_correct_test() -> None:
    """
    Metadata filtering (by document type and date) that is correct — the test checks that
    filtered search does not silently drop results that should match.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_100_query_evaluation_set_judged_relevance() -> None:
    """
    A 100-query evaluation set with judged relevance.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_full_ablation_report_recall_1_5_10() -> None:
    """
    A full ablation report: Recall@1/5/10 and NDCG@10 for every configuration.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_10m_chunks_indexed_report_build_time_index() -> None:
    """
    10M chunks indexed; report build time, index memory, p95 query latency and Recall@10,
    with the recall/latency trade-off curve across `ef_search`.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_correct_filtered_search_scale_demonstrate_post_filter() -> None:
    """
    Correct filtered search at scale: demonstrate the post-filter recall collapse that naive
    filtering causes, then fix it, with the numbers for both.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

