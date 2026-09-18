from fastapi import APIRouter, Depends, status

from src.core.schemes import ErrorResponse
from src.users.dependencies import get_user, get_users_service
from src.users.schemes import AccessToken, Login, Passwords, Register, User
from src.users.service import UsersService

router = APIRouter(prefix="/auth", tags=["Authentication"])


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
