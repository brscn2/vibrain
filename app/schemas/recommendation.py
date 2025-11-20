from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, EmailStr, Field

from app.schemas.quote import QuoteCategory, QuotePublic


class RecommendationStatus(str, Enum):
    DELIVERED = "delivered"
    NOT_FOUND = "not_found"


class RecommendationRequest(BaseModel):
    email: EmailStr
    category: QuoteCategory | None = None
    hamming_threshold: int = Field(default=16, ge=1, le=64)
    candidate_limit: int = Field(default=10, ge=1, le=100)


class RecommendationResponse(BaseModel):
    status: RecommendationStatus
    quote: QuotePublic | None = None
    category: QuoteCategory | None = None

