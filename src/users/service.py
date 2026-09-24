from fastapi import HTTPException, status
from fastapi_pagination import Page
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.jwt import create_access_token
from src.core.security import hash_password, verify_password
from src.core.transactional import transactional
from src.receipts.filters import ReceiptsFilters
from src.receipts.schemes import Receipt
from src.receipts.service import ReceiptsService
from src.users.dao import UsersDao
from src.users.schemes import AccessToken, Login, Passwords, Register, User


class UsersService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users_dao = UsersDao(db)
        self.receipts_service = ReceiptsService(db)

    async def get_by_id(self, user_id: UUID7) -> User:
        result = await self.users_dao.get_by_id(user_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return User.model_validate(result)

    async def get_by_username(self, user: User, username: str) -> User:
        result = await self.users_dao.get_by_username(username)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if not user.is_admin and user.id != result.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have no rights to view this user",
            )

        return User.model_validate(result)

    @transactional
    async def register(self, register: Register) -> User:
        user = await self.users_dao.get_by_username(register.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This username already taken",
            )

        hashed_password = hash_password(register.password)
        result = await self.users_dao.create(
            username=register.username,
            hashed_password=hashed_password,
        )

        return User.model_validate(result)

    async def login(self, login: Login) -> AccessToken:
        result = await self.users_dao.get_by_username(login.username)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        if not verify_password(login.password, result.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        access_token = create_access_token(result.id)

        return AccessToken(access_token=access_token)

    @transactional
    async def change_password(self, user: User, passwords: Passwords) -> User:
        result = await self.users_dao.get_by_id(user.id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        if not verify_password(passwords.old_password, result.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        hashed_password = hash_password(passwords.new_password)
        result = await self.users_dao.update_password(
            user_id=user.id,
            hashed_password=hashed_password,
        )
        return User.model_validate(result)

    async def get_receipts(
        self,
        user: User,
        username: str,
        filters: ReceiptsFilters,
    ) -> Page[Receipt]:
        owner = await self.users_dao.get_by_username(username)
        if not owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if not user.is_admin and user.id != owner.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have no rights to view this user",
            )

        return await self.receipts_service.get_by_owner(owner.id, filters)
