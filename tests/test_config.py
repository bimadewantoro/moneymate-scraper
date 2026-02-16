"""Smoke tests for configuration loading."""

from pathlib import Path

from moneymate_scraper.config import Settings


def test_default_settings() -> None:
    """Settings should load with sensible defaults even without a .env file."""
    s = Settings()
    assert s.google_credentials_path == Path("credentials.json")
    assert s.google_token_path == Path("token.json")
    assert s.log_level == "INFO"


def test_moneymate_api_url_default() -> None:
    """The default API URL should point to localhost."""
    s = Settings()
    assert "localhost" in s.moneymate_api_url
