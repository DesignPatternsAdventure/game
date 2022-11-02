"""Decouple sprite creation from main class."""

from typing import Callable
from pathlib import Path

import arcade
from beartype import beartype


class SpriteRegister:

    listener: Callable[[arcade.Sprite, Path], None] | None = None

    @beartype
    def set_listener(self, listener: Callable) -> None:
        """For the main game, register a listener to be notified on changes."""
        self.listener = listener

    # FIXME: Create a BaseModel that accepts the Sprite and any callbacks to register
    #    ^ This is important if the sprite needs to react to on_update, on_keypress, etc.
    @beartype
    def register_sprite(self, sprite: arcade.Sprite, source: Path) -> None:
        """Register a sprite with the main game."""
        if not self.listener:
            raise NotImplementedError('No listener has been set.')
        self.listener(sprite, source)
