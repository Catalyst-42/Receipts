from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.transactional import transactional
from src.operators.dao import OperatorsDao
from src.operators.filters import OperatorsFilters
from src.operators.schemes import Operator, OperatorList, OperatorsStats


class OperatorsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.operators_dao = OperatorsDao(db)

    async def get(self, filters: OperatorsFilters) -> Page[Operator]:
        stmt = self.operators_dao.build_query()
        stmt = filters.filter(stmt)
        stmt = filters.sort(stmt)

        return await apaginate(self.db, stmt)

    async def get_all(self) -> OperatorList:
        result = await self.operators_dao.get_all()

        return OperatorList(items=[Operator.model_validate(item) for item in result])

    async def get_by_id(self, operator_id: UUID7) -> Operator:
        result = await self.operators_dao.get_by_id(operator_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Operator with id {operator_id} not found",
            )

        return Operator.model_validate(result)

    async def get_stats(self) -> OperatorsStats:
        return await self.operators_dao.get_stats()

    @transactional
    async def create(
        self, retailer_id: UUID7, shop_id: UUID7 | None, name: str
    ) -> Operator:
        result = await self.operators_dao.get_by_retailer_shop_and_name(
            retailer_id, shop_id, name
        )
        if not result:
            result = await self.operators_dao.create(retailer_id, shop_id, name)

        return Operator.model_validate(result)
