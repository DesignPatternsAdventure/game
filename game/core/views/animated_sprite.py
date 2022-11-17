"""Shiny stars sprite."""

import arcade
from beartype import beartype


class AnimatedSprite(arcade.Sprite):
    @beartype
    def __init__(
        self, game_clock, name, center_x, center_y, paired_sprite=None, scale=1
    ) -> None:
        super().__init__()

        # Configure when to update frame
        self.game_clock = game_clock
        self.update_time = 0.2
        self.time_to_update_frame = self.game_clock.get_time_in_future(self.update_time)

        # Configure sprite
        self.paired_sprite = paired_sprite
        self.name = name
        self.center_x = center_x
        self.center_y = center_y
        self.scale = scale
        self.cur_texture_index = 1
        self.increase = True
        self.texture = arcade.load_texture(self.get_filename())

    @beartype
    def get_filename(self) -> str:
        return f":misc:{self.name}-{self.cur_texture_index}.png"

    @beartype
    def on_update(self, delta_time) -> None:
        if self.paired_sprite and self.paired_sprite.visible == False:
            self.visible = False
        if self.game_clock.current_time > self.time_to_update_frame:
            if self.cur_texture_index == 3:
                self.increase = False
            if self.cur_texture_index == 1:
                self.increase = True
            if self.increase:
                self.cur_texture_index += 1
            else:
                self.cur_texture_index -= 1
            self.texture = arcade.load_texture(self.get_filename())
            self.time_to_update_frame = self.game_clock.get_time_in_future(
                self.update_time
            )
