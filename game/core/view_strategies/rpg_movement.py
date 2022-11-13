"""Extracted methods from community-rpg's GameView."""

import arcade
from game.core.game_gui import GameGUI
from game.core.game_state import GameState

from .. import constants


class RPGMovement:
    player_sprite = None

    up_pressed = False
    down_pressed = False
    left_pressed = False
    right_pressed = False

    physics_engine = None
    animate = False
    item_target = None

    def __init__(self, map: arcade.TileMap, state: GameState, gui: GameGUI) -> None:
        self.map = map
        self.state = state
        self.gui = gui

    def setup_player_sprite(self, player_sprite: arcade.Sprite) -> None:
        self.player_sprite = player_sprite
        self.player_sprite.center_x = self.state.center_x
        self.player_sprite.center_y = self.state.center_y
        self.player_sprite.inventory = self.state.inventory
        if self.state.item:
            self.player_sprite.item = self.state.item
            self.player_sprite.update_item_position()

    def setup_physics(self) -> None:
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.map.scene["wall_list"]
        )

    def on_update(self) -> None:
        """All the logic to move, and the game logic goes here."""
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        moving_up = (
            self.up_pressed
            and not self.down_pressed
            and not self.right_pressed
            and not self.left_pressed
        )

        moving_down = (
            self.down_pressed
            and not self.up_pressed
            and not self.right_pressed
            and not self.left_pressed
        )

        moving_right = (
            self.right_pressed
            and not self.left_pressed
            and not self.up_pressed
            and not self.down_pressed
        )

        moving_left = (
            self.left_pressed
            and not self.right_pressed
            and not self.up_pressed
            and not self.down_pressed
        )

        moving_up_left = (
            self.up_pressed
            and self.left_pressed
            and not self.down_pressed
            and not self.right_pressed
        )

        moving_down_left = (
            self.down_pressed
            and self.left_pressed
            and not self.up_pressed
            and not self.right_pressed
        )

        moving_up_right = (
            self.up_pressed
            and self.right_pressed
            and not self.down_pressed
            and not self.left_pressed
        )

        moving_down_right = (
            self.down_pressed
            and self.right_pressed
            and not self.up_pressed
            and not self.left_pressed
        )

        if moving_up:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED

        if moving_down:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED

        if moving_left:
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED

        if moving_right:
            self.player_sprite.change_x = constants.MOVEMENT_SPEED

        if moving_up_left:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED / 1.5

        if moving_up_right:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = constants.MOVEMENT_SPEED / 1.5

        if moving_down_left:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED / 1.5

        if moving_down_right:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = constants.MOVEMENT_SPEED / 1.5

        # Call update to move the sprite
        if self.physics_engine:
            self.physics_engine.update()

        # Update player animation
        self.player_sprite.on_update()

        if self.animate and self.player_sprite.item:
            self.animate_player_item(self.player_sprite)

        self.search()

    def on_key_press(self, key, modifiers) -> None:
        """Called whenever a key is pressed."""
        if key in constants.KEY_UP:
            self.up_pressed = True
        elif key in constants.KEY_DOWN:
            self.down_pressed = True
        elif key in constants.KEY_LEFT:
            self.left_pressed = True
        elif key in constants.KEY_RIGHT:
            self.right_pressed = True
        # elif key in constants.INVENTORY:
        #     self.window.show_view(self.window.views["inventory"])
        # elif key == arcade.key.ESCAPE:
        #     self.window.show_view(self.window.views["main_menu"])
        elif key == arcade.key.KEY_1:
            self.player_sprite.equip(1)

    def on_key_release(self, key, modifiers) -> None:
        """Called when the user releases a key."""

        if key in constants.KEY_UP:
            self.up_pressed = False
        elif key in constants.KEY_DOWN:
            self.down_pressed = False
        elif key in constants.KEY_LEFT:
            self.left_pressed = False
        elif key in constants.KEY_RIGHT:
            self.right_pressed = False
        self.state.save_player_data(self.player_sprite)

    def on_mouse_press(self, x, y, button, key_modifiers) -> None:
        """Called when the user presses a mouse button."""
        if (
            button == arcade.MOUSE_BUTTON_LEFT
            and self.player_sprite.item
            and "interactables_blocking" in self.map.map_layers
        ):
            closest = arcade.get_closest_sprite(
                self.player_sprite, self.map.map_layers["interactables_blocking"]
            )
            if not closest:
                return
            (sprite, dist) = closest
            if dist < constants.SPRITE_SIZE * 2:
                self.item_target = sprite
                self.animate = True

    def search(self):
        """Picks up any item that user collides with"""
        if "searchable" in self.map.map_layers:
            map_layers = self.map.map_layers

            searchable_sprites = map_layers["searchable"]
            sprites_in_range = arcade.check_for_collision_with_list(
                self.player_sprite, searchable_sprites
            )
            if not len(sprites_in_range):
                return

            for sprite in sprites_in_range:

                if "item" in sprite.properties:
                    key = self.player_sprite.add_item_to_inventory(sprite)
                    self.gui.draw_message_box(
                        message=f"{sprite.properties['item']} added to inventory!",
                        notes=f"Press {key} to use",
                        seconds=3,
                    )
                    self.state.remove_sprite_from_map(sprite, True)

    def animate_player_item(self, player_sprite):
        config = constants.ITEM_CONFIG[player_sprite.item.properties["item"]][
            "animation"
        ]
        self.animate = player_sprite.animate_item(self, config)
        # Finished animation
        if not self.animate and self.item_target:
            self.state.remove_sprite_from_map(self.item_target)
            if "item" in self.item_target.properties:
                item_drop = self.item_target.properties["item"]
                file_path = f":assets:{item_drop}.png"
                sprite = arcade.Sprite(file_path)
                sprite.properties = {"item": item_drop}
                self.player_sprite.add_item_to_inventory(sprite)
                self.gui.draw_message_box(message=f"{item_drop} added to inventory!")
            self.item_target = None
