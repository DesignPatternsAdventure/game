"""Game Environment Configuration."""

from pydantic import BaseSettings


class _Settings(BaseSettings):

    KEY_REPEAT_PER_MINUTE: int = 1200

    class Config:
        env_prefix = ''


SETTINGS = _Settings()
