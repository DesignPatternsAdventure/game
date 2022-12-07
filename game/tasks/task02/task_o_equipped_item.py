"""Task 02: Equipped Item.

The second task will be to apply the "O" of the S.O.L.I.D design principles to the inventory

> (O) **Open-Close Principle**
>
> Open for extension, not modification.
> Adding new features should not require changing the base class

"""

from beartype import beartype

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
            # TODO: Remove this error and write the logic for RIGHT, UP, and DOWN
            raise NotImplementedError(
                f"Something is off with your pickaxe. You must complete a task to fix it!\
                \nEdit the code in 'task02/task_o_equipped_item.py' to fix"
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
