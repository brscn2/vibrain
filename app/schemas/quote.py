from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import ConfigDict, Field

from app.schemas.base import DocumentModel


class QuoteCategory(str, Enum):
    STOICISM = "stoicism"
    TECH = "tech"
    HUMOR = "humor"
    MOTIVATION = "motivation"
    HISTORY = "history"


class QuoteBase(DocumentModel):
    content: str = Field(min_length=1, max_length=2048)
    author: str = Field(default="Unknown", max_length=256)
    category: QuoteCategory
    sim_hash: str = Field(min_length=16, max_length=32, description="64-bit SimHash hex string")


class QuoteCreate(QuoteBase):
    ingestion_batch_id: str | None = None


class QuoteInDB(QuoteBase):
    created_at: datetime
    ingestion_batch_id: str | None = None

    model_config = ConfigDict(from_attributes=True)


class QuotePublic(QuoteInDB):
    class Config:
        from_attributes = True

