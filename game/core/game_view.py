"""Main Game Window."""

from collections import defaultdict
from importlib import reload
from types import ModuleType

import arcade
import arcade.csscolor
import arcade.key
from beartype import beartype
from loguru import logger

from .game_clock import GameClock
from .pressed_keys import PressedKeys
from .registration import Register, SpriteRegister


class GameView(arcade.View):

    @beartype
    def __init__(self, code_modules: list[ModuleType] | None = None, **kwargs) -> None:  # type: ignore[no-untyped-def]
        """Configure window.

        Docs: https://api.arcade.academy/en/latest/api/window.html#arcade-window

        """
        super().__init__(**kwargs)
        self.game_clock = GameClock()
        self.pressed_keys = PressedKeys()

        # FIXME: For collision detection, the character and visible items need to be separate
        self.visible_items = arcade.SpriteList()
        self.registered_items: dict[str, list[Register]] = defaultdict(list)
        self.sprite_register = SpriteRegister()
        self.sprite_register.set_listener(self.on_register)

        self.code_modules = code_modules or []
        self.reload_modules()

    @beartype
    def on_show_view(self) -> None:
        """Run on switch to the this View."""
        # FIXME: Implement the map and not just this placeholder fill color
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    @beartype
    def on_register(self, register: Register) -> None:
        self.registered_items[register.source].append(register)
        self.visible_items.append(register.sprite)

    @beartype
    def get_all_registers(self) -> list[Register]:
        return sum(self.registered_items.values(), [])

    @beartype
    def on_draw(self) -> None:
        """Arcade Draw Event."""
        self.clear()
        self.visible_items.draw()  # type: ignore[no-untyped-call]

    @beartype
    def on_mouse_motion(self, x_pos: int, y_pos: int, d_x: float, d_y: float) -> None:
        """React to mouse position."""
        for register in self.get_all_registers():
            if register.on_mouse_motion:
                register.on_mouse_motion(register.sprite, x_pos, y_pos, d_x, d_y)

    @beartype
    def on_key_press(self, key: int, modifiers: int) -> None:
        """React to key press."""
        self.pressed_keys.pressed(key, modifiers)
        # Convenience handlers for Reload and Quit
        meta_keys = {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}
        if key == arcade.key.R and modifiers in meta_keys:
            logger.warning('Reloading modules')
            self.reload_modules()
        if key == arcade.key.Q and modifiers in meta_keys:
            logger.error('Received Keyboard Shortcut to Quit')
            arcade.exit()

        for register in self.get_all_registers():
            if register.on_key_press:
                register.on_key_press(register.sprite, key, modifiers)

    @beartype
    def on_key_hold(self) -> None:
        """Custom implementation to trigger at intervals from on_update for pressed keys."""
        for register in self.get_all_registers():
            if register.on_key_hold:
                for key in self.pressed_keys.keys:
                    register.on_key_hold(register.sprite, key, self.pressed_keys.modifiers)

    @beartype
    def on_key_release(self, key: int, modifiers: int) -> None:
        """React to key release.

        Docs: https://api.arcade.academy/en/stable/arcade.key.html#key

        """
        self.pressed_keys.released(key, modifiers)
        for register in self.get_all_registers():
            if register.on_key_release:
                register.on_key_release(register.sprite, key, modifiers)

    @beartype
    def _reload_module(self, module_instance: ModuleType) -> None:
        """Generically reload a given module."""
        try:
            module_instance.SOURCE_NAME
        except AttributeError as exc:
            raise NotImplementedError('The code module must contain a global "SOURCE_NAME"') from exc

        try:
            reload(module_instance)
        except Exception:  # pylint: disable=broad-except
            logger.exception(f'Failed to reload {module_instance.SOURCE_NAME}')

        try:
            module_instance.load_sprites
        except AttributeError as exc:
            raise NotImplementedError('The code module must contain a "load_sprites" function') from exc

        for source, registers in self.registered_items.items():
            if source.startswith(module_instance.SOURCE_NAME):
                for register in registers:
                    register.sprite.remove_from_sprite_lists()
        module_instance.load_sprites(self.sprite_register)

    @beartype
    def reload_modules(self) -> None:
        """Reload all modules."""
        for module_instance in self.code_modules:
            self._reload_module(module_instance)

    @beartype
    def on_update(self, delta_time: float) -> None:
        """Incremental redraw."""
        if self.pressed_keys.on_update():
            self.on_key_hold()
        game_clock = self.game_clock.on_update(delta_time)
        for register in self.get_all_registers():
            if register.on_update:
                register.on_update(register.sprite, game_clock)
