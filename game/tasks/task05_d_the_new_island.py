"""Task 05: TBD.

The fifth task will be to apply the "D" of the S.O.L.I.D design principles to ...

> (D) **Dependency Inversion Principle**
>
> Depend upon abstract interfaces and not concrete implementations

"""

from ..core.registration import SpriteRegister

# ==============================      Part 1      ==============================

# TODO: This last step should be a sort-of-victory lap where the user could add a random walking sprite or a follow the character sprite. Then the task would demonstrate how the implementation shouldn't be dependent on the algorithm.

# ==============================      Part 2      ==============================

SOURCE_NAME = "task05_d_the_new_island"  # FYI: Required for code reload


# FYI: Required for code reload
def load_sprites(sprite_register: SpriteRegister) -> None:
    """Create the special 'player sprite' who can be moved with WASD or the arrow keys."""


"""

If you would like to learn more about the Dependency Inversion Principle, you can take a look at:

- https://en.wikipedia.org/wiki/Dependency_inversion_principle
- https://phoenixnap.com/blog/solid-principles
- https://ezzeddinabdullah.com/post/solid-principles-dip-py-copy/

"""
