from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from src.products.model import ProductsOrm


class ProductsDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[ProductsOrm]:
        stmt = select(ProductsOrm)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, product_id: int) -> ProductsOrm | None:
        stmt = select(ProductsOrm).where(ProductsOrm.id == product_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        payment_id: int,
        description: str,
        pf_format: str,
    ) -> ProductsOrm:
        result = ProductsOrm(
            id=payment_id,
            description=description,
            pf_format=pf_format,
        )

        self.db.add(result)
        await self.db.flush()
        return result
