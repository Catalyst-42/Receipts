from fastapi_filter.contrib.sqlalchemy import Filter

from src.employees.model import EmployeesOrm


class EmployeesFilters(Filter):
    name__ilike: str | None = None

    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = EmployeesOrm
        ordering_field_name = "order_by"
