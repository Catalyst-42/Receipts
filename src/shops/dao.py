from pydantic import UUID7
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.shops.model import ShopsOrm


class ShopsDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, shop_id: UUID7) -> ShopsOrm | None:
        stmt = select(ShopsOrm).where(ShopsOrm.id == shop_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_retailer_id_and_address(
        self, retailer_id: UUID7, address: str | None
    ) -> ShopsOrm | None:
        stmt = select(ShopsOrm).where(
            ShopsOrm.retailer_id == retailer_id,
        )
        if address is None:
            stmt = stmt.where(ShopsOrm.address.is_(None))
        else:
            stmt = stmt.where(ShopsOrm.address == address)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        retailer_id: UUID7,
        address: str | None,
    ) -> ShopsOrm:
        result = ShopsOrm(
            retailer_id=retailer_id,
            address=address,
        )

        self.db.add(result)
        await self.db.flush()
        return result
