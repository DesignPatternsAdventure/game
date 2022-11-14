"""Message box"""

import arcade


class MessageBox:
    """Model the GUI message box."""

    message = ""
    notes = ""
    seconds = None
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

    def draw(self):
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
