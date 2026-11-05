import pytest
from efs.config import Settings
from pydantic import ValidationError


def test_settings_accept_postgresql():
    settings = Settings(database_url="postgresql+psycopg://u:p@h/db")
    assert settings.database_url.startswith("postgresql+psycopg://")


def test_settings_reject_sqlite():
    with pytest.raises(ValidationError):
        Settings(database_url="sqlite:///bad.db")
