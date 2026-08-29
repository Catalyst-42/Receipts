from sqlalchemy.ext.asyncio import AsyncSession
from src.nds.dao import NdsDao

from src.nds.schemes import Nds, NdsList
from fastapi import HTTPException, status
from src.core.schemes import Count

class NdsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.nds_dao = NdsDao(db)

    async def get_all(self) -> NdsList:
        result = await self.nds_dao.get_all()

        return NdsList(items=[Nds.model_validate(item) for item in result])

    async def get_by_id(self, nds_id: int) -> Nds:
        result = await self.nds_dao.get_by_id(nds_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nds rate with id {nds_id} not found "
            )

        return Nds.model_validate(result)

    async def get_count(self) -> Count:
        result = await self.nds_dao.get_count()
        return Count(total=result)