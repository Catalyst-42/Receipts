from decimal import Decimal
from typing import Any

from fastapi import HTTPException, status
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemes import Average, CountDistinct, Count, Median
from src.core.transactional import transactional
from src.items.dao import ItemsDao
from src.items.schemes import Item, ItemList


class ItemsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.items_dao = ItemsDao(db)

    async def get_all(self) -> ItemList:
        result = await self.items_dao.get_all()
        return ItemList(items=[Item.model_validate(item) for item in result])

    async def get_by_receipt_id(self, receipt_id: UUID7) -> ItemList:
        result = await self.items_dao.get_by_receipt_id(receipt_id)
        return ItemList(items=[Item.model_validate(item) for item in result])

    async def get_by_id(self, item_id: UUID7) -> Item:
        result = await self.items_dao.get_by_id(item_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found",
            )

        return Item.model_validate(result)

    async def get_count(self) -> Count:
        result = await self.items_dao.get_count()
        return Count(total=result)

    async def get_count_distinct(self) -> CountDistinct:
        distinct = await self.items_dao.get_count_distinct()
        count = await self.items_dao.get_count()
        return CountDistinct(total=distinct, selectivity=distinct / count)

    async def get_avg_price(self) -> Count:
        result = await self.items_dao.get_avg_price()
        return Average(avg=result)

    async def get_median_price(self) -> Median:
        result = await self.items_dao.get_median_price()
        return Median(median=result)

    @transactional
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
    ) -> Item:
        result = await self.items_dao.create(
            receipt_id,
            name,
            price,
            total,
            quantity,
            measure,
            nds,
            payment,
            product,
        )

        return Item.model_validate(result)

    @transactional
    async def create_many(self, receipt_id: UUID7, items: list[Any]) -> ItemList:
        result = await self.items_dao.get_by_receipt_id(receipt_id)
        if not result:
            result = await self.items_dao.create_many(receipt_id, items)

        return ItemList(items=[Item.model_validate(item) for item in result])
