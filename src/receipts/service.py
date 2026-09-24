from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.transactional import transactional
from src.items.schemes import Item, ItemList
from src.receipts.dao import ReceiptsDao
from src.receipts.filters import ReceiptsFilters, ReceiptsStatsFilters
from src.receipts.schemes import FiscalFields, Receipt, ReceiptsStats


class ReceiptsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.receipts_dao = ReceiptsDao(db)

    async def get(self, filters: ReceiptsFilters) -> Page[Receipt]:
        stmt = self.receipts_dao.build_query()
        stmt = filters.filter(stmt)
        stmt = filters.sort(stmt)

        return await apaginate(self.db, stmt)

    async def get_by_owner(
        self, owner_id: UUID7, filters: ReceiptsFilters
    ) -> Page[Receipt]:
        stmt = self.receipts_dao.build_query_by_owner(owner_id=owner_id)
        stmt = filters.filter(stmt)
        stmt = filters.sort(stmt)

        return await apaginate(self.db, stmt)

    async def get_stats_by_owner(
        self,
        owner_id: UUID7,
        filters: ReceiptsStatsFilters,
    ) -> ReceiptsStats:
        base = self.receipts_dao.build_query_by_owner(owner_id=owner_id)
        base = filters.filter(base)

        return await self.receipts_dao.get_stats(base)

    async def get_stats(self) -> ReceiptsStats:
        return await self.receipts_dao.get_stats()

    async def get_by_id(self, receipt_id: UUID7) -> Receipt:
        result = await self.receipts_dao.get_by_id(receipt_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Receipt with id {receipt_id} was not found",
            )

        return Receipt.model_validate(result)

    async def get_by_fiscal_fields(self, fiscal_fields: FiscalFields) -> Receipt:
        result = await self.receipts_dao.get_by_fiscal_fields(
            fiscal_fields.t_datetime,
            fiscal_fields.s,
            fiscal_fields.fn,
            fiscal_fields.i,
            fiscal_fields.fp,
            fiscal_fields.n,
        )
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receipt was not found by fiscal data",
            )

        return Receipt.model_validate(result)

    async def get_items(self, receipt_id: UUID7) -> ItemList:
        result = await self.receipts_dao.get_by_id(receipt_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Receipt with id {receipt_id} was not found",
            )
        return ItemList(items=[Item.model_validate(item) for item in result.items])

    @transactional
    async def create(
        self,
        owner_id: UUID7,
        crpt_id: UUID7,
        retailer_id: UUID7,
        shop_id: UUID7 | None,
        employee_id: UUID7 | None,
        fiscal_fields: FiscalFields,
    ) -> Receipt:
        result = await self.receipts_dao.get_by_fiscal_fields(
            fiscal_fields.t_datetime,
            fiscal_fields.s,
            fiscal_fields.fn,
            fiscal_fields.i,
            fiscal_fields.fp,
            fiscal_fields.n,
        )
        if not result:
            result = await self.receipts_dao.create(
                owner_id=owner_id,
                crpt_id=crpt_id,
                retailer_id=retailer_id,
                shop_id=shop_id,
                employee_id=employee_id,
                t=fiscal_fields.t_datetime,
                s=fiscal_fields.s,
                fn=fiscal_fields.fn,
                i=fiscal_fields.i,
                fp=fiscal_fields.fp,
                n=fiscal_fields.n,
            )

        return Receipt.model_validate(result)
