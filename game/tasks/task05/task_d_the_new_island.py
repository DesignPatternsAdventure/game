"""Task 05: The New Island.

The fifth task will be to apply the "D" of the S.O.L.I.D design principles to landing on the new island!

> (D) **Dependency Inversion Principle**
>
> Depend upon abstract interfaces and not concrete implementations

"""

import random
from datetime import datetime

from beartype import beartype

from ...core.constants import STARTING_X, STARTING_Y, NumT
from ...core.game_clock import GameClock
from ...core.models import EntityAttr, SpriteState
from ...core.registration import CameraView, Register, SpriteRegister
from ...core.views import GameSprite

SOURCE_NAME = "task_5"  # FYI: Required for code reload

"""

This task hasn't been Implemented yet!

FYI: We are considering making this a task to implement different algorithms for random
walking vs. follow the player. The task could demonstrate how the implementation
shouldn't be dependent on the algorithm.

Alternatively, for this task, the user could create logic to generate vegetation and
static items that can be picked up or used

"""

# TODO: Different implementations and how they get around? Maybe some flap or walk vs. teleport?

BAT_FAMILIAR = ":assets:characters/Animals/pipo-nekonin020.png"
PANDA_FAMILIAR = ":assets:characters/Animals/pipo-nekonin018.png"


@beartype
def get_random_movement_vector(
    last_change_x: NumT, last_change_y: NumT, movement_speed: NumT
) -> tuple[float, float]:
    """Calculate a semi-random movement vector."""
    choices = [-1, 0, 0, 1, 1]
    # Include the last vector to smooth motion
    x_vector = random.choice(choices + [last_change_x] * 3)
    y_vector = random.choice(choices + [last_change_y] * 3)
    if x_vector and y_vector:
        movement_speed = 0.75 * movement_speed
    return (x_vector * float(movement_speed), y_vector * float(movement_speed))


class FamiliarSprite(GameSprite):

    movement_speed: float = 0.5
    next_update: datetime | None = None
    player_center: tuple[NumT, NumT] = (STARTING_X, STARTING_Y)
    camera_view: CameraView = CameraView(center=player_center)

    # TODO: When this task is complete, `self.follow` shouldn't be necessary
    follow: bool = True

    @classmethod
    @beartype
    def new(cls) -> "FamiliarSprite":
        attr = EntityAttr(step_size=999)
        state = SpriteState(
            sprite_resource=PANDA_FAMILIAR,
            center_x=STARTING_X,
            center_y=STARTING_Y,
        )
        return cls(attr, state)

    @beartype
    def on_update(self, game_clock: GameClock) -> None:
        # For more natural movement, set the Familiar's trajectory to 0 every 0.1s
        if self.next_update is None or game_clock.current_time > self.next_update:
            self.change_x, self.change_y = 0, 0
            self.next_update = game_clock.get_time_in_future(0.1)
        # Wait for the user to find the Familiar
        elif not self.camera_view.in_view((self.center_x, self.center_y)):
            pass
        # Otherwise calculate the trajectory for the Familiar
        elif self.follow:
            offset = 20
            destination = [pos + offset for pos in self.player_center]
            self.change_x = (destination[0] - self.center_x) / 5
            self.change_y = (destination[1] - self.center_y) / 5
        else:
            self.change_x, self.change_y = get_random_movement_vector(
                self.change_x, self.change_y, self.movement_speed
            )

        super().on_update(game_clock)

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
        on_player_sprite_motion=sprite.on_player_sprite_motion,
    )
    sprite_register.register_sprite(register)
