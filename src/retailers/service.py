from fastapi import HTTPException, status
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemes import Count
from src.core.transactional import transactional
from src.items.schemes import ItemList
from src.items.service import ItemsService
from src.retailers.dao import RetailersDao
from src.retailers.schemes import Retailer, RetailerList


class RetailersService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.retailers_dao = RetailersDao(db)
        self.items_service = ItemsService(db)

    async def get_all(self) -> RetailerList:
        result = await self.retailers_dao.get_all()

        return RetailerList(items=[Retailer.model_validate(item) for item in result])

    async def get_by_id(self, retailer_id: UUID7) -> Retailer:
        result = await self.retailers_dao.get_by_id(retailer_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Retailer id {retailer_id} not found ",
            )

        return Retailer.model_validate(result)

    async def get_count(self) -> Count:
        result = await self.retailers_dao.get_count()
        return Count(total=result)

    async def get_items(self, retailer_id: UUID7) -> ItemList:
        result = await self.items_service.get_all_by_retailer_id(retailer_id)
        return result

    @transactional
    async def create(self, inn: str, name: str) -> Retailer:
        result = await self.retailers_dao.get_by_inn(inn)
        if not result:
            result = await self.retailers_dao.create(inn, name)

        return Retailer.model_validate(result)
