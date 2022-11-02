import random

from pydantic import BaseModel, Field

class State(BaseModel):

    x_pos: int = Field(default_factory=lambda: random.randrange(50, 450))
    y_pos: int = Field(default_factory=lambda: random.randrange(50, 450))
    sprite_resource: str = ":resources:images/animated_characters/male_person/malePerson_idle.png"
