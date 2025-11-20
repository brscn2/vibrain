from __future__ import annotations

from typing import Any

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: object) -> ObjectId:
        if isinstance(value, ObjectId):
            return value
        if isinstance(value, str) and ObjectId.is_valid(value):
            return ObjectId(value)
        raise ValueError("Invalid ObjectId")


class DocumentModel(BaseModel):
    id: str | PyObjectId | None = Field(default=None, alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def _validate_id(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, ObjectId):
            return PyObjectId(value)
        if isinstance(value, str):
            if ObjectId.is_valid(value):
                return PyObjectId(value)
            return value
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

