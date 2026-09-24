from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page

from src.employees.dependencies import get_employees_service
from src.employees.filters import EmployeesFilters
from src.employees.schemes import Employee
from src.employees.service import EmployeesService
from src.users.dependencies import get_admin
from src.users.schemes import User

router = APIRouter(prefix="/admin/employees", tags=["Admin"])


@router.get("/")
async def get_employees(
    admin: User = Depends(get_admin),
    filters: EmployeesFilters = FilterDepends(EmployeesFilters),
    employees_service: EmployeesService = Depends(get_employees_service),
) -> Page[Employee]:
    """Returns list of employees"""
    return await employees_service.get(filters)
