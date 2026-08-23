from sqlalchemy.ext.asyncio import AsyncSession
from src.measures.dao import MeasuresDao

from src.measures.schemes import Measure, MeasureList

class MeasuresService:
    def __init__(self, db: AsyncSession):
        self.measures_dao = MeasuresDao(db)

    async def get_all(self) -> MeasureList:
        result = await self.measures_dao.get_all()

        return MeasureList(items=[Measure.model_validate(item) for item in result])

    async def get_by_id(self, crpt_id: int) -> Measure:
        result = await self.measures_dao.get_by_id(crpt_id)
        return Measure.model_validate(result)
