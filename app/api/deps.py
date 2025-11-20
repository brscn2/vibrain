"""Shared dependencies for FastAPI routes."""

from collections.abc import AsyncIterator

from aioredis import Redis
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.cache.redis import get_redis
from app.db.mongo import get_database


async def get_mongo_db() -> AsyncIterator[AsyncIOMotorDatabase]:
    db = get_database()
    try:
        yield db
    finally:
        # Motor handles connection pooling; nothing to cleanup per-request.
        pass


async def get_redis_client() -> AsyncIterator[Redis]:
    client = get_redis()
    try:
        yield client
    finally:
        # Connections are pooled; nothing to clean per-request.
        pass
