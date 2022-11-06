from itertools import zip_longest

import pytest
from arcade import key

from game.core.models import EntityAttr, SpriteState
from game.core.view_strategies.movement import _resolve_cardinal_direction, cardinal_key_move
from game.core.views import GameSprite


@pytest.mark.parametrize(
    ('card_keys', 'directions'), (
        ([key.UP, key.DOWN, key.LEFT, key.RIGHT], [(0, 1), (0, -1), (-1, 0), (1, 0)]),
        ([key.W, key.S, key.A, key.D], [(0, 1), (0, -1), (-1, 0), (1, 0)]),
        ([key.G], [(0, 0)]),
    ),
)
def test_resolve_cardinal_direction(card_keys, directions):
    errors = []
    for card_key, expected in zip_longest(card_keys, directions):
        if (result := _resolve_cardinal_direction(card_key)) != expected:
            errors.append(f'For key {card_key}, expected {expected}, but found: {result}')

    assert not errors


def test_cardinal_key_move():
    attr = EntityAttr(step_size=None)
    resource = ':resources:images/animated_characters/female_person/femalePerson_idle.png'
    state = SpriteState(sprite_resource=resource, center_x=0, center_y=0)
    sprite = GameSprite(attr, state)

    assert cardinal_key_move(sprite, 0, 0) is None
