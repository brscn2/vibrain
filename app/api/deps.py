"""Shared dependencies for FastAPI routes."""

from collections.abc import AsyncIterator

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongo import get_database


async def get_mongo_db() -> AsyncIterator[AsyncIOMotorDatabase]:
    db = get_database()
    try:
        yield db
    finally:
        # Motor handles connection pooling; nothing to cleanup per-request.
        pass
