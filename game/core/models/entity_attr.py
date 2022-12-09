"""Generic Entity Attributes."""

from datetime import datetime, timedelta

from beartype import beartype
from pydantic import BaseModel  # pylint: disable=E0611

from ..game_clock import GameClock


class EntityAttr(BaseModel):
    """Entity Attribute Model."""

    health: float | None = None
    """Optional current health."""

    counter: int | None = None
    """Optional count of uses or components."""

    last_update: datetime | None = None
    """Track last update in game clock time to calculate changes when reloaded."""

    # PLANNED: Consider other generic attributes to model

    @beartype
    def on_update(self, game_clock: GameClock) -> timedelta:
        """On update, get the time difference since last update for calculating any changes."""
        now = game_clock.current_time
        time_since_last_update = now - (self.last_update or now)
        self.last_update = now
        return time_since_last_update  # noqa: R504
