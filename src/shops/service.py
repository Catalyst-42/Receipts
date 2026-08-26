from fastapi import HTTPException, status
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.shops.dao import ShopsDao
from src.shops.schemes import Shop, ShopList
from src.core.transactional import transactional


class ShopsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.shops_dao = ShopsDao(db)

    async def get_all(self) -> ShopList:
        result = await self.shops_dao.get_all()

        return ShopList(items=[Shop.model_validate(item) for item in result])

    async def get_by_id(self, shop_id: int) -> Shop:
        result = await self.shops_dao.get_by_id(shop_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shop with id {shop_id} not found ",
            )

        return Shop.model_validate(result)

    @transactional
    async def create(self, retailer_id: UUID7, address: str | None) -> Shop:
        result = await self.shops_dao.get_by_retailer_id_and_address(
            retailer_id, address
        )
        if not result:
            result = await self.shops_dao.create(retailer_id, address)

        return Shop.model_validate(result)
