"""Sprite Classes from community_rpg."""

import arcade
from arcade import Sprite
from beartype import beartype

from ..constants import SPRITE_SIZE
from ..models.base_player_inventory import PlayerInventoryInterface
from ..models.sprite_state import Direction, PlayerState


class CharacterSprite(arcade.Sprite):
    @beartype
    def __init__(self, sheet_name: str) -> None:
        super().__init__()
        self.state = PlayerState()
        self._textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width=SPRITE_SIZE,
            sprite_height=SPRITE_SIZE,
            columns=3,
            count=12,
        )
        self.texture = self._textures[self.state.cur_texture_index]
        self.sheet_name = sheet_name

    @beartype
    def on_update(self, delta_time: float = 0.0) -> None:
        self.state.on_update(delta_time)
        if not self.change_x and not self.change_y:
            return

        slope = self.change_y / (self.change_x + 0.0001)
        if abs(slope) < 0.8:
            self.state.direction = (
                Direction.RIGHT if self.change_x > 0 else Direction.LEFT
            )
        else:
            self.state.direction = Direction.UP if self.change_y > 0 else Direction.DOWN
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.texture = self._textures[self.state.cur_texture_index]


class PlayerSprite(CharacterSprite):

    _item_anim_frame = 0
    _item_anim_reversed = False

    _sound_update: float = 0.0

    player_inventory: PlayerInventoryInterface

    @property
    @beartype
    def item(self) -> Sprite | None:
        item = self.player_inventory.equipped_item
        return item.sprite if item else None

    @item.setter
    @beartype
    def item(self, item_name: str) -> None:
        item = self.player_inventory.equip_item(item_name)
        self.update_item_position()
        item.draw()  # type: ignore[no-untyped-call]

    @property
    @beartype
    def inventory(self) -> list[Sprite]:
        return self.player_inventory.get_ordered_sprites()

    @beartype
    def __init__(
        self, sheet_name: str, player_inventory: PlayerInventoryInterface
    ) -> None:
        super().__init__(sheet_name)
        self.player_inventory = player_inventory
        self._footstep_sound = arcade.load_sound(":sounds:footstep00.wav")

    @beartype
    def equip(self, item_name: str) -> bool:
        """Attempt to equip the item by name."""
        if self.item and self.item.properties["name"] == item_name:
            self.player_inventory.unequip_item()
            return False
        self.item = item_name
        return True

    @beartype
    def add_item_to_inventory(self, sprite: Sprite) -> int | None:
        return self.player_inventory.store_item(sprite)

    @beartype
    def on_update(self, delta_time: float = 0.0) -> None:
        super().on_update(delta_time)
        if not self.change_x and not self.change_y:
            self._sound_update = 0
            return

        if self.state.time_since_last_update > 1:
            self._sound_update += 0.5
        if self._sound_update >= 1:
            arcade.play_sound(self._footstep_sound, volume=0.3)
            self._sound_update = 0

        self.update_item_position()

    @beartype
    def animate_item(self, config):  # type: ignore[no-untyped-def]
        if self._item_anim_frame < config["frames"]:
            self._item_anim_frame += 1
            angle = config["speed"]
            shift_x = config["shift_x"]
            shift_y = config["shift_y"]
            if self.state.direction in (Direction.RIGHT, Direction.DOWN):
                angle = -angle

            # Normal animation
            if not config["reversible"]:
                self.item.angle += angle
                self.item.center_x -= shift_x
                self.item.center_y -= shift_y
                return True

            # Reversible animation (back-and-forth)
            if self._item_anim_frame % config["reverse_frame"] == 0:
                self._item_anim_reversed = not self._item_anim_reversed
            if self._item_anim_reversed:
                self.item.angle -= angle
                self.item.center_x += shift_x
                self.item.center_y += shift_y
            else:
                self.item.angle += angle
                self.item.center_x -= shift_x
                self.item.center_y -= shift_y
            return True

        # Finished animation
        self._item_anim_frame = 0
        return False

    @beartype
    def update_item_position(self) -> None:
        raise NotImplementedError("update_item_position must be implemented")

    @beartype
    def update_player_position(self, center_x, center_y) -> None:
        self.center_x = center_x
        self.center_y = center_y
