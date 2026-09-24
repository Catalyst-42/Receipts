from pydantic import UUID7
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.operators.model import OperatorsOrm
from src.operators.schemes import OperatorsStats


class OperatorsDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    def build_query(self) -> Select:
        return Select(OperatorsOrm)

    async def get_by_id(self, operator_id: UUID7) -> OperatorsOrm | None:
        stmt = select(OperatorsOrm).where(OperatorsOrm.id == operator_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_retailer_shop_and_name(
        self, retailer_id: UUID7, shop_id: UUID7 | None, name: str
    ) -> OperatorsOrm | None:
        stmt = select(OperatorsOrm).where(
            OperatorsOrm.retailer_id == retailer_id,
            OperatorsOrm.name == name,
        )
        if shop_id:
            stmt = stmt.where(
                OperatorsOrm.shop_id == shop_id,
            )
        else:
            stmt = stmt.where(
                OperatorsOrm.shop_id.is_(shop_id),
            )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_stats(self) -> OperatorsStats:
        stmt = select(func.count()).select_from(OperatorsOrm)

        result = await self.db.execute(stmt)
        return OperatorsStats(count=result.scalar())

    async def create(
        self, retailer_id: UUID7 | None, shop_id: UUID7, name: str
    ) -> OperatorsOrm:
        result = OperatorsOrm(
            retailer_id=retailer_id,
            shop_id=shop_id,
            name=name,
        )

        self.db.add(result)
        await self.db.flush()
        return result
