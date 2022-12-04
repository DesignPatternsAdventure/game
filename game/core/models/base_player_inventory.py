"""Base Player Inventory, which is extended by the user."""

from collections import defaultdict
from contextlib import suppress
from typing import runtime_checkable

from arcade.sprite import Sprite
from beartype import beartype
from beartype.typing import Protocol
from pydantic import BaseModel, Field

from ..constants import MAX_INVENTORY_SIZE


@runtime_checkable
class BaseItemInterface(Protocol):
    """Interface for items that can be stored in an inventory."""

    name: str
    sprite: Sprite


@runtime_checkable
class PlayerInventoryInterface(Protocol):

    equipped_item: BaseItemInterface | None
    last_equipped_item: BaseItemInterface | None
    inventory: dict[str, BaseItemInterface]

    def get_item_one_index(self, item_name: str) -> int | None:
        ...

    def get_ordered_sprites(self) -> list[Sprite]:
        ...

    def store_equipped_item(self) -> None:
        ...

    def equip_item(self, item_name: str) -> Sprite:
        ...

    # FYI: Implemented by the player in Task 3
    def store_item(self, sprite: Sprite) -> int | None:
        ...


class BasePlayerInventory(BaseModel):
    """Manage the player's inventory."""

    equipped_item: BaseItemInterface | None = None
    """The currently equipped item."""

    last_equipped_item: BaseItemInterface | None = None
    """The last equipped item."""

    inventory: dict[str, BaseItemInterface] = Field(default_factory=defaultdict)
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
    def store_equipped_item(self) -> None:
        """Remove the reference to the equipped item."""
        self.last_equipped_item = self.equipped_item
        self.equipped_item = None

    @beartype
    def equip_item(self, item_name: str) -> Sprite:
        """Equip an item (if present) by name."""
        self.equipped_item = self.inventory[item_name]
        return self.equipped_item.sprite

    @beartype
    def unequip_item(self) -> None:
        """Unequip current item."""
        self.equipped_item = None

    @beartype
    def discard_item(self, item_name: str) -> BaseItemInterface | None:
        """Discard a single item by name."""
        if item := self.inventory[item_name]:
            if (count := item.sprite.properties["count"] - 1) > 0:
                self.inventory[item_name].sprite.properties["count"] = count
            else:
                del self.inventory[item_name]
            return item
        return None
