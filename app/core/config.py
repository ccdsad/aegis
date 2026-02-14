from enum import StrEnum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppMode(StrEnum):
    """Runtime execution mode for the trading pipeline."""

    PAPER = 'paper'
    REAL = 'real'


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    mode: AppMode = AppMode.PAPER
    api_v1_prefix: str = '/api/v1'

    model_config = SettingsConfigDict(env_prefix='app_')


@lru_cache
def get_settings() -> Settings:
    return Settings()
