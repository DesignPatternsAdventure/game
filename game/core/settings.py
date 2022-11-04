"""Game Environment Configuration."""

from pydantic import BaseSettings


class _Settings(BaseSettings):

    KEY_REPEAT_PER_MINUTE: int = 600

    class Config:
        env_prefix = ''


SETTINGS = _Settings()
