"""Sprite Classes from community_rpg."""

from enum import Enum

import arcade

from ..constants import SPRITE_SIZE

Direction = Enum("Direction", "DOWN LEFT RIGHT UP")

SPRITE_INFO = {
    Direction.DOWN: [0, 1, 2],
    Direction.LEFT: [3, 4, 5],
    Direction.RIGHT: [6, 7, 8],
    Direction.UP: [9, 10, 11],
}


class CharacterSprite(arcade.Sprite):
    def __init__(self, sheet_name, inventory=None):
        super().__init__()
        inventory = inventory or []
        self.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width=SPRITE_SIZE,
            sprite_height=SPRITE_SIZE,
            columns=3,
            count=12,
        )
        self.should_update = 0
        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]
        self.inventory = inventory
        self.direction = Direction.LEFT

    def on_update(self, delta_time):
        if not self.change_x and not self.change_y:
            return

        if self.should_update <= 3:
            self.should_update += 1
        else:
            self.should_update = 0
            self.cur_texture_index += 1

        slope = self.change_y / (self.change_x + 0.0001)
        if abs(slope) < 0.8:
            self.direction = Direction.RIGHT if self.change_x > 0 else Direction.LEFT
        else:
            self.direction = Direction.UP if self.change_y > 0 else Direction.DOWN

        if self.cur_texture_index not in SPRITE_INFO[self.direction]:
            self.cur_texture_index = SPRITE_INFO[self.direction][0]

        self.texture = self.textures[self.cur_texture_index]


class PlayerSprite(CharacterSprite):
    def __init__(self, sheet_name, inventory=None):
        super().__init__(sheet_name, inventory)
        self.sound_update = 0
        self.footstep_sound = arcade.load_sound(":sounds:footstep00.wav")
        self.item = None
        self.item_anim_frame = 0
        self.item_anim_reversed = False
        self.item_target = None

    # def equip(self, slot):
    #     if len(self.inventory) < slot:
    #         logger.info(f"No item in inventory slot {slot}")
    #         return

    #     index = slot - 1
    #     if "equippable" not in self.inventory[index].properties:
    #         item_name = self.inventory[index].properties["item"]
    #         logger.info(f"{item_name} is not equippable!")
    #         return
    #     if self.item and self.item == self.inventory[index]:
    #         self.item = None
    #     else:
    #         self.item = self.inventory[index]
    #         self.update_item_position()

    def on_update(self, delta_time):
        super().on_update(delta_time)

        if not self.change_x and not self.change_y:
            self.sound_update = 0
            return

        if self.should_update > 3:
            self.sound_update += 1

        if self.sound_update >= 3:
            arcade.play_sound(self.footstep_sound)
            self.sound_update = 0

        # if self.item:
        #     self.update_item_position()

    # def update_item_position(self):
    #     self.item.center_y = self.center_y - 5

    #     if self.direction == Direction.LEFT:
    #         self.item.center_x = self.center_x - 10
    #         self.item.scale = -1
    #         self.item.angle = -90

    #     if self.direction == Direction.RIGHT:
    #         self.item.center_x = self.center_x + 10
    #         self.item.scale = 1
    #         self.item.angle = 0

    #     if self.direction == Direction.UP:
    #         self.item.center_x = self.center_x - 15
    #         self.item.scale = -1
    #         self.item.angle = -90

    #     if self.direction == Direction.DOWN:
    #         self.item.center_x = self.center_x + 15
    #         self.item.scale = 1
    #         self.item.angle = 0

    # def add_item_to_inventory(self, view, item):
    #     item_name = item.properties["item"]
    #     item_in_list = next(
    #         (item for item in self.inventory if item.properties["item"] == item_name),
    #         None,
    #     )
    #     if item_in_list:
    #         item_in_list.properties["count"] += 1
    #     else:
    #         item.properties["count"] = 1
    #         self.inventory.append(item)
    #     view.message_box = MessageBox(
    #         view,
    #         f"{item.properties['item']} added to inventory!",
    #         f"Press {str(len(self.inventory))} to use item. Press any key to close this message.",
    #     )

    # def animate_item(self, view, config):
    #     if self.item_anim_frame < config["frames"]:
    #         self.item_anim_frame += 1
    #         angle = config["speed"]
    #         shift_x = config["shift_x"]
    #         shift_y = config["shift_y"]
    #         if self.direction == Direction.RIGHT or self.direction == Direction.DOWN:
    #             angle = -angle

    #         # Normal animation
    #         if not config["reversable"]:
    #             self.item.angle += angle
    #             self.item.center_x -= shift_x
    #             self.item.center_y -= shift_y
    #             return True

    #         # Reversable animation (back-and-forth)
    #         if self.item_anim_frame % config["reverse_frame"] == 0:
    #             self.item_anim_reversed = not self.item_anim_reversed
    #         if self.item_anim_reversed:
    #             self.item.angle -= angle
    #             self.item.center_x += shift_x
    #             self.item.center_y += shift_y
    #         else:
    #             self.item.angle += angle
    #             self.item.center_x -= shift_x
    #             self.item.center_y -= shift_y
    #         return True

    #     # Finished animation
    #     self.item_anim_frame = 0
    #     if self.item_target:
    #         self.item_target.remove_from_sprite_lists()
    #         if "item" in self.item_target.properties:
    #             item_drop = self.item_target.properties["item"]
    #             file_path = f":misc:{item_drop}.png"
    #             sprite = arcade.Sprite(file_path, {"item": item_drop})
    #             if sprite:
    #                 self.add_item_to_inventory(view, sprite)
    #                 if "task" in self.item_target.properties:
    #                     view.message_box = MessageBox(
    #                         view,
    #                         f"Task 1 complete",
    #                         f"Great, you've made your first code change!",
    #                         True,  # When task 2 is implemented, this lock will be removed
    #                     )
    #             else:
    #                 view.message_box = MessageBox(
    #                     view,
    #                     f"Time for some coding!",
    #                     f"Close the game and navigate to this file: src/tasks/task1.py",
    #                     True,
    #                 )
    #         self.item_target = None
    #     return False
