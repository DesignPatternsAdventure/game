"""Task 02: Inventory.

The second task will be to apply the "O" of the S.O.L.I.D design principles to the inventory

> (O) **Open-Close Principle**
>
> Open for extension, not modification.
> Adding new features should not require changing the base class

"""

# FIXME: Rename files to match the actual task once finalized

import random

import arcade
from arcade.sprite import Sprite
from beartype import beartype
from loguru import logger

from ...core.models.base_player_inventory import PlayerInventoryInterface
from ...core.models.sprite_state import Direction
from ...core.views.rpg_sprites import PlayerSprite as BasePlayerSprite


class PlayerSprite(BasePlayerSprite):

    _sound_update: float = 0.0

    # FIXME: These methods could be moved back to core if not used, but might make for good tasks

    @beartype
    def __init__(
        self, sheet_name: str, player_inventory: PlayerInventoryInterface
    ) -> None:
        super().__init__(sheet_name)
        self.player_inventory = player_inventory
        self._footstep_sound = arcade.load_sound(":sounds:footstep00.wav")

    @beartype
    def equip(self, item_name: str) -> bool:
        """Attempt to equip the item by name."""
        if self.item and self.item.properties["name"] == item_name:
            self.player_inventory.unequip_item()
            return False
        self.item = item_name
        return True

    @beartype
    def add_item_to_inventory(self, sprite: Sprite) -> int | None:
        return self.player_inventory.store_item(sprite)

    @beartype
    def on_update(self, delta_time: float = 0.0) -> None:
        super().on_update(delta_time)
        if not self.change_x and not self.change_y:
            self._sound_update = 0
            return

        if self.state.time_since_last_update > 1:
            self._sound_update += 0.5
        if self._sound_update >= 1:
            arcade.play_sound(self._footstep_sound, volume=0.3)
            self._sound_update = 0

        self.update_item_position()

    @beartype
    def update_item_position(self) -> None:
        if not self.item:
            return

        """
        Goal: write the logic to position the item based on the player's direction
        (self.state.direction). Right now, only the Left direction is implemented,
        but you'll need to extend this class to support RIGHT, UP, and DOWN
        """

        self.item.center_y = self.center_y - 5

        if self.state.direction == Direction.LEFT:
            self.item.center_x = self.center_x - 10
            self.item.scale = -1
            self.item.angle = -90
        else:
            logger.error(  # FIXME: Show this in the message box
                f"{self.state.direction} is not yet implemented!"
                " Edit the code in 'task02/task_o_inventory.py' to fix."
            )

        if self.state.direction == Direction.RIGHT:
            self.item.center_x = self.center_x - random.choice([-40, -15, 15, 40])
            self.item.scale = random.choice([-1, 1, 3])
            self.item.angle = random.choice([-90, -45, 45, 90])
            logger.warning(
                "Randomly setting the item position to demonstrate how the different"
                f" values work. Now at: ({self.item.center_x}, {self.item.center_y})"
                f" with angle={self.item.angle} and scale={self.item.scale}"
            )

        # if self.state.direction == Direction.RIGHT:
        #     self.item.center_x = self.center_x + 10
        #     self.item.scale = 1
        #     self.item.angle = 0
        #
        # if self.state.direction == Direction.UP:
        #     self.item.center_x = self.center_x - 15
        #     self.item.scale = -1
        #     self.item.angle = -90
        #
        # if self.state.direction == Direction.DOWN:
        #     self.item.center_x = self.center_x + 15
        #     self.item.scale = 1
        #     self.item.angle = 0
