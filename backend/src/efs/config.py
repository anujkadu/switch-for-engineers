from functools import lru_cache

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="EFS_", extra="ignore")

    database_url: str = Field(validation_alias=AliasChoices("EFS_DATABASE_URL", "database_url"))
    test_database_url: str | None = Field(
        default=None, validation_alias=AliasChoices("EFS_TEST_DATABASE_URL", "test_database_url")
    )
    log_level: str = Field(
        default="INFO", validation_alias=AliasChoices("EFS_LOG_LEVEL", "log_level")
    )

    @field_validator("database_url", "test_database_url")
    @classmethod
    def require_postgresql(cls, value: str | None) -> str | None:
        if value is not None and not value.startswith(("postgresql://", "postgresql+psycopg://")):
            raise ValueError("database URLs must use PostgreSQL with the psycopg driver")
        return value

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        level = value.upper()
        if level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("EFS_LOG_LEVEL must be a standard logging level")
        return level


@lru_cache
def get_settings() -> Settings:
    return Settings()
