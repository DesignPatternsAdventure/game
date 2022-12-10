from itertools import zip_longest

import pytest
from arcade import key

from game.core.view_strategies.movement import _resolve_cardinal_direction


@pytest.mark.parametrize(
    ("card_keys", "directions"),
    (
        ([key.UP, key.DOWN, key.LEFT, key.RIGHT], [(0, 1), (0, -1), (-1, 0), (1, 0)]),
        ([key.W, key.S, key.A, key.D], [(0, 1), (0, -1), (-1, 0), (1, 0)]),
        ([key.G], [(0, 0)]),
    ),
)
def test_resolve_cardinal_direction(card_keys, directions):
    errors = []
    for card_key, expected in zip_longest(card_keys, directions):
        if (result := _resolve_cardinal_direction(card_key)) != expected:
            errors.append(
                f"For key {card_key}, expected {expected}, but found: {result}"
            )

    assert not errors
