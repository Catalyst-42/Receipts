from decimal import Decimal
from typing import Any

from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.transactional import transactional
from src.items.dao import ItemsDao
from src.items.filters import ItemsFilters
from src.items.schemes import Item, ItemList, ItemsStats


class ItemsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.items_dao = ItemsDao(db)

    async def get(self, filters: ItemsFilters) -> Page[Item]:
        stmt = self.items_dao.build_query()
        stmt = filters.filter(stmt)
        stmt = filters.sort(stmt)

        return await apaginate(self.db, stmt)

    async def get_all(self) -> ItemList:
        result = await self.items_dao.get_all()
        return ItemList(items=[Item.model_validate(item) for item in result])

    async def get_all_by_retailer_id(self, retailer_id: UUID7) -> ItemList:
        result = await self.items_dao.get_all_by_retailer_id(retailer_id)
        return ItemList(items=[Item.model_validate(item) for item in result])

    async def get_all_by_shop_id(self, shop_id: UUID7) -> ItemList:
        result = await self.items_dao.get_all_by_shop_id(shop_id)
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

    async def get_stats(self) -> ItemsStats:
        return await self.items_dao.get_stats()

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
