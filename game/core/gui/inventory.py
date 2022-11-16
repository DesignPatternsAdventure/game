"""Inventory GUI."""

import arcade.color
from beartype import beartype

from ..constants import SPRITE_SIZE
from ..game_state import GameState


class InventoryGUI:
    """Model the GUI inventory."""

    capacity: int = 10

    _sprite_height: int = 16

    @beartype
    def __init__(self, state: GameState, window_shape: tuple[int, int]) -> None:
        self.state = state
        self.window_width = window_shape[0]
        numpad_key_id = 51  # Uses different indexing than 'arcade.key.KEY_1'
        self.hotbar_sprite_list = arcade.load_spritesheet(
            file_name=":assets:maps/input_prompts_kenney.png",
            sprite_width=self._sprite_height,
            sprite_height=self._sprite_height,
            columns=34,
            count=816,
            margin=1,
        )[numpad_key_id : numpad_key_id + self.capacity]

    @beartype
    def draw(self, activated_item_index: int | None) -> None:
        """Draw the Inventory Hotbar."""
        hotbar_height = 80
        y_mid = hotbar_height / 2

        field_width = self.window_width / (self.capacity + 1)

        arcade.draw_rectangle_filled(
            self.window_width / 2,
            y_mid,
            self.window_width,
            hotbar_height,
            arcade.color.ALMOND,
        )

        # Draw each slot
        for idx in range(self.capacity):
            x_center = idx * field_width + 5
            if activated_item_index and idx == activated_item_index - 1:
                arcade.draw_lrtb_rectangle_outline(
                    x_center,
                    x_center + field_width,
                    y_mid + 35,
                    y_mid - 25,
                    arcade.color.BLACK,
                    2,
                )

            item = (
                self.state.inventory[idx] if len(self.state.inventory) > idx else None
            )

            hotkey_sprite = self.hotbar_sprite_list[idx]
            hotkey_sprite.draw_scaled(
                x_center + self._sprite_height / 2 + 20,
                y_mid + self._sprite_height / 2,
                2.0,
            )

            # Draw item in slot
            if item:
                text = item.properties["name"]
                count = item.properties["count"]
                if count > 1:
                    text = f"{text} ({count})"
                arcade.draw_text(
                    text,
                    x_center + 40,
                    y_mid - 20,
                    arcade.color.ALLOY_ORANGE,
                    12,
                )
                arcade.draw_lrwh_rectangle_textured(
                    x_center + SPRITE_SIZE + 20,
                    y_mid,
                    SPRITE_SIZE,
                    SPRITE_SIZE,
                    item.texture,
                )
