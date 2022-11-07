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
from enum import Enum

import arcade

from ..core.constants import SPRITE_SIZE
from ..core.registration import Register, SpriteRegister

SOURCE_NAME = 'task01_player'  # FYI: Required for code reload

Direction = Enum('Direction', 'DOWN LEFT RIGHT UP')

SPRITE_INFO = {
    Direction.DOWN: [0, 1, 2],
    Direction.LEFT: [3, 4, 5],
    Direction.RIGHT: [6, 7, 8],
    Direction.UP: [9, 10, 11],
}


class PlayerSprite(arcade.Sprite):
    """Main Player Character."""

    def __init__(self, sheet_name):
        super().__init__()
        self.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width=SPRITE_SIZE,
            sprite_height=SPRITE_SIZE,
            columns=3,
            count=12,
        )
        self.should_update = 0
        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]
        self.inventory = []
        self.direction = Direction.LEFT

    def on_update(self, delta_time):
        if not self.change_x and not self.change_y:
            return

        if self.should_update <= 3:
            self.should_update += 1
        else:
            self.should_update = 0
            self.cur_texture_index += 1

        slope = self.change_y / (self.change_x + 0.0001)
        if abs(slope) < 0.8:
            if self.change_x > 0:
                self.direction = Direction.RIGHT
            else:
                self.direction = Direction.LEFT
        else:
            if self.change_y > 0:
                self.direction = Direction.UP
            else:
                self.direction = Direction.DOWN

        if self.cur_texture_index not in SPRITE_INFO[self.direction]:
            self.cur_texture_index = SPRITE_INFO[self.direction][0]

        self.texture = self.textures[self.cur_texture_index]


def load_sprites(sprite_register: SpriteRegister) -> None:  # FYI: Required for code reload
    """Single entry point for the main game Player, which can only be created once."""
    resources = [
        *[f':characters:Female/Female {idx + 1:02}-1.png' for idx in range(25)],
        *[f':characters:Male/Male {idx + 1:02}-1.png' for idx in range(18)],
    ]
    resource = random.choice(resources)  # nosec B311
    register = Register(sprite=PlayerSprite(resource), source=SOURCE_NAME)
    sprite_register.register_sprite(register)
