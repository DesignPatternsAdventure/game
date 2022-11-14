"""Inventory"""

import arcade

from ..constants import SPRITE_SIZE


class Inventory:
    """Model the GUI inventory."""

    capacity = 10
    vertical_hotbar_location = 40
    hotbar_height = 80
    sprite_height = 16
    first_number_pad_sprite_index = 51
    last_number_pad_sprite_index = 61
    number_pressed = None

    def __init__(self, view):
        self.view = view
        self.hotbar_sprite_list = arcade.load_spritesheet(
            file_name=":assets:maps/input_prompts_kenney.png",
            sprite_width=16,
            sprite_height=16,
            columns=34,
            count=816,
            margin=1,
        )[self.first_number_pad_sprite_index : self.last_number_pad_sprite_index]

    def draw(self):
        self.draw_inventory()
        if self.show_message_box:
            current_time = self.view.game_clock.current_time
            if current_time < self.close_message_box_time:
                self._draw_message_box()
            else:
                self.show_message_box = False

    def draw(self):
        field_width = self.view.window.width / (self.capacity + 1)

        x = self.view.window.width / 2
        y = self.vertical_hotbar_location

        arcade.draw_rectangle_filled(
            x, y, self.view.window.width, self.hotbar_height, arcade.color.ALMOND
        )

        # Draw each slot
        for i in range(self.capacity):
            y = self.vertical_hotbar_location
            x = i * field_width + 5
            if self.number_pressed and i == self.number_pressed - 1:
                arcade.draw_lrtb_rectangle_outline(
                    x, x + field_width, y + 35, y - 25, arcade.color.BLACK, 2
                )

            if len(self.view.state.inventory) > i:
                item = self.view.state.inventory[i]
            else:
                item = None

            hotkey_sprite = self.hotbar_sprite_list[i]
            hotkey_sprite.draw_scaled(
                x + self.sprite_height / 2 + 20, y + self.sprite_height / 2, 2.0
            )

            # Draw item in slot
            if item:
                text = item.properties["name"]
                count = item.properties["count"]
                if count > 1:
                    text = f"{text} ({count})"
                arcade.draw_text(text, x + 40, y - 20, arcade.color.ALLOY_ORANGE, 12)
                arcade.draw_lrwh_rectangle_textured(
                    x + SPRITE_SIZE + 20,
                    y,
                    SPRITE_SIZE,
                    SPRITE_SIZE,
                    item.texture,
                )
