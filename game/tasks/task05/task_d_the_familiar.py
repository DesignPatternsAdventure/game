"""Task 05: The New Island.

The fifth task will be to apply the "D" of the S.O.L.I.D design principles to meeting your familiar!

> (D) **Dependency Inversion Principle**
>
> Depend upon abstract interfaces and not concrete implementations

"""

import itertools
import random
from collections.abc import Iterable
from datetime import datetime
from enum import Enum

import arcade.key
from beartype import beartype
from loguru import logger

from ...core.constants import (
    HORIZONTAL_MARGIN,
    STARTING_X,
    STARTING_Y,
    TREASURE_CHEST_X,
    TREASURE_CHEST_Y,
    VERTICAL_MARGIN,
    NumT,
)
from ...core.game_clock import GameClock
from ...core.models import EntityAttr, SpriteState
from ...core.registration import CameraView, Register, SpriteRegister
from ...core.views import GameSprite

SOURCE_NAME = "task_5"  # FYI: Required for code reload

"""
-----------------------------------------------------------------------------------------
Goal: Refactor the FamiliarSprite class so that the class is not dependent on the
implementation of sprite motion. When done, the 'self.follow' and 'self.find_chest'
attributes can be removed and the movement logic should be managed externally to
the class.
-----------------------------------------------------------------------------------------
"""

# Here are a few recommended assets if you want to personalize your FamiliarSprite!
BAT_FAMILIAR = ":assets:characters/Animals/pipo-nekonin020.png"  # < Default
CAT_FAMILIAR = ":assets:characters/Animals/Cat 01-1.png"
DOG_FAMILIAR = ":assets:characters/Animals/Dog 01-3.png"
GHOST_FAMILIAR = ":assets:characters/Monsters/Ghost-01.png"
PANDA_FAMILIAR = ":assets:characters/Animals/pipo-nekonin018.png"
WRAITH_FAMILIAR = ":assets:characters/Monsters/Wraith-02.png"


class SpriteMotion(Enum):

    FOLLOW = "follow"
    SEEK_TREASURE = "seek_treasure"
    RANDOM = "random"


@beartype
def get_random_movement_vector(movement_speed: NumT) -> tuple[float, float]:
    """Calculate a semi-random movement vector."""
    choices = [-1, 0, 0, 1, 1]
    x_vector = random.choice(choices)
    y_vector = random.choice(choices)
    if x_vector and y_vector:
        movement_speed = 0.75 * movement_speed
    return (x_vector * float(movement_speed), y_vector * float(movement_speed))


@beartype
def get_vector_to_object(
    center: tuple[NumT, NumT],
    destination: tuple[NumT, NumT],
    max_step: int = 10,
) -> tuple[NumT, NumT]:
    """Calculate a reasonable step-size vector for specified destination."""
    vector = [0.0, 0.0]
    for idx in range(2):
        value = (destination[idx] - center[idx]) / 5
        sign = -1 if value < 0 else 1
        vector[idx] = min(abs(value), max_step) * sign
    return tuple(vector)


class FamiliarSprite(GameSprite):

    movement_speed: NumT = 0.5
    next_update: datetime | None = None
    player_center: tuple[NumT, NumT] = (STARTING_X, STARTING_Y)
    camera_view: CameraView = CameraView(center=player_center)

    # TODO: When this task is complete, `self.follow` and `self.find_chest` shouldn't be necessary
    motion_algorithms: Iterable[SpriteMotion] = itertools.cycle(
        [SpriteMotion.FOLLOW, SpriteMotion.SEEK_TREASURE, SpriteMotion.RANDOM]
    )
    active_algorithm: SpriteMotion = SpriteMotion.FOLLOW

    @classmethod
    @beartype
    def new(cls) -> "FamiliarSprite":
        attr = EntityAttr()
        state = SpriteState(
            state_name="The_FamiliarSprite",
            sprite_resource=BAT_FAMILIAR,  # FYI: Feel free to select a different asset!
            center_x=STARTING_X - int(HORIZONTAL_MARGIN * 1.5),
            center_y=STARTING_Y + int(VERTICAL_MARGIN * 1.4),
        )
        return cls(attr, state)

    @beartype
    def on_update(self, game_clock: GameClock) -> None:
        center = (self.center_x, self.center_y)
        in_view = self.camera_view.in_view(center)
        # Wait for the user to find the Familiar after reload
        if not in_view:
            self.change_x, self.change_y = 0, 0
        # For more natural movement, set the Familiar's trajectory to 0 every 0.1s
        elif self.next_update is None or game_clock.current_time > self.next_update:
            self.change_x, self.change_y = 0, 0
            self.next_update = game_clock.get_time_in_future(0.1)
        # Otherwise calculate the trajectory for the Familiar
        #
        # TODO: These three conditions are what you will be refactoring
        #   How can this logic be extracted and specified outside of this
        #   class without the need for attributes, like 'self.follow'?
        #
        elif self.active_algorithm == SpriteMotion.FOLLOW:
            offset = 20
            destination = tuple(pos + offset for pos in self.player_center)
            self.change_x, self.change_y = get_vector_to_object(center, destination)
        elif self.active_algorithm == SpriteMotion.SEEK_TREASURE:
            destination = (TREASURE_CHEST_X, TREASURE_CHEST_Y)
            self.change_x, self.change_y = get_vector_to_object(center, destination)
            # Check that the Familiar would still be visible
            new_x = self.center_x + self.change_x
            new_y = self.center_y + self.change_y
            if not self.camera_view.in_view((new_x, new_y)):
                self.change_x, self.change_y = 0, 0
        else:
            self.change_x, self.change_y = get_random_movement_vector(
                self.movement_speed
            )

        super().on_update(game_clock)

    @beartype
    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.F:
            self.active_algorithm = next(self.motion_algorithms)
            logger.warning(f"Familiar is now using '{self.active_algorithm}' motion")
            # # =====================================================================
            # # TODO: Instead of toggling these flags, this key press could call some
            # #   method on the injected dependency. Remove this error
            # #   FIXME: better clarification too?
            # #   Extract classes for each? Iterttols.cycle?
            # #   Best skill - refactor for enum
            # raise NotImplementedError(
            #     "Your familiar needs your help!\
            #     \nEdit the code in 'task05/task_d_the_familiar.py' to help"
            # )

    @beartype
    def on_player_sprite_motion(self, player_center: tuple[NumT, NumT]) -> None:
        """Store the player sprite position on motion."""
        self.player_center = player_center
        self.camera_view.center = player_center


# FYI: Required for code reload
def load_sprites(sprite_register: SpriteRegister) -> None:
    """Common entry point for modules that register a graphical element."""
    sprite = FamiliarSprite.new()
    register = Register(
        sprite=sprite,
        source=SOURCE_NAME,
        on_update=sprite.on_update,
        on_key_press=sprite.on_key_press,
        on_player_sprite_motion=sprite.on_player_sprite_motion,
    )
    sprite_register.register_sprite(register)
