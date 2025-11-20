from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.recommendation import RecommendationRequest, RecommendationResponse, RecommendationStatus
from app.services.recommendations import QuoteRecommendationService


router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def get_recommendation_service() -> QuoteRecommendationService:
    return QuoteRecommendationService()


@router.post("/", response_model=RecommendationResponse)
async def recommend_quote(
    payload: RecommendationRequest,
    service: QuoteRecommendationService = Depends(get_recommendation_service),
) -> RecommendationResponse:
    quote = await service.recommend_quote(
        email=payload.email,
        category=payload.category,
        hamming_threshold=payload.hamming_threshold,
        candidate_limit=payload.candidate_limit,
    )

    if quote is None:
        return RecommendationResponse(
            status=RecommendationStatus.NOT_FOUND,
            quote=None,
            category=payload.category,
        )

    return RecommendationResponse(
        status=RecommendationStatus.DELIVERED,
        quote=quote,
        category=payload.category or quote.category,
    )

