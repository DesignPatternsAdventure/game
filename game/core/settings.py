"""Game Environment Configuration."""

from pydantic import BaseSettings


class _Settings(BaseSettings):
    """Configurable Game Settings."""

    KEY_REPEAT_PER_MINUTE: int = 1200

    # PLANNED: These could be inferred based on the display size
    WIDTH: int = 750
    HEIGHT: int = 750

    class Config:
        env_prefix = 'GAME_'


SETTINGS = _Settings()
"""Game Settings loaded from Environment Variables."""
