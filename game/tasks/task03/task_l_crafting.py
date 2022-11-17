"""Task 03: Crafting.

> (L) **Liskov-Substitution Principle**
> Software entities should be interchangeable.

"""

from typing import runtime_checkable

from arcade.sprite import Sprite
from beartype import beartype
from beartype.typing import Protocol
from pydantic import BaseModel

from ...core.models.base_player_inventory import BasePlayerInventory


@runtime_checkable
class ItemInterface(Protocol):
    """Interface for items that can be stored in an inventory.

    This is the abstract interface that all of the Items should implement

    """

    name: str
    sprite: Sprite


class BasicItem(BaseModel):
    """Standard item."""

    name: str
    sprite: Sprite

    class Config:
        arbitrary_types_allowed = True


class EquippableItem(BasicItem):
    """Any item that a character can hold."""


class ConsumableItem(BasicItem):
    """Any item that can be used for crafting."""


@beartype
def from_sprite(sprite: Sprite) -> ItemInterface:
    item_name = sprite.properties["name"]
    if "equippable" in sprite.properties:
        return EquippableItem(name=item_name, sprite=sprite)
    return ConsumableItem(name=item_name, sprite=sprite)


class PlayerInventory(BasePlayerInventory):
    """Manage the player's inventory.

    Note: we have partially implemented this class so that you can focus on the most
    relevant aspects. See the source class by opening:
    `game/core/models/base_player_inventory.py`

    For this task, just focus on editing the Models above and use this function as a
    reference for how that code will be used.

    """

    @beartype
    def store_item(self, sprite: Sprite) -> int | None:
        """Place a sprite in the inventory."""
        item = from_sprite(sprite)

        if self.is_inventory_full() and item.name not in self.inventory:
            err = f"Too many items in the inventory. Discard one before adding {item.name}"
            raise RuntimeError(err)

        if item.name in self.inventory:
            self.inventory[item.name].sprite.properties["count"] += 1
        else:
            item.sprite.properties["count"] = item.sprite.properties.get("count", 1)
            self.inventory[item.name] = item

        return self.get_item_one_index(item.name)
