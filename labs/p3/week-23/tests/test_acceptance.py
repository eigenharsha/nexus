"""Acceptance tests for LAB-P3-W23 — Containerized prediction service → serverless.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_fastapi_wrapper_around_model_plus_dockerfile_builds() -> None:
    """
    A FastAPI wrapper around the model plus a Dockerfile that builds and runs locally, with
    a documented `docker run` command that returns a prediction.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_versioned_model_artifact_file_sha256_training_commit() -> None:
    """
    A versioned model artifact: the file, its sha256, the training commit, and the metrics
    it achieved, all recorded and served at `/version`.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_validated_request_response_models_range_input_returns() -> None:
    """
    Validated request and response models; an out-of-range input returns 422 with a useful
    message.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_healthz_process_alive_readyz_model_loaded_warm() -> None:
    """
    `/healthz` (process is alive) and `/readyz` (model loaded and a warm inference
    succeeded) — and they must be able to disagree, which the test checks by starting the
    app with the model absent.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_multi_stage_docker_build_under_600_mb() -> None:
    """
    A multi-stage Docker build under **600 MB** final image size, asserted by the test.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_docker_compose_stack_bringing_service_dependencies() -> None:
    """
    `docker compose` stack bringing the service up with its dependencies.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_github_actions_ci_building_image_running_tests() -> None:
    """
    GitHub Actions CI building the image, running the tests inside it, and pushing on a tag.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_deployed_aws_lambda_behind_api_gateway_documented() -> None:
    """
    Deployed to AWS Lambda behind API Gateway (or a documented equivalent free-tier target).
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_load_test_cost_report_cost_1_000() -> None:
    """
    A load test and a cost report: cost per 1,000 predictions with the arithmetic shown.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_p95_300_ms_measured_including_cold_starts() -> None:
    """
    p95 < 300 ms measured including cold starts, with the cold-start mitigation you chose
    (provisioned concurrency, a smaller runtime, or a warming ping) and its cost.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_canary_deployment_routing_percentage_traffic_new_version() -> None:
    """
    A canary deployment routing a percentage of traffic to the new version.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_automatic_rollback_triggered_error_rate_threshold_demonstrated() -> None:
    """
    Automatic rollback triggered by an error-rate threshold, demonstrated by deliberately
    deploying a broken version and showing the rollback in the logs.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

