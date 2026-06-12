from __future__ import annotations

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Fake Review Detection API"
    database_url: str = "sqlite:///./fake_reviews.db"
    model_dir: str = "../model/saved_model"
    frontend_origin: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        protected_namespaces=("settings_",),
    )

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith(("sqlite", "postgresql", "mysql", "sqlite+aiosqlite")):
            raise ValueError("Invalid database URL scheme. Supported: sqlite, postgresql, mysql.")
        return v

    @field_validator("frontend_origin")
    @classmethod
    def validate_frontend_origin(cls, v: str) -> str:
        if not v.startswith(("http://", "https://")):
            raise ValueError("frontend_origin must start with http:// or https://")
        return v


settings = Settings()
