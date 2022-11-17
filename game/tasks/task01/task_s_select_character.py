"""Task 01: Select your player character.

Welcome to Design Pattern Island! Your first task will be to personalize your character
by applying the "S" of the S.O.L.I.D design principles.

> (S) **Single Responsibility**
>
> A class, function, method or module should have a single responsibility.
> If it has many responsibilities, it increases the possibility of bugs!

"""

import random

from loguru import logger

from ...core.registration import Register, SpriteRegister
from ...core.views.rpg_sprites import PlayerSprite
from ..task03.task_l_crafting import PlayerInventory

"""

Each task can be reloaded when you make code changes with either `Ctrl R` or `CMD R`!

Avoid making any changes to `SOURCE_NAME` or the function signature to `load_sprites`
because those are required for reload, but you can change the content of the
`load_sprites` function. On reload, the game will attempt to identify any errors and
recommended fixes, so you can often fix and reload without quitting!

"""

SOURCE_NAME = "task01_S_player"  # FYI: Required for code reload


class ResourcePicker:
    """Initial challenge."""

    @classmethod
    def pick_resource_path(cls) -> str:
        """Returns the string path to a sprite resource.

        Design Pattern Island is built using the Python arcade library. The library has
        a set of shorthand ways to refer to file paths to make them easier to load.

        All of the initial assets are placed in `game/assets`, which can be referenced
        with `:assets:`, but we provide additional shorthand for `:characters:` which
        evaluates to `game/assets/characters`. For reference, this file is currently in
        the `game/tasks` directory.

        For this first task, return the string `resource` that you want as your primary
        character. Note that for demonstration purposes, the character is chosen randomly
        from the list, but you only need to return a single hardcoded string.

        """
        resources = []
        for idx in range(18):  # There are more than just 18!
            resources.extend(
                [
                    f":characters:Female/Female {idx + 1:02}-1.png",
                    f":characters:Male/Male {idx + 1:02}-1.png",
                    f":characters:Animals/pipo-nekonin{idx + 1:03}.png",
                ]
            )
        resource = random.choice(resources)  # nosec B311
        logger.info(f"Selecting resource: '{resource}'")
        return resource

        # # Example solution:
        # return ':characters:Female/Female 02-3.png'


# FYI: Required for code reload
def load_sprites(sprite_register: SpriteRegister) -> None:
    """Create the special 'player sprite' who can be moved with WASD or the arrow keys."""
    resource = ResourcePicker.pick_resource_path()
    register = Register(
        sprite=PlayerSprite(resource, PlayerInventory()), source=SOURCE_NAME
    )
    sprite_register.register_sprite(register)
