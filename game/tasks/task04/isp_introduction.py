"""Task 04: The Raft.

The fourth task will be to apply the "I" of the S.O.L.I.D design principles to building the raft

> (I) **Interface Segregation Principle**
>
> Clients should not be forced to depend upon interfaces or methods that they do not use

"""

from abc import ABC, abstractmethod

"""

Consider this hypothetical example, where the `Raft` class and the `Carriage` class both inherit
from the `VehicleInterface` base class and implement the `move_on_water` and `move_on_land` methods.

This example violates the Interface Segregation Principle because `Raft` and `Carriage` are both
implementing methods that they do not use.

"""


class VehicleInterface(ABC):
    """Base class for all vehicles."""

    @abstractmethod
    def move_on_water(self):
        ...

    @abstractmethod
    def move_on_land(self):
        ...

    @abstractmethod
    def stop(self):
        ...


class Raft(VehicleInterface):
    def move_on_water(self):
        print("Moving raft")

    def move_on_land(self):
        raise Exception("The raft cannot move on land!")


class Carriage(VehicleInterface):
    def move_on_water(self):
        raise Exception("The carriage cannot move on water!")

    def move_on_land(self):
        print("Moving carriage")


"""

Our goal is to remove `move_on_land` from `Raft` and `move_on_water` from `Carriage`, but we cannot
do that easily because the base class contains those methods, and all methods in the base class must
be implemented by a subclass. Therefore, the solution is to make two separate base classes.

"""


class WaterVehicleInterface(ABC):
    """Base class for vehicles that move on water."""

    @abstractmethod
    def move_on_water(self):
        ...

    @abstractmethod
    def stop(self):
        ...


class LandVehicleInterface(ABC):
    """Base class for vehicles that move on land."""

    @abstractmethod
    def move_on_land(self):
        ...

    @abstractmethod
    def stop(self):
        ...


class BetterRaft(WaterVehicleInterface):
    def move_on_water(self):
        print("Moving raft")


class BetterCarriage(LandVehicleInterface):
    def move_on_land(self):
        print("Moving carriage")


"""

In our hypothetical example, making two separate base classes may seem redundant, since each one is
only implemented by one subclass, but in the real world, you may come across code that be improved
by following this principle.

If you would like to learn more about the Interface Segregation Principle, you can take a look at:

- https://en.wikipedia.org/wiki/Interface_segregation_principle
- https://phoenixnap.com/blog/solid-principles
- https://ezzeddinabdullah.com/post/solid-principles-isp-py/

"""
