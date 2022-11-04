"""Track which keys are held down."""

from contextlib import suppress
from datetime import datetime, timedelta

import arrow
from beartype import beartype
from pydantic import BaseModel, Field, PrivateAttr

from .settings import SETTINGS


class PressedKeys(BaseModel):
    """Track repeated keys."""

    keys: set[int] = Field(default_factory=set)
    modifiers: int = 0
    repeat_per_minute: int = SETTINGS.KEY_REPEAT_PER_MINUTE
    _last_update: datetime = PrivateAttr(default_factory=lambda: arrow.now().datetime)

    @beartype
    def pressed(self, key: int, modifiers: int) -> None:
        self._last_update = arrow.now().datetime
        self.keys.add(key)
        self.modifiers = modifiers

    @beartype
    def released(self, key: int, modifiers: int) -> None:
        self._last_update = arrow.now().datetime
        with suppress(KeyError):
            self.keys.remove(key)
        self.modifiers = modifiers

    @beartype
    def on_update(self) -> bool:
        now = arrow.now()
        delta = timedelta(seconds=60 / self.repeat_per_minute)
        if (now - arrow.get(self._last_update)) > delta:
            self._last_update = now.datetime
            return True
        return False
