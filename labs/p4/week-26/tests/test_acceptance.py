"""Acceptance tests for LAB-P4-W26 — QLoRA fine-tune for strict structured output.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_run_provided_qlora_config_end_end_verify() -> None:
    """
    Run the provided QLoRA config end to end; verify the model loads, generates, and that
    the adapter actually changed the output versus the base model.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_build_dataset_500_examples_real_structured_extraction() -> None:
    """
    Build a dataset of 500+ examples for a real structured-extraction task, with a
    documented construction process and a held-out split that was never trained on.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_qlora_fine_tune_3b_model_4_bit() -> None:
    """
    QLoRA fine-tune of a 3B model: 4-bit base, LoRA adapters on the attention and MLP
    projections, with the rank, alpha and target modules chosen and justified.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_99_schema_valid_output_held_set_measured() -> None:
    """
    >99% schema-valid output on the held-out set, measured by actually parsing and
    validating against the schema — not by eyeballing.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_merge_adapter_serve_vllm_behind_openai_compatible() -> None:
    """
    Merge the adapter and serve via vLLM behind an OpenAI-compatible endpoint.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_integrate_week_6_service_replacing_rule_based() -> None:
    """
    Integrate into the Week-6 service, replacing the rule-based path behind a feature flag.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_documented_cpu_colab_fallback_path_so_lab() -> None:
    """
    A documented CPU/Colab fallback path so this lab is completable with no local GPU.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_beat_base_constrained_decoding_accuracy_cost_both() -> None:
    """
    Beat base + constrained decoding on accuracy *and* cost, with both measured.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_lora_rank_sweep_least_r_4_8() -> None:
    """
    A LoRA rank sweep (at least r = 4, 8, 16, 32) with quality and training cost for each.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_quantization_pareto_plot_quality_vs_latency_vs() -> None:
    """
    A quantization Pareto plot: quality vs latency vs memory across at least three
    quantization settings.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_written_serve_vs_api_cost_analysis_three() -> None:
    """
    A written serve-vs-API cost analysis at three volume levels, including the GPU hours.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

