"""Task 02: Equipped Item.

The second task will be to apply the "O" of the S.O.L.I.D design principles to the inventory

> (O) **Open-Close Principle**
>
> Open for extension, not modification.
> Adding new features should not require changing the base class

"""

import random

from beartype import beartype
from loguru import logger

from ...core.models.sprite_state import Direction
from ...core.views.rpg_sprites import PlayerSprite as BasePlayerSprite

"""
----------------------------------------------------------------------------------------
Goal: Write the logic to position the item based on the player's direction. Right now,
only the Left direction is implemented, but you'll need to extend this class to support
RIGHT, UP, and DOWN.
----------------------------------------------------------------------------------------
"""


class PlayerSprite(BasePlayerSprite):
    @beartype
    def update_item_position(self) -> None:
        """
        TODO: Modify this method by setting the item position (self.state.direction) based
        on the player's direction
        """

        if not self.item:
            return

        self.item.center_y = self.center_y - 5

        if self.state.direction == Direction.LEFT:
            self.item.center_x = self.center_x - 10
            self.item.scale = -1
            self.item.angle = -90
        else:
            logger.error(  # FIXME: Show this in the message box
                f"{self.state.direction} is not yet implemented!"
                " Edit the code in 'task02/task_o_equipped_item.py' to fix."
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
