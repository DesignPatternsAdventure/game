"""Class for animated sprite."""

import itertools

import arcade
from beartype import beartype


class AnimatedSprite(arcade.Sprite):
    @beartype
    def __init__(  # type: ignore[no-untyped-def]
        self, game_clock, name, center_x, center_y, paired_sprite=None, scale=1
    ) -> None:
        super().__init__()

        # Configure when to update texture
        self.game_clock = game_clock
        self._update_time_increment = 0.2
        self._cur_texture_index = 1
        self._time_to_update_texture = self.game_clock.get_time_in_future(
            self._update_time_increment
        )

        # Configure sprite
        self._paired_sprite = paired_sprite
        self._name = name
        self.center_x = center_x
        self.center_y = center_y
        self.scale = scale
        self.texture = arcade.load_texture(self.get_filename())

        # Only 3-frame animations are supported for now. Restarts on 1
        self.index_counter = itertools.cycle([1, 2, 3, 2])

    @beartype
    def get_filename(self) -> str:
        return f":animation:{self._name}/{self._cur_texture_index}.png"

    @beartype
    def on_update(self, delta_time) -> None:  # type: ignore[no-untyped-def, override]
        if self._paired_sprite and "removed" in self._paired_sprite.properties:
            self.remove_from_sprite_lists()  # type: ignore[no-untyped-call]
        if self.game_clock.current_time > self._time_to_update_texture:
            self._cur_texture_index = next(self.index_counter)
            self.texture = arcade.load_texture(self.get_filename())
            self._time_to_update_texture = self.game_clock.get_time_in_future(
                self._update_time_increment
            )
