"""Game GUI."""

from ..constants import NUMRIC_KEY_MAPPING
from .inventory import Inventory
from .message_box import MessageBox


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
        if idx := NUMRIC_KEY_MAPPING.get(key):
            self.inventory.number_pressed = idx

    def on_key_release(self, key, modifiers) -> None:
        """Called when the user releases a key."""
        self.inventory.number_pressed = None
