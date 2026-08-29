from fastapi import HTTPException, status
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.receipts.dao import ReceiptsDao
from src.receipts.schemes import FiscalFields, Receipt
from src.core.transactional import transactional
from src.core.schemes import Count, Sum
from src.items.schemes import ItemList, Item


class ReceiptsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.receipts_dao = ReceiptsDao(db)

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
        return ItemList(items=[Item.model_validate(item) for item in result.items])

    async def get_count(self) -> Count:
        result = await self.receipts_dao.get_count()
        return Count(total=result)

    async def get_sum(self) -> Sum:
        result = await self.receipts_dao.get_sum()
        return Sum(sum=result)

    @transactional
    async def create(
        self,
        crpt_id: UUID7,
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
                crpt_id,
                shop_id,
                employee_id,
                fiscal_fields.t_datetime,
                fiscal_fields.s,
                fiscal_fields.fn,
                fiscal_fields.i,
                fiscal_fields.fp,
                fiscal_fields.n,
            )

        return Receipt.model_validate(result)
