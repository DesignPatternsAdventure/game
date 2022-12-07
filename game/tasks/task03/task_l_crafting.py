"""Task 03: Crafting.

The third task will be to apply the "L" of the S.O.L.I.D design principles to crafting

> (L) **Liskov-Substitution Principle**
>
> Software entities should be interchangeable.

"""
from typing import runtime_checkable

from arcade.sprite import Sprite
from beartype import beartype
from beartype.typing import Protocol
from loguru import logger
from pydantic import BaseModel

from ...core.models.base_player_inventory import BasePlayerInventory

"""
-----------------------------------------------------------------------------------------
Goal: Create new classes that provide the same interface and can thus be interchangeable,
but internally encapsulate different logic for how the item is used.
-----------------------------------------------------------------------------------------
"""

@runtime_checkable
class ItemInterface(Protocol):
    """Interface for items that can be stored in an inventory.

    This is the abstract interface that all of the Items should implement

    """

    name: str
    sprite: Sprite


class EquippableItem(BaseModel):
    """Standard item."""

    name: str
    sprite: Sprite

    class Config:
        arbitrary_types_allowed = True


class PlayerInventory(BasePlayerInventory):
    """Manage the player's inventory.

    Note: we have partially implemented this class so that you can focus on the most
    relevant aspects. See the source class by opening:
    `game/core/models/base_player_inventory.py`

    """

    @beartype
    def store_item(self, sprite: Sprite) -> int | None:
        """Place a sprite in the inventory.

        Note: this is called when walking over an item or on reload

        """
        logger.debug(f"For Task 3, storing sprite with properties: {sprite.properties}")
        item_name = sprite.properties["name"]
        if "equippable" not in sprite.properties:
            raise NotImplementedError(  # FIXME: The message box doesn't fit this text
                f"{item_name} is not an equippable item and must be represented by a new"
                " ConsumableItem class. Edit the code in 'task03/task_l_crafting.py' to fix."
            )
        """
        Currently only a single ItemInterface and EquippableItem are provided as templates
        to show how the Python libraries can be used, but you'll need to extend them
        """
        item = EquippableItem(name=item_name, sprite=sprite)

        if self.is_inventory_full() and item.name not in self.inventory:
            err = f"Too many items in the inventory. Discard one before adding {item.name}"
            raise RuntimeError(err)

        if item.name in self.inventory:
            self.inventory[item.name].sprite.properties["count"] += 1
        else:
            item.sprite.properties["count"] = item.sprite.properties.get("count", 1)
            self.inventory[item.name] = item

        return self.get_item_one_index(item.name)
