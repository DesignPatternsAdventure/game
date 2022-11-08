"""Task 05: TBD.

The fifth task will be to apply the "D" of the S.O.L.I.D design principles to ...

> (D) **Dependency Inversion Principle**
>
> Depend upon abstract interfaces and not concrete implementations

"""

from ..core.registration import SpriteRegister

"""

# TODO: This last step should be a sort-of-victory lap where the user could add a random walking sprite or a follow the character sprite. Then the task would demonstrate how the implementation shouldn't be dependent on the algorithm.

"""

SOURCE_NAME = 'task05_D_TBD'  # FYI: Required for code reload


def load_sprites(sprite_register: SpriteRegister) -> None:  # FYI: Required for code reload
    """Create the special 'player sprite' who can be moved with WASD or the arrow keys."""
