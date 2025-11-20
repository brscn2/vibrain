from __future__ import annotations

from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument

from app.db.mongo import get_database
from app.schemas.user import UserCreate, UserInDB

COLLECTION_NAME = "users"


def get_user_collection() -> AsyncIOMotorCollection:
    return get_database()[COLLECTION_NAME]


def _document_to_model(document: dict[str, Any]) -> UserInDB:
    document["_id"] = document.get("_id", ObjectId())
    return UserInDB.model_validate(document)


class UserRepository:
    def __init__(self, collection: AsyncIOMotorCollection | None = None) -> None:
        self._collection = collection or get_user_collection()

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._collection

    async def get_by_email(self, email: str) -> UserInDB | None:
        document = await self.collection.find_one({"email": email})
        if not document:
            return None
        return _document_to_model(document)

    async def upsert_user(self, user: UserCreate) -> UserInDB:
        payload = user.model_dump(by_alias=True)
        result = await self.collection.find_one_and_update(
            {"email": payload["email"]},
            {"$set": payload},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        if result is None:
            # Upsert may return None when the document did not exist before.
            result = await self.collection.find_one({"email": payload["email"]})
        assert result is not None  # for type checking
        return _document_to_model(result)

    async def append_seen_hashes(self, email: str, hashes: list[str]) -> None:
        if not hashes:
            return
        await self.collection.update_one(
            {"email": email},
            {"$addToSet": {"seen_sim_hashes": {"$each": hashes}}},
        )

