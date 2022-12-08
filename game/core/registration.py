"""Decouple sprite creation from main class."""

from collections.abc import Callable
from typing import Any

from beartype import beartype
from pydantic import BaseModel  # pylint: disable=E0611

from .constants import HORIZONTAL_MARGIN, VERTICAL_MARGIN, NumT
from .game_clock import GameClock

# PLANNED: Should be 'arcade.Sprite'. Need validator + arbitrary_types_allowed
ArcadeSpriteType = Any


class CameraView(BaseModel):

    center: tuple[NumT, NumT]
    height: NumT = HORIZONTAL_MARGIN
    width: NumT = VERTICAL_MARGIN

    @beartype
    def in_view(self, point: tuple[NumT, NumT]) -> bool:
        """Return True if the provided point is within the camera view."""
        radii = [abs(self.center[idx] - point[idx]) for idx in range(2)]
        return radii[0] < self.height and radii[1] < self.width


class Register(BaseModel):
    """Sprite and associated handlers for flexible registration."""

    sprite: ArcadeSpriteType
    """Registered Sprite."""

    source: str
    """Unique identifier for the module."""

    on_mouse_motion: Callable[[int, int, float, float], None] | None = None
    """Arcade mouse_motion handler."""

    on_update: Callable[[GameClock], None] | None = None
    """Arcade update handler."""

    on_key_press: Callable[[int, int], None] | None = None
    """Arcade key_press handler."""
    on_key_hold: Callable[[int, int], None] | None = None
    """Fires at greater than a set interval when a key is held pressed."""
    on_key_release: Callable[[int, int], None] | None = None
    """Arcade key_release handler."""

    on_player_sprite_motion: Callable[
        [tuple[NumT, NumT], CameraView], None
    ] | None = None
    """Register a handler to update whenever the player's position changes."""


class SpriteRegister:
    """Generic way to register a Sprite."""

    listener: Callable[[Register], None] | None = None

    @beartype
    def set_listener(self, listener: Callable[[Register], None]) -> None:
        """For the main game, register a listener to be notified on changes."""
        self.listener = listener

    @beartype
    def register_sprite(self, register: Register) -> None:
        """Register a sprite with the main game."""
        if not self.listener:  # pragma: no cover
            raise NotImplementedError("No listener has been set.")
        self.listener(register)
