from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.nds.model import NdsOrm


class NdsDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[NdsOrm]:
        stmt = select(NdsOrm)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, nds_id: int) -> NdsOrm | None:
        stmt = select(NdsOrm).where(NdsOrm.id == nds_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_count(self) -> int:
        stmt = select(func.count()).select_from(NdsOrm)

        result = await self.db.execute(stmt)
        return result.scalar()

    async def create(
        self,
        nds_id: int,
        rate_name: str,
        pf_format: str,
    ) -> NdsOrm:
        result = NdsOrm(
            id=nds_id,
            rate_name=rate_name,
            pf_format=pf_format,
        )

        self.db.add(result)
        await self.db.flush()
        return result
