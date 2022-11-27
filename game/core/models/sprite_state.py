"""Generic Sprite State."""

from enum import Enum
from typing import Literal

from pydantic import BaseModel  # pylint: disable=E0611

from ..constants import STARTING_X, STARTING_Y


class SpriteState(BaseModel):
    """Sprite Model."""

    # PLANNED: Consider extending from: https://api.arcade.academy/en/stable/api/sprites.html#arcade.Sprite

    angle: float = 0
    center_x: int = STARTING_X
    center_y: int = STARTING_Y
    hit_box_algorithm: Literal["None", "Simple", "Detailed"] = "None"
    scale: float = 1.0
    sprite_resource: str


class Direction(Enum):

    DOWN = [0, 1, 2]
    LEFT = [3, 4, 5]
    RIGHT = [6, 7, 8]
    UP = [9, 10, 11]


class PlayerState(SpriteState):

    sprite_resource: str = "N/A"
    should_update: int | float = 0
    cur_texture_index: int = 0
    direction: Direction = Direction.DOWN
