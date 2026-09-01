"""Acceptance tests for LAB-P3-W24 — Kubernetes model-serving cluster.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_deployment_service_week_23_image_kind_cluster() -> None:
    """
    A Deployment and a Service for the Week-23 image on a `kind` cluster, reachable via
    `kubectl port-forward`, returning a prediction.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_full_manifests_deployment_service_ingress_configmap_secret() -> None:
    """
    Full manifests: Deployment, Service, Ingress, ConfigMap, Secret,
    liveness/readiness/startup probes, and resource requests and limits that you chose from
    measured usage rather than guessed.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_horizontalpodautoscaler_scaling_cpu_demonstrated_scaling_under_load() -> None:
    """
    A HorizontalPodAutoscaler scaling on CPU, demonstrated scaling up under load and back
    down.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_tensorflow_serving_deployment_alongside_fastapi_trade_off() -> None:
    """
    A TensorFlow Serving deployment alongside the FastAPI one, with the trade-off written
    down.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_prometheus_metrics_exposed_service_scraped_plus_grafana() -> None:
    """
    Prometheus metrics exposed by the service and scraped, plus a Grafana dashboard with
    request rate, latency percentiles, error rate and pod count.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_load_test_report_showing_scale_behaviour_timing() -> None:
    """
    A load-test report showing the scale-up behaviour with the timing of each phase.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_zero_downtime_rolling_update_under_sustained_load() -> None:
    """
    Zero-downtime rolling update under sustained load, with the client-side request log
    committed as evidence: zero failed requests across the rollout.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_custom_metric_autoscaling_queue_depth_prometheus_adapter() -> None:
    """
    Custom-metric autoscaling on queue depth (via the Prometheus adapter), with the reason
    CPU is the wrong signal for this workload.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_p50_p95_p99_documented_three_load_levels() -> None:
    """
    p50/p95/p99 documented at three load levels, plus a cost-per-1M-predictions estimate
    compared against the Week-23 serverless number.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

