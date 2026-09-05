from pydantic import UUID7
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.model import UsersOrm


class UsersDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: UUID7) -> UsersOrm | None:
        stmt = select(UsersOrm).where(UsersOrm.id == user_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> UsersOrm | None:
        stmt = select(UsersOrm).where(UsersOrm.username == username)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        username: str,
        hashed_password: str,
        is_admin: bool = False,
    ) -> UsersOrm:
        result = UsersOrm(
            username=username,
            hashed_password=hashed_password,
            is_admin=is_admin,
        )
        self.db.add(result)

        await self.db.flush()
        return result

    async def update_password(self, user_id: UUID7, hashed_password: str) -> UsersOrm:
        stmt = (
            update(UsersOrm)
            .where(UsersOrm.id == user_id)
            .values(hashed_password=hashed_password)
            .returning(UsersOrm)
        )

        result = await self.db.execute(stmt)
        await self.db.flush()
        return result.scalar_one()
