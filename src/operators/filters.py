from fastapi_filter.contrib.sqlalchemy import Filter

from src.operators.model import OperatorsOrm


class OperatorsFilters(Filter):
    name__ilike: str | None = None

    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = OperatorsOrm
        ordering_field_name = "order_by"
