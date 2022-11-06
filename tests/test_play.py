from inspect import signature

from game import play


def test_play():
    """Smoke test to ensure that play.main() exists."""
    result = str(signature(play.main))

    assert result.endswith(') -> None')
