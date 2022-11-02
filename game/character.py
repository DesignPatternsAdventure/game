import random

import arcade
from beartype import beartype
from pydantic import BaseModel, Field


class State(BaseModel):

    center_x: int = Field(default_factory=lambda: random.randrange(50, 450))
    center_y: int = Field(default_factory=lambda: random.randrange(50, 450))
    sprite_resource: str = ":resources:images/animated_characters/male_person/malePerson_idle.png"
    scale: float = 1.0


class CharacterSprite(arcade.Sprite):

    @beartype
    def __init__(self, state: State) -> None:
        super().__init__(state.sprite_resource, state.scale)
        self.state = state
        for attr in ('center_x', 'center_y'):
            setattr(self, attr, getattr(state, attr))
