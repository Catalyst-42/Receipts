from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from src.payments.model import PaymentsOrm


class PaymentsDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[PaymentsOrm]:
        stmt = select(PaymentsOrm)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, payment_id: int) -> PaymentsOrm | None:
        stmt = select(PaymentsOrm).where(PaymentsOrm.id == payment_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        payment_id: int,
        description: str,
        pf_format: str,
    ) -> PaymentsOrm:
        result = PaymentsOrm(
            id=payment_id,
            description=description,
            pf_format=pf_format,
        )

        self.db.add(result)
        await self.db.flush()
        return result
