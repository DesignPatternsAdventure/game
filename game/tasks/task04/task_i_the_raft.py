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
-------------------------------------------------------------------------------------------------
Goal: Refactor the `BaseVehicle` class into two separate base classes with relevant methods.

Look for 'TODO's to see where to make your code changes!
-------------------------------------------------------------------------------------------------

Note: You may notice that the base classes in this exercise are slightly different from those in
the introduction. The base classes here neither inherit from `ABC` (a helper class that has ABCMeta
as its metaclass) nor use @abstractmethod. This means that the base classes are are not abstract,
and their methods should not be re-implemented by their subclasses! 

Regardless of whether a base class is abstract of not, its subclasses should not depend on a base
class that has methods that they do not need.
"""


class BaseVehicle(VehicleSprite):
    """
    Base class for vehicles. This is inherited by the `RaftBefore` class, but it has a method,
    `move_on_land`, that `RaftBefore` does not need.

    Do not modify.
    """

    def __init__(self, sheet_name: str, center_x: int, center_y: int):
        super().__init__(sheet_name, center_x=center_x, center_y=center_y)

    def move_on_water(self):
        ...

    def move_on_land(self):
        ...


class RaftBefore(BaseVehicle):
    """
    Raft class before refactoring. This is a subclass of `BaseVehicle`.

    Do not modify.
    """

    def __init__(self, sheet_name: str):
        super().__init__(sheet_name, center_x=RAFT_STARTING_X, center_y=RAFT_STARTING_Y)
        self.type = VehicleType.RAFT


"""
The `BaseVehicle` class has already been split into two base classes for you. Your task is to
move the relevant method into each base class.

After you make your changes, reload the game with Ctrl R and try building the raft again!
"""


class BaseWaterVehicle(VehicleSprite):
    """
    Base class for vehicles that move on water.

    TODO: Move the relevant method from the `BaseVehicle` class to this class.
    """

    def __init__(self, sheet_name: str, center_x: int, center_y: int):
        super().__init__(sheet_name, center_x=center_x, center_y=center_y)


class BaseLandVehicle(VehicleSprite):
    """
    Base class for vehicles that move on land.

    TODO: Move the relevant method from the `BaseVehicle` class to this class.
    """

    def __init__(self, sheet_name: str, center_x: int, center_y: int):
        super().__init__(sheet_name, center_x=center_x, center_y=center_y)


class Raft(BaseWaterVehicle):
    """
    Raft class after refactoring. This is now a subclass of `BaseWaterVehicle`.

    Do not modify.
    """

    def __init__(self, sheet_name: str):
        super().__init__(sheet_name, center_x=RAFT_STARTING_X, center_y=RAFT_STARTING_Y)
        self.type = VehicleType.RAFT


# FYI: Required for code reload
def load_sprites(sprite_register: SpriteRegister) -> None:
    """
    Create the Raft class that can move on water.

    Do not modify.
    """
    register = Register(
        sprite=Raft(":assets:raft.png"),
        source=SOURCE_NAME,
    )
    sprite_register.register_sprite(register)
