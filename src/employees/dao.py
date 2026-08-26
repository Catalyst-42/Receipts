from pydantic import UUID7

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.employees.model import EmployeesOrm


class EmployeesDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, employee_id: UUID7) -> EmployeesOrm | None:
        stmt = select(EmployeesOrm).where(EmployeesOrm.id == employee_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_shop_and_name(
        self, shop_id: UUID7, name: str
    ) -> EmployeesOrm | None:
        stmt = select(EmployeesOrm).where(
            EmployeesOrm.shop_id == shop_id,
            EmployeesOrm.name == name,
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, shop_id: UUID7, name: str) -> EmployeesOrm:
        result = EmployeesOrm(
            shop_id=shop_id,
            name=name,
        )

        self.db.add(result)
        await self.db.commit()
        return result
