from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import ConfigDict, Field

from app.schemas.base import DocumentModel


class QuoteCategory(str, Enum):
    CORE_PERSONAL_GROWTH = "core_personal_growth"
    PSYCHOLOGY = "psychology"
    PHILOSOPHY = "philosophy"
    MENTAL_HEALTH_WELLNESS = "mental_health_wellness"
    FITNESS_BODY = "fitness_body"
    WORK_PRODUCTIVITY_MONEY = "work_productivity_money"
    LIFE_RELATIONSHIPS = "life_relationships"
    TECH_AI_FUTURE = "tech_ai_future"
    CREATIVE_ARTISTIC = "creative_artistic"
    TREND_ADAPTIVE = "trend_adaptive"
    HISTORY = "history"


class QuoteBase(DocumentModel):
    content: str = Field(min_length=1, max_length=2048)
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
