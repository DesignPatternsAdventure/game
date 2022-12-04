"""Class for animated sprite."""

import itertools

import arcade
from beartype import beartype


class AnimatedSprite(arcade.Sprite):
    @beartype
    def __init__(  # type: ignore[no-untyped-def]
        self,
        game_clock,
        name,
        center_x,
        center_y,
        paired_sprite=None,
        scale: int | float = 1,
    ) -> None:
        super().__init__()

        # Configure when to update texture
        self.game_clock = game_clock
        self.update_time = 0.2
        self.cur_texture_index = 1
        self.increase_index = True
        self.time_to_update_texture = self.game_clock.get_time_in_future(
            self.update_time
        )

        # Configure sprite
        self.paired_sprite = paired_sprite
        self.name = name
        self.center_x = center_x
        self.center_y = center_y
        self.scale = scale
        self.texture = arcade.load_texture(self.get_filename())

        # Only 3-frame animations are supported for now. Restarts on 1
        self.index_counter = itertools.cycle([1, 2, 3, 2])

    @beartype
    def get_filename(self) -> str:
        return f":animation:{self.name}/{self.cur_texture_index}.png"

    @beartype
    def on_update(self, delta_time) -> None:  # type: ignore[no-untyped-def, override]
        if self.paired_sprite and "removed" in self.paired_sprite.properties:
            self.remove_from_sprite_lists()  # type: ignore[no-untyped-call]
        if self.game_clock.current_time > self.time_to_update_texture:
            self.cur_texture_index = next(self.index_counter)
            self.texture = arcade.load_texture(self.get_filename())
            self.time_to_update_texture = self.game_clock.get_time_in_future(
                self.update_time
            )
