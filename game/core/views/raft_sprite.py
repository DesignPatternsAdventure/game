"""Sprite Classes from community_rpg."""

import arcade
from arcade import Sprite
from beartype import beartype

from ..constants import SPRITE_SIZE
from ..models.base_player_inventory import PlayerInventoryInterface
from ..models.sprite_state import Direction, PlayerState


class RaftSprite(arcade.Sprite):
    should_update: int | float = 0
    cur_texture_index: int = 0
    direction: Direction = Direction.DOWN
    @beartype
    def __init__(self, sheet_name: str, center_x, center_y) -> None:
        super().__init__()
        self.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width=SPRITE_SIZE * 6,
            sprite_height=SPRITE_SIZE * 6,
            columns=3,
            count=12,
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
                Direction.RIGHT if self.change_x > 0 else Direction.LEFT
            )
        else:
            self.direction = Direction.UP if self.change_y > 0 else Direction.DOWN

        if self.cur_texture_index not in self.direction.value:
            self.cur_texture_index = self.direction.value[0]

        self.texture = self.textures[self.cur_texture_index]

        self.center_x += self.change_x
        self.center_y += self.change_y
