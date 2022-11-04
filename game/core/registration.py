"""Decouple sprite creation from main class."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

from beartype import beartype
from pydantic import BaseModel


class Register(BaseModel):
    """Sprite and associated handlers for registration."""

    # FIXME: 'Any' should be 'arcade.Sprite'. Need validator + arbitrary_types_allowed

    sprite: Any
    source: Path
    on_mouse_motion: Callable[[Any, int, int, float, float], None] | None = None
    on_key_press: Callable[[Any, int, int], None] | None = None
    on_key_release: Callable[[Any, int, int], None] | None = None
    on_update: Callable[[Any, float], None] | None = None


class SpriteRegister:

    listener: Callable[[Register], None] | None = None

    @beartype
    def set_listener(self, listener: Callable[[Register], None]) -> None:
        """For the main game, register a listener to be notified on changes."""
        self.listener = listener

    # FIXME: Create a BaseModel that accepts the Sprite and any callbacks to register
    #    ^ This is important if the sprite needs to react to on_update, on_keypress, etc.
    @beartype
    def register_sprite(self, register: Register) -> None:
        """Register a sprite with the main game."""
        if not self.listener:
            raise NotImplementedError('No listener has been set.')
        self.listener(register)
