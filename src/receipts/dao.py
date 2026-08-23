from datetime import datetime, timezone
from decimal import Decimal
from typing import Sequence

from pydantic import UUID7
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.receipts.model import ReceiptsOrm


class ReceiptsDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[ReceiptsOrm]:
        stmt = select(ReceiptsOrm)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, receipt_id: UUID7) -> ReceiptsOrm | None:
        stmt = select(ReceiptsOrm).where(ReceiptsOrm.id == receipt_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_fiscal_fields(
        self,
        t: datetime,
        s: Decimal,
        fn: int,
        i: int,
        fp: int,
        n: int,
    ) -> ReceiptsOrm | None:
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

    async def create_receipt(self, crpt_data: dict) -> ReceiptsOrm:
        fiscal_data = crpt_data["fiscalData"]
        code_data = fiscal_data["codeData"]
        fiscal_date = code_data["fiscalDate"]

        t = datetime.fromtimestamp(fiscal_date / 1000, tz=timezone.utc).replace(
            tzinfo=None
        )
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

    async def get_total_sum(self) -> Decimal:
        stmt = select(func.sum(ReceiptsOrm.s))
        result = await self.db.execute(stmt)
        return result.scalar()

    async def get_count(self) -> int:
        stmt = select(func.count()).select_from(ReceiptsOrm)
        result = await self.db.execute(stmt)
        return result.scalar()
