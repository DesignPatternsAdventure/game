"""Task 05: The New Island.

The fifth task will be to apply the "D" of the S.O.L.I.D design principles to landing on the new island!

> (D) **Dependency Inversion Principle**
>
> Depend upon abstract interfaces and not concrete implementations

"""

from ...core.models import EntityAttr, SpriteState
from ...core.registration import Register, SpriteRegister
from ...core.view_strategies.movement import cardinal_key_move
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

# Maybe implementation is how the character is animated? Flapping vs. walking?


class BatFamiliar:  # ":assets:characters/Animals/pipo-nekonin020.png"
    def fly_spiral(self):
        pass


class PandaFamiliar:  # ":assets:characters/Animals/pipo-nekonin018.png"
    def wander(self):
        pass


class Familiar:
    def tbd(self):
        pass


# FYI: Required for code reload
def load_sprites(sprite_register: SpriteRegister) -> None:
    """Common entry point for modules that register a graphical element."""
    resource = (
        ":resources:images/animated_characters/female_person/femalePerson_idle.png"
    )
    attr = EntityAttr(step_size=999)
    state = SpriteState(sprite_resource=resource, center_x=10, center_y=10)
    register = Register(
        sprite=GameSprite(attr, state),
        source=SOURCE_NAME,
        on_key_release=cardinal_key_move,
        on_mouse_motion=(lambda _cls, _x, _y, _dx, _dy: None),
        on_update=(lambda _cls, _x: None),
    )
    sprite_register.register_sprite(register)
