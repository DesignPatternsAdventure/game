"""Task 03: Crafting.

The third task will be to apply the "L" of the S.O.L.I.D design principles to crafting

> (L) **Liskov-Substitution Principle**
>
> Software entities should be interchangeable.

"""

"""

An important step in designing reusable code is to find opportunities to write code
that is interchangeable. Liskov substitution principle aims to ensure that the child
class can assume the place of its parent class without causing any errors.

Consider this example: we have three classes: ItemInterface, ItemTypeA, and ItemTypeB.
ItemTypeA and ItemTypeB classes inherit from the ItemInterface class.
"""

from typing import runtime_checkable

from beartype.typing import Protocol
from pydantic import BaseModel


@runtime_checkable
class ItemInterface(Protocol):
    """Interface for items that can be stored in an inventory."""

    name: str
    count: int


class ItemTypeA(BaseModel):
    """Standard item."""

    name: str
    number: int

    def useItemTypeA():
        ...


class ItemTypeB(BaseModel):
    """Standard item."""

    id: str
    count: int

    def useItemTypeB():
        ...


"""
The example above violates the Liskov-Substitution Principle because ItemTypeA uses `number`
instead of `count`, and ItemTypeB uses `id` instead of `name`.

To conform with the principle, we simply need to rename the class variables for ItemTypeA
and ItemTypeB!
"""


@runtime_checkable
class ItemInterface(Protocol):
    """Interface for items that can be stored in an inventory."""

    name: str
    count: int


class ItemTypeA(BaseModel):
    """Standard item."""

    name: str
    count: int

    def useItemTypeA():
        ...


class ItemTypeB(BaseModel):
    """Standard item."""

    name: str
    count: int

    def useItemTypeB():
        ...


"""

If you would like to learn more about the Liskov-Substitution Principle, you can take a look at:

- https://en.wikipedia.org/wiki/Liskov_substitution_principle
- https://phoenixnap.com/blog/solid-principles
- https://ezzeddinabdullah.com/post/solid-principles-lsp-py/

"""
