from pydantic import UUID7
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.retailers.models import ShopsOrm


class RetailersDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, retailer_id: UUID7) -> ShopsOrm | None:
        stmt = select(ShopsOrm).where(ShopsOrm.id == retailer_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        inn: str,
        name: str,
    ) -> ShopsOrm:
        result = ShopsOrm(
            inn=inn,
            name=name,
        )

        self.db.add(result)
        await self.db.commit()
        return result
