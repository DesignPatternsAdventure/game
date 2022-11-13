"""Game GUI."""

import arcade

from .constants import SPRITE_SIZE


class GameGUI:
    """Model the Game's GUI."""

    # Inventory
    capacity = 10
    vertical_hotbar_location = 40
    hotbar_height = 80
    sprite_height = 16
    first_number_pad_sprite_index = 51
    last_number_pad_sprite_index = 61
    number_pressed = None

    # Message box
    show_message_box = False
    default_seconds_to_show = 2
    message_box_width = 500
    message_box_height = 60
    message_font = 12
    notes_font = 8

    def __init__(self, view):
        self.view = view
        self.message_box_center_x = self.view.window.width / 2
        self.message_box_center_y = (
            self.view.window.height - self.view.window.height / 10
        )
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

    def draw_inventory(self):
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

    def draw_message_box(self, message, notes=None, seconds=default_seconds_to_show):
        self.close_message_box_time = self.view.game_clock.get_time_in_future(seconds)
        self.message = message
        self.notes = notes
        self.seconds = seconds
        self.show_message_box = True

    def _draw_message_box(self):
        message_center_y = (
            self.message_box_center_y
            if not self.notes
            else self.message_box_center_y + 10
        )
        arcade.draw_rectangle_filled(
            self.message_box_center_x,
            self.message_box_center_y,
            self.message_box_width,
            self.message_box_height,
            arcade.color.ALMOND,
        )
        arcade.draw_rectangle_outline(
            self.message_box_center_x,
            self.message_box_center_y,
            self.message_box_width,
            self.message_box_height,
            arcade.color.ALLOY_ORANGE,
            2,
        )
        self._draw_message_box_text(self.message, self.message_font, message_center_y)
        if self.notes:
            self._draw_message_box_text(
                self.notes, self.notes_font, self.message_box_center_y - 10
            )

    def _draw_message_box_text(self, text, font_size, center_y):
        arcade.draw_text(
            text,
            self.message_box_center_x,
            center_y,
            arcade.color.ALLOY_ORANGE,
            font_size,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.message_box_width,
        )

    def on_key_press(self, key, modifiers) -> None:
        """Called whenever a key is pressed."""
        if key == arcade.key.KEY_1:
            self.number_pressed = 1
        elif key == arcade.key.KEY_2:
            self.number_pressed = 2
        elif key == arcade.key.KEY_3:
            self.number_pressed = 3
        elif key == arcade.key.KEY_4:
            self.number_pressed = 4
        elif key == arcade.key.KEY_5:
            self.number_pressed = 5
        elif key == arcade.key.KEY_6:
            self.number_pressed = 6
        elif key == arcade.key.KEY_7:
            self.number_pressed = 7
        elif key == arcade.key.KEY_8:
            self.number_pressed = 8
        elif key == arcade.key.KEY_9:
            self.number_pressed = 9
        elif key == arcade.key.KEY_0:
            self.number_pressed = 10

    def on_key_release(self, key, modifiers) -> None:
        """Called when the user releases a key."""
        self.number_pressed = None
