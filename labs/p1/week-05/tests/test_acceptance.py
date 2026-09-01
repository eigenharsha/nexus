"""Acceptance tests for LAB-P1-W05 — Static frontend against a public API.

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_fetch_list_provided_public_api_render() -> None:
    """
    Fetch a list from the provided public API and render it.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")

@pytest.mark.basic
def test_basic_show_loading_indicator_while_request_flight() -> None:
    """
    Show a loading indicator while the request is in flight.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")

@pytest.mark.basic
def test_basic_show_error_message_empty_list_when_request() -> None:
    """
    Show an error message (not an empty list) when the request fails — test it by blocking
    the request in devtools.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_responsive_layout_works_360_px_1920_px() -> None:
    """
    Responsive layout, works from 360 px to 1920 px with no horizontal scroll.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_search_250_ms_debounce_flight_request_aborted() -> None:
    """
    Search with a 250 ms debounce; the in-flight request is aborted when the query changes.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_pagination_correct_aria_current_keyboard_access() -> None:
    """
    Pagination with correct `aria-current` and keyboard access.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_dark_mode_following_prefers_color_scheme_manual() -> None:
    """
    Dark mode following `prefers-color-scheme`, with a manual override that persists.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_four_states_own_visual_treatment_own_test() -> None:
    """
    All four states, each with its own visual treatment and its own test.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_framework_vanilla_es2022_modules() -> None:
    """
    No framework. Vanilla ES2022 modules.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_lighthouse_90_four_categories_screenshot_readme() -> None:
    """
    Lighthouse >= 90 on all four categories, screenshot in the README.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_offline_caching_service_worker_explicit_cache_versioning() -> None:
    """
    Offline caching via a service worker with an explicit cache-versioning strategy.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_request_cancellation_proven_rapid_typing_produces_exactly() -> None:
    """
    Request cancellation proven: rapid typing produces exactly one rendered result set.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_virtualized_list_rendering_only_visible_window_dom() -> None:
    """
    A virtualized list rendering only the visible window; DOM node count stays bounded
    (assert it in the console) while scrolling 50,000 rows.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

