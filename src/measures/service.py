from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemes import Count
from src.measures.dao import MeasuresDao
from src.measures.schemes import Measure, MeasureList


class MeasuresService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.measures_dao = MeasuresDao(db)

    async def get_all(self) -> MeasureList:
        result = await self.measures_dao.get_all()

        return MeasureList(items=[Measure.model_validate(item) for item in result])

    async def get_by_id(self, measure_id: int) -> Measure:
        result = await self.measures_dao.get_by_id(measure_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Measure with id {measure_id} not found",
            )

        return Measure.model_validate(result)

    async def get_count(self) -> Count:
        result = await self.measures_dao.get_count()
        return Count(total=result)
