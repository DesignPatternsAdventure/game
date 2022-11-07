"""Game GUI."""

import arcade
from game.core.constants import SPRITE_SIZE


class GameGUI():
    """Model the Game's GUI."""
    capacity = 10
    vertical_hotbar_location = 40
    hotbar_height = 80
    sprite_height = 16
    first_number_pad_sprite_index = 51
    last_number_pad_sprite_index = 61
    selected_item = None

    def __init__(self, view):
        self.window = view.window
        self.player_sprite = view.player_sprite
        self.selected_item = view.selected_item
        self.hotbar_sprite_list = arcade.load_spritesheet(
            file_name=":assets:maps/input_prompts_kenney.png",
            sprite_width=16,
            sprite_height=16,
            columns=34,
            count=816,
            margin=1,
        )[self.first_number_pad_sprite_index:self.last_number_pad_sprite_index]

    def draw_inventory(self):
        field_width = self.window.width / (self.capacity + 1)

        x = self.window.width / 2
        y = self.vertical_hotbar_location

        arcade.draw_rectangle_filled(
            x, y, self.window.width, self.hotbar_height, arcade.color.ALMOND
        )

        # Draw each slot
        for i in range(self.capacity):
            y = self.vertical_hotbar_location
            x = i * field_width + 5
            if self.selected_item and i == self.selected_item - 1:
                arcade.draw_lrtb_rectangle_outline(
                    x - 6, x + field_width - 15, y + 35, y - 25, arcade.color.BLACK, 2
                )

            if len(self.player_sprite.inventory) > i:
                item = self.player_sprite.inventory[i]
            else:
                item = None

            hotkey_sprite = self.hotbar_sprite_list[i]
            hotkey_sprite.draw_scaled(x + self.sprite_height / 2 + 20, y + self.sprite_height / 2, 2.0)

            # Draw item in slot
            if item:
                text = item.properties["item"]
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

    def draw_message_box(self):
        # TODO
        pass
