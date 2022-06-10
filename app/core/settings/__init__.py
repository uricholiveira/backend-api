from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'backend-api'
    app_version: str = '0.1.0'


settings = Settings()
