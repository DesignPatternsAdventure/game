"""Task 03: TBD.

The third task will be to apply the "L" of the S.O.L.I.D design principles to ...

> (L) **Liskov-Substitution Principle**
>
> Software entities should be interchangeable.

"""

from ..core.registration import SpriteRegister

# ==============================      Part 1      ==============================
"""

An important step in designing reusable code is to find opportunities to write code that
is interchangeable.

"""


# TODO: I think the Inventory could be a good example where we provide a naive implementation that has all of the logic implemented together, but then we can demo how one aspect could be split, then leave it up to the user to make the rest of the refactoring


# ==============================      Part 2      ==============================

SOURCE_NAME = "task03_l_crafting"  # FYI: Required for code reload


# FYI: Required for code reload
def load_sprites(sprite_register: SpriteRegister) -> None:
    """Create the special 'player sprite' who can be moved with WASD or the arrow keys."""


"""

If you would like to learn more about the Liskov-Substitution Principle, you can take a look at:

- https://en.wikipedia.org/wiki/Liskov_substitution_principle
- https://phoenixnap.com/blog/solid-principles
- https://ezzeddinabdullah.com/post/solid-principles-lsp-py/

"""
