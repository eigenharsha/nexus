"""Acceptance tests for LAB-P3-W18 — Customer churn: end-to-end tabular modelling.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_train_random_forest_prepared_dataset_report_accuracy() -> None:
    """
    Train a random forest on the prepared dataset and report accuracy and AUC on the held-
    out split.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_full_workflow_real_churn_dataset_majority_class() -> None:
    """
    A full workflow on the real churn dataset: a majority-class baseline, then logistic
    regression, then random forest, then XGBoost — each with the same validation strategy.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_validation_strategy_chosen_deliberately_stratified_k_fold() -> None:
    """
    A validation strategy chosen deliberately (stratified k-fold, or time-based if the data
    has a time axis) and documented, including why the other option is wrong here.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_hyperparameter_search_stated_budget_search_space_justified() -> None:
    """
    Hyperparameter search with a stated budget, and the search space justified.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_permutation_feature_importance_just_impurity_based_difference() -> None:
    """
    Permutation feature importance (not just the impurity-based one) with the difference
    explained.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_calibration_check_reliability_curve_plus_brier_score() -> None:
    """
    A calibration check: reliability curve plus Brier score, before and after calibration.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_k_means_segmentation_predicted_churners_k_chosen() -> None:
    """
    K-Means segmentation of the predicted churners, with the k chosen by a stated method and
    each cluster described in one business sentence.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_business_recommendation_estimated_impact_assumptions_written() -> None:
    """
    A business recommendation with an estimated £/$ impact and the assumptions written out.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_meet_auc_target_inside_training_time_budget() -> None:
    """
    Meet the AUC target inside the training-time budget; report both.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_shap_explanations_five_individual_customers_paragraph_reading() -> None:
    """
    SHAP explanations for five individual customers, each with a one-paragraph reading a
    non-technical reader would follow.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_model_card_intended_use_training_data_metrics() -> None:
    """
    A model card: intended use, training data, metrics by slice, known limitations, and the
    conditions under which the model should be retired.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

