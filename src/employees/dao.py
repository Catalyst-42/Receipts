from pydantic import UUID7

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.employees.models import EmployeesOrm


class EmployeesDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, employee_id: UUID7) -> EmployeesOrm | None:
        stmt = select(EmployeesOrm).where(EmployeesOrm.id == employee_id)

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
