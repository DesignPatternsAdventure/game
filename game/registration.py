"""Decouple sprite creation from main class."""

from typing import Any, Callable

from beartype import beartype


class SpriteRegister:

    listener: Callable[[Any], None] | None = None

    @beartype
    def set_listener(self, listener: Callable) -> None:
        """For the main game, register a listener to be notified on changes."""
        self.listener = listener

    @beartype
    def register_sprite(self, sprite) -> None:
        """Register a sprite with the main game."""
        if self.listener:
            self.listener(sprite)
        raise NotImplementedError('No listener has been set.')


sprite_register = SpriteRegister()
"""Singleton register."""
