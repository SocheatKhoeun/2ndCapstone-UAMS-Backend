from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "fastapi-manual"
    ENV: str = "dev"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "fastapi_user"
    DB_PASSWORD: str = "change-me"
    DB_NAME: str = "fastapipro"

    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5000", "http://127.0.0.1:5000"]
    # JWT secret used to sign tokens. Prefer keeping this out of source control (.env or environment variable).
    JWT_PRIVATE: Optional[str] = None

    # Load environment from .env and ignore extra keys so unknown env entries
    # (for deployment or docker-compose) don't cause validation failures.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def sqlalchemy_uri(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()