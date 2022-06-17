from pydantic import BaseSettings

from app.core.settings.app import AppConfig
from app.core.settings.authentication import AuthConfig
from app.core.settings.database import DatabaseConfig
from app.core.settings.util import UtilConfig


class Settings(BaseSettings):
    database: DatabaseConfig = DatabaseConfig()
    app: AppConfig = AppConfig()
    auth: AuthConfig = AuthConfig()
    util: UtilConfig = UtilConfig()


settings = Settings()
