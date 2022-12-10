"""Task 03: Crafting.

The third task will be to apply the "L" of the S.O.L.I.D design principles to crafting

> (L) **Liskov-Substitution Principle**
>
> Software entities should be interchangeable.

```sh
# FYI: if you want to test this code, run with:
python -m game.tasks.task03.lsp_introduction
```

"""

from typing import Any, runtime_checkable

from beartype import beartype
from beartype.typing import Protocol
from pydantic import BaseModel

"""
As a quick aside, 'pydantic.BaseModel' helps us write less code by replacing:

```py
class Item(BaseModel):

    def __init__(self, name: str, count: int = 0) -> None:
        self.name = name
        self.count = count
```

With:

```py
class Item(BaseModel):
    name: str
    count: int = 0
```

And with or without BaseModel, the class can be called in the same ways:

```py
item = Item(name="name_0")
print(item.count)
item = Item(name="name_1", count=1)
print(item.count)
```

Along with code that is easier to write, pydantic adds additional logic to enforce
the specified type like this:

```sh
> Item(name="will fail", count="many")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "pydantic/main.py", line 342, in pydantic.main.BaseModel.__init__
    raise validation_error
pydantic.error_wrappers.ValidationError: 1 validation error for Item
count
  value is not a valid integer (type=type_error.integer)
```

Back to the introduction!

"""
"""

The LSP is based on a 1994 paper, "A behavioral notion of subtyping," by Barbara H.
Liskov and Jeannette M. Wing (https://dl.acm.org/doi/abs/10.1145/197320.197383).
One of the core concepts of the paper was:

"If S is a subtype of T, then objects of type T in a program may be replaced with
objects of type S without altering any of the desirable properties of that program."

This academic description essentially means that for classes to be interchangeable,
the class needs to preserve both the interface and behavior.

Below are a few examples of items that all have different interfaces and behavior
which means that the code that uses them needs to be fairly complex

"""


class Helmet(BaseModel):

    name: str
    durability: int = 100

    def wear(self) -> None:
        print(f"Wearing the '{self.name}' helmet")
        self.durability -= 10


class Map(BaseModel):

    name: str

    def view(self) -> None:
        print(f"Viewing the '{self.name}' map")


class Bread(BaseModel):

    nourishment: int = 10

    def eat(self) -> None:
        print(f"Eating bread to recover {self.nourishment} for hunger")


def use(item: Any) -> None:
    if isinstance(item, Helmet):
        item.wear()
        if item.durability <= 0:
            print(f"The {repr(item)} was consumed and would be removed from the inventory!")
    elif isinstance(item, Map):
        item.view()
    elif isinstance(item, Bread):
        item.eat()
        # Here would be logic to discard the item from the inventory
        print(f"The {repr(item)} was consumed and would be removed from the inventory!")


if __name__ == "__main__":
    print("Part 1: Initial Implementation")
    helmet = Helmet(name="Basic Helmet", durability=10)
    map_item = Map(name="Land Map")
    bread = Bread(nourishment=100)
    for item in (helmet, map_item, bread):
        use(item)
    print("\n")

"""

One way to refactor for the LSP is to reconsider the item behavior as a core set of
abstract methods.

Here, we are using an interface for type annotations and not as a base class (i.e.
don't inherit from ItemInterface directly)

"""


@runtime_checkable
class ItemInterface(Protocol):
    def use(self) -> bool:
        ...


"""

Now these Items can be refactored to comply with the ItemInterface's 'use()' method where
the method accepts no arguments and must return True if the item has been consumed.

You'll notice that the below classes have different attributes and initialization,
which is OK because the interface only specifies the 'use()' method.

"""


class HelmetItem(BaseModel):

    name: str
    durability: int = 100

    def use(self) -> bool:
        print(f"Wearing the '{self.name}' helmet")
        self.durability -= 10
        return self.durability <= 0


class MapItem(BaseModel):

    name: str

    def use(self) -> bool:
        print(f"Viewing the '{self.name}' map")
        return False


class BreadItem(BaseModel):

    nourishment: int = 10

    def use(self) -> bool:
        print(f"Eating bread to recover {self.nourishment} for hunger")
        return True


@beartype
def use_item(item: ItemInterface) -> None:
    if item.use():
        # If `use()` returns True, then the logic to discard the item can be called here
        print(f"The {repr(item)} was consumed and would be removed from the inventory!")


if __name__ == "__main__":
    print("Part 2: Refactored Implementation")
    helmet_item = HelmetItem(name="Basic Helmet", durability=10)
    map_item = MapItem(name="Land Map")
    bread_item = BreadItem(nourishment=100)
    for item in (helmet_item, map_item, bread_item):
        use_item(item)
    print("\n")

"""

Now, all of the classes conform to the ItemInterface and can be used in the same way
and adding new Items becomes far easier!

"""

"""

If you would like to learn more about the Liskov-Substitution Principle, you can take a look at:

- https://en.wikipedia.org/wiki/Liskov_substitution_principle
- https://phoenixnap.com/blog/solid-principles
- https://ezzeddinabdullah.com/post/solid-principles-lsp-py/

"""
