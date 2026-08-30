from fastapi import HTTPException, status
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemes import Count
from src.core.transactional import transactional
from src.employees.dao import EmployeesDao
from src.employees.schemes import Employee, EmployeeList


class EmployeesService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.employees_dao = EmployeesDao(db)

    async def get_all(self) -> EmployeeList:
        result = await self.employees_dao.get_all()

        return EmployeeList(items=[Employee.model_validate(item) for item in result])

    async def get_by_id(self, employee_id: UUID7) -> Employee:
        result = await self.employees_dao.get_by_id(employee_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with id {employee_id} not found",
            )

        return Employee.model_validate(result)

    async def get_count(self) -> Count:
        result = await self.employees_dao.get_count()
        return Count(total=result)

    @transactional
    async def create(
        self, retailer_id: UUID7, shop_id: UUID7 | None, name: str
    ) -> Employee:
        result = await self.employees_dao.get_by_retailer_shop_and_name(
            retailer_id, shop_id, name
        )
        if not result:
            result = await self.employees_dao.create(retailer_id, shop_id, name)

        return Employee.model_validate(result)
