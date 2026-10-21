from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import EmailAlreadyExists
from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserRead
from app.services.auth import authenticate_user, get_user_by_email, register_user
from app.core.security import create_access_token 

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    data: UserCreate, session: AsyncSession = Depends(get_db)
) -> UserRead:
    """Register a new user.

    Creates a user with the given email and password.
    Returns 409 if the email is already registered.
    """
    try:
        user = await register_user(session, data)
    except EmailAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        ) from None
    return UserRead.model_validate(user)


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login to get access token",
)
async def login(
    session: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await authenticate_user(
        session, email=form_data.username, password=form_data.password
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    elif user.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")