"""Main Game Window."""

from collections import defaultdict
from importlib import reload
from types import ModuleType

import arcade
import arcade.key
import arcade.resources
from beartype import beartype
from loguru import logger
from pyglet.math import Vec2

from .constants import CAMERA_SPEED
from .game_clock import GameClock
from .game_map import GameMap
from .game_gui import GameGUI
from .pressed_keys import PressedKeys
from .registration import Register, SpriteRegister
from .view_strategies.rpg_movement import RPGMovement


class GameView(arcade.View):

    @beartype
    def __init__(
            self,
            player_module: ModuleType,
            code_modules: list[ModuleType] | None = None,
            **kwargs,
    ) -> None:  # type: ignore[no-untyped-def]
        """Configure window.

        Docs: https://api.arcade.academy/en/latest/api/window.html#arcade-window

        """
        super().__init__(**kwargs)
        arcade.resources.add_resource_handle('assets', 'game/assets')
        arcade.resources.add_resource_handle('characters', 'game/assets/characters')
        arcade.resources.add_resource_handle('maps', 'game/assets/maps')
        arcade.resources.add_resource_handle('sounds', 'game/assets/sounds')

        self.map = GameMap()
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)
        self.game_clock = GameClock()
        self.pressed_keys = PressedKeys()
        self.rpg_movement = RPGMovement(self.map)

        self.searchable_items = self.map.map_layers['searchable']
        self.selected_item = None

        self.registered_items: dict[str, list[Register]] = defaultdict(list)
        self.sprite_register = SpriteRegister()
        self.sprite_register.set_listener(self.on_register)

        self.registered_player = None
        self.player_sprite = None
        self.player_register = SpriteRegister()
        self.player_register.set_listener(self.on_register_player)

        self.player_module = player_module
        self.code_modules = code_modules or []
        self.reload_modules()

    @beartype
    def on_register(self, register: Register) -> None:
        self.registered_items[register.source].append(register)
        self.searchable_items.append(register.sprite)

    @beartype
    def on_register_player(self, register: Register) -> None:
        self.registered_player = register

    @beartype
    def get_all_registers(self) -> list[Register]:
        return sum(self.registered_items.values(), [])

    @beartype
    def on_draw(self) -> None:
        """Arcade Draw Event."""
        self.clear()
        self.camera.use()
        self.map.scene.draw()
        self.player_sprite.draw()
        if self.player_sprite.item:
            self.player_sprite.item.draw()
        self.searchable_items.draw()
        self.scroll_to_player()

        # Draw GUI
        self.camera_gui.use()
        self.gui = GameGUI(self)
        self.gui.draw_inventory()

    @beartype
    def on_mouse_motion(self, x_pos: int, y_pos: int, d_x: float, d_y: float) -> None:
        """React to mouse position."""
        for register in self.get_all_registers():
            if register.on_mouse_motion:
                register.on_mouse_motion(register.sprite, x_pos, y_pos, d_x, d_y)

    @beartype
    def on_mouse_press(self, x_pos: int, y_pos: int, button, key_modifiers) -> None:
        """React to mouse press."""
        self.rpg_movement.on_mouse_press(x_pos, y_pos, button, key_modifiers)

    @beartype
    def on_key_press(self, key: int, modifiers: int) -> None:
        """React to key press."""
        self.pressed_keys.pressed(key, modifiers)
        self.rpg_movement.on_key_press(key, modifiers)
        # Convenience handlers for Reload and Quit
        meta_keys = {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}
        if key == arcade.key.R and modifiers in meta_keys:
            logger.warning('Reloading modules')
            self.reload_modules()
        if key == arcade.key.Q and modifiers in meta_keys:  # pragma: no cover
            logger.error('Received Keyboard Shortcut to Quit')
            arcade.exit()  # type: ignore[no-untyped-call]
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
        self.rpg_movement.on_key_release(key, modifiers)
        for register in self.get_all_registers():
            if register.on_key_release:
                register.on_key_release(register.sprite, key, modifiers)
        self.selected_item = None

    @beartype
    def _reload_module(self, module_instance: ModuleType, sprite_register: SpriteRegister) -> None:
        """Generically reload a given module."""
        try:
            module_instance.SOURCE_NAME
        except AttributeError as exc:  # pragma: no cover
            raise NotImplementedError('The code module must contain a global "SOURCE_NAME"') from exc

        try:
            reload(module_instance)
        except Exception:  # pylint: disable=broad-except  # pragma: no cover
            logger.exception(f'Failed to reload {module_instance.SOURCE_NAME}')

        try:
            module_instance.load_sprites
        except AttributeError as exc:  # pragma: no cover
            raise NotImplementedError('The code module must contain a "load_sprites" function') from exc

        for source, registers in self.registered_items.items():
            if source.startswith(module_instance.SOURCE_NAME):
                for register in registers:
                    register.sprite.remove_from_sprite_lists()
        module_instance.load_sprites(sprite_register)

    @beartype
    def reload_modules(self) -> None:
        """Reload all modules."""
        for module_instance in self.code_modules:
            self._reload_module(module_instance, self.sprite_register)

        self._reload_module(self.player_module, self.player_register)
        self.player_sprite: arcade.Sprite = self.registered_player.sprite

        self.rpg_movement.setup_player_sprite(self.player_sprite)
        self.rpg_movement.setup_physics()

    @beartype
    def on_update(self, delta_time: float) -> None:
        """Incremental redraw."""
        if self.pressed_keys.on_update():
            self.on_key_hold()
        self.rpg_movement.on_update()
        game_clock = self.game_clock.on_update(delta_time)
        for register in self.get_all_registers():
            if register.on_update:
                register.on_update(register.sprite, game_clock)

    @beartype
    def scroll_to_player(self, speed: int = CAMERA_SPEED) -> None:
        vector = Vec2(
            self.player_sprite.center_x - self.window.width / 2,
            self.player_sprite.center_y - self.window.height / 2,
        )
        self.camera.move_to(vector, speed)
