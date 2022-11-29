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

from .constants import CAMERA_SPEED, HORIZONTAL_MARGIN, MAP_SIZE, VERTICAL_MARGIN
from .game_clock import GameClock
from .game_map import GameMap
from .game_state import GameState
from .gui import GameGUI
from .gui.rpg_movement import RPGMovement
from .pause_menu import PauseMenu
from .pressed_keys import PressedKeys
from .registration import Register, SpriteRegister


class GameView(arcade.View):  # pylint: disable=R0902
    """Main Game View and Event Dispatcher.

    Implements code reload

    """

    @beartype
    def __init__(  # type: ignore[no-untyped-def]
        self,
        player_module: ModuleType,
        code_modules: list[ModuleType] | None = None,
        **kwargs,
    ) -> None:  # type: ignore[no-untyped-def]
        """Configure window.

        Docs: https://api.arcade.academy/en/latest/api/window.html#arcade-window

        """
        super().__init__(**kwargs)
        arcade.resources.add_resource_handle("assets", "game/assets")
        arcade.resources.add_resource_handle("characters", "game/assets/characters")
        arcade.resources.add_resource_handle("maps", "game/assets/maps")
        arcade.resources.add_resource_handle("sounds", "game/assets/sounds")
        arcade.resources.add_resource_handle("animation", "game/assets/animation")

        self.state = GameState()  # type: ignore[no-untyped-call]
        self.game_clock = GameClock()
        self.pressed_keys = PressedKeys()
        self.item = self.state.item
        window_shape = (self.window.width, self.window.height)  # type: ignore[has-type]
        self.gui = GameGUI(self.state, self.game_clock, self.pressed_keys, window_shape)
        self.tile_map = GameMap(self.state, self.game_clock)  # type: ignore[no-untyped-call]
        self.rpg_movement = RPGMovement(
            self.game_clock, self.tile_map, self.state, self.gui, self.pressed_keys
        )
        self.camera = arcade.Camera(self.window.width, self.window.height)  # type: ignore[has-type]
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)  # type: ignore[has-type]

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

    @beartype
    def on_register_player(self, register: Register) -> None:
        self.registered_player = register  # type: ignore[assignment]

    @beartype
    def get_all_registers(self) -> list[Register]:
        return sum(self.registered_items.values(), [])

    @beartype
    def on_draw(self) -> None:
        """Arcade Draw Event."""
        self.clear()
        self.camera.use()  # type: ignore[no-untyped-call]
        self.tile_map.draw()  # type: ignore[no-untyped-call]
        self.rpg_movement.draw()
        self.scroll_to_player()

        # Draw GUI
        self.camera_gui.use()  # type: ignore[no-untyped-call]
        self.gui.draw()

    @beartype
    def on_mouse_motion(self, x_pos: int, y_pos: int, d_x: float, d_y: float) -> None:
        """React to mouse position."""
        for register in self.get_all_registers():
            if register.on_mouse_motion:
                register.on_mouse_motion(register.sprite, x_pos, y_pos, d_x, d_y)

    @beartype
    def on_mouse_press(
        self, x_pos: int, y_pos: int, button: int, key_modifiers: int
    ) -> None:
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
            logger.warning("Reloading modules")
            self.reload_modules()
        if key == arcade.key.Q and modifiers in meta_keys:  # pragma: no cover
            logger.error("Received Keyboard Shortcut to Quit")
            arcade.exit()  # type: ignore[no-untyped-call]
        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseMenu(self))  # type: ignore[has-type]
        for register in self.get_all_registers():
            if register.on_key_press:
                register.on_key_press(register.sprite, key, modifiers)

    @beartype
    def on_key_hold(self) -> None:
        """Custom implementation to trigger at intervals from on_update for pressed keys."""
        for register in self.get_all_registers():
            if register.on_key_hold:
                for key in self.pressed_keys.keys:
                    register.on_key_hold(
                        register.sprite, key, self.pressed_keys.modifiers
                    )

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

    @beartype
    def _reload_module(
        self, module_instance: ModuleType, sprite_register: SpriteRegister
    ) -> None:
        """Generically reload a given module."""
        try:
            source_name = module_instance.SOURCE_NAME
        except AttributeError:
            # raise NotImplementedError('The code module must contain a global "SOURCE_NAME"') from exc
            source_name = str(module_instance)

        try:  # noqa: TC101
            reload(module_instance)
        except Exception:  # pylint: disable=broad-except  # pragma: no cover
            logger.exception(f"Failed to reload {source_name}")

        try:  # noqa: TC101
            load_sprites = module_instance.load_sprites
        except AttributeError:
            # raise NotImplementedError('The code module must contain a "load_sprites" function') from exc
            load_sprites = None

        for source, registers in self.registered_items.items():
            if source.startswith(source_name):
                for register in registers:
                    register.sprite.remove_from_sprite_lists()
        if load_sprites:
            load_sprites(sprite_register)

    @beartype
    def reload_modules(self) -> None:
        """Reload all modules."""
        for module_instance in self.code_modules:
            self._reload_module(module_instance, self.sprite_register)

        self._reload_module(self.player_module, self.player_register)
        self.player_sprite: arcade.Sprite = self.registered_player.sprite

        self.rpg_movement.setup_player_sprite(self.player_sprite)  # type: ignore[arg-type]
        self.rpg_movement.setup_physics()

    @beartype
    def on_update(self, delta_time: float) -> None:
        """Incremental redraw."""
        if self.pressed_keys.on_update():
            self.on_key_hold()
        self.rpg_movement.on_update()
        self.tile_map.on_update()  # type: ignore[no-untyped-call]
        game_clock = self.game_clock.on_update(delta_time)
        for register in self.get_all_registers():
            if register.on_update:
                register.on_update(register.sprite, game_clock)

    @beartype
    def scroll_to_player(self, speed: float = CAMERA_SPEED) -> None:
        x_cam = self.player_sprite.center_x  # type: ignore[attr-defined]
        y_cam = self.player_sprite.center_y  # type: ignore[attr-defined]

        if x_cam < HORIZONTAL_MARGIN:
            x_cam = HORIZONTAL_MARGIN
        elif x_cam > MAP_SIZE - HORIZONTAL_MARGIN:
            x_cam = MAP_SIZE - HORIZONTAL_MARGIN
        if y_cam < VERTICAL_MARGIN:
            y_cam = VERTICAL_MARGIN
        elif y_cam > MAP_SIZE - VERTICAL_MARGIN:
            y_cam = MAP_SIZE - VERTICAL_MARGIN

        vector = Vec2(
            x_cam - self.window.width / 2,  # type: ignore[has-type]
            y_cam - self.window.height / 2,  # type: ignore[has-type]
        )
        self.camera.move_to(vector, speed)

    @beartype
    def restart(self) -> None:
        self.window.show_view(GameView(self.player_module, self.code_modules))  # type: ignore[has-type]
