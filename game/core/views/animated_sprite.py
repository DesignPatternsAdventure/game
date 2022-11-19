"""Class for animated sprite."""

import arcade
from beartype import beartype


class AnimatedSprite(arcade.Sprite):
    @beartype
    def __init__(
        self, game_clock, name, center_x, center_y, paired_sprite=None, scale=1
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

    @beartype
    def get_filename(self) -> str:
        return f":animation:{self.name}/{self.cur_texture_index}.png"

    @beartype
    def on_update(self, delta_time) -> None:
        if self.paired_sprite and "removed" in self.paired_sprite.properties:
            self.remove_from_sprite_lists()
        if self.game_clock.current_time > self.time_to_update_texture:
            if self.cur_texture_index == 3:
                self.increase_index = False
            if self.cur_texture_index == 1:
                self.increase_index = True
            if self.increase_index:
                self.cur_texture_index += 1
            else:
                self.cur_texture_index -= 1
            self.texture = arcade.load_texture(self.get_filename())
            self.time_to_update_texture = self.game_clock.get_time_in_future(
                self.update_time
            )
