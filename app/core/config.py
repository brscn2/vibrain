from functools import lru_cache

from pydantic import Field, MongoDsn, RedisDsn
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
    redis_url: RedisDsn = Field(
        default="redis://localhost:6379/0",
        validation_alias="REDIS_URL",
        description="Redis connection string",
    )
<<<<<<< HEAD
    hamming_threshold: int = Field(
        default=5,
        ge=1,
        le=10,
        validation_alias="HAMMING_THRESHOLD",
        description="Minimum Hamming distance threshold for quote similarity",
    )
    candidate_limit: int = Field(
        default=20,
        ge=1,
        le=100,
        validation_alias="CANDIDATE_LIMIT",
        description="Maximum number of candidate quotes to fetch per category",
    )
=======
    openai_api_key: str = Field(validation_alias="OPENAI_API_KEY")
    tavily_api_key: str | None = Field(default=None, validation_alias="TAVILY_API_KEY")
>>>>>>> 83995126626a7dc10bc2d9015101476c57b92ac8


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
