from pydantic import BaseSettings


class DatabaseParamsConfig(BaseSettings):
    auto_commit: bool = True
    auto_flush: bool = True
    check_same_thread: bool = False


class DatabaseConfig(BaseSettings):
    params: DatabaseParamsConfig = DatabaseParamsConfig()
    driver: str = "postgresql"
    user: str = "user"
    password: str = "supersecretpassword"
    host: str = "localhost"
    port: int = 5432
    url: str = f"{driver}://{user}:{password}@{host}:{port}/postgres"
