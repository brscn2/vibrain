from __future__ import annotations

from typing import List

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import DocumentModel
from app.schemas.quote import QuoteCategory


class UserSettings(BaseModel):
    subscribed_topics: List[QuoteCategory] = Field(default_factory=list, max_length=5)


class UserBase(DocumentModel):
    email: EmailStr
    settings: UserSettings = Field(default_factory=UserSettings)


class UserCreate(UserBase):
    seen_sim_hashes: list[str] = Field(default_factory=list)


class UserInDB(UserBase):
    seen_sim_hashes: list[str] = Field(default_factory=list)


class UserPublic(UserBase):
    pass

