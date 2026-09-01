"""Acceptance tests for LAB-P4-W25 — `minbpe` + `nanoGPT` from scratch.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_bpe_encode_decode_against_provided_merge_table() -> None:
    """
    BPE encode/decode against a provided merge table, round-tripping the provided corpus
    exactly.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")

@pytest.mark.basic
def test_basic_compute_attention_fixed_example_hand_code_show() -> None:
    """
    Compute attention for one fixed example by hand and in code, and show they agree.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_train_own_byte_level_bpe_tokenizer_corpus() -> None:
    """
    Train your own byte-level BPE tokenizer on a corpus: merge training, encode, decode,
    special tokens, and exact round-trip on arbitrary UTF-8 including emoji and unpaired
    surrogates.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_full_causal_transformer_scaled_dot_product_attention() -> None:
    """
    A full causal Transformer: scaled dot-product attention with the causal mask, multi-head
    attention, an MLP block, layer norm placed deliberately (pre-norm, and say why),
    residual connections, a block, a stack, and an LM head with weight tying.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_component_unit_tested_against_torch_nn_equivalent() -> None:
    """
    Every component unit-tested against the `torch.nn` equivalent given identical weights,
    to 1e-5.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_trained_small_corpus_stated_loss_generated_samples() -> None:
    """
    Trained on a small corpus to a stated loss, with generated samples committed.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_kv_cached_generation_producing_token_identical_output() -> None:
    """
    KV-cached generation producing **token-identical** output to the uncached path, with the
    speedup measured at three sequence lengths.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_rotary_position_embeddings_replacing_learned_positional_embeddings() -> None:
    """
    Rotary position embeddings replacing learned positional embeddings, with the equivalence
    check against a reference implementation.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_grouped_query_attention_configurable_group_count_report() -> None:
    """
    Grouped-query attention with a configurable group count; report the KV-cache memory
    saving.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_flashattention_f_scaled_dot_product_attention_output() -> None:
    """
    FlashAttention via `F.scaled_dot_product_attention`, with output parity against your own
    implementation to 1e-4.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_tokens_sec_peak_memory_three_context_lengths() -> None:
    """
    Tokens/sec and peak memory at three context lengths (512 / 2048 / 8192) for each
    variant, in one table.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_attention_visualization_tool_rendering_head_attention_pattern() -> None:
    """
    An attention-visualization tool rendering the per-head attention pattern for a given
    prompt.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

