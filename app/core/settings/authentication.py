from pydantic import BaseSettings


class AuthConfig(BaseSettings):
    access_token_expire_minutes: int = 15
    secret_key: str = "supersecretkey"
    algorithm: str = "HS256"
