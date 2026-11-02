from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[UUID] = mapped_column(
        ForeignKey("habits.id", ondelete="CASCADE"), index=True
    )
    completed_at: Mapped[date] = mapped_column(Date)

    __table_args__ = (
    UniqueConstraint(
        "habit_id",
        "completed_at",
        name="uq_habit_logs_habit_id_completed_at",
    ),
)
    habit: Mapped["Habit"] = relationship(back_populates="logs")
