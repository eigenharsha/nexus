"""Acceptance tests for LAB-P1-W06 — "Resume Tailor" full-stack service.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_post_tailor_accepting_resume_text_job_description() -> None:
    """
    `POST /tailor` accepting `{resume_text, job_description}` returns formatted Markdown.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")

@pytest.mark.basic
def test_basic_pydantic_models_both_request_response_missing_field() -> None:
    """
    Pydantic models for both request and response; a missing field returns 422 with a useful
    body.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")

@pytest.mark.basic
def test_basic_wire_week_5_frontend() -> None:
    """
    Wire the Week-5 frontend to it.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_fastapi_pydantic_v2_models_request_response() -> None:
    """
    FastAPI with Pydantic v2 models on every request and response.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_file_upload_endpoint_size_limit_2_mb() -> None:
    """
    File upload endpoint with size limit (2 MB), content-type allowlist, and
    extension/`magic` agreement — reject a `.pdf` that is actually a zip.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_api_key_auth_write_endpoints_401_vs() -> None:
    """
    API-key auth on write endpoints; 401 vs 403 used correctly.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_rate_limiting_key_retry_after_header() -> None:
    """
    Rate limiting per key with a `Retry-After` header.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_structured_error_responses_shape_error_machine_readable() -> None:
    """
    Structured error responses: one shape for every error, with a machine-readable `code`.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_fully_async_i_o_blocking_call_coroutine() -> None:
    """
    Fully async I/O — no blocking call in a coroutine (the test asserts the event loop is
    never blocked for more than 50 ms).
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_25_tests_including_auth_failures_oversize_uploads() -> None:
    """
    25+ tests including auth failures, oversize uploads, malformed JSON and rate-limit
    behaviour.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_docs_renders_endpoint_has_description_example() -> None:
    """
    `/docs` renders and every endpoint has a description and an example.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_idempotency_keys_same_key_same_body_returns() -> None:
    """
    Idempotency keys: same key + same body returns the cached response; same key + different
    body returns 409.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_background_job_processing_status_polling_endpoint_202() -> None:
    """
    Background job processing with a status-polling endpoint (`202` + `Location`).
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_load_test_locust_k6_50_concurrent_users() -> None:
    """
    Load test (`locust` or `k6`) at 50 concurrent users showing p95 < 200 ms, report
    committed.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

