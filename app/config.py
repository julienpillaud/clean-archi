from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    SQLALCHEMY_DATABASE_URI: str


settings = Settings()
