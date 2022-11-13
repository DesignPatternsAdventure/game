"""Sprite Classes from community_rpg."""

import arcade
from loguru import logger

from ..constants import SPRITE_SIZE
from ..models.sprite_state import Direction, PlayerState


class CharacterSprite(arcade.Sprite):
    def __init__(self, sheet_name):
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

    def on_update(self):
        if not self.change_x and not self.change_y:
            return

        if self.state.should_update <= 3:
            self.state.should_update += 1
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
    def __init__(self, sheet_name):
        super().__init__(sheet_name)
        self.sound_update = 0
        self.footstep_sound = arcade.load_sound(":sounds:footstep00.wav")
        self.item = None
        self.item_anim_frame = 0
        self.item_anim_reversed = False
        self.inventory = []

    def equip(self, slot):
        if len(self.inventory) < slot:
            logger.info(f"No item in inventory slot {slot}")
            return

        index = slot - 1
        item_name = self.inventory[index].properties["item"]
        if "equippable" not in self.inventory[index].properties:
            logger.info(f"{item_name} is not equippable!")
            return
        if self.item and self.item.properties["item"] == item_name:
            self.item = None
        else:
            self.item = self.inventory[index]
            self.update_item_position()
            self.item.draw()

    def on_update(self):
        super().on_update()

        if not self.change_x and not self.change_y:
            self.sound_update = 0
            return

        if self.state.should_update > 3:
            self.sound_update += 1

        if self.sound_update >= 3:
            arcade.play_sound(self.footstep_sound)
            self.sound_update = 0

        if self.item:
            self.update_item_position()

    def update_item_position(self):
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

    def add_item_to_inventory(self, new_item):
        item_name = new_item.properties["item"]
        item_in_list = None
        item_index = None
        for index, item in enumerate(self.inventory):
            if item.properties["item"] == item_name:
                item_in_list = item
                item_index = index
        # If item exists in inventory, stack items in existing slot
        if item_in_list:
            item_in_list.properties["count"] += 1
        # Else add to new slot
        else:
            new_item.properties["count"] = 1
            self.inventory.append(new_item)
            item_index = len(self.inventory)
        inventory_key = str(item_index)
        return inventory_key

    def animate_item(self, view, config):
        if self.item_anim_frame < config["frames"]:
            self.item_anim_frame += 1
            angle = config["speed"]
            shift_x = config["shift_x"]
            shift_y = config["shift_y"]
            if (
                self.state.direction == Direction.RIGHT
                or self.state.direction == Direction.DOWN
            ):
                angle = -angle

            # Normal animation
            if not config["reversable"]:
                self.item.angle += angle
                self.item.center_x -= shift_x
                self.item.center_y -= shift_y
                return True

            # Reversable animation (back-and-forth)
            if self.item_anim_frame % config["reverse_frame"] == 0:
                self.item_anim_reversed = not self.item_anim_reversed
            if self.item_anim_reversed:
                self.item.angle -= angle
                self.item.center_x += shift_x
                self.item.center_y += shift_y
            else:
                self.item.angle += angle
                self.item.center_x -= shift_x
                self.item.center_y -= shift_y
            return True

        # Finished animation
        self.item_anim_frame = 0
        return False
