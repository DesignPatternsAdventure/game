"""Task 05: The New Island.

The fifth task will be to apply the "D" of the S.O.L.I.D design principles to landing on the new island!

> (D) **Dependency Inversion Principle**
>
> Depend upon abstract interfaces and not concrete implementations

"""

import random
from beartype import beartype

from ...core.constants import STARTING_X, STARTING_Y
from ...core.game_clock import GameClock
from ...core.models import EntityAttr, SpriteState
from ...core.registration import Register, SpriteRegister
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
def get_random_movement_vector(movement_speed: int | float = 1) -> tuple[float, float]:
    """Calculate a random movement vector."""
    choices = [-1, 0, 0, 0, 0, 0, 1]
    x_vector = random.choice(choices)
    y_vector = random.choice(choices)
    if x_vector and y_vector:
        movement_speed = 0.75 * movement_speed
    return (x_vector * float(movement_speed), y_vector * float(movement_speed))


class FamiliarSprite(GameSprite):

    movement_speed: int = 5

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

    # FIXME: Needs the player position...
    @beartype
    def on_update(self, game_clock: GameClock) -> None:
        self.change_x, self.change_y = get_random_movement_vector(self.movement_speed)
        super().on_update(game_clock)


# FYI: Required for code reload
def load_sprites(sprite_register: SpriteRegister) -> None:
    """Common entry point for modules that register a graphical element."""
    sprite = FamiliarSprite.new()
    register = Register(
        sprite=sprite,
        source=SOURCE_NAME,
        on_update=sprite.on_update,
    )
    sprite_register.register_sprite(register)
