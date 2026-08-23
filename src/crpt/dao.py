from typing import Sequence

from pydantic import UUID7
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crpt.models import CrptOrm


class CrptDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[CrptOrm]:
        stmt = select(CrptOrm)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, crpt_id: UUID7) -> CrptOrm | None:
        stmt = select(CrptOrm).where(CrptOrm.id == crpt_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, dump: dict) -> CrptOrm:
        result = CrptOrm(
            dump=dump,
        )

        self.db.add(result)
        await self.db.commit()
        return result
