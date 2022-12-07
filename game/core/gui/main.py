"""Game GUI."""

from beartype import beartype

from ..constants import NUMERIC_KEY_MAPPING
from ..game_clock import GameClock
from ..game_state import GameState
from ..pressed_keys import PressedKeys
from .inventory import InventoryGUI
from .message_box import MessageBox


class GameGUI:
    """Model the Game's GUI."""

    _show_message_box = False
    _default_seconds_to_show_message_box = 3

    @beartype
    def __init__(
        self,
        game_state: GameState,
        game_clock: GameClock,
        pressed_keys: PressedKeys,
        window_shape: tuple[int, int],
    ) -> None:
        self.inventory = InventoryGUI(game_state, window_shape)
        self.game_clock = game_clock
        self.pressed_keys = pressed_keys
        self.message_box = MessageBox(window_shape)
        self._close_message_box_time = self.game_clock.get_time_in_future(5)

    @beartype
    def draw(self) -> None:
        activated_item_index = None
        for key in self.pressed_keys.keys.intersection({*NUMERIC_KEY_MAPPING}):
            if idx := NUMERIC_KEY_MAPPING.get(key):
                activated_item_index = idx
                break
        self.inventory.draw(activated_item_index)
        if self._show_message_box:
            current_time = self.game_clock.current_time
            if current_time < self._close_message_box_time:
                self.message_box.draw()
            else:
                self._show_message_box = False

    @beartype
    def draw_message_box(
        self,
        message: str,
        notes: str = "",
        seconds: int = _default_seconds_to_show_message_box,
    ) -> None:
        self._show_message_box = True
        message, notes, seconds_override = self.message_box.process_message(
            message, notes
        )
        self.message_box.message = message
        self.message_box.notes = notes

        if seconds_override:
            self._close_message_box_time = self.game_clock.get_time_in_future(
                seconds_override
            )
        else:
            self._close_message_box_time = self.game_clock.get_time_in_future(seconds)

    @beartype
    def clear(self) -> None:
        self._show_message_box = False
