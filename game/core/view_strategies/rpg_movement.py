"""Extracted methods from community-rpg's GameView."""

import arcade

from .. import constants


class RPGMovement:
    center_x = constants.STARTING_X
    center_y = constants.STARTING_Y
    player_sprite = None

    up_pressed = False
    down_pressed = False
    left_pressed = False
    right_pressed = False

    physics_engine = None
    animate = False

    def __init__(self, map: arcade.TileMap) -> None:
        self.map = map

    def setup_player_sprite(self, player_sprite: arcade.Sprite) -> None:
        self.player_sprite = player_sprite
        self.player_sprite.center_x = self.center_x
        self.player_sprite.center_y = self.center_y

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
        # if self.message_box:
        #     self.message_box.on_key_press(key, modifiers)
        #     return

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
        self.center_x = self.player_sprite.center_x
        self.center_y = self.player_sprite.center_y
        # self.game_state.save_player_data()

    def on_mouse_press(self, x, y, button, key_modifiers) -> None:
        """Called when the user presses a mouse button."""
        # if self.message_box:
        #     self.close_message_box()
        if button == arcade.MOUSE_BUTTON_LEFT and self.player_sprite.item:
            closest = arcade.get_closest_sprite(
                self.player_sprite, self.map.map_layers["interactables_blocking"]
            )
            if not closest:
                return
            (sprite, dist) = closest
            if dist < constants.SPRITE_SIZE * 2:
                self.player_sprite.item_target = sprite
                self.animate = True

    def search(self):
        """Picks up any item that user collides with"""
        map_layers = self.map.map_layers

        searchable_sprites = map_layers["searchable"]
        sprites_in_range = arcade.check_for_collision_with_list(
            self.player_sprite, searchable_sprites
        )
        if not len(sprites_in_range):
            return

        for sprite in sprites_in_range:

            if "item" in sprite.properties:
                self.player_sprite.add_item_to_inventory(self, sprite)
                sprite.remove_from_sprite_lists()

    def animate_player_item(self, player_sprite):
        config = constants.ITEM_CONFIG[player_sprite.item.properties["item"]][
            "animation"
        ]
        self.animate = player_sprite.animate_item(self, config)
