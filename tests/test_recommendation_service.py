from datetime import datetime, timezone
from typing import Iterable, Sequence

import pytest

from app.schemas.quote import QuoteCategory, QuoteInDB
from app.schemas.user import UserInDB, UserSettings
from app.services.recommendations import QuoteRecommendationService


class FakeQuoteRepo:
    def __init__(self, quotes: Sequence[QuoteInDB]):
        self.quotes = list(quotes)

    async def fetch_candidates(self, category, limit=10):
        return [quote for quote in self.quotes if quote.category == category][:limit]


class FakeUserRepo:
    def __init__(self, user: UserInDB):
        self.user = user
        self.seen: list[str] = []

    async def get_by_email(self, email: str):
        return self.user if self.user.email == email else None

    async def append_seen_hashes(self, email: str, hashes: list[str]):
        self.seen.extend(hashes)


class FakeHistoryCache:
    def __init__(self, history: Iterable[str] | None = None):
        self.history = set(history or [])

    async def get_history(self, user_id: str):
        return set(self.history)

    async def add_hashes(self, user_id: str, hashes: Iterable[str]):
        self.history.update(hashes)


@pytest.mark.asyncio
async def test_recommendation_service_returns_quote():
    user = UserInDB(
        _id="user1",
        email="test@example.com",
        settings=UserSettings(subscribed_topics=[QuoteCategory.PHILOSOPHY]),
        seen_sim_hashes=[],
    )
    quote = QuoteInDB(
        _id="hash1",
        content="Test quote",
        category=QuoteCategory.PHILOSOPHY,
        sim_hash="ff00ff00ff00ff00",
        created_at=datetime.now(timezone.utc),
    )

    service = QuoteRecommendationService(
        quote_repo=FakeQuoteRepo([quote]),
        user_repo=FakeUserRepo(user),
        history_cache=FakeHistoryCache(),
    )

    result = await service.recommend_quote(email="test@example.com")

    assert result is not None
    assert result.content == "Test quote"

