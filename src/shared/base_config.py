from typing import Any, Optional

from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow",
    )

    # JWT Section
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # POSTGRES section
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_URL: Optional[PostgresDsn] = None

    @field_validator("POSTGRES_URL", mode="before")
    @classmethod
    def db_connection(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            return v

        # build in case we don't send the POSTGRES_URL
        values: dict[str, Any] = info.data
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=values.get("POSTGRES_HOST"),
            username=values.get("POSTGRES_USER"),
            port=values.get("POSTGRES_PORT"),
            password=values.get("POSTGRES_PASSWORD"),
            path=values.get("POSTGRES_DB"),
        )


settings = ConfigBaseSettings()
