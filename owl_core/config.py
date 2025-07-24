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
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def get_db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()  # type: ignore
