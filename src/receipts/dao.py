from datetime import datetime, timezone

from pydantic import UUID7
from sqlalchemy import func, select
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.receipts.models import ReceiptsOrm
from decimal import Decimal


class ReceiptsDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_receipts_all(self) -> Sequence[ReceiptsOrm]:
        """Returns all receipts table"""
        stmt = select(ReceiptsOrm)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_receipt_by_fiscal_data(
        self,
        t: datetime,
        s: Decimal,
        fn: int,
        i: int,
        fp: int,
        n: int,
    ) -> ReceiptsOrm | None:
        """Tries to find receipt by its fiscal data"""
        stmt = select(ReceiptsOrm).where(
            ReceiptsOrm.t == t,
            ReceiptsOrm.s == s,
            ReceiptsOrm.fn == fn,
            ReceiptsOrm.i == i,
            ReceiptsOrm.fp == fp,
            ReceiptsOrm.n == n,
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_receipt_total_sum(self) -> Decimal:
        """Counts sum of all cost `s` fields in receipts table"""
        stmt = select(func.sum(ReceiptsOrm.s))
        result = await self.db.execute(stmt)
        return result.scalar()

    async def get_receipt_by_id(self, receipt_id: UUID7) -> ReceiptsOrm | None:
        """Tries to find receipt by its UUID"""
        stmt = select(ReceiptsOrm).where(ReceiptsOrm.id == receipt_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_receipt_count(self) -> int:
        """Returns total number of rows in receipts table"""
        stmt = select(func.count()).select_from(ReceiptsOrm)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def create_receipt(self, crpt_data: dict) -> ReceiptsOrm:
        """Creates new record in receipts table from CRPT receipt data"""
        fiscal_data = crpt_data["fiscalData"]
        code_data = fiscal_data["codeData"]
        fiscal_date = code_data["fiscalDate"]

        t = datetime.fromtimestamp(fiscal_date / 1000, tz=timezone.utc).replace(tzinfo=None)
        s = Decimal(code_data["cost"]) / 100
        fn = code_data["fiscalDriveNumber"]
        i = code_data["fiscalDocumentNumber"]
        fp = code_data["fiscalSign"]
        n = code_data["operationType"]

        result = ReceiptsOrm(
            t=t,
            s=s,
            fn=fn,
            i=i,
            fp=fp,
            n=n,
            crpt_data=crpt_data,
        )

        self.db.add(result)
        await self.db.commit()
        return result
