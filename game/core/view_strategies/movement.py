"""Movement strategies."""

from beartype import beartype

from ..constants import KEYS_DOWN, KEYS_LEFT, KEYS_RIGHT, KEYS_UP


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
