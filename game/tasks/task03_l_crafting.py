"""Task 03: TBD.

The third task will be to apply the "L" of the S.O.L.I.D design principles to ...

> (L) **Liskov-Substitution Principle**
>
> Software entities should be interchangeable.

"""

from ..core.registration import SpriteRegister

"""

An important step in designing reusable code is to find opportunities to write code that
is interchangeable.

# TODO: I think the logic to build items would be a good use case where the class needs to handle the interface for different items that output a new sprite

"""

SOURCE_NAME = "task03_L_TBD"  # FYI: Required for code reload


# FYI: Required for code reload
def load_sprites(sprite_register: SpriteRegister) -> None:
    """Create the special 'player sprite' who can be moved with WASD or the arrow keys."""
