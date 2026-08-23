from decimal import Decimal

from pydantic import UUID7
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.items.model import ItemsOrm


class ItemsDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, item_id: UUID7) -> ItemsOrm | None:
        stmt = select(ItemsOrm).where(ItemsOrm.id == item_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        receipt_id: UUID7,
        name: str,
        price: Decimal,
        total: Decimal,
        quantity: float,
        measure: int,
        nds: int,
        payment: int,
        product: int,
    ) -> ItemsOrm:
        result = ItemsOrm(
            receipt_id=receipt_id,
            name=name,
            price=price,
            total=total,
            quantity=quantity,
            measure=measure,
            nds=nds,
            payment=payment,
            product=product,
        )

        self.db.add(result)
        await self.db.commit()
        return result
