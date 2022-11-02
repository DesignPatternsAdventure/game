"""Example character module that is separate of the main game."""

import random
from pathlib import Path
from typing import Literal

from loguru import logger
import arcade
from beartype import beartype
from pydantic import BaseModel, Field

from .registration import SpriteRegister

_resources = [
    ':resources:images/animated_characters/female_person/femalePerson_idle.png',
    ':resources:images/animated_characters/male_person/malePerson_idle.png',
]


class State(BaseModel):  # pylint: disable=too-few-public-methods

    # PLANNED: Consider extending: https://api.arcade.academy/en/stable/api/sprites.html#arcade.Sprite

    sprite_resource: str = Field(default_factory=lambda: random.choice(_resources))
    center_x: int = Field(default_factory=lambda: random.randrange(50, 450))
    center_y: int = Field(default_factory=lambda: random.randrange(50, 450))
    hit_box_algorithm: Literal['None', 'Simple', 'Detailed'] = 'None'
    scale: float = 1.0


class CharacterSprite(arcade.Sprite):  # pylint: disable=too-few-public-methods

    @beartype
    def __init__(self, state: State) -> None:
        super().__init__(state.sprite_resource, state.scale)
        self.state = state
        for attr in ('center_x', 'center_y'):
            setattr(self, attr, getattr(state, attr))

def load_sprites(sprite_register: SpriteRegister) -> None:
    """Common entry point for modules that register a graphical element."""
    state = State()
    logger.debug(state)
    player_sprite = CharacterSprite(state)
    # TODO: Is there a way to automatically resolve 'Path(__file__)'?
    sprite_register.register_sprite(player_sprite, Path(__file__))
