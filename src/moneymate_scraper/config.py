"""Application configuration loaded from environment variables via pydantic-settings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for MoneyMate Scraper.

    Values are loaded from a `.env` file in the project root and can be
    overridden by real environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Google OAuth ---
    google_credentials_path: Path = Path("credentials.json")
    google_token_path: Path = Path("token.json")

    # --- MoneyMate API ---
    moneymate_api_url: str = "http://localhost:3000/api"

    # --- General ---
    log_level: str = "INFO"


# Singleton instance — import this wherever config is needed.
settings = Settings()
