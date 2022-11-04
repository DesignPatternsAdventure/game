"""Example character module that is separate of the main game."""

import random
from pathlib import Path
from typing import Literal

import arcade
import arcade.key
from beartype import beartype
from pydantic import BaseModel, Field

from .registration import Register, SpriteRegister

_resources = [
    ':resources:images/animated_characters/female_person/femalePerson_idle.png',
    ':resources:images/animated_characters/male_person/malePerson_idle.png',
]


# TODO: Move this to a shared location
class State(BaseModel):

    # PLANNED: Consider extending: https://api.arcade.academy/en/stable/api/sprites.html#arcade.Sprite

    sprite_resource: str = Field(default_factory=lambda: random.choice(_resources))  # nosec B311
    angle: float = 0
    center_x: int = Field(default_factory=lambda: random.randrange(50, 450))  # nosec B311
    center_y: int = Field(default_factory=lambda: random.randrange(50, 450))  # nosec B311
    hit_box_algorithm: Literal['None', 'Simple', 'Detailed'] = 'None'
    scale: float = 1.0


class GameSprite(arcade.Sprite):
    """Generic Base Class for Sprites."""

    @beartype
    def __init__(self, state: State) -> None:
        super().__init__(state.sprite_resource, state.scale)
        self.state = state
        self.sync_with_state()

    @beartype
    def sync_with_state(self) -> None:
        """Sync the Sprite with the state."""
        for attr in ('center_x', 'center_y', 'angle'):
            setattr(self, attr, getattr(self.state, attr))

        # Update the rotation if necessary
        point = [self.center_x, self.center_y]
        self.position = arcade.rotate_point(self.center_x, self.center_y, point[0], point[1], self.angle)
        print(self.state)  # FIXME: Reloading detaches this logger from the main one...

    @beartype
    def move(self, d_x: int | float, d_y: int | float) -> None:
        """Update the sprite position and state."""
        self.state.center_x = int(self.state.center_x + d_x)
        self.state.center_y = int(self.state.center_y + d_y)
        self.sync_with_state()


class CharacterSprite(GameSprite):

    @beartype
    def move(self, d_x: int | float, d_y: int | float) -> None:
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

        print(self.angle, degrees, d_x, d_y)  # FIXME: Reloading detaches this logger from the main one...
        # Move the sprite along a circle centered on the point by degrees
        self.state.angle = degrees  # FIXME: Is this relative?
        self.sync_with_state()


# TODO: Move this to a shared location
@beartype
def move_sprite(sprite: GameSprite, key: int, modifiers: int) -> None:
    """Handle moving a sprite based on key press."""
    d_x, d_y = 0, 0
    movement_speed = 5
    match key:
        case arcade.key.RIGHT:
            d_x = movement_speed
        case arcade.key.D:
            d_x = movement_speed
        case arcade.key.LEFT:
            d_x = -1 * movement_speed
        case arcade.key.A:
            d_x = -1 * movement_speed
        case arcade.key.UP:
            d_y = movement_speed
        case arcade.key.W:
            d_y = movement_speed
        case arcade.key.DOWN:
            d_y = -1 * movement_speed
        case arcade.key.S:
            d_y = -1 * movement_speed
        case _:
            return

    sprite.move(d_x, d_y)


def load_sprites(sprite_register: SpriteRegister) -> None:
    """Common entry point for modules that register a graphical element."""
    state = State()
    print(state)  # FIXME: Reloading detaches this logger from the main one...
    # TODO: Is there a way to automatically resolve 'Path(__file__)'?
    register = Register(
        sprite=CharacterSprite(state),
        source=Path(__file__),
        on_key_press=move_sprite,
        on_key_hold=move_sprite,
    )
    sprite_register.register_sprite(register)
