from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # `.env` takes priority over `.env.local`
    model_config = SettingsConfigDict(env_file=(".env.local", ".env"))
    DB_HOST: str = Field("postgres", alias="POSTGRES_HOST")
    DB_PORT: int = Field(5432, alias="POSTGRES_PORT")
    DB_NAME: str = Field("owl_db", alias="POSTGRES_DB")
    DB_USER: str = Field("owl", alias="POSTGRES_USER")
    DB_PASSWORD: str = Field("hoot", alias="POSTGRES_PASSWORD")
    SECRET_KEY: str = Field("owerride-me-secret-key")


settings = Settings()  # type: ignore


def get_db_url() -> str:
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
