"""Acceptance tests for LAB-P2-W11 — `nanomath`: a from-scratch math library.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_dot_u_v_transpose_matmul_b_nested() -> None:
    """
    `dot(u, v)`, `transpose(A)`, `matmul(A, B)` on nested Python lists, passing the provided
    tests.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")

@pytest.mark.basic
def test_basic_shape_errors_raise_clear_exception_rather_producing() -> None:
    """
    Shape errors raise a clear exception rather than producing a wrong answer.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_vector_matrix_types_indexing_shape_validation() -> None:
    """
    `Vector` and `Matrix` types with `+ - * @`, indexing, and shape validation.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_l1_l2_l_inf_norms_cosine_similarity() -> None:
    """
    L1 / L2 / L-inf norms; cosine similarity.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_gauss_jordan_inverse_partial_pivoting_singular_matrix() -> None:
    """
    Gauss-Jordan inverse with partial pivoting; a singular matrix raises, not returns
    garbage.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_power_iteration_dominant_eigenvalue_eigenvector_convergence_criterion() -> None:
    """
    Power iteration for the dominant eigenvalue/eigenvector, with a convergence criterion
    you chose.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_pca_svd_validated_against_sklearn_decomposition_pca() -> None:
    """
    PCA via SVD, validated against `sklearn.decomposition.PCA` on the same data (signs may
    differ — handle that in the test, not by fudging).
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_numerical_gradient_central_difference_documented_step_size() -> None:
    """
    Numerical gradient (central difference) with a documented step size and the error
    analysis for it.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_reverse_mode_autodiff_engine_about_100_lines() -> None:
    """
    A reverse-mode autodiff engine in about 100 lines, supporting `+ * - / ** exp log tanh`.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_numeric_result_tested_against_numpy_1e_6() -> None:
    """
    Every numeric result tested against NumPy to 1e-6.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_tiled_blocked_matmul_10x_naive_version_n() -> None:
    """
    Tiled/blocked matmul >= 10x the naive version at n=512; report the tile size you chose
    and the measured numbers for at least three tile sizes.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_autodiff_engine_trains_2_layer_network_toy() -> None:
    """
    The autodiff engine trains a 2-layer network on a toy classification set to a stated
    accuracy.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_benchmark_report_numbers_cache_explanation_tile_size() -> None:
    """
    A benchmark report with the numbers and the cache explanation for the tile size.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

