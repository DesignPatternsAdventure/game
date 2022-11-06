"""Generic Sprite State."""

from enum import Enum
from typing import Literal

from pydantic import BaseModel


class SpriteState(BaseModel):
    """Sprite Model."""

    # PLANNED: Consider extending from: https://api.arcade.academy/en/stable/api/sprites.html#arcade.Sprite

    angle: float = 0
    center_x: int
    center_y: int
    hit_box_algorithm: Literal['None', 'Simple', 'Detailed'] = 'None'
    scale: float = 1.0
    sprite_resource: str


class Direction(Enum):

    DOWN = [0, 1, 2]
    LEFT = [3, 4, 5]
    RIGHT = [6, 7, 8]
    UP = [9, 10, 11]


class PlayerState(SpriteState):

    should_update: int = 0
    cur_texture_index: int = 0
    direction: Direction = Direction.LEFT
