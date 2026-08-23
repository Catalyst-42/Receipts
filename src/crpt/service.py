from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.crpt.dao import CrptDao
from src.crpt.schemes import Crpt, CrptList


class CrptService:
    def __init__(self, db: AsyncSession):
        self.crpt_dao = CrptDao(db)

    async def get_all(self) -> CrptList:
        result = await self.crpt_dao.get_all()

        return CrptList(items=[Crpt.model_validate(item) for item in result])

    async def get_by_id(self, crpt_id: UUID7) -> Crpt:
        result = await self.crpt_dao.get_by_id(crpt_id)
        return Crpt.model_validate(result)
