from fastapi import APIRouter, Depends

from src.core.schemes import ErrorResponse
from src.receipts.schemes import ReceiptList
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
    response_model=ReceiptList,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        404: {"model": ErrorResponse, "description": "User not found"},
    },
)
async def get_user_profile(
    username: str,
    user: User = Depends(get_user),
    service: UsersService = Depends(get_users_service),
) -> ReceiptList:
    """Get list of user receipts"""
    return await service.get_receipts(user, username)


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
