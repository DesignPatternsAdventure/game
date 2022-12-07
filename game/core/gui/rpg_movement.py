"""Extracted methods from community-rpg's GameView."""
import arcade
from beartype import beartype
from loguru import logger

from .. import constants
from ..game_clock import GameClock
from ..game_map import GameMap
from ..game_state import GameState
from ..pressed_keys import PressedKeys
from ..registration import Register
from ..view_strategies.raft_utils import (
    RAFT_COMPONENTS,
    board_raft,
    check_missing_components,
    dock_raft,
    generate_missing_components_text,
    initial_board_raft,
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
        game_clock: GameClock,
        game_map: GameMap,
        state: GameState,
        gui: GameGUI,
        pressed_keys: PressedKeys,
    ) -> None:
        self.game_clock = game_clock
        self.next_save = self.game_clock.get_time_in_future(0.2)
        self.game_map = game_map
        self.state = state
        self.gui = gui
        self.pressed_keys = pressed_keys
        self.vehicle = None

    @beartype
    def setup_player_sprite(self, player_sprite: arcade.Sprite) -> None:
        self.player_sprite = player_sprite
        self.player_sprite.center_x = self.state.center_x
        self.player_sprite.center_y = self.state.center_y
        for sprite in self.state.inventory:
            self.player_sprite.add_item_to_inventory(sprite)  # type: ignore[attr-defined]
        if self.state.item:
            self.player_sprite.equip(self.state.item.properties["name"])  # type: ignore[attr-defined]
        if self.state.vehicle:
            self.vehicle = self.state.vehicle
            self.vehicle.docked = self.state.vehicle_docked

    @beartype
    def setup_registered_vehicle(self, registered_vehicle: Register) -> None:
        self.registered_vehicle = registered_vehicle
        if self.vehicle:
            self.vehicle = registered_vehicle.sprite
            self.vehicle.center_x = self.state.vehicle_x
            self.vehicle.center_y = self.state.vehicle_y
            self.vehicle.docked = self.state.vehicle_docked
            self.vehicle.visible = True

    @beartype
    def setup_physics(self) -> None:
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.game_map.scene["wall_list"]  # type: ignore[arg-type]
        )

    @beartype
    def draw(self) -> None:
        if self.vehicle:
            self.vehicle.draw()
        self.player_sprite.draw()
        if self.player_sprite.item:
            self.player_sprite.item.draw()

    @beartype
    def on_update(self) -> None:
        """Calculate speed based on the keys pressed."""
        (
            self.player_sprite.change_x,
            self.player_sprite.change_y,
        ) = self.pressed_keys.get_movement_vector(constants.MOVEMENT_SPEED)

        # Call update to move the sprite
        if self.physics_engine:
            self.physics_engine.update()  # type: ignore[no-untyped-call]

        # Update player animation
        self.player_sprite.on_update()

        if self.animate and self.player_sprite.item:
            self.animate_player_item()

        # Sync with vehicle
        if self.vehicle and not self.vehicle.docked:
            self.vehicle.sync_with_player(self.player_sprite)
            self.vehicle.on_update()

        self.search()
        self.state.inventory = self.player_sprite.inventory

    @beartype
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called whenever a key is pressed."""
        if idx := constants.NUMERIC_KEY_MAPPING.get(key):
            self.use_item(idx)

    @beartype
    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key."""
        # Cap saving to once per second
        if self.game_clock.current_time > self.next_save:
            self.state.save_player_data(self.player_sprite, self.vehicle)
            self.next_save = self.game_clock.get_time_in_future(0.2)

    def on_mouse_press(self, x, y, button, key_modifiers) -> None:  # type: ignore[no-untyped-def]
        """Called when the user presses a mouse button."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.vehicle:
                is_on_vehicle = arcade.check_for_collision(
                    self.player_sprite, self.vehicle
                )
                if is_on_vehicle:
                    # prioritize handling mouse click for raft if player is on raft
                    if self.vehicle.docked:
                        self.handle_mouse_press_board_raft()
                    else:
                        self.handle_mouse_press_dock_raft()
            if (
                self.player_sprite.item
                and "interactables_blocking" in self.game_map.map_layers
            ):
                self.handle_mouse_press_item()

    @beartype
    def search(self) -> None:
        """Picks up any item that user collides with."""
        if searchable_sprites := self.game_map.map_layers.get("searchable"):
            sprites_in_range = arcade.check_for_collision_with_list(
                self.player_sprite, searchable_sprites  # type: ignore[arg-type]
            )
            for sprite in sprites_in_range or []:
                if item_name := sprite.properties.get("name"):
                    try:
                        key = self.player_sprite.add_item_to_inventory(sprite)
                    except Exception as exc:
                        self.gui.draw_message_box(message=str(exc))
                        return
                    self.gui.draw_message_box(
                        message=f"{item_name} added to inventory!",
                        notes=f"Press {key} to use",
                    )
                    self.game_map.remove_sprite(sprite, searchable=True)

    @beartype
    def use_item(self, slot: int) -> None:
        inventory = self.player_sprite.inventory
        if len(inventory) < slot:
            self.gui.draw_message_box(message=f"No item in inventory slot {slot}")
            return

        # FIXME: The raft-building logic needs to be moved to Task 4
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
                try:
                    self.vehicle = self.registered_vehicle.sprite
                    self.vehicle.move_on_water()
                    self.vehicle.sync_with_player(self.player_sprite)
                    initial_board_raft(self.vehicle, self.player_sprite, self.game_map)
                    self.gui.draw_message_box(
                        message="You built a raft!",
                        notes=f"Use WASD to move and left click to dock",
                    )
                except:
                    self.vehicle = None
                    self.gui.draw_message_box(
                        message=f"You try to build and raft and realize you need to complete a task!",
                        notes=f"Edit the code in 'task04/task_i_the_raft.py' to build the raft",
                        seconds=5,
                    )
            return

        if "equippable" not in inventory[index].properties:
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
        item_name = self.player_sprite.item.properties["name"]
        if config := constants.ITEM_CONFIG[item_name].get("animation"):
            self.animate = self.player_sprite.animate_item(config)
            # Finished animation
            if not self.animate and self.item_target:
                self.game_map.remove_sprite(self.item_target, searchable=False)
                self.item_target = None

    @beartype
    def handle_mouse_press_item(self) -> None:
        closest = arcade.get_closest_sprite(
            self.player_sprite, self.game_map.map_layers["interactables_blocking"]  # type: ignore[arg-type]
        )
        if not closest:
            return
        (sprite, dist) = closest
        if dist < constants.SPRITE_SIZE * 2:
            self.item_target = sprite
            self.animate = True
        else:
            self.gui.draw_message_box(
                message="Seems like nothing is within range...", seconds=1
            )

    @beartype
    def handle_mouse_press_board_raft(self) -> None:
        board_raft(self.vehicle, self.player_sprite, self.game_map)
        self.gui.draw_message_box(
            message="Boarded raft!",
            notes="Left click while close to the shore to dock",
            seconds=3,
        )

    @beartype
    def handle_mouse_press_dock_raft(self) -> None:
        sprites_colliding = arcade.check_for_collision_with_list(
            self.vehicle, self.game_map.scene["wall_list"]  # type: ignore[arg-type]
        )
        # First, check if raft is touching shore (otherwise player cannot get on raft)
        if len(sprites_colliding):
            # Then, find closest land to move player to
            (sprite, _) = arcade.get_closest_sprite(
                self.player_sprite, self.game_map.scene["wall_list"]  # type: ignore[arg-type]
            )
            dock_raft(self.vehicle, self.player_sprite, self.game_map, sprite)
            self.gui.draw_message_box(
                message="Docked raft!",
                notes="Left click while close to the raft to board again",
                seconds=3,
            )
        else:
            self.gui.draw_message_box(
                message="Not close enough to shore to dock!", seconds=1
            )
