"""Raft class."""

import arcade
from beartype import beartype

from ..constants import SPRITE_SIZE
from ..models.sprite_state import PlayerState, VehicleDirection, VehicleType


class RaftSprite(arcade.Sprite):
    @beartype
    def __init__(self, sheet_name: str, center_x, center_y) -> None:  # type: ignore[no-untyped-def]
        super().__init__()
        self.type = VehicleType.RAFT
        self.state = PlayerState()
        self.state.vehicle_direction = VehicleDirection.DOWN
        self.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width=int(SPRITE_SIZE * 4.5),
            sprite_height=SPRITE_SIZE * 6,
            columns=4,
            count=16,
        )
        self.texture = self.textures[self.state.vehicle_texture_index]
        # HACK: This jumps the camera to this start position
        self.center_x = center_x
        self.center_y = center_y
        self.docked = False

    @beartype
    def on_update(self, delta_time: float = 0.0) -> None:
        self.state.on_update(delta_time)
        if not self.change_x and not self.change_y:
            return

        slope = self.change_y / (self.change_x + 0.0001)
        if abs(slope) < 0.8:
            self.state.vehicle_direction = (
                VehicleDirection.RIGHT if self.change_x > 0 else VehicleDirection.LEFT
            )
        else:
            self.state.vehicle_direction = (
                VehicleDirection.UP if self.change_y > 0 else VehicleDirection.DOWN
            )
        self.texture = self.textures[self.state.vehicle_texture_index]

    @beartype
    def sync_with_player(self, player_sprite) -> None:
        self.change_x = player_sprite.change_x
        self.change_y = player_sprite.change_y
        self.center_x = player_sprite.center_x
        self.center_y = player_sprite.center_y
