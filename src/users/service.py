from fastapi import HTTPException, status
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import hash_password, verify_password
from src.core.transactional import transactional
from src.users.dao import UsersDao
from src.users.schemes import User, Login, AccessToken, Passwords, Register
from src.core.jwt import create_access_token


class UsersService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users_dao = UsersDao(db)

    async def get_by_id(self, user_id: UUID7) -> User:
        result = await self.users_dao.get_by_id(user_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return User.model_validate(result)

    async def get_by_username(self, username: str) -> User:
        result = await self.users_dao.get_by_username(username)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
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
