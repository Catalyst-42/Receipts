from fastapi_filter.contrib.sqlalchemy import Filter

from src.crpt.model import CrptOrm


class CrptFilters(Filter):
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = CrptOrm
        ordering_field_name = "order_by"
