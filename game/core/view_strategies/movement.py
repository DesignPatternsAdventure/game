"""Movement strategies."""

from beartype import beartype

from ..constants import KEYS_DOWN, KEYS_LEFT, KEYS_RIGHT, KEYS_UP
from ..views import GameSprite


@beartype
def _resolve_cardinal_direction(key: int) -> tuple[int, int]:
    """Resolve cardinal keys direction."""
    d_x, d_y = 0, 0
    if key in KEYS_UP:
        d_y = 1
    elif key in KEYS_LEFT:
        d_x = -1
    elif key in KEYS_DOWN:
        d_y = -1
    elif key in KEYS_RIGHT:
        d_x = 1
    return d_x, d_y


@beartype
def cardinal_key_move(sprite: GameSprite, key: int, modifiers: int) -> None:
    """Resolve sprite motion based on key input for both Arrow and WASD Keys."""
    step = sprite.attr.step_size
    if not step:
        return

    d_x, d_y = (step * _d for _d in _resolve_cardinal_direction(key))
    sprite.move(d_x, d_y)
