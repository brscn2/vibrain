from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any, Iterable, Sequence

from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import UpdateOne

from app.db.mongo import get_database
from app.schemas.quote import QuoteCategory, QuoteCreate, QuoteInDB

COLLECTION_NAME = "quotes"


def get_quote_collection() -> AsyncIOMotorCollection:
    return get_database()[COLLECTION_NAME]


def _document_to_model(document: dict[str, Any]) -> QuoteInDB:
    return QuoteInDB.model_validate(document)


def compute_lexical_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


class QuoteRepository:
    def __init__(self, collection: AsyncIOMotorCollection | None = None) -> None:
        self._collection = collection or get_quote_collection()

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._collection

    async def insert_quote(self, quote: QuoteCreate) -> str:
        lexical_hash = compute_lexical_hash(quote.content)
        payload = quote.model_dump(by_alias=True, exclude_none=True)
        payload["_id"] = lexical_hash
        payload["created_at"] = datetime.now(timezone.utc)

        await self.collection.update_one(
            {"_id": lexical_hash},
            {"$setOnInsert": payload},
            upsert=True,
        )
        return lexical_hash

    async def exists_by_sim_hash(self, sim_hash: str) -> bool:
        doc = await self.collection.find_one({"sim_hash": sim_hash}, {"_id": 1})
        return doc is not None

    async def fetch_candidates(
        self,
        category: QuoteCategory,
        limit: int = 10,
    ) -> Sequence[QuoteInDB]:
        cursor = (
            self.collection.find({"category": category.value})
            .sort("_id", -1)
            .limit(limit)
        )
        documents: list[QuoteInDB] = []
        async for doc in cursor:
            documents.append(_document_to_model(doc))
        return documents

    async def bulk_insert(self, quotes: Iterable[QuoteCreate]) -> list[str]:
        operations: list[UpdateOne] = []
        now = datetime.now(timezone.utc)
        for quote in quotes:
            payload = quote.model_dump(by_alias=True, exclude_none=True)
            lexical_hash = compute_lexical_hash(payload["content"])
            payload["_id"] = lexical_hash
            payload.setdefault("created_at", now)
            operations.append(
                UpdateOne(
                    {"_id": lexical_hash},
                    {"$setOnInsert": payload},
                    upsert=True,
                )
            )

        if not operations:
            return []

        result = await self.collection.bulk_write(operations, ordered=False)
        return [value for value in result.upserted_ids.values()]

