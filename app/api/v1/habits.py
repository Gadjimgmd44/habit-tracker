from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.core.exceptions import NotFoundException
from app.db.session import get_db
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.services import habit as habit_service

router = APIRouter(
    prefix="/habits",
    tags=["habits"],
)


@router.get(
    "",
    response_model=list[HabitRead],
    status_code=status.HTTP_200_OK,
    summary="List habits",
)
async def list_habits(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[HabitRead]:
    """List habits belonging to the current user, newest first."""
    return await habit_service.get_habits(session=session, user_id=current_user.id)


@router.post(
    "",
    response_model=HabitRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create habit",
)
async def create_habit(
    data: HabitCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HabitRead:
    """Create a new habit for the current user."""
    habit = await habit_service.create_habit(
        session=session, data=data, user_id=current_user.id
    )
    return HabitRead.model_validate(habit)


@router.get(
    "/{habit_id}",
    response_model=HabitRead,
    status_code=status.HTTP_200_OK,
    summary="Get habit",
)
async def get_one_habit(
    habit_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HabitRead:
    """get a habit belonging to the current user"""
    try:
        habit = await habit_service.get_habit(
            session=session, habit_id=habit_id, user_id=current_user.id
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from None
    return HabitRead.model_validate(habit)


@router.patch(
    "/{habit_id}",
    response_model=HabitRead,
    status_code=status.HTTP_200_OK,
    summary="Update habit",
)
async def update_habit(
    data: HabitUpdate,
    habit_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HabitRead:
    """Update a habit owned by the current user."""
    try:
        habit = await habit_service.update_habit(
            session=session, data=data, habit_id=habit_id, user_id=current_user.id
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from None
    return HabitRead.model_validate(habit)


@router.delete(
    "/{habit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete habit",
)
async def delete_habit(
    habit_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a habit owned by the current user."""
    try:
        await habit_service.delete_habit(
            session=session, habit_id=habit_id, user_id=current_user.id
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from None
