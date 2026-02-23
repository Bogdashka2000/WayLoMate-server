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
    STATIC_DIR_AVATAR: str
    STATIC_DIR_HEADER: str
    STATIC_DIR_POST_PICTURES: str
    

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

setup = Setup()


def get_db_url():
    return (f"mysql+aiomysql://{setup.DB_USER}:{setup.DB_PASSWORD}@"
            f"{setup.DB_HOST}:{setup.DB_PORT}/{setup.DB_NAME}")


def get_auth_data():
    return {"secret_key": setup.SECRET_KEY, "algorithm": setup.ALGORITHM}

def get_static_path():
      return {
            "static_dir_avatar": f"app/{setup.STATIC_DIR_AVATAR}",
            "static_dir_header": f"app/{setup.STATIC_DIR_HEADER}",
            "static_dir_post_pictures": f"app/{setup.STATIC_DIR_POST_PICTURES}",

            "static_dir_avatar_for_link": setup.STATIC_DIR_AVATAR,
            "static_dir_header_for_link": setup.STATIC_DIR_HEADER,
            "static_dir_post_pictures_for link": setup.STATIC_DIR_POST_PICTURES,
             }