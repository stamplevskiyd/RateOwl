from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # `.env` takes priority over `.env.local`
    model_config = SettingsConfigDict(env_file=(".env.local", ".env"))
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "owl_db"
    DB_USER: str = "owl"
    DB_PASSWORD: str = "hoot"
    SECRET_KEY: str = "secret"


settings = Settings()


def get_db_url() -> str:
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
