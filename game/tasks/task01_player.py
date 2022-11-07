"""Task 01: Player.

Welcome to the <game>! Your first task will be to personalize your character.

*Learning Objective*: Learn the "S" of the S.O.L.I.D design principles.

> (S) **Single Responsibility**
>
> A class, function, method or module should have a single responsibility.
> If it has many responsibilities, it increases the possibility of bugs!

TODO: Provide SRP task instructions and task: "Our character module contains all character-specific logic...""

"""

import random

from ..core.registration import Register, SpriteRegister
from ..core.views.rpg_sprites import PlayerSprite

SOURCE_NAME = 'task01_player'  # FYI: Required for code reload


def load_sprites(sprite_register: SpriteRegister) -> None:  # FYI: Required for code reload
    """Single entry point for the main game Player, which can only be created once."""
    resources = [
        *[f':characters:Female/Female {idx + 1:02}-1.png' for idx in range(25)],
        *[f':characters:Male/Male {idx + 1:02}-1.png' for idx in range(18)],
    ]
    resource = random.choice(resources)  # nosec B311
    register = Register(sprite=PlayerSprite(resource), source=SOURCE_NAME)
    sprite_register.register_sprite(register)
