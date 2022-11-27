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
    def on_update(self, delta_time: float = 0.0) -> None:
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

    _sound_update: float = 0
    _item_anim_frame = 0
    _item_anim_reversed = False

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
            self.player_inventory.store_equipped_item()
            return False
        self.item = item_name  # type: ignore[assignment]
        return True

    @beartype
    def on_update(self, delta_time: float = 0.0) -> None:
        super().on_update(delta_time)
        if not self.change_x and not self.change_y:
            self._sound_update = 0
            return
        if self.state.should_update > 1:
            self._sound_update += 0.5
        if self._sound_update >= 1 and self._footstep_sound:
            arcade.play_sound(self._footstep_sound)
            self._sound_update = 0

        self.update_item_position()

    @beartype
    def update_item_position(self) -> None:
        if not self.item:
            return

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
        return self.player_inventory.store_item(sprite)

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
