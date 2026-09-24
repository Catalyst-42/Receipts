from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter

from src.core.schemes import ErrorResponse
from src.employees.dependencies import get_employees_service
from src.employees.schemes import Employee, EmployeeId, EmployeesStats
from src.employees.service import EmployeesService

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get(
    "/stats",
    response_model=EmployeesStats,
)
async def get_employees_stats(
    employees_service: EmployeesService = Depends(get_employees_service),
) -> EmployeesStats:
    """Returns statistics for employee records."""
    return await employees_service.get_stats()


@router.get(
    "/{employee_id}",
    response_model=Employee,
    responses={
        404: {"model": ErrorResponse, "description": "Employee not found"},
    },
)
async def get_employee(
    request: Annotated[EmployeeId, Path()],
    employees_service: EmployeesService = Depends(get_employees_service),
) -> Employee:
    """Returns employee by its unique"""
    result = await employees_service.get_by_id(request.employee_id)
    return result
