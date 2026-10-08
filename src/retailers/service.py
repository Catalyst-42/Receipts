from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate
from httpx import AsyncClient, ConnectError, HTTPError
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.core.transactional import transactional
from src.items.filters import ItemsFilters
from src.items.schemes import Item
from src.items.service import ItemsService
from src.retailers.dao import RetailersDao
from src.retailers.filters import RetailersFilters
from src.retailers.schemes import Retailer, RetailerList, RetailersStats


class RetailersService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.retailers_dao = RetailersDao(db)
        self.items_service = ItemsService(db)

    async def get_name_by_inn(self, inn: str) -> str:
        client_kwargs = {
            "timeout": 10,
            "headers": {
                "content-type": "application/json",
                "accept": "application/json",
                "Authorization": f"Token {settings.dadata_token}",
                "X-Secret": settings.dadata_secret,
            },
        }

        try:
            async with AsyncClient(**client_kwargs) as dadata_client:
                response = await dadata_client.post(
                    "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party",
                    json={"query": inn},
                )
                response.raise_for_status()
                data = response.json()

        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Cannot reach the DaData API by timeout",
            )

        except ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No internet connection",
            )

        suggestions = data.get("suggestions", [])
        if not suggestions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company with INN {inn} not found",
            )

        return suggestions[0]["value"]

    async def get(self, filters: RetailersFilters) -> Page[Retailer]:
        stmt = self.retailers_dao.build_query()
        stmt = filters.filter(stmt)
        stmt = filters.sort(stmt)

        return await apaginate(self.db, stmt)

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

    async def get_stats(self) -> RetailersStats:
        return await self.retailers_dao.get_stats()

    async def get_items(
        self, retailer_id: UUID7, filters: ItemsFilters = None
    ) -> Page[Item]:
        return await self.items_service.get_by_retailer_id(retailer_id, filters)

    @transactional
    async def create(self, inn: str, name: str) -> Retailer:
        result = await self.retailers_dao.get_by_inn(inn)
        if not result:
            name = await self.get_name_by_inn(inn)
            result = await self.retailers_dao.create(inn, name)

        return Retailer.model_validate(result)
