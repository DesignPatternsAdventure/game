"""Message box."""

import arcade
import arcade.color
from beartype import beartype


class MessageBox:
    """Model the GUI message box."""

    message: str = ""
    notes: str = ""
    _message_box_width = 500
    _message_box_height = 60
    _message_font = 12
    _notes_font = 8

    @beartype
    def __init__(self, window_shape: tuple[int, int]) -> None:
        width, height = window_shape
        self.message_box_center_x = width / 2
        self.message_box_center_y = int(height * 0.9)

    @beartype
    def draw(self) -> None:
        message_center_y = (
            self.message_box_center_y
            if not self.notes
            else self.message_box_center_y + 10
        )
        arcade.draw_rectangle_filled(
            self.message_box_center_x,
            self.message_box_center_y,
            self._message_box_width,
            self._message_box_height,
            arcade.color.ALMOND,
        )
        arcade.draw_rectangle_outline(
            self.message_box_center_x,
            self.message_box_center_y,
            self._message_box_width,
            self._message_box_height,
            arcade.color.ALLOY_ORANGE,
            2,
        )
        self._draw_message_box_text(self.message, self._message_font, message_center_y)
        if self.notes:
            self._draw_message_box_text(
                self.notes, self._notes_font, self.message_box_center_y - 10
            )

    @beartype
    def _draw_message_box_text(self, text: str, font_size: int, center_y) -> None:  # type: ignore[no-untyped-def]
        arcade.draw_text(
            text,
            self.message_box_center_x,
            center_y,
            arcade.color.ALLOY_ORANGE,
            font_size,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self._message_box_width,
        )

    @beartype
    def process_message(
        self, message: str, notes: str | None
    ) -> tuple[str, str | None, int | None]:
        if "\n" not in message:
            return message, notes, None
        message_list = message.split("\n")
        notes = message_list.pop().strip()
        message = (" ").join(message_list).strip()
        return message, notes, 5
