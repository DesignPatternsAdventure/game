"""Generic Sprite State."""

from enum import Enum
from typing import Literal

from beartype import beartype
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


class VehicleDirection(Enum):

    DOWN = [0, 1, 2, 3]
    LEFT = [4, 5, 6, 7]
    RIGHT = [8, 9, 10, 11]
    UP = [12, 13, 14, 15]


class PlayerState(SpriteState):

    sprite_resource: str = "N/A"
    time_since_last_update: int | float = 0
    cur_texture_index: int = 0
    direction: Direction = Direction.DOWN
    vehicle_texture_index: int = 0
    vehicle_direction: VehicleDirection | None = None

    @beartype
    def on_update(self, delta_time: float = 0.0) -> None:
        self.time_since_last_update += delta_time
        if self.time_since_last_update >= 1:
            self.time_since_last_update = 0
            self.cur_texture_index += 1

        if self.cur_texture_index not in self.direction.value:
            self.cur_texture_index = self.direction.value[0]

        if (
            self.vehicle_direction
            and self.vehicle_texture_index not in self.vehicle_direction.value
        ):
            self.vehicle_texture_index = self.vehicle_direction.value[0]
