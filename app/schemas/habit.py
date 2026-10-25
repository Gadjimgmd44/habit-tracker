from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

DAY_ORDER = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
DayName = Literal["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class HabitCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    days: list[DayName] = Field(
        min_length=1,
    )

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_strings(cls, v: str | None) -> str | None:
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("days", mode="after")
    @classmethod
    def normalize_days(cls, v: list[DayName]) -> list[DayName]:
        if len(v) != len(set(v)):
            raise ValueError("days must not contain duplicates")
        return sorted(set(v), key=DAY_ORDER.index)


class HabitRead(BaseModel):
    id: UUID
    title: str
    description: str | None
    days: list[DayName]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HabitUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    days: list[DayName] | None = Field(
        default=None,
        min_length=1,
    )

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("days", mode="after")
    @classmethod
    def normalize_days(cls, v: list[DayName]) -> list[DayName]:
        if v is None:
            return v
        if len(v) != len(set(v)):
            raise ValueError("days must not contain duplicates")
        return sorted(set(v), key=DAY_ORDER.index)
