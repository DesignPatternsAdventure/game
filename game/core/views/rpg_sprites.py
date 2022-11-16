"""Sprite Classes from community_rpg."""

import arcade
from arcade import Sprite
from beartype import beartype
from loguru import logger

from ..constants import SPRITE_SIZE
from ..models.sprite_state import Direction, PlayerState


class CharacterSprite(arcade.Sprite):
    @beartype
    def __init__(self, sheet_name: str) -> None:
        super().__init__()
        self.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width=SPRITE_SIZE,
            sprite_height=SPRITE_SIZE,
            columns=3,
            count=12,
        )
        self.state = PlayerState()
        self.texture = self.textures[self.state.cur_texture_index]

    @beartype
    def on_update(self) -> None:
        if not self.change_x and not self.change_y:
            return

        if self.state.should_update <= 1:
            self.state.should_update += 0.4
        else:
            self.state.should_update = 0
            self.state.cur_texture_index += 1

        slope = self.change_y / (self.change_x + 0.0001)
        if abs(slope) < 0.8:
            self.state.direction = (
                Direction.RIGHT if self.change_x > 0 else Direction.LEFT
            )
        else:
            self.state.direction = Direction.UP if self.change_y > 0 else Direction.DOWN

        if self.state.cur_texture_index not in self.state.direction.value:
            self.state.cur_texture_index = self.state.direction.value[0]

        self.texture = self.textures[self.state.cur_texture_index]

        self.center_x += self.change_x
        self.center_y += self.change_y


class PlayerSprite(CharacterSprite):

    item: Sprite | None = None

    _sound_update: float = 0

    @beartype
    def __init__(self, sheet_name: str, player_inventory) -> None:
        super().__init__(sheet_name)
        self.player_inventory = player_inventory
        self._footstep_sound = arcade.load_sound(":sounds:footstep00.wav")

    @beartype
    def equip(self, item_name: str) -> bool:
        was_equipped = self.player_inventory.equip_item(item_name)
        self.item = self.player_inventory.equipped_item
        # if self.item:  # FIXME: Implement the draw logic!
        #     self.update_item_position()
        #     self.item.draw()
        return was_equipped  # noqa: R504

    @beartype
    def on_update(self) -> None:
        super().on_update()
        if not self.change_x and not self.change_y:
            self._sound_update = 0
            return
        if self.state.should_update > 1:
            self._sound_update += 0.5
        if self._sound_update >= 1:
            arcade.play_sound(self._footstep_sound)
            self._sound_update = 0

        self.player_inventory.on_update()
        # if self.item:  # FIXME: Implement the draw logic!
        #     self.update_item_position()

    @beartype
    def update_item_position(self) -> None:
        self.item.center_y = self.center_y - 5

        if self.state.direction == Direction.LEFT:
            self.item.center_x = self.center_x - 10
            self.item.scale = -1
            self.item.angle = -90

        if self.state.direction == Direction.RIGHT:
            self.item.center_x = self.center_x + 10
            self.item.scale = 1
            self.item.angle = 0

        if self.state.direction == Direction.UP:
            self.item.center_x = self.center_x - 15
            self.item.scale = -1
            self.item.angle = -90

        if self.state.direction == Direction.DOWN:
            self.item.center_x = self.center_x + 15
            self.item.scale = 1
            self.item.angle = 0

    @beartype
    def add_item_to_inventory(self, sprite: Sprite) -> int | None:
        try:
            return self.player_inventory.store_item(sprite)
        except RuntimeError as exc:
            logger.error(exc)  # TODO: Show this in the GUI!
        return None

    @beartype
    def animate_item(self, config):
        raise NotImplementedError("UGH!")
