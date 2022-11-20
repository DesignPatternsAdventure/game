"""Raft class."""

from enum import Enum

import arcade
from arcade import Sprite
from beartype import beartype

from ..constants import SPRITE_SIZE


class RaftDirection(Enum):

    DOWN = [0, 1, 2, 3]
    LEFT = [4, 5, 6, 7]
    RIGHT = [8, 9, 10, 11]
    UP = [12, 13, 14, 15]

class RaftSprite(arcade.Sprite):
    should_update: int | float = 0
    cur_texture_index: int = 0
    direction: RaftDirection = RaftDirection.DOWN
    @beartype
    def __init__(self, sheet_name: str, center_x, center_y) -> None:
        super().__init__()
        self.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width=SPRITE_SIZE * 4.5,
            sprite_height=SPRITE_SIZE * 6,
            columns=4,
            count=16,
        )
        self.texture = self.textures[self.cur_texture_index]
        self.center_x = center_x
        self.center_y = center_y

    @beartype
    def on_update(self, delta_time: float = 0.0) -> None:
        if not self.change_x and not self.change_y:
            return

        if self.should_update <= 1:
            self.should_update += 0.4
        else:
            self.should_update = 0
            self.cur_texture_index += 1

        slope = self.change_y / (self.change_x + 0.0001)
        if abs(slope) < 0.8:
            self.direction = (
                RaftDirection.RIGHT if self.change_x > 0 else RaftDirection.LEFT
            )
        else:
            self.direction = RaftDirection.UP if self.change_y > 0 else RaftDirection.DOWN

        if self.cur_texture_index not in self.direction.value:
            self.cur_texture_index = self.direction.value[0]

        self.texture = self.textures[self.cur_texture_index]
