import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the application."""

    # Database settings
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    # Redis settings
    redis_username: str
    redis_password: str
    redis_host: str
    redis_port: int
    redis_db: int
    redis_max_connections: int = 5

    broadcast_redis_max_connections: int = 5
    broadcast_type: str = "redis"

    # API settings
    secret_key: str
    access_token_expire_minutes: int
    refresh_token_expire_hours: int

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.db_username}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )

    def get_redis_url(self):
        return (
            f"redis://{self.redis_username}:{self.redis_password}@"
            f"{self.redis_host}:{self.redis_port}/{self.redis_db}"
        )


settings = Settings()
