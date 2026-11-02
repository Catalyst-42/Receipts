from datetime import datetime
from decimal import Decimal
from typing import Sequence
from unittest import result

from pydantic import UUID7
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.receipts.model import ReceiptsOrm
from src.receipts.schemas import ReceiptsStats
from src.transactions.enums import TransactionType
from src.transactions.model import TransactionsOrm


class TransactionsDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, transaction_id: UUID7) -> TransactionsOrm:
        stmt = select(TransactionsOrm).where(TransactionsOrm.id == transaction_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        owner_id: UUID7,
        receipt_id: UUID7,
        total: Decimal,
        type: TransactionType,
    ) -> TransactionsOrm:
        result = TransactionsOrm(
            owner_id=owner_id,
            receipt_id=receipt_id,
            total=total,
            type=type,
        )

        self.db.add(result)
        await self.db.flush()
        return result
