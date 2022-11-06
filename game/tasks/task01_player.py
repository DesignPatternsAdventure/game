"""Task 01: Player.

Welcome to the <game>! Your first task will be to personalize your character.

*Learning Objective*: Learn the "S" of the S.O.L.I.D design principles.

> (S) **Single Responsibility**
>
> A class, function, method or module should have a single responsibility.
> If it has many responsibilities, it increases the possibility of bugs!

TODO: Provide SRP task instructions: "Our character module contains all character-specific logic...""

"""

import random

from beartype import beartype
from loguru import logger

from ..core.constants import STARTING_X, STARTING_Y
from ..core.models import EntityAttr, SpriteState
from ..core.registration import Register, SpriteRegister
from ..core.view_strategies.movement import cardinal_key_move
from ..core.views import GameSprite

SOURCE_NAME = 'task01_player'  # FYI: Required for code reload


class PlayerSprite(GameSprite):
    """Main Player Character."""

    @beartype
    def move(self, d_x: int | float, d_y: int | float, angle: float | None = None) -> None:
        # FIXME: Replace with logic for orienting a top-down sprite
        super().move(d_x, d_y)
        degrees = 0
        if d_x > 0:
            degrees = 270
        elif d_x < 0:
            degrees = 90

        if d_y > 0:
            degrees = 0
        elif d_y < 0:
            degrees = 180

        # Move the sprite along a circle centered on the point by degrees
        self.state.angle = degrees
        self.sync_with_state()


def load_sprites(sprite_register: SpriteRegister) -> None:  # FYI: Required for code reload
    """Single entry point for the main game Player, which can only be created once."""
    # TODO: Make the task here to change the character resource?
    resources = [
        *[f':characters:Female/Female {idx + 1:02}-1.png' for idx in range(25)],
        *[f':characters:Male/Male {idx + 1:02}-1.png' for idx in range(18)],
    ]
    resource = random.choice(resources)  # nosec B311

    attr = EntityAttr(step_size=5)  # FIXME: Does this work with tiles?
    state = SpriteState(sprite_resource=resource, center_x=STARTING_X, center_y=STARTING_Y)
    logger.warning(f'Loading "{SOURCE_NAME}" with State of {state}')
    register = Register(
        sprite=PlayerSprite(attr, state),
        source=SOURCE_NAME,
        on_key_press=cardinal_key_move,
        on_key_hold=cardinal_key_move,
    )
    sprite_register.register_sprite(register)
