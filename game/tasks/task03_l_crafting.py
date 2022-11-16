"""Task 03: TBD.

The third task will be to apply the "L" of the S.O.L.I.D design principles to ...

> (L) **Liskov-Substitution Principle**
>
> Software entities should be interchangeable.

"""

from collections import defaultdict
from contextlib import suppress
from typing import runtime_checkable

from arcade.sprite import Sprite
from beartype import beartype
from beartype.typing import Protocol
from loguru import logger
from pydantic import BaseModel, Field

# ==============================    Part 1 (Learn)    ==============================
"""

An important step in designing reusable code is to find opportunities to write code that
is interchangeable.

"""


# ==============================    Part 2 (Edit)    ==============================


@runtime_checkable
class ItemInterface(Protocol):
    """Interface for items that can be stored in an inventory."""

    # FIXME: Calculate orientation of item based on character position!

    # TODO: Extend the interface in a way that will allow these functions to be interchangeable


class BasicItem(BaseModel):
    """TBD."""

    name: str
    sprite: Sprite | None = None  # FIXME: TBD...

    class Config:
        arbitrary_types_allowed = True


class ConsumableItem(BasicItem):
    """TBD."""


class EquippableItem(BasicItem):
    """TBD."""


class PlayerInventory(BaseModel):
    """Manage the player's inventory."""

    equipped_item: ItemInterface | None = None
    """The currently equipped item, which is removed and returned from the inventory."""

    inventory: dict[str, list[ItemInterface]] = Field(
        default_factory=lambda: defaultdict(list)
    )
    """The user's current inventory.

    The `defaultdict` is used to avoid KeyError's when checking if an item is present

    """

    max_inventory_size: int = 10
    """Cap for the number of items that can be stored."""

    class Config:
        arbitrary_types_allowed = True

    @beartype
    def is_inventory_full(self) -> bool:
        """If True, no new items can be added to the inventory."""
        return len(self.inventory) > self.max_inventory_size

    @beartype
    def store_item(self, sprite: Sprite) -> None:
        """Place a sprite in the inventory."""
        item_name = sprite.properties["name"]

        if self.is_inventory_full and item_name not in self.inventory:
            err = f"Too many items in the inventory. Discard one before adding {item_name}"
            raise RuntimeError(err)

        logger.debug(f"Sorting item {item_name} with {sprite.properties}")

        if "equippable" in sprite.properties:
            item = EquippableItem(name=item_name, sprite=sprite)
        else:
            item = ConsumableItem(name=item_name, sprite=sprite)
        self.inventory[item_name].append(item)

    @beartype
    def store_equipped_item(self) -> None:
        """Move the equipped item (if present) into storage."""
        logger.debug("Attempting to store the equipped item")
        if self.equipped_item:
            self.store_item(self.equipped_item)
            self.equipped_item = None

    @beartype
    def equip_item(self, item_name: str) -> None:
        """Equip an item (if present) by name."""
        self.store_equipped_item()
        self.equipped_item = self.discard_item(item_name)

    @beartype
    def discard_item(self, item_name: str) -> ItemInterface | None:
        """Discard a single item by name."""
        with suppress(IndexError):
            return self.inventory[item_name].pop()
        return None

    @beartype
    def on_update(self) -> None:
        if self.equipped_item:
            logger.debug("Should move the item!")

        # if not self.change_x and not self.change_y:
        #     self.sound_update = 0
        #     return
        # if self.state.should_update > 3:
        #     self.sound_update += 1
        # if self.sound_update >= 3:
        #     arcade.play_sound(self.footstep_sound)
        #     self.sound_update = 0
        # if self.item:
        #     self.update_item_position()

    # def update_item_position(self):
    #     self.item.center_y = self.center_y - 5

    #     if self.state.direction == Direction.LEFT:
    #         self.item.center_x = self.center_x - 10
    #         self.item.scale = -1
    #         self.item.angle = -90

    #     if self.state.direction == Direction.RIGHT:
    #         self.item.center_x = self.center_x + 10
    #         self.item.scale = 1
    #         self.item.angle = 0

    #     if self.state.direction == Direction.UP:
    #         self.item.center_x = self.center_x - 15
    #         self.item.scale = -1
    #         self.item.angle = -90

    #     if self.state.direction == Direction.DOWN:
    #         self.item.center_x = self.center_x + 15
    #         self.item.scale = 1
    #         self.item.angle = 0

    # @beartype
    # def add_item_to_inventory(self, new_item: Sprite) -> int | None:
    #     item_name = new_item.properties["name"]
    #     item_in_list = None
    #     item_index = None
    #     for index, item in enumerate(self.inventory):
    #         if item.properties["name"] == item_name:
    #             item_in_list = item
    #             item_index = index
    #     # If item exists in inventory, stack items in existing slot
    #     if item_in_list:
    #         item_in_list.properties["count"] += 1
    #     # Else add to new slot
    #     else:
    #         new_item.properties["count"] = 1
    #         self.inventory.append(new_item)
    #         item_index = len(self.inventory)
    #     return item_index

    # def animate_item(self, config):
    #     if self.item_anim_frame < config["frames"]:
    #         self.item_anim_frame += 1
    #         angle = config["speed"]
    #         shift_x = config["shift_x"]
    #         shift_y = config["shift_y"]
    #         if self.state.direction in (Direction.RIGHT, Direction.DOWN):
    #             angle = -angle

    #         # Normal animation
    #         if not config["reversable"]:
    #             self.item.angle += angle
    #             self.item.center_x -= shift_x
    #             self.item.center_y -= shift_y
    #             return True

    #         # Reversable animation (back-and-forth)
    #         if self.item_anim_frame % config["reverse_frame"] == 0:
    #             self.item_anim_reversed = not self.item_anim_reversed
    #         if self.item_anim_reversed:
    #             self.item.angle -= angle
    #             self.item.center_x += shift_x
    #             self.item.center_y += shift_y
    #         else:
    #             self.item.angle += angle
    #             self.item.center_x -= shift_x
    #             self.item.center_y -= shift_y
    #         return True

    #     # Finished animation
    #     self.item_anim_frame = 0
    #     return False


"""

If you would like to learn more about the Liskov-Substitution Principle, you can take a look at:

- https://en.wikipedia.org/wiki/Liskov_substitution_principle
- https://phoenixnap.com/blog/solid-principles
- https://ezzeddinabdullah.com/post/solid-principles-lsp-py/

"""
