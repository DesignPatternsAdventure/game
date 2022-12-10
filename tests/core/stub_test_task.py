"""Stub Task used for testing."""

from game.core.models import EntityAttr, SpriteState
from game.core.registration import Register, SpriteRegister
from game.core.views import GameSprite

SOURCE_NAME = "stub_test_task"  # FYI: Required for code reload


# FYI: Required for code reload
def load_sprites(sprite_register: SpriteRegister) -> None:
    """Common entry point for modules that register a graphical element."""
    resource = (
        ":resources:images/animated_characters/female_person/femalePerson_idle.png"
    )
    attr = EntityAttr()
    state = SpriteState(
        state_name="_", sprite_resource=resource, center_x=10, center_y=10
    )
    register = Register(
        sprite=GameSprite(attr, state),
        source=SOURCE_NAME,
        on_mouse_motion=(lambda _x, _y, _dx, _dy: None),
        on_update=(lambda _x: None),
    )
    sprite_register.register_sprite(register)
