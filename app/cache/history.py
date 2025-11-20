from __future__ import annotations

from collections.abc import Iterable
from typing import Set

from aioredis import Redis

from app.cache.redis import get_redis


def _history_key(user_id: str) -> str:
    return f"user:{user_id}:history"


class HistoryCache:
    def __init__(self, redis: Redis | None = None) -> None:
        self._redis = redis or get_redis()

    @property
    def redis(self) -> Redis:
        return self._redis

    async def get_history(self, user_id: str) -> set[str]:
        members = await self.redis.smembers(_history_key(user_id))
        return set(members) if members else set()

    async def add_hashes(self, user_id: str, hashes: Iterable[str]) -> int:
        hashes = [hash_value for hash_value in hashes if hash_value]
        if not hashes:
            return 0
        return await self.redis.sadd(_history_key(user_id), *hashes)

    async def clear_history(self, user_id: str) -> None:
        await self.redis.delete(_history_key(user_id))

