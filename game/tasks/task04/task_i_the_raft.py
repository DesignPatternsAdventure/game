"""Task 04: The Raft.

The fourth task will be to apply the "I" of the S.O.L.I.D design principles to building the raft

> (I) **Interface Segregation Principle**
>
> Clients should not be forced to depend upon interfaces that they do not use

"""
import arcade
from beartype import beartype
from ...core.registration import Register, SpriteRegister
from ...core.views.vehicle_sprite import VehicleSprite, VehicleType
from ...core.constants import RAFT_STARTING_X, RAFT_STARTING_Y

SOURCE_NAME = "task04_I_raft"  # FYI: Required for code reload


class RaftSprite(VehicleSprite):
    def __init__(self, sheet_name: str):
        super().__init__(sheet_name, RAFT_STARTING_X, RAFT_STARTING_Y)
        self.type = VehicleType.RAFT


# FYI: Required for code reload
def load_sprites(sprite_register: SpriteRegister) -> None:
    """Create the special 'raft sprite' who can be moved on the water."""
    register = Register(
        sprite=RaftSprite(":assets:raft.png"),
        source=SOURCE_NAME,
    )
    sprite_register.register_sprite(register)
