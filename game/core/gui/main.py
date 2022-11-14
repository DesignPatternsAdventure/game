"""Game GUI."""

import arcade

from game.core.gui.inventory import Inventory
from game.core.gui.message_box import MessageBox


class GameGUI:
    """Model the Game's GUI."""

    show_message_box = False
    close_message_box_time = None
    default_seconds_to_show_message_box = 3

    def __init__(self, view) -> None:
        self.view = view
        self.inventory = Inventory(self.view)
        self.message_box = MessageBox(self.view)

    def draw(self) -> None:
        self.inventory.draw()
        if self.show_message_box:
            current_time = self.view.game_clock.current_time
            if current_time < self.close_message_box_time:
                self.message_box.draw()
            else:
                self.show_message_box = False

    def draw_message_box(
        self, message, notes="", seconds=default_seconds_to_show_message_box
    ):
        self.close_message_box_time = self.view.game_clock.get_time_in_future(seconds)
        self.message_box.message = message
        self.message_box.notes = notes
        self.message_box.seconds = seconds
        self.show_message_box = True

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
