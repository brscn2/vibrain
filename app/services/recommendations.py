from __future__ import annotations

from typing import Iterable, Sequence

from app.cache.history import HistoryCache
from app.core.config import settings
from app.models.quote import QuoteRepository
from app.models.user import UserRepository
from app.schemas.quote import QuoteCategory, QuoteInDB, QuotePublic
from app.schemas.user import UserInDB
from app.services.similarity import hamming_distance


class QuoteRecommendationService:
    def __init__(
        self,
        quote_repo: QuoteRepository | None = None,
        user_repo: UserRepository | None = None,
        history_cache: HistoryCache | None = None,
    ) -> None:
        self.quote_repo = quote_repo or QuoteRepository()
        self.user_repo = user_repo or UserRepository()
        self.history_cache = history_cache or HistoryCache()

    async def recommend_quote(
        self,
        email: str,
        category: QuoteCategory | None = None,
    ) -> QuotePublic | None:
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None

        active_categories = self._resolve_categories(user, category)
        if not active_categories:
            return None

        user_id = str(user.id or user.email)
        history = await self._load_history(user_id, user)

        threshold = settings.hamming_threshold
        limit = settings.candidate_limit

        for active_category in active_categories:
            candidates = await self.quote_repo.fetch_candidates(active_category, limit=limit)
            selected = self._select_candidate(candidates, history, threshold)
            if selected:
                await self._mark_seen(user, user_id, selected.sim_hash)
                return QuotePublic.model_validate(selected)
        return None

    async def _mark_seen(self, user: UserInDB, user_id: str, sim_hash: str) -> None:
        await self.history_cache.add_hashes(user_id, [sim_hash])
        await self.user_repo.append_seen_hashes(user.email, [sim_hash])

    async def _load_history(self, user_id: str, user: UserInDB) -> set[str]:
        history = await self.history_cache.get_history(user_id)
        if not history and user.seen_sim_hashes:
            await self.history_cache.add_hashes(user_id, user.seen_sim_hashes)
            history = set(user.seen_sim_hashes)
        return history

    def _select_candidate(
        self,
        candidates: Sequence[QuoteInDB],
        history: set[str],
        threshold: int,
    ) -> QuoteInDB | None:
        if not history:
            return candidates[0] if candidates else None

        for candidate in candidates:
            if self._is_beyond_threshold(candidate.sim_hash, history, threshold):
                return candidate
        return None

    @staticmethod
    def _is_beyond_threshold(sim_hash: str, history: Iterable[str], threshold: int) -> bool:
        for seen_hash in history:
            if hamming_distance(sim_hash, seen_hash) <= threshold:
                return False
        return True

    @staticmethod
    def _resolve_categories(user: UserInDB, category: QuoteCategory | None) -> list[QuoteCategory]:
        if category:
            return [category]
        subscribed = user.settings.subscribed_topics
        return list(subscribed)

