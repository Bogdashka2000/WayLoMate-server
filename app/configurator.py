from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Setup(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=".env",          # ← относительно места запуска сервера
        env_file_encoding="utf-8",
        extra="ignore"
    )

setup = Setup()


def get_db_url():
    return (f"mysql+aiomysql://{setup.DB_USER}:{setup.DB_PASSWORD}@"
            f"{setup.DB_HOST}:{setup.DB_PORT}/{setup.DB_NAME}")


def get_auth_data():
    return {"secret_key": setup.SECRET_KEY, "algorithm": setup.ALGORITHM}
