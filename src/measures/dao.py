from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.measures.models import MeasuresOrm


class MeasuresDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[MeasuresOrm]:
        stmt = select(MeasuresOrm)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, measure_id: int) -> MeasuresOrm | None:
        stmt = select(MeasuresOrm).where(MeasuresOrm.id == measure_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        measure_id: int,
        description: str,
        pf_format: str,
    ) -> MeasuresOrm:
        result = MeasuresOrm(
            id=measure_id,
            description=description,
            pf_format=pf_format,
        )

        self.db.add(result)
        await self.db.commit()
        return result
