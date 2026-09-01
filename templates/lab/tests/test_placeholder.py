"""Replace this file with the lab's real acceptance tests.

Rules for a Nexus lab test suite:

1. Tests import the implementation by module name, never by path — `make verify` controls
   which directory is on `sys.path`.
2. Every test carries exactly one track marker: `basic`, `standard` or `hard`.
   Tracks are cumulative — a `basic` test also runs on `standard` and `hard`.
3. `make contract` must pass: the suite is green on `solution/` and red on `starter/`.
   A test that passes against an empty starter is not a test.
"""
import pytest


@pytest.mark.basic
def test_replace_me() -> None:
    pytest.fail("this lab has no acceptance tests yet")
