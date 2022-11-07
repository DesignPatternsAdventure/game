"""Extracted methods from community-rpg's GameView."""

import arcade

from .. import constants


class RPGMovement:

    up_pressed = False
    down_pressed = False
    left_pressed = False
    right_pressed = False

    physics_engine = None

    def setup_physics(self, player_sprite: arcade.Sprite, wall_list: arcade.SpriteList) -> None:
        self.physics_engine = arcade.PhysicsEngineSimple(player_sprite, wall_list)

    def on_update(self, player_sprite: arcade.Sprite, delta_time: float) -> None:
        """All the logic to move, and the game logic goes here."""
        # Calculate speed based on the keys pressed
        player_sprite.change_x = 0
        player_sprite.change_y = 0

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
            player_sprite.change_y = constants.MOVEMENT_SPEED

        if moving_down:
            player_sprite.change_y = -constants.MOVEMENT_SPEED

        if moving_left:
            player_sprite.change_x = -constants.MOVEMENT_SPEED

        if moving_right:
            player_sprite.change_x = constants.MOVEMENT_SPEED

        if moving_up_left:
            player_sprite.change_y = constants.MOVEMENT_SPEED / 1.5
            player_sprite.change_x = -constants.MOVEMENT_SPEED / 1.5

        if moving_up_right:
            player_sprite.change_y = constants.MOVEMENT_SPEED / 1.5
            player_sprite.change_x = constants.MOVEMENT_SPEED / 1.5

        if moving_down_left:
            player_sprite.change_y = -constants.MOVEMENT_SPEED / 1.5
            player_sprite.change_x = -constants.MOVEMENT_SPEED / 1.5

        if moving_down_right:
            player_sprite.change_y = -constants.MOVEMENT_SPEED / 1.5
            player_sprite.change_x = constants.MOVEMENT_SPEED / 1.5

        # Call update to move the sprite
        if self.physics_engine:
            self.physics_engine.update()

        # Update player animation
        player_sprite.on_update(delta_time)

        # if self.animate and player_sprite.item:
        #     self.animate_player_item()

        # # Update the characters
        # try:
        #     self.map.scene["characters"].on_update(delta_time)
        # except KeyError:
        #     # no characters on map
        #     pass

    def on_key_press(self, key, modifiers) -> None:
        """Called whenever a key is pressed."""
        # if self.message_box:
        #     self.message_box.on_key_press(key, modifiers)
        #     return

        # self.selected_item = None

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
        # elif key in constants.SEARCH:
        #     self.search()
        # elif key == arcade.key.KEY_1:
        #     self.selected_item = 1
        #     # Will add this to the other keys once there are more items
        #     player_sprite.equip(1)
        # elif key == arcade.key.KEY_2:
        #     self.selected_item = 2
        #     player_sprite.equip(2)
        # elif key == arcade.key.KEY_3:
        #     self.selected_item = 3
        # elif key == arcade.key.KEY_4:
        #     self.selected_item = 4
        # elif key == arcade.key.KEY_5:
        #     self.selected_item = 5
        # elif key == arcade.key.KEY_6:
        #     self.selected_item = 6
        # elif key == arcade.key.KEY_7:
        #     self.selected_item = 7
        # elif key == arcade.key.KEY_8:
        #     self.selected_item = 8
        # elif key == arcade.key.KEY_9:
        #     self.selected_item = 9
        # elif key == arcade.key.KEY_0:
        #     self.selected_item = 10

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
        # self.game_state.save_player_data()

    def on_mouse_press(self, x, y, button, key_modifiers) -> None:
        """Called when the user presses a mouse button."""
        # if self.message_box:
        #     self.close_message_box()
        # if button == arcade.MOUSE_BUTTON_RIGHT:
        #     self.player_sprite.destination_point = x, y
        # if button == arcade.MOUSE_BUTTON_LEFT and self.player_sprite.item:
        #     closest = arcade.get_closest_sprite(
        #         self.player_sprite, self.map.map_layers['interactables_blocking']
        #     )
        #     if not closest:
        #         return
        #     (sprite, dist) = closest
        #     if dist < constants.SPRITE_SIZE * 2:
        #         self.player_sprite.item_target = sprite
        #         self.animate = True
