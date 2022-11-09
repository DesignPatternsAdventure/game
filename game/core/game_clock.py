"""Track the game clock time."""

from datetime import datetime, timedelta

import arrow
from beartype import beartype
from pydantic import BaseModel, Field

from .settings import SETTINGS


class GameClock(BaseModel):
    """Track game clock time."""

    current_time: datetime = Field(
        default_factory=lambda: arrow.get(SETTINGS.START_DATE).datetime
    )
    delta_time: float = 0

    @beartype
    def on_update(self, delta_time: float) -> "GameClock":
        self.delta_time = delta_time
        self.current_time += timedelta(seconds=delta_time)
        return self
