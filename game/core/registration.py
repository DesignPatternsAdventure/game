"""Decouple sprite creation from main class."""

from collections.abc import Callable
from typing import Any

from beartype import beartype
from pydantic import BaseModel


class Register(BaseModel):
    """Sprite and associated handlers for flexible registration."""

    sprite: Any  # FIXME: Should be 'arcade.Sprite'. Need validator + arbitrary_types_allowed
    """Registered Sprite."""

    source: str
    """Unique identifier for the module."""

    on_mouse_motion: Callable[[Any, int, int, float, float], None] | None = None
    """Arcade mouse_motion handler."""

    on_update: Callable[[Any, float], None] | None = None
    """Arcade update handler."""

    on_key_press: Callable[[Any, int, int], None] | None = None
    """Arcade key_press handler."""
    on_key_hold: Callable[[Any, int, int], None] | None = None
    """Fires at greater than a set interval when a key is held pressed."""
    on_key_release: Callable[[Any, int, int], None] | None = None
    """Arcade key_release handler."""


class SpriteRegister:

    listener: Callable[[Register], None] | None = None

    @beartype
    def set_listener(self, listener: Callable[[Register], None]) -> None:
        """For the main game, register a listener to be notified on changes."""
        self.listener = listener

    @beartype
    def register_sprite(self, register: Register) -> None:
        """Register a sprite with the main game."""
        if not self.listener:
            raise NotImplementedError('No listener has been set.')
        self.listener(register)
