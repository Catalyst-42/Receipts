from pydantic import UUID7
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.employees.model import EmployeesOrm
from src.employees.schemes import EmployeesStats


class EmployeesDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    def build_query(self) -> Select:
        return Select(EmployeesOrm)

    async def get_by_id(self, employee_id: UUID7) -> EmployeesOrm | None:
        stmt = select(EmployeesOrm).where(EmployeesOrm.id == employee_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_retailer_shop_and_name(
        self, retailer_id: UUID7, shop_id: UUID7 | None, name: str
    ) -> EmployeesOrm | None:
        stmt = select(EmployeesOrm).where(
            EmployeesOrm.retailer_id == retailer_id,
            EmployeesOrm.name == name,
        )
        if shop_id:
            stmt = stmt.where(
                EmployeesOrm.shop_id == shop_id,
            )
        else:
            stmt = stmt.where(
                EmployeesOrm.shop_id.is_(shop_id),
            )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_stats(self) -> EmployeesStats:
        stmt = select(func.count()).select_from(EmployeesOrm)

        result = await self.db.execute(stmt)
        return EmployeesStats(count=result.scalar())

    async def create(
        self, retailer_id: UUID7 | None, shop_id: UUID7, name: str
    ) -> EmployeesOrm:
        result = EmployeesOrm(
            retailer_id=retailer_id,
            shop_id=shop_id,
            name=name,
        )

        self.db.add(result)
        await self.db.flush()
        return result
