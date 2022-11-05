"""Movement strategies."""

import arcade.key
from beartype import beartype

from ..views import GameSprite


def _resolve_cardinal_direction(key: int) -> tuple[int, int]:
    """Resolve cardinal keys direction."""
    d_x, d_y = 0, 0
    match key:
        # Support Arrow Keys
        case arcade.key.UP:
            d_y = 1
        case arcade.key.LEFT:
            d_x = -1
        case arcade.key.DOWN:
            d_y = -1
        case arcade.key.RIGHT:
            d_x = 1
        # And WASD
        case arcade.key.W:
            d_y = 1
        case arcade.key.A:
            d_x = -1
        case arcade.key.S:
            d_y = -1
        case arcade.key.D:
            d_x = 1
    return d_x, d_y


@beartype
def cardinal_key_move(sprite: GameSprite, key: int, modifiers: int) -> None:
    """Resolve sprite motion based on key input for both Arrow and WASD Keys."""
    step = sprite.state.step_size
    if not step:
        return

    d_x, d_y = (step * _d for _d in _resolve_cardinal_direction(key))
    sprite.move(d_x, d_y)
