from __future__ import annotations

from typing import Optional

from aioredis import Redis

from app.core.config import settings

_redis: Optional[Redis] = None


async def connect_to_redis() -> None:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(
            settings.redis_url.unicode_string(),
            encoding="utf-8",
            decode_responses=True,
        )
        # Perform a health check to fail fast if the connection is invalid.
        await _redis.ping()


async def close_redis_connection() -> None:
    global _redis
    if _redis is not None:
        await _redis.close()
        _redis = None


def get_redis() -> Redis:
    if _redis is None:
        raise RuntimeError("Redis client has not been initialized")
    return _redis

