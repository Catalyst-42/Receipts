from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination import Page

from src.receipts.schemes import Receipt
from src.core.schemes import ErrorResponse
from src.receipts.filters import ReceiptFilter
from src.users.dependencies import get_user, get_users_service
from src.users.schemes import User
from src.users.service import UsersService

router = APIRouter(prefix="/users", tags=["Users"])


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


@router.get(
    "/{username}/receipts",
    response_model=Page[Receipt],
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "User not found"},
    },
)
async def get_user_receipts(
    username: str,
    user: User = Depends(get_user),
    filters: ReceiptFilter = FilterDepends(ReceiptFilter),
    service: UsersService = Depends(get_users_service),
) -> Page[Receipt]:
    """Get list of user receipts"""
    return await service.get_receipts(user, username, filters)

@router.get(
    "/{username}",
    response_model=User,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        403: {
            "model": ErrorResponse,
            "description": "You have no rights to view this user",
        },
        404: {"model": ErrorResponse, "description": "User not found"},
    },
)
async def get_user_profile(
    username: str,
    user: User = Depends(get_user),
    service: UsersService = Depends(get_users_service),
) -> User:
    """Get current user by username"""
    return await service.get_by_username(user, username)
