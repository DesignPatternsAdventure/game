from inspect import signature

import pytest

from game import play


@pytest.mark.tasks
def test_play():
    """Smoke test to ensure that play.main() exists."""
    result = str(signature(play.main))

    assert result.endswith(") -> None")
