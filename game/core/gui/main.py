"""Game GUI."""

from beartype import beartype

from ..constants import NUMERIC_KEY_MAPPING
from ..game_clock import GameClock
from ..game_state import GameState
from .inventory import InventoryGUI
from .message_box import MessageBox


class GameGUI:
    """Model the Game's GUI."""

    show_message_box = False
    close_message_box_time = None
    default_seconds_to_show_message_box = 3

    def __init__(
        self,
        game_state: GameState,
        game_clock: GameClock,
        window_shape: tuple[int, int],
    ) -> None:
        self.game_clock = game_clock
        self.inventory = InventoryGUI(game_state, window_shape)
        self.message_box = MessageBox(window_shape)

    @beartype
    def draw(self) -> None:
        self.inventory.draw()
        if self.show_message_box:
            current_time = self.game_clock.current_time
            if current_time < self.close_message_box_time:
                self.message_box.draw()
            else:
                self.show_message_box = False

    def draw_message_box(
        self, message, notes="", seconds=default_seconds_to_show_message_box
    ):
        self.close_message_box_time = self.game_clock.get_time_in_future(seconds)
        self.message_box.message = message
        self.message_box.notes = notes
        self.message_box.seconds = seconds
        self.show_message_box = True

    @beartype
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called whenever a key is pressed."""
        if idx := NUMERIC_KEY_MAPPING.get(key):
            self.inventory.number_pressed = idx

    @beartype
    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key."""
        self.inventory.number_pressed = None
