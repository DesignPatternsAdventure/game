from datetime import timedelta

from game.core.game_clock import GameClock
from game.core.models.entity_attr import EntityAttr


def test_entity_attr_update():
    attr = EntityAttr()
    game_clock = GameClock()

    result = attr.on_update(game_clock)

    assert result == timedelta(seconds=0)
