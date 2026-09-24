from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.employees.service import EmployeesService


def get_employees_service(db: AsyncSession = Depends(get_db)):
    return EmployeesService(db)
