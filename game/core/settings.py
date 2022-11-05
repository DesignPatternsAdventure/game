"""Game Environment Configuration."""

import arcade
from pydantic import BaseSettings

_DISPLAY_WIDTH, _DISPLAY_HEIGHT = arcade.get_display_size()


class _Settings(BaseSettings):
    """Configurable Game Settings."""

    START_DATE: str = '2500-01-01'
    """Game clock start date."""

    KEY_REPEAT_PER_MINUTE: int = 1200
    """When held, number of key repetitions per minute."""

    WIDTH: int = int(_DISPLAY_WIDTH * 0.9)
    HEIGHT: int = int(_DISPLAY_HEIGHT * 0.9)

    class Config:
        env_prefix = 'GAME_'


SETTINGS = _Settings()
"""Game Settings loaded from Environment Variables."""
