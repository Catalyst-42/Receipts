from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import Count, ErrorResponse
from src.employees.schemes import Employee, EmployeeId
from src.employees.service import EmployeesService
from src.users.dependencies import get_user
from src.users.schemes import User

router = APIRouter(prefix="/employees", tags=["Employees"])


def get_employees_service(db: AsyncSession = Depends(get_db)):
    return EmployeesService(db)


@router.get(
    "/stats/count",
    response_model=Count,
)
async def get_employees_count(
    employees_service: EmployeesService = Depends(get_employees_service),
) -> Count:
    """Returns total count of employees in database"""
    return await employees_service.get_count()


@router.get(
    "/{employee_id}",
    response_model=Employee,
    responses={
        404: {"model": ErrorResponse, "description": "Employee not found"},
    },
)
async def get_employee(
    request: Annotated[EmployeeId, Path()],
    user: User = Depends(get_user),
    employees_service: EmployeesService = Depends(get_employees_service),
) -> Employee:
    """Returns employee by its unique"""
    result = await employees_service.get_by_id(user, request.employee_id)
    return result
