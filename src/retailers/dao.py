from pydantic import UUID7
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.retailers.model import RetailersOrm


class RetailersDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, retailer_id: UUID7) -> RetailersOrm | None:
        stmt = select(RetailersOrm).where(RetailersOrm.id == retailer_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_inn(self, inn: str) -> RetailersOrm | None:
        stmt = select(RetailersOrm).where(
            RetailersOrm.inn == inn,
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_count(self) -> int:
        stmt = select(func.count()).select_from(RetailersOrm)

        result = await self.db.execute(stmt)
        return result.scalar()

    async def create(
        self,
        inn: str,
        name: str,
    ) -> RetailersOrm:
        result = RetailersOrm(
            inn=inn,
            name=name,
        )

        self.db.add(result)
        await self.db.flush()
        return result
