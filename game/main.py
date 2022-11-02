"""Main Game View."""

import arcade
import arcade.color
import arcade.key
import arrow
from importlib import reload
from beartype import beartype
from loguru import logger

from . import character  # FYI: Import as module to allow reload


class MainGame(arcade.Window):
    """Arcade Window."""

    def __init__(self, **kwargs):
        """Configure window."""
        super().__init__(**kwargs)

        # FIXME: Decouple from main class
        self.character_state = character.State()
        self.player_sprite_list = arcade.SpriteList()
        state = character.State(sprite_resource=":resources:images/animated_characters/female_person/femalePerson_idle.png")
        logger.debug(state)
        self.player_sprite = arcade.Sprite(state.sprite_resource, 0.25)
        self.player_sprite.center_x = state.x_pos
        self.player_sprite.center_y = state.y_pos
        self.player_sprite_list.append(self.player_sprite)

        arcade.set_background_color(arcade.color.BLUE)

    def on_draw(self):
        """Arcade Draw Event."""
        self.clear()

        # FIXME: Decouple from main class
        self.player_sprite_list.draw()

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        """React to mouse position."""
        logger.debug("x:{x} ({dx}), y:{y} ({dy})", x=x, y=y, dx=dx, dy=dy)

    def on_key_press(self, key, modifiers):
        """React to key press."""
        logger.debug("pressed:{key} {modifiers}", key=key, modifiers=modifiers)

    def on_key_release(self, key, modifiers):
        """React to key release."""
        logger.debug("released:{key} {modifiers}", key=key, modifiers=modifiers)
        if key == arcade.key.UP:
            logger.warning("UP!")
            # FIXME: Decouple from main class
            reload(character)
            for sprite in self.player_sprite_list:
                sprite.remove_from_sprite_lists()
            state = character.State()
            logger.debug(state)
            self.player_sprite = arcade.Sprite(state.sprite_resource, 0.5)
            self.player_sprite.center_x = state.x_pos
            self.player_sprite.center_y = state.y_pos
            self.player_sprite_list.append(self.player_sprite)


    def on_update(self, delta_time) -> None:
        """Incremental redraw."""
        # logger.debug("delta_time:{delta_time}", delta_time=delta_time)
        ...


@beartype
def main() -> None:
    window = MainGame(
        width=500,
        height=500,
        title='Initial Game Experiment',
    )
    arcade.run()


if __name__ == "__main__":
    main()
