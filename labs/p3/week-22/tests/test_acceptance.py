"""Acceptance tests for LAB-P3-W22 — Blood-cell image classifier (>=90% test accuracy).

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_train_provided_cnn_skeleton_prepared_split_modest() -> None:
    """
    Train the provided CNN skeleton on the prepared split to a modest stated accuracy, with
    the training loop, checkpointing and a plotted curve.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_dataset_audit_first_class_balance_duplicates_near() -> None:
    """
    A dataset audit first: class balance, duplicates, near-duplicates across the train/test
    split, corrupt files, and label spot-checks. Report what you found before you train
    anything.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_augmentation_policy_chosen_domain_justified_rejected_reason() -> None:
    """
    An augmentation policy chosen for this domain and justified — and one you rejected, with
    the reason (horizontal flip is fine for cells; it is not fine for text).
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_custom_cnn_baseline_trained_scratch_transfer_learning() -> None:
    """
    A custom CNN baseline trained from scratch, then transfer learning from a pretrained
    backbone (ResNet-18 or EfficientNet-B0), with the frozen/unfrozen schedule documented.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_90_test_accuracy_held_split() -> None:
    """
    >= 90% test accuracy on the held-out split.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_mixed_precision_amp_where_gpu_present_cpu() -> None:
    """
    Mixed precision (AMP) where a GPU is present, with the CPU path still correct.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_checkpointing_resumes_correctly_mid_epoch() -> None:
    """
    Checkpointing that resumes correctly mid-epoch.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_class_precision_recall_f1_confusion_matrix_error() -> None:
    """
    Per-class precision/recall/F1, a confusion matrix, and an error analysis of the 20 worst
    misclassifications with a written pattern.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_model_card() -> None:
    """
    A model card.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_93_test_accuracy_under_stated_cpu_latency() -> None:
    """
    >= 93% test accuracy under the stated CPU latency budget.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_onnx_export_output_parity_against_pytorch_model() -> None:
    """
    ONNX export with output parity against the PyTorch model to 1e-4.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_latency_size_table_pytorch_eager_torchscript_onnx() -> None:
    """
    A latency/size table: PyTorch eager, TorchScript, ONNX Runtime, and a quantized variant
    — p50/p95 latency and file size for each, measured on CPU.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_grad_cam_explanations_five_predictions_including_least() -> None:
    """
    Grad-CAM explanations for five predictions, including at least one the model got wrong.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

