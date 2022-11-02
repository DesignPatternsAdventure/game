"""Main Game View."""

from collections import defaultdict
from importlib import reload

import arcade
import arcade.color
import arcade.key
from beartype import beartype
from loguru import logger

from . import character  # FYI: Import as module to allow reload
from .registration import Register, SpriteRegister


class MainGame(arcade.Window):
    """Arcade Window."""

    def __init__(self, **kwargs) -> None:
        """Configure window."""
        super().__init__(**kwargs)
        # FIXME: For collision detection, the character and visible items need to be separate
        self.visible_items = arcade.SpriteList()
        self.registered_items: dict[str, list[Register]] = defaultdict(list)
        self.sprite_register = SpriteRegister()
        self.sprite_register.set_listener(self.on_register)
        self.reload_character_module()
        self.setup_arcade()

    @beartype
    def setup_arcade(self) -> None:
        arcade.set_background_color(arcade.color.BLUE)

    @beartype
    def on_register(self, register: Register) -> None:
        self.registered_items[register.source.stem].append(register)
        self.visible_items.append(register.sprite)

    @beartype
    def get_all_registers(self) -> list[Register]:
        return sum(self.registered_items.values(), [])

    @beartype
    def on_draw(self) -> None:
        """Arcade Draw Event."""
        self.clear()
        self.visible_items.draw()

    @beartype
    def on_mouse_motion(self, x_pos: int, y_pos: int, d_x: float, d_y: float) -> None:
        """React to mouse position."""
        # logger.debug('x_pos:{x_pos} ({d_x}), y_pos:{y_pos} ({d_y})', x_pos=x_pos, y_pos=y_pos, d_x=d_x, d_y=d_y)
        for register in self.get_all_registers():
            if register.on_mouse_motion:
                register.on_mouse_motion(register.sprite, x_pos, y_pos, d_x, d_y)

    @beartype
    def on_key_press(self, key: int, modifiers: int) -> None:
        """React to key press."""
        # logger.debug('pressed:{key} {modifiers}', key=key, modifiers=modifiers)
        for register in self.get_all_registers():
            if register.on_key_press:
                register.on_key_press(register.sprite, key, modifiers)

    @beartype
    def on_key_release(self, key: int, modifiers: int) -> None:
        """React to key release.

        Docs: https://api.arcade.academy/en/stable/arcade.key.html#key

        """
        # logger.debug('released:{key} {modifiers}', key=key, modifiers=modifiers)
        if key == arcade.key.R and modifiers == arcade.key.MOD_COMMAND:
            logger.warning('Reloading modules')
            self.reload_character_module()
        for register in self.get_all_registers():
            if register.on_key_release:
                register.on_key_release(register.sprite, key, modifiers)

    @beartype
    def reload_module(self, module_name: str, module) -> None:
        """Generically reload a given module."""
        try:
            reload(module)
        except Exception:  # pylint: disable=broad-except
            logger.exception(f'Failed to reload {module_name}')

        for source, registers in self.registered_items.items():
            if source.startswith(module_name):
                for register in registers:
                    register.sprite.remove_from_sprite_lists()
        character.load_sprites(self.sprite_register)

    @beartype
    def reload_character_module(self) -> None:
        """Reload the 'character module'."""
        self.reload_module('character', character)

    @beartype
    def on_update(self, delta_time: float) -> None:
        """Incremental redraw."""
        # logger.debug('delta_time:{delta_time}', delta_time=delta_time)
        for register in self.get_all_registers():
            if register.on_update:
                register.on_update(register.sprite, delta_time)


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
