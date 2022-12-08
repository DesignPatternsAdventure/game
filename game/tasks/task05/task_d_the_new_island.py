"""Task 05: The New Island.

The fifth task will be to apply the "D" of the S.O.L.I.D design principles to landing on the new island!

> (D) **Dependency Inversion Principle**
>
> Depend upon abstract interfaces and not concrete implementations

"""

import random
from datetime import datetime

import arcade.key
from beartype import beartype
from loguru import logger

from ...core.constants import (
    HORIZONTAL_MARGIN,
    STARTING_X,
    STARTING_Y,
    TREASURE_CHEST_X,
    TREASURE_CHEST_Y,
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
    follow: bool = True
    find_chest: bool = False

    @classmethod
    @beartype
    def new(cls) -> "FamiliarSprite":
        attr = EntityAttr(step_size=999)
        state = SpriteState(
            sprite_resource=BAT_FAMILIAR,  # FYI: Feel free to select a different asset!
            center_x=STARTING_X - (HORIZONTAL_MARGIN * 2),
            center_y=STARTING_Y,
        )
        return cls(attr, state)

    @beartype
    def on_update(self, game_clock: GameClock) -> None:
        center = (self.center_x, self.center_y)
        # For more natural movement, set the Familiar's trajectory to 0 every 0.1s
        if self.next_update is None or game_clock.current_time > self.next_update:
            self.change_x, self.change_y = 0, 0
            self.next_update = game_clock.get_time_in_future(0.1)
        # Wait for the user to find the Familiar
        elif not self.camera_view.in_view(center):
            self.change_x, self.change_y = 0, 0
        # Otherwise calculate the trajectory for the Familiar
        #
        # TODO: These three conditions are what you will be refactoring
        #   How can this logic be extracted and specified outside of this class?
        #
        elif self.follow:
            offset = 20
            destination = tuple(pos + offset for pos in self.player_center)
            self.change_x, self.change_y = get_vector_to_object(center, destination)
        # Otherwise calculate the trajectory for the Familiar
        elif self.find_chest:
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

        # FIXME: Need a better way to inform the user about this task...
        if self.follow and game_clock.current_time > self.next_update:
            # raise NotImplementedError( # FIXME: Merge PR #38
            logger.error(
                "Your BAT_FAMILIAR can only follow. Complete a task to help it!\
                \nEdit the code in 'task05/task_d_the_new_island.py' to help"
            )

    @beartype
    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.F:
            # TODO: Instead of toggling these flags, this key press could call some
            #   method on the injected dependency
            if self.follow:
                logger.warning("Switching to 'Find Chest' motion!")
                self.follow = False
                self.find_chest = True
            elif self.find_chest:
                logger.warning("Switching to 'Random' motion")
                self.follow = False
                self.find_chest = False
            else:
                logger.warning("Switching to 'Follow' motion")
                self.follow = True
                self.find_chest = False

    @beartype
    def on_player_sprite_motion(self, player_center: tuple[NumT, NumT]) -> None:
        """Store the player sprite position on motion."""
        self.player_center = player_center
        self.camera_view.center = player_center


# FYI: Required for code reload
def load_sprites(sprite_register: SpriteRegister) -> None:
    """Common entry point for modules that register a graphical element."""
    sprite = FamiliarSprite.new()
    # TODO: To complete the game, you'll want your Familiar's help with finding the Treasure Chest
    #   This can be done now with:
    # > sprite.follow = False
    # > sprite.find_chest = True
    # But this code could be improve with the Dependency Inversion Principle
    #   and you could further extend the behavior of your Familiar if you would like.
    #   For example, maybe you would want your familiar to find the Raft.
    register = Register(
        sprite=sprite,
        source=SOURCE_NAME,
        on_update=sprite.on_update,
        on_key_press=sprite.on_key_press,
        on_player_sprite_motion=sprite.on_player_sprite_motion,
    )
    sprite_register.register_sprite(register)
