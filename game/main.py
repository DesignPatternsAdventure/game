"""Main Game View."""

from collections import defaultdict
from importlib import reload
from pathlib import Path

import arcade
import arcade.color
import arcade.key
from beartype import beartype
from loguru import logger

from . import character  # FYI: Import as module to allow reload
from .registration import SpriteRegister


class MainGame(arcade.Window):
    """Arcade Window."""

    def __init__(self, **kwargs) -> None:
        """Configure window."""
        super().__init__(**kwargs)
        # FIXME: For collision detection, the character and visible items need to be separate
        self.visible_items = arcade.SpriteList()
        self.registered_items: dict[str, list[arcade.Sprite]] = defaultdict(list)
        self.sprite_register = SpriteRegister()
        self.sprite_register.set_listener(self.on_register)
        self.reload_character_module()
        self.setup_arcade()

    @beartype
    def setup_arcade(self) -> None:
        arcade.set_background_color(arcade.color.BLUE)

    @beartype
    def on_register(self, sprite: arcade.Sprite, source: Path) -> None:
        self.registered_items[source.stem].append(sprite)
        self.visible_items.append(sprite)

    @beartype
    def on_draw(self) -> None:
        """Arcade Draw Event."""
        self.clear()
        self.visible_items.draw()

    @beartype
    def on_mouse_motion(self, x: int, y: int, dx: float, dy: float) -> None:  # pylint: disable=C0103
        """React to mouse position."""
        # logger.debug('x:{x} ({dx}), y:{y} ({dy})', x=x, y=y, dx=dx, dy=dy)

    @beartype
    def on_key_press(self, key: int, modifiers: int) -> None:
        """React to key press."""
        # logger.debug('pressed:{key} {modifiers}', key=key, modifiers=modifiers)

    @beartype
    def on_key_release(self, key: int, modifiers: int) -> None:
        """React to key release."""
        # logger.debug('released:{key} {modifiers}', key=key, modifiers=modifiers)
        if key == arcade.key.R and modifiers == arcade.key.MOD_COMMAND:
            logger.warning('Reloading modules')
            self.reload_character_module()

    @beartype
    def reload_module(self, module_name: str, module) -> None:
        """Generically reload a given module."""
        try:
            reload(module)
        except Exception:  # pylint: disable=broad-except
            logger.exception(f'Failed to reload {module_name}')

        for source, sprites in self.registered_items.items():
            if source.startswith(module_name):
                for sprite in sprites:
                    sprite.remove_from_sprite_lists()
        character.load_sprites(self.sprite_register)

    @beartype
    def reload_character_module(self) -> None:
        """Reload the 'character module'."""
        self.reload_module('character', character)

    @beartype
    def on_update(self, delta_time: float) -> None:
        """Incremental redraw."""
        # logger.debug('delta_time:{delta_time}', delta_time=delta_time)


@beartype
def main() -> None:
    MainGame(
        width=500,
        height=500,
        title='Experimenting with Module Reload and Dependency Inversion',
    )
    arcade.run()


if __name__ == '__main__':
    main()
