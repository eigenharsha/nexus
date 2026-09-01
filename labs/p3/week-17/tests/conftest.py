"""Shared pytest fixtures for a Nexus lab.

`make verify` puts the implementation directory (starter/ or solution/) first on PYTHONPATH,
so tests always `import` the module by name and never care which one they are grading.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

LAB_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def track() -> str:
    """The track `make verify` was invoked with: basic | standard | hard."""
    return os.environ.get("NEXUS_TRACK", "standard")


@pytest.fixture(scope="session")
def impl_dir() -> Path:
    """The implementation directory under test: starter/ or solution/."""
    return LAB_ROOT / os.environ.get("NEXUS_IMPL", "starter")


@pytest.fixture(scope="session")
def lab_root() -> Path:
    return LAB_ROOT
