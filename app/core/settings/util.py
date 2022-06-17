from pydantic import BaseSettings, Field


class LogConfig(BaseSettings):
    level: str = Field("INFO", env="LOG_LEVEL")


class UtilConfig(BaseSettings):
    log: LogConfig = LogConfig()
