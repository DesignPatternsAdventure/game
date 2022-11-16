"""Extracted methods from community-rpg's GameView."""

import arcade
from beartype import beartype
from loguru import logger

from .. import constants
from ..game_map import GameMap
from ..game_state import GameState
from ..pressed_keys import PressedKeys
from ..view_strategies.raft_movement import (
    RAFT_COMPONENTS,
    check_missing_components,
    generate_missing_components_text,
)
from .main import GameGUI


class RPGMovement:
    player_sprite = None

    up_pressed = False
    down_pressed = False
    left_pressed = False
    right_pressed = False

    physics_engine = None
    animate = False
    item_target = None

    @beartype
    def __init__(
        self,
        game_map: GameMap,
        state: GameState,
        gui: GameGUI,
        pressed_keys: PressedKeys,
    ) -> None:
        self.game_map = game_map
        self.state = state
        self.gui = gui
        self.pressed_keys = pressed_keys

    @beartype
    def setup_player_sprite(self, player_sprite: arcade.Sprite) -> None:
        self.player_sprite = player_sprite
        self.player_sprite.center_x = self.state.center_x
        self.player_sprite.center_y = self.state.center_y
        self.player_sprite.inventory = self.state.inventory
        if self.state.item:
            self.player_sprite.item = self.state.item
            self.player_sprite.update_item_position()

    @beartype
    def setup_physics(self) -> None:
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.game_map.scene["wall_list"]
        )

    @beartype
    def on_update(self) -> None:
        """Calculate speed based on the keys pressed."""
        (
            self.player_sprite.change_x,
            self.player_sprite.change_y,
        ) = self.pressed_keys.get_movement_vector(constants.MOVEMENT_SPEED)

        # Call update to move the sprite
        if self.physics_engine:
            self.physics_engine.update()

        # Update player animation
        self.player_sprite.on_update()

        if self.animate and self.player_sprite.item:
            self.animate_player_item()

        self.search()

    @beartype
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called whenever a key is pressed."""
        if idx := constants.NUMERIC_KEY_MAPPING.get(key):
            self.use_item(idx)

    @beartype
    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key."""
        self.state.save_player_data(self.player_sprite)

    def on_mouse_press(self, x, y, button, key_modifiers) -> None:
        """Called when the user presses a mouse button."""
        if (
            button == arcade.MOUSE_BUTTON_LEFT
            and self.player_sprite.item
            and "interactables_blocking" in self.game_map.map_layers
        ):
            closest = arcade.get_closest_sprite(
                self.player_sprite, self.game_map.map_layers["interactables_blocking"]
            )
            if not closest:
                return
            (sprite, dist) = closest
            if dist < constants.SPRITE_SIZE * 2:
                self.item_target = sprite
                self.animate = True
            else:
                self.gui.draw_message_box(
                    message=f"Seems like nothing is within range...", seconds=1
                )

    @beartype
    def search(self) -> None:
        """Picks up any item that user collides with."""
        if "searchable" in self.game_map.map_layers:
            map_layers = self.game_map.map_layers

            searchable_sprites = map_layers["searchable"]
            sprites_in_range = arcade.check_for_collision_with_list(
                self.player_sprite, searchable_sprites
            )
            for sprite in sprites_in_range or []:
                if "name" in sprite.properties:
                    key = self.player_sprite.add_item_to_inventory(sprite)
                    self.gui.draw_message_box(
                        message=f"{sprite.properties['name']} added to inventory!",
                        notes=f"Press {key} to use",
                    )
                    self.state.remove_sprite_from_map(sprite, True)

    @beartype
    def use_item(self, slot: int) -> None:
        inventory = self.player_sprite.player_inventory.get_ordered_sprites()
        if len(inventory) < slot:
            self.gui.draw_message_box(message=f"No item in inventory slot {slot}")
            return

        # FIXME: This logic needs to be moved to Task 4
        index = slot - 1
        item_name = inventory[index].properties["name"]
        # Build raft
        if item_name in RAFT_COMPONENTS:
            if check_missing_components(inventory):
                missing_components_text = generate_missing_components_text(inventory)
                self.gui.draw_message_box(
                    message=missing_components_text["message"],
                    notes=missing_components_text["notes"],
                    seconds=5,
                )
            else:
                # TODO spawn raft
                self.gui.draw_message_box(
                    message="Raft is not implemented yet, check back later!"
                )
        elif "equippable" not in inventory[index].properties:
            logger.info(f"{item_name} is not equippable!")
            return

        if self.player_sprite.equip(item_name):
            self.gui.draw_message_box(
                message=f"Equipped {item_name}",
                notes="Left click to activate",
            )
        else:
            self.gui.draw_message_box(message=f"Unequipped {item_name}", seconds=1)

    @beartype
    def animate_player_item(self) -> None:
        config = constants.ITEM_CONFIG[self.player_sprite.item.properties["name"]][
            "animation"
        ]
        self.animate = self.player_sprite.animate_item(config)
        # Finished animation
        if not self.animate and self.item_target:
            self.state.remove_sprite_from_map(self.item_target)
            if "drop" in self.item_target.properties:
                item_drop = self.item_target.properties["drop"]
                file_path = f":assets:{item_drop}.png"
                sprite = arcade.Sprite(file_path)
                sprite.properties = {"name": item_drop}
                key = self.player_sprite.add_item_to_inventory(sprite)
                self.gui.draw_message_box(
                    message=f"{item_drop} added to inventory!",
                    notes=f"Press {key} to use",
                )
            self.item_target = None
