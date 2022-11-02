"""Main Game View."""

from importlib import reload
from typing import Any

import arcade
import arcade.color
import arcade.key
from beartype import beartype
from loguru import logger

from . import character  # FYI: Import as module to allow reload
from .registration import sprite_register


class MainGame(arcade.Window):
    """Arcade Window."""

    def __init__(self, **kwargs) -> None:
        """Configure window."""
        super().__init__(**kwargs)
        sprite_register.set_listener(self.on_register)

        self.visible_items = arcade.SpriteList()
        self.registered_items = {}

        # FIXME: Decouple from main class
        self.character_state = character.State()
        state = character.State(
            sprite_resource=":resources:images/animated_characters/female_person/femalePerson_idle.png",
            scale=0.25,
        )
        logger.debug(state)
        self.player_sprite = character.CharacterSprite(state)
        self.visible_items.append(self.player_sprite)

        arcade.set_background_color(arcade.color.BLUE)

    @beartype
    def on_register(self, sprite: Any) -> None:
        pass

    @beartype
    def on_draw(self) -> None:
        """Arcade Draw Event."""
        self.clear()
        self.visible_items.draw()

    @beartype
    def on_mouse_motion(self, x: int, y: int, dx: float, dy: float) -> None:
        """React to mouse position."""
        logger.debug("x:{x} ({dx}), y:{y} ({dy})", x=x, y=y, dx=dx, dy=dy)

    @beartype
    def on_key_press(self, key: int, modifiers: int) -> None:
        """React to key press."""
        logger.debug("pressed:{key} {modifiers}", key=key, modifiers=modifiers)

    @beartype
    def on_key_release(self, key: int, modifiers: int) -> None:
        """React to key release."""
        logger.debug("released:{key} {modifiers}", key=key, modifiers=modifiers)
        if key == arcade.key.UP:
            logger.warning("UP!")
            # FIXME: Decouple from main class
            reload(character)
            for sprite in self.visible_items:
                sprite.remove_from_sprite_lists()
            state = character.State(scale=0.5)
            logger.debug(state)
            self.player_sprite = character.CharacterSprite(state)
            self.visible_items.append(self.player_sprite)

    @beartype
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
