from datetime import datetime
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

    async def get_count(self) -> int:
        stmt = select(func.count()).select_from(ReceiptsOrm)

        result = await self.db.execute(stmt)
        return result.scalar()

    async def get_sum(self) -> Decimal:
        stmt = select(func.sum(ReceiptsOrm.s))

        result = await self.db.execute(stmt)
        return result.scalar()

    async def create(
        self,
        crpt_id: UUID7,
        shop_id: UUID7 | None,
        employee_id: UUID7 | None,
        t: datetime,
        s: Decimal,
        fn: int,
        i: int,
        fp: int,
        n: int,
    ) -> ReceiptsOrm:
        result = ReceiptsOrm(
            crpt_id=crpt_id,
            shop_id=shop_id,
            employee_id=employee_id,
            t=t,
            s=s,
            fn=fn,
            i=i,
            fp=fp,
            n=n,
        )

        self.db.add(result)
        await self.db.flush()
        return result
