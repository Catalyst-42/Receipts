from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter

from src.retailers.model import RetailersOrm


class RetailersFilters(Filter):
    inn__in: list[str] | None = None
    name__ilike: str | None = None
    is_individual: bool | None = None

    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = RetailersOrm
        ordering_field_name = "order_by"
