from functools import lru_cache

from pydantic import Field, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    project_name: str = "vibrain"
    version: str = "0.1.0"
    mongodb_uri: MongoDsn = Field(
        default="mongodb://localhost:27017/vibrain",
        validation_alias="MONGODB_URI",
        description="MongoDB Atlas connection string",
    )
    mongodb_db: str = Field(default="vibrain", validation_alias="MONGODB_DB")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
