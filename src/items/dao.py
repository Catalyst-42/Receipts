from decimal import Decimal
from typing import Sequence

from pydantic import UUID7
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.items.model import ItemsOrm
from src.items.schemes import ItemsStats
from src.receipts.model import ReceiptsOrm


class ItemsDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[ItemsOrm]:
        stmt = select(ItemsOrm)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_all_by_retailer_id(self, retailer_id: UUID7) -> Sequence[ItemsOrm]:
        stmt = (
            select(ItemsOrm)
            .join(ItemsOrm.receipt)
            .where(ReceiptsOrm.retailer_id == retailer_id)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_all_by_shop_id(self, shop_id: UUID7) -> Sequence[ItemsOrm]:
        stmt = (
            select(ItemsOrm)
            .join(ItemsOrm.receipt)
            .where(ReceiptsOrm.shop_id == shop_id)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, item_id: UUID7) -> ItemsOrm | None:
        stmt = select(ItemsOrm).where(ItemsOrm.id == item_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_receipt_id(self, receipt_id: UUID7) -> Sequence[ItemsOrm]:
        stmt = select(ItemsOrm).where(ItemsOrm.receipt_id == receipt_id)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_stats(self) -> ItemsStats:
        stmt = select(
            func.count(ItemsOrm.id),
            func.count(func.distinct(ItemsOrm.name)),
            func.avg(ItemsOrm.price),
            func.percentile_cont(0.5)
            .within_group(ItemsOrm.price.desc())
            .label("median"),
        )

        result = await self.db.execute(stmt)
        count, distinct, average, median = result.one()
        return ItemsStats(
            count=count,
            distinct=distinct,
            selectivity=distinct / count if count else 0,
            average=average,
            median=median,
        )

    async def create(
        self,
        receipt_id: UUID7,
        name: str | None,
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
        await self.db.flush()
        return result

    async def create_many(
        self, receipt_id: UUID7, items: list[dict]
    ) -> Sequence[ItemsOrm]:
        items = [ItemsOrm(receipt_id=receipt_id, **item) for item in items]

        self.db.add_all(items)
        await self.db.flush()
        return items
