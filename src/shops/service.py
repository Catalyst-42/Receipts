from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.transactional import transactional
from src.items.schemes import ItemList
from src.items.service import ItemsService
from src.shops.dao import ShopsDao
from src.shops.filters import ShopsFilters
from src.shops.schemes import Shop, ShopList, ShopsStats


class ShopsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.shops_dao = ShopsDao(db)
        self.items_service = ItemsService(db)

    async def get(self, filters: ShopsFilters) -> Page[Shop]:
        stmt = self.shops_dao.build_query()
        stmt = filters.filter(stmt)
        stmt = filters.sort(stmt)

        return await apaginate(self.db, stmt)

    async def get_all(self) -> ShopList:
        result = await self.shops_dao.get_all()

        return ShopList(items=[Shop.model_validate(item) for item in result])

    async def get_by_id(self, shop_id: UUID7) -> Shop:
        result = await self.shops_dao.get_by_id(shop_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shop with id {shop_id} not found ",
            )

        return Shop.model_validate(result)

    async def get_stats(self) -> ShopsStats:
        return await self.shops_dao.get_stats()

    async def get_items(self, shop_id: UUID7) -> ItemList:
        result = await self.items_service.get_all_by_shop_id(shop_id)
        return result

    @transactional
    async def create(self, retailer_id: UUID7, address: str | None) -> Shop:
        result = await self.shops_dao.get_by_retailer_id_and_address(
            retailer_id, address
        )
        if not result:
            result = await self.shops_dao.create(retailer_id, address)

        return Shop.model_validate(result)
