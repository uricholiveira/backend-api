from pydantic import BaseSettings

from app.core.settings.app import AppConfig
from app.core.settings.authentication import AuthConfig
from app.core.settings.database import DatabaseConfig


class Settings(BaseSettings):
    database: DatabaseConfig = DatabaseConfig()
    app: AppConfig = AppConfig()
    auth: AuthConfig = AuthConfig()


settings = Settings()
