"""Task 04: The Raft.

The fourth task will be to apply the "I" of the S.O.L.I.D design principles to building the raft

> (I) **Interface Segregation Principle**
>
> Clients should not be forced to depend upon interfaces or methods that they do not use

"""
from arcade import Sprite
from ...core.registration import Register, SpriteRegister
from ...core.views.vehicle_sprite import VehicleSprite, VehicleType
from ...core.constants import RAFT_STARTING_X, RAFT_STARTING_Y


SOURCE_NAME = "task04_I_raft"  # FYI: Required for code reload

"""
Goal: there are three base classes commented out below! Uncomment the correct one to be used
with `RaftSprite`. Scroll down to the `RaftSprite` for more details.

Note: You may notice that the base classes in this exercise are slightly different from those in
the instructions. The base classes here neither inherit from `ABC` (a helper class that has ABCMeta
as its metaclass) nor use @abstractmethod. This means that the base classes are are not abstract,
and their methods should not be re-implemented by their subclasses! 

Regardless of whether a base class is abstract of not, its subclasses should not depend on a base
class that has methods that they do not need.
"""


# class VehicleInterface(Sprite):
#     """Base class for vehicles that move on water."""

#     def __init__(self, sheet_name: str, center_x: int, center_y: int):
#         super().__init__(sheet_name, center_x=center_x, center_y=center_y)

#     def move_on_water():
#         ...

#     def move_on_land():
#         ...


# class WaterVehicleInterface(VehicleSprite):
#     """Base class for vehicles that move on water."""

#     def __init__(self, sheet_name: str, center_x: int, center_y: int):
#         super().__init__(sheet_name, center_x=center_x, center_y=center_y)

#     def move_on_water():
#         ...


# class LandVehicleInterface(Sprite):
#     """Base class for vehicles that move on land."""

#     def __init__(self, sheet_name: str, center_x: int, center_y: int):
#         super().__init__(sheet_name, center_x=center_x, center_y=center_y)

#     def move_on_land():
#         ...


class RaftSprite(Sprite):
    """
    Class for the raft sprite.

    TODO: Uncomment one of the three base classes above, and replace the `Sprite` parameter
    with the class that you uncommented.

    Example: `class RaftSprite(NewBaseClass):`

    Once you are finished, reload the game with Ctrl R and try building the raft again!
    """

    def __init__(self, sheet_name: str):
        super().__init__(sheet_name, center_x=RAFT_STARTING_X, center_y=RAFT_STARTING_Y)
        self.type = VehicleType.RAFT


# FYI: Required for code reload
def load_sprites(sprite_register: SpriteRegister) -> None:
    """Create the special 'raft sprite' who can be moved on the water."""
    register = Register(
        sprite=RaftSprite(":assets:raft.png"),
        source=SOURCE_NAME,
    )
    sprite_register.register_sprite(register)
