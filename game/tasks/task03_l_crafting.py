"""Task 03: Crafting.

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
from pydantic import BaseModel, Field

from ..core.constants import MAX_INVENTORY_SIZE

# ==============================    Part 1 (Learn)    ==============================
"""

An important step in designing reusable code is to find opportunities to write code that
is interchangeable.


FYI: We don't have a lesson yet for this task, but we will add one shortly!

"""


# ==============================    Part 2 (Edit)    ==============================


@runtime_checkable
class ItemInterface(Protocol):
    """Interface for items that can be stored in an inventory."""

    sprite: Sprite

    # FIXME: Possible task is to calculate orientation of item based on character position?
    # TODO: Extend the interface in a way that will allow these functions to be interchangeable


class BasicItem(BaseModel):
    """Standard item."""

    name: str
    sprite: Sprite

    class Config:
        arbitrary_types_allowed = True


class EquippableItem(BasicItem):
    """Any item that a character can hold."""


class ConsumableItem(EquippableItem):
    """Any item that can be used for crafting."""


class PlayerInventory(BaseModel):
    """Manage the player's inventory."""

    equipped_item: ItemInterface | None = None
    """The currently equipped item."""

    inventory: dict[str, ItemInterface] = Field(default_factory=defaultdict)
    """The user's current inventory store by unique `item_name`."""

    class Config:
        arbitrary_types_allowed = True

    @beartype
    def is_inventory_full(self) -> bool:
        """If True, no new items can be added to the inventory."""
        return len(self.inventory) > MAX_INVENTORY_SIZE

    @beartype
    def get_item_one_index(self, item_name: str) -> int | None:
        """Retrieve the one-indexed location by item name."""
        with suppress(ValueError):
            return [*self.inventory].index(item_name) + 1
        return None

    @beartype
    def get_ordered_sprites(self) -> list[Sprite]:
        """Returns the list of sprites for GUI operations."""
        return [item.sprite for item in self.inventory.values()]

    @beartype
    def store_item(self, sprite: Sprite) -> int | None:
        """Place a sprite in the inventory."""
        item_name = sprite.properties["name"]

        if self.is_inventory_full() and item_name not in self.inventory:
            err = f"Too many items in the inventory. Discard one before adding {item_name}"
            raise RuntimeError(err)

        if "equippable" in sprite.properties:
            item = EquippableItem(name=item_name, sprite=sprite)
        else:
            item = ConsumableItem(name=item_name, sprite=sprite)

        if item_name in self.inventory:
            self.inventory[item_name].sprite.properties["count"] += 1
        else:
            item.sprite.properties["count"] = 1
            self.inventory[item_name] = item

        return self.get_item_one_index(item_name)

    @beartype
    def store_equipped_item(self) -> None:
        """Remove the reference to the equipped item."""
        self.equipped_item = None

    @beartype
    def equip_item(self, item_name: str) -> bool:
        """Equip an item (if present) by name."""
        self.store_equipped_item()
        with suppress(KeyError):
            self.equipped_item = self.inventory[item_name]
            return True
        return False

    @beartype
    def discard_item(self, item_name: str) -> ItemInterface | None:
        """Discard a single item by name."""
        if item := self.inventory[item_name]:
            if (count := item.sprite.properties["count"] - 1) > 0:
                self.inventory[item_name].sprite.properties["count"] = count
            else:
                del self.inventory[item_name]
            return item
        return None


"""

If you would like to learn more about the Liskov-Substitution Principle, you can take a look at:

- https://en.wikipedia.org/wiki/Liskov_substitution_principle
- https://phoenixnap.com/blog/solid-principles
- https://ezzeddinabdullah.com/post/solid-principles-lsp-py/

"""
