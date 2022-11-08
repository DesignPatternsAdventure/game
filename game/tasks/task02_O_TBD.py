"""Task 02: TBD.

The second task will be to apply the "O" of the S.O.L.I.D design principles to ...

> (O) **Open-Close Principle**
>
> Open for extension, not modification.

"""

from ..core.registration import SpriteRegister

"""

Extending is much easier to maintain that modification. Below is an example:

# TODO: I think the Inventory could be a good example where we provide a naive implementation that has all of the logic implemented together, but then we can demo how one aspect could be split, then leave it up to the user to make the rest of the refactoring

"""

SOURCE_NAME = 'task02_O_TBD'  # FYI: Required for code reload


def load_sprites(sprite_register: SpriteRegister) -> None:  # FYI: Required for code reload
    """Create the special 'player sprite' who can be moved with WASD or the arrow keys."""
