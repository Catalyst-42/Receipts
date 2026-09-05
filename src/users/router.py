from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import ErrorResponse
from src.users.dependencies import get_user
from src.users.schemes import AccessToken, Login, Register, User, Passwords
from src.users.service import UsersService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_users_service(db: AsyncSession = Depends(get_db)) -> UsersService:
    return UsersService(db)


@router.post(
    "/login",
    response_model=AccessToken,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    },
)
async def login(
    login: Login,
    users_service: UsersService = Depends(get_users_service),
) -> AccessToken:
    """Authorize user by it's login and password"""
    return await users_service.login(login)


@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        409: {"model": ErrorResponse, "description": "Username already exists"},
    },
)
async def register(
    register: Register,
    users_service: UsersService = Depends(get_users_service),
) -> User:
    """Register a new user by login and password"""
    return await users_service.register(register)


@router.post(
    "/change-password",
    response_model=User,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    },
)
async def change_password(
    passwords: Passwords,
    user: User = Depends(get_user),
    users_service: UsersService = Depends(get_users_service),
) -> AccessToken:
    """Change user password to a new one"""
    return await users_service.change_password(user, passwords)


@router.get(
    "/me",
    response_model=User,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    },
)
async def get_current_user(
    user: User = Depends(get_user),
) -> User:
    """Get current user by auth cridentials"""
    return user
