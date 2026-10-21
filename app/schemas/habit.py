from typing import Literal

from pydantic import BaseModel, Field, field_validator

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
    def strip_strings(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("days", mode="after")
    @classmethod
    def normalize_days(cls, v: list[DayName]) -> list[DayName]:
        return sorted(set(v), key=DAY_ORDER.index)
